import os


BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")


class LoginPage:
    def __init__(self, page):
        self.page = page

    def goto(self):
        self.page.goto(f"{BASE_URL}/login")

    def login(self, email, password):
        self.page.get_by_test_id("email").fill(email)
        self.page.get_by_test_id("password").fill(password)
        self.page.get_by_test_id("login-submit").click()
