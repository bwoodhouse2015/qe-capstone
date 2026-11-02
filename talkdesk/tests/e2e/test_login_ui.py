from pages.login_page import LoginPage ## Interacts with login_page.py
import time

def test_reviewer_can_sign_in(page): ## Creates pytest, page is parameter that is pulled using playwright (browser tab)
    login_page = LoginPage(page) ## Created new object and passes page into the constructor inside of login_page.py

    login_page.goto() ## Navigates to log in page

    login_page.login(
        "reviewer@talkdesk.test", ## Data input for test
        "reviewer"
    )

    from playwright.sync_api import expect
    ## Imports playwright's assertion library, which then verifies what is excepted below

    time.sleep(5) ## Set wait to see the long in page open when the test isn't run headless

    expect( ## This verifies the result
        page.locator("text=Welcome, reviewer") ## The output needed to PASS
    ).to_be_visible() ## Was the text visible?

