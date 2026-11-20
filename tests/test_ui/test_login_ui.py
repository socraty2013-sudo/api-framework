"""登录页 UI 用例"""
import pytest

from config import config
from common.ui_utils import wait_url_changes
from pages.login_page import LoginPage

def test_login_success(driver):
    """正确的账号密码：应该跳到首页，看到商品列表"""
    page = LoginPage(driver)    # 类的实例化，这里的 driver 是fixture 的注入机制，无需 import
    page.open(config["base_url"])

    old_url = driver.current_url       # 点之前先记下地址（顺序不能调整）
    page.login(config["user"]["username"], config["user"]["password"])
    wait_url_changes(driver, old_url)

    assert driver.current_url == config["base_url"]  + "/"  # 断言等待变更后的 url 是 否为：登录成功后的 url


# UI 自动化--参数化。每一组参数都会打开一个浏览器
# 因为 driver 是每个用例一份，这里两组参数，相当于两个用例
@pytest.mark.parametrize("username, password", [
    ("admin", "wrong"),     # 用户名对，密码错
    ("nobody", "123456"),    # 用户不存在
])
def test_login_fail(driver, username, password):
    page = LoginPage(driver)
    page.open(config["base_url"])
    page.login(username, password)

    # get_error_text 内部用的是 wait_element, 会等提示出现，不用额外等
    assert page.get_error_text() == "用户名或密码错误"

