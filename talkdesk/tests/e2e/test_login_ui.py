from pages.login_page import LoginPage


def test_reviewer_can_sign_in(page):
    login_page = LoginPage(page)

    login_page.goto()

    login_page.login(
        "reviewer@talkdesk.test",
        "reviewer"
    )

    assert page.locator("text=Welcome, reviewer").is_visible()
