"""登录页的页面对象：用例只用这里的方法，不碰 Selenium 原始 API"""

from common.ui_utils import click, input_text, get_text
from pages.locators.login_locators import LoginLocators


class LoginPage:
    """代表「登录页」这个页面"""

    def __init__(self, driver):
        # 把浏览器遥控器存到对象上，这个类的每个方法都能用 self.driver 拿到它
        self.driver = driver

    def open(self, base_url):
        """打开登录页"""
        self.driver.get(base_url + "/login")

    def login(self, username, password):
        """完整的登录动作：输用户名 → 输密码 → 点登录"""
        input_text(self.driver, LoginLocators.USERNAME_INPUT, username)
        input_text(self.driver, LoginLocators.PASSWORD_INPUT, password)
        click(self.driver, LoginLocators.LOGIN_BUTTON)

    def get_title_text(self):
        """取页面大标题"""
        return get_text(self.driver, LoginLocators.H1_TITLE)

    def get_error_text(self):
        """取红色错误提示"""
        return get_text(self.driver, LoginLocators.ERROR_MSG)