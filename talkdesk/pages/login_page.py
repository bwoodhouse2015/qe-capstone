import os ## Import python operating system

## http://127.0.0.1:8001/login

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8080") ## Import os gives access to this function which reads environment variables, "Is there an environment variable named BASE_URL?"


class LoginPage: ##Blueprint for interacting with the login page, creates reusable functions
    def __init__(self, page): ## This is a constructor, which means that it is a method that runs automatically whenever you create an object from a class. (Initialize object)
        self.page = page ## Stores the browser, this can be used from anywhere from inside the class, pretty much once python recognizes "LoginPage" it will immediately call this page

    def goto(self):
        self.page.goto(f"{BASE_URL}/login") ##Instead of hard coding the link in every test, this imports the url

    def login(self, email, password):
        self.page.get_by_test_id("email").fill(email)
        self.page.get_by_test_id("password").fill(password)
        self.page.get_by_test_id("login-submit").click()

## Playwright's purpose here is to find the elements that in the string and then either fill or click

## Instead of having to write fill email etc. in each test using the log in function we can call them using this class created
