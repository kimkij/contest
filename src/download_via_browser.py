from playwright.sync_api import sync_playwright
import os
import time

print("Launching browser to download seoul and gyeonggi route datasets...")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(accept_downloads=True)
    
    # 1. Seoul
    page = context.new_page()
    page.goto("https://www.data.go.kr/data/15086332/fileData.do", wait_until="networkidle")
    print("Seoul page loaded")
    time.sleep(2)
    with page.expect_download(timeout=15000) as download_info:
        page.locator("button:has-text('다운로드'), a:has-text('다운로드')").first.click()
    download = download_info.value
    download.save_as("data/seoul_routes_raw.csv")
    print("Saved data/seoul_routes_raw.csv")
    page.close()
    
    # 2. Gyeonggi
    page2 = context.new_page()
    page2.goto("https://www.data.go.kr/data/15113523/fileData.do", wait_until="networkidle")
    print("Gyeonggi page loaded")
    time.sleep(2)
    with page2.expect_download(timeout=15000) as download_info2:
        page2.locator("button:has-text('다운로드'), a:has-text('다운로드')").first.click()
    download2 = download_info2.value
    download2.save_as("data/gyeonggi_routes_raw.csv")
    print("Saved data/gyeonggi_routes_raw.csv")
    page2.close()

    browser.close()
