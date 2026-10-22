class LoginPage:
    def __init__(self, page):
        self.page = page

    def goto(self):
        self.page.goto("http://127.0.0.1:8000/login")

    def login(self, email, password):
        self.page.fill("#email", email)
        self.page.fill("#password", password)
        self.page.click("text=Sign in")
