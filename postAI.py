from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv

# 讀取 .env 檔案
load_dotenv()
FB_EMAIL = os.getenv("FACEBOOK_EMAIL")
FB_PASSWORD = os.getenv("FACEBOOK_PASSWORD")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # 顯示瀏覽器
    page = browser.new_page()

    print("啟動瀏覽器，開始登入 Facebook...")

    # 進入 Facebook 登入頁面
    page.goto("https://www.facebook.com/")
    page.wait_for_timeout(3000)

    # 使用 .env 讀取帳號密碼
    page.fill("#email", FB_EMAIL)
    page.fill("#pass", FB_PASSWORD)

    # 按下登入按鈕
    page.press("#pass", "Enter")

    # 等待登入完成
    page.wait_for_timeout(5000)
    print("登入成功！")
    page.screenshot(path="debug_1_after_login.png")

    # 直接前往個人頁面
    page.goto("https://www.facebook.com/me")
    page.wait_for_timeout(3000)
    print("進入個人首頁")
    page.screenshot(path="debug_2_after_profile.png")

    # 點擊「在想些什麼？」開啟發文對話框
    post_trigger = page.locator("span:has-text('在想些什麼？')").first
    post_trigger.wait_for()
    post_trigger.click()
    page.wait_for_timeout(2000)
    print("Facebook 貼文對話框開啟成功！")
    page.screenshot(path="debug_3_after_click_post_box.png")

    # 使用 `div[contenteditable='true']` 找到發文框
    post_box = page.locator("div[role='dialog'] div[contenteditable='true']").first
    post_box.wait_for(state="visible", timeout=5000)
    print("發文框已載入")

    # 使用 `keyboard.type()` 模仿真人輸入
    page.keyboard.type("Pecu AI 開張了，這是一則由 Playwright 自動發佈的 Facebook 貼文！", delay=100)
    print("已模擬真人輸入")

    # 確保 Facebook 偵測到輸入
    page.evaluate("""
        let postBox = document.querySelector('div[contenteditable="true"]');
        postBox.focus();
        postBox.dispatchEvent(new Event('focus', { bubbles: true }));
        postBox.dispatchEvent(new Event('input', { bubbles: true }));
        postBox.dispatchEvent(new Event('change', { bubbles: true }));
    """)
    print("Facebook 偵測到輸入")

    # 等待「發佈」按鈕變成可點擊
    print("⌛ 等待 Facebook 啟用發佈按鈕...")
    page.wait_for_selector("div[aria-label='發佈']:not([aria-disabled='true'])", timeout=10000)
    print("發佈按鈕已啟用，可以點擊！")

    # 點擊發佈按鈕
    publish_button = page.locator("div[aria-label='發佈']")
    publish_button.click()
    print("🚀 貼文發佈中...")

    # 等待貼文完成
    page.wait_for_timeout(5000)
    print("貼文成功發佈！")
    page.screenshot(path="debug_6_after_publish.png")

    # 保持瀏覽器開啟，方便 Debug
    input("瀏覽器保持開啟，按 Enter 關閉...")

    # 關閉瀏覽器
    browser.close()
    print("瀏覽器已關閉")