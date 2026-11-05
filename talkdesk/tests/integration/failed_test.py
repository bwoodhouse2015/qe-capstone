from playwright.sync_api import expect

def test_failing_playwright_test(page):
    page.goto("http://127.0.0.1:8080/login")

    expect(
        page.locator("text=hahaha")
    ).to_be_visible()


