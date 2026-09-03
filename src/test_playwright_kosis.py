from playwright.sync_api import sync_playwright
import time
import os

url = "https://kosis.kr/statHtml/statHtml.do?orgId=117&tblId=DT_117061_001"
print("Launching playwright...")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url, wait_until="networkidle")
    print("Page title:", page.title())
    time.sleep(3)
    # take screenshot or check table
    tables = page.locator("table").count()
    print("Tables count:", tables)
    # check if download button exists
    export_btn = page.locator("text='다운로드'")
    print("Download button count:", export_btn.count())
    browser.close()
