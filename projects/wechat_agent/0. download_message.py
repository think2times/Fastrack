import csv
import time
from playwright.sync_api import sync_playwright

def run_wechat_perfect_scroll():
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir="./wechat_session",
            headless=False,
            viewport={'width': 1400, 'height': 900}
        )
        page = context.new_page()
        page.goto("https://mp.weixin.qq.com/")

        # 1. 进入私信
        page.wait_for_selector("text=互动管理", timeout=60000)
        page.get_by_text("互动管理").click()
        page.get_by_text("私信").first.click()
        time.sleep(5) 

        # 定位 Frame
        target_frame = next((f for f in page.frames if "message" in f.url), None)
        if not target_frame: return

        # 点击“全部”
        try:
            target_frame.get_by_text("全部", exact=True).click()
            time.sleep(3)
        except: pass

        all_data = []
        processed_keys = set()
        
        # 结束逻辑相关变量
        no_new_data_streak = 0  # 连续无新数据的计数器
        MAX_STREAK = 6          # 连续 6 次没新数据才退出
        MAX_STEPS = 200         # 最大安全循环上限

        print(">>> 启动‘深度物理滚动’模式...")

        for step in range(MAX_STEPS):
            # 获取数据
            nicks = target_frame.locator(".user-info__name").all_inner_texts()
            times = target_frame.locator(".user-info__time").all_inner_texts()
            contents = target_frame.locator(".user-msg-text").all_inner_texts()

            min_len = min(len(nicks), len(times), len(contents))
            new_this_round = 0
            
            for i in range(min_len):
                # 唯一键：昵称 + 时间 + 内容前10位（防止同一用户连续发多条）
                key = f"{nicks[i]}_{times[i]}_{contents[i][:10]}"
                if key not in processed_keys:
                    all_data.append([times[i], nicks[i], contents[i]])
                    processed_keys.add(key)
                    new_this_round += 1
            
            print(f"步数 {step+1}: 抓到 {new_this_round} 条新数据，当前总计 {len(all_data)} 条")

            # --- 核心滚动操作 ---
            # 移动到左侧列表区域并滚动
            page.mouse.move(300, 500) 
            page.mouse.wheel(0, 2000) # 增大滚动幅度
            
            # --- 结束逻辑判定 ---
            if new_this_round == 0:
                no_new_data_streak += 1
                print(f"    (警告: 连续 {no_new_data_streak}/{MAX_STREAK} 次未发现新消息，正在重试...)")
                # 发现 0 条时，尝试“补救滚动”：模拟按下 End 键
                page.keyboard.press("End")
                time.sleep(4) # 给更长的加载时间
            else:
                no_new_data_streak = 0 # 只要有新数据，计数器归零
                time.sleep(2) # 正常速度

            if no_new_data_streak >= MAX_STREAK:
                print(">>> 确认已抓取所有可见历史数据，准备退出...")
                break

        # 2. 最终保存
        if all_data:
            filename = 'wechat_complete_msgs.csv'
            # 排序：按时间倒序或正序（可选）
            # all_data.sort(key=lambda x: x[0]) 
            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(['时间', '昵称', '内容摘要'])
                writer.writerows(all_data)
            print(f"✅ 抓取圆满完成！共导出 {len(all_data)} 条记录。")

        context.close()

if __name__ == "__main__":
    run_wechat_perfect_scroll()