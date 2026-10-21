from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto("https://the-internet.herokuapp.com/two_factor")

    print("Page Title:", page.title())
    print("Page URL:", page.url)

    browser.close()