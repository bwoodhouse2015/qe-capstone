from pages.login_page import LoginPage ## Interacts with login_page.py
import time

def test_reviewer_can_sign_in(page): ## Creates pytest, page is parameter that is pulled using playwright (browser tab)
    login_page = LoginPage(page) ## Created new object and passes page into the constructor inside of login_page.py

    login_page.goto() ## Navigates to log in page

    login_page.login(
        "hacker@hacker.com", ## Data input for test
        "123456789"
    )
    from playwright.sync_api import expect
    ## Imports playwright's assertion library, which then verifies what is excepted below

    time.sleep(3) ## Set wait to see the long in page open when the test isn't run headless

    expect( ## This verifies the result

        page.locator("text=Invalid credentials") ## The output needed to PASS
        ).to_be_visible()

## this test is an automated version of api_test_security_login.py
