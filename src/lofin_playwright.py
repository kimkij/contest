from playwright.sync_api import sync_playwright
import time
import os

print("Launching browser for lofin365...")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(accept_downloads=True)
    page = context.new_page()
    
    # 1. search page in lofin365
    page.goto("https://lofin365.go.kr/portal/bbs/bbsSelect.do", wait_until="networkidle")
    print("BBS page title:", page.title())
    
    # Let's search "저상버스" in total search
    search_input = page.locator("input[name='searchWrd'], input[name='searchWord'], input[id*='search'], input[type='text']").first
    if search_input.count() > 0:
        search_input.fill("저상버스")
        page.keyboard.press("Enter")
        page.wait_for_timeout(3000)
        print("Search results title:", page.title())
        # print text snippets
        print("Text snippet:", page.locator("body").inner_text()[:400])
    
    browser.close()
