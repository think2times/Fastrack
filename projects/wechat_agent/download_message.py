import time
import csv
from playwright.sync_api import sync_playwright

# 配置文件名和路径
USER_DATA_DIR = "./wechat_session"  # 存储登录状态的文件夹
OUTPUT_FILE = "wechat_messages.csv"

def scrape_wechat_mp():
    with sync_playwright() as p:
        # 1. 启动持久化浏览器
        # headless=False 必须为 False，否则你看不见二维码，无法扫码登录
        context = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            args=["--start-maximized"]
        )
        
        page = context.new_page()
        page.goto("https://mp.weixin.qq.com/")

        # 2. 判断是否需要登录
        # 如果检测到登录页面的特征，就等待用户扫码
        if page.locator(".login__type__container").is_visible():
            print("请在打开的浏览器中扫码登录...")
            # 等待登录成功跳转到首页（通常 URL 会包含 token）
            page.wait_for_url("**/cgi-bin/home?**", timeout=0)
            print("登录成功！")

        # 3. 跳转到“消息管理”页面
        # 注意：微信后台的 URL 带有 token，不能直接写死，需要从当前 URL 提取或点击侧边栏
        print("正在前往消息管理页面...")
        page.locator("a:has-text('消息管理')").click()
        page.wait_for_load_state("networkidle")

        # 4. 循环抓取页面内容
        messages_data = []
        
        while True:
            # 等待列表加载
            page.wait_for_selector(".message_item")
            
            # 获取当前页所有消息块
            items = page.locator(".message_item").all()
            for item in items:
                # 提取用户名、时间、内容（选择器需根据实际后台结构微调）
                # 微信后台结构复杂，建议通过 .inner_text() 获取整块文本再正则解析，或者精确定位
                nickname = item.locator(".nickname").inner_text()
                msg_time = item.locator(".time").inner_text()
                content = item.locator(".msg_content").inner_text()
                
                messages_data.append({
                    "nickname": nickname,
                    "time": msg_time,
                    "content": content
                })
            
            print(f"已抓取 {len(messages_data)} 条数据...")

            # 5. 翻页逻辑
            next_button = page.locator("a.btn.next") # 这里的选择器需根据实际翻页按钮 ID 确定
            if next_button.is_visible() and next_button.is_enabled():
                next_button.click()
                time.sleep(2) # 关键：一定要慢，避免触发反爬
            else:
                break # 没有下一页了

        # 6. 保存数据
        save_to_csv(messages_data)
        print(f"抓取完成，数据已存入 {OUTPUT_FILE}")
        context.close()

def save_to_csv(data):
    keys = data[0].keys() if data else []
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8-sig') as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

if __name__ == "__main__":
    scrape_wechat_mp()