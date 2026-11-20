"""登录页的元素定位器。页面一改，只改这个文件"""

from selenium.webdriver.common.by import By

class LoginLocators:
    """类里放「常量」：全大写的名字表示它是固定的配置值，不是变量"""

    # 用户名输入框：name 属性 = username
    USERNAME_INPUT = (By.NAME, "username")

    # 密码输入框：name 属性 = password
    PASSWORD_INPUT = (By.NAME, "password")

    # 登录按钮：页面上只有一个 button
    LOGIN_BUTTON = (By.TAG_NAME, "button")

    # 错误提示 <p style="color: red;">：带 style 属性的 p 标签
    # p[style] 是 CSS 选择器语法，读作「有 style 属性的 p 标签」
    ERROR_MSG = (By.CSS_SELECTOR, "p[style]")

    # 页面大标题 h1
    H1_TITLE = (By.TAG_NAME, "h1")

