from pages.login_page import LoginPage ## Interacts with the login page file


def test_reviewer_can_sign_in(page):
    login_page = LoginPage(page) ## Page is browser, creates object, controls browser

    login_page.goto() ## Navigates to log in page

    login_page.login(
        "reviewer@talkdesk.test", ## Data input for test
        "reviewer"
    )

    from playwright.sync_api import expect ## This verifies the output on the screen, finds the text below

    expect(
        page.locator("text=Welcome, reviewer") ## The output needed to PASS
    ).to_be_visible()
