from playwright.sync_api import Page

class LoginPage:
    EMAIL_INPUT_XPATH = (
        "//input[@type='email' or contains(@placeholder,'Enter your email') or contains(@name,'email')]"
    )
    PASSWORD_INPUT_XPATH = (
        "//input[@type='password' or contains(@placeholder,'Enter your password') or contains(@name,'password')]"
    )
    LOGIN_BUTTON_XPATH = (
        "//button[normalize-space()='Login' or contains(text(),'Log in') or contains(text(),'Login')]"
    )

    def __init__(self, page: Page, login_url: str, email: str, password: str):
        self.page = page
        self.login_url = login_url
        self.email = email
        self.password = password

    def do_login(self):
        self.page.goto(self.login_url, timeout=60000)
        self.page.locator(self.EMAIL_INPUT_XPATH).wait_for(state="visible", timeout=30000)
        self.page.locator(self.EMAIL_INPUT_XPATH).fill(self.email)
        self.page.locator(self.PASSWORD_INPUT_XPATH).wait_for(state="visible", timeout=30000)
        self.page.locator(self.PASSWORD_INPUT_XPATH).fill(self.password)
        self.page.locator(self.LOGIN_BUTTON_XPATH).wait_for(state="attached", timeout=30000)
        self.page.locator(self.LOGIN_BUTTON_XPATH).click()
