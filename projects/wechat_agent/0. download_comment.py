import csv
import time
import os
import re
from playwright.sync_api import sync_playwright

# --- 配置 ---
CHECKPOINT_FILE = "checkpoint_page.txt"
DATA_FILE = 'wechat_comments_final.csv'

def get_page_nums_robust(target_frame, is_left=True):
    """
    结合坐标判定，确保左侧只找左边，右侧只找右边
    """
    try:
        area_class = 'comment-articles' if is_left else 'comment-list-wrp'
        xpath = f"//div[contains(@class, '{area_class}')]//label[contains(@class, 'weui-desktop-pagination__num')]"
        
        target_frame.wait_for_selector(f"xpath={xpath}", timeout=3000)
        elements = target_frame.locator(f"xpath={xpath}").all()
        
        # 进一步通过物理坐标过滤，防止XPath越界
        valid_elements = []
        for el in elements:
            box = el.bounding_box()
            if box:
                if is_left and box['x'] < 600: valid_elements.append(el)
                elif not is_left and box['x'] >= 600: valid_elements.append(el)

        if len(valid_elements) >= 2:
            curr = int(valid_elements[0].inner_text().strip())
            total = int(valid_elements[1].inner_text().strip())
            return curr, total
    except: pass
    return 1, 1

def save_checkpoint(page_num):
    with open(CHECKPOINT_FILE, "w") as f:
        f.write(str(page_num))

def load_checkpoint():
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "r") as f:
            return int(f.read().strip())
    return 1

def run_wechat_comments_with_resume():
    resume_page = load_checkpoint()
    # 判断是否是第一次运行（决定是否写表头）
    is_first_run = not os.path.exists(DATA_FILE)

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir="./wechat_session",
            headless=False,
            viewport={'width': 1400, 'height': 900}
        )
        page = context.new_page()
        page.goto("https://mp.weixin.qq.com/")

        # 1. 进入留言页面
        page.wait_for_selector("text=互动管理", timeout=60000)
        page.get_by_text("互动管理").click()
        page.get_by_text("留言").first.click()
        time.sleep(5)

        target_frame = next((f for f in page.frames if "appmsgcomment" in f.url), None)
        if not target_frame: return

        # 2. 【自动跳页】如果上次崩溃在第7页，这里会自动翻过去
        if resume_page > 1:
            print(f">>> 检测到历史进度，正在自动翻向第 {resume_page} 页...")
            for i in range(1, resume_page):
                btn = target_frame.locator(".comment-articles .weui-desktop-btn_default").last
                btn.click()
                time.sleep(1.5)
            print(f">>> 已到达第 {resume_page} 页，开始抓取。")

        # --- 文章列表大循环 ---
        while True:
            a_curr, a_total = get_page_nums_robust(target_frame, is_left=True)
            print(f"\n>>> 【文章列表进度】第 {a_curr} / {a_total} 页")
            save_checkpoint(a_curr) # 实时记录断点

            articles_locator = target_frame.locator(".comment-article-list > div")
            articles_locator.first.wait_for(state="visible", timeout=10000)
            
            # 每一页抓完立即保存，防止再次崩溃丢失数据
            page_results = []

            for i in range(articles_locator.count()):
                try:
                    current_article = articles_locator.nth(i)
                    title = current_article.locator(".article-list__item-title").inner_text().strip()
                    print(f"  --- 抓取文章: {title}")
                    current_article.click()
                    time.sleep(2) 

                    # --- 评论翻页循环 (处理一篇文章的所有留言) ---
                    while True:
                        # 【修正点 1】确保抓取动作在循环体内，翻页后会重新执行
                        items = target_frame.locator(".comment-list__item:visible").all()
                        print(f"    正在抓取当前页 {len(items)} 条主评论...")
                        
                        for item in items:
                            try:
                                nick = item.locator(".comment-nickname").first.inner_text().strip()
                                content = item.locator(".comment-text").first.inner_text().strip()
                                msg_time = item.locator(".comment-list__item-time").first.inner_text().strip()
                                page_results.append([title, msg_time, nick, content, "主评论"])

                                # 展开回复并抓取
                                extend_btn = item.locator(".comment-list__item-extend")
                                if extend_btn.count() > 0 and "收起" not in extend_btn.inner_text():
                                    extend_btn.click()
                                    time.sleep(0.5)

                                for reply in item.locator(".comment-reply-item").all():
                                    page_results.append([
                                        title, 
                                        reply.locator(".comment-list__item-time").inner_text().strip(),
                                        reply.locator(".comment-nickname").inner_text().strip(),
                                        reply.locator(".comment-text").inner_text().strip(), 
                                        "回复"
                                    ])
                            except: continue

                        # 【修正点 2】判定翻页并在点击后等待加载
                        c_curr, c_total = get_page_nums_robust(target_frame, is_left=False)
                        if c_curr < c_total:
                            print(f"    评论第 {c_curr} 页处理完，翻向第 {c_curr + 1} 页...")
                            target_frame.locator(".comment-list-wrp .weui-desktop-pagination__nav .weui-desktop-btn_default").last.click()
                            
                            # 关键：翻页后必须等待 DOM 刷新，否则下一轮循环抓到的还是旧数据
                            time.sleep(2) 
                        else:
                            break
                except Exception as e:
                    print(f"    处理文章异常: {e}")
                    continue

            # --- 每一页文章处理完，立即追加写入CSV ---
            if page_results:
                file_exists = os.path.isfile(DATA_FILE)
                with open(DATA_FILE, 'a', newline='', encoding='utf-8-sig') as f:
                    writer = csv.writer(f)
                    if not file_exists:
                        writer.writerow(['文章标题', '时间', '昵称', '内容', '类型'])
                    writer.writerows(page_results)
                print(f"  ✅ 第 {a_curr} 页数据已持久化保存。")

            # --- 文章列表翻页 ---
            if a_curr < a_total:
                left_next_btn = target_frame.locator(".comment-articles .weui-desktop-btn_default").last
                left_next_btn.click()
                
                # 等待页码跳动
                success = False
                for _ in range(10):
                    time.sleep(1.5)
                    new_curr, _ = get_page_nums_robust(target_frame, is_left=True)
                    if new_curr > a_curr:
                        success = True
                        break
                if not success:
                    print("!!! 页码未跳动，尝试二次点击...")
                    left_next_btn.click()
            else:
                print("🎉 全部 14 页抓取完成！")
                if os.path.exists(CHECKPOINT_FILE): os.remove(CHECKPOINT_FILE)
                break

        context.close()

if __name__ == "__main__":
    run_wechat_comments_with_resume()