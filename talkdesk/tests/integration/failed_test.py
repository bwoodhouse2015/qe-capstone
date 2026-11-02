from playwright.sync_api import expect

def test_failing_playwright_test(page):
    page.goto("http://127.0.0.1:8001/login")

    expect(
        page.locator("text=hahaha") ##Reviewer sign-in
    ).to_be_visible()

