import allure
import pytest
from common.logger import get_logger
from common.assert_util import assert_status_code, assert_contains
# import allure


log = get_logger(__name__)


@allure.feature("登录模块")
@allure.story("正常登录")
@allure.title("管理员用正确密码登录")
@pytest.mark.smoke
def test_login_success(api):
    log.info("开始登录")
    res = api.login()
    log.info(f"登录完成，状态码 {res.status_code}")
    assert_status_code(res, 302)
    assert res.headers["Location"] == "/"

@pytest.mark.smoke
def test_add_page_needs_login(api):
    """未登录 → 被踢回登录页"""
    res = api.open_add_page()
    assert_status_code(res, 302)
    assert res.headers["Location"]  == "/login"

@pytest.mark.regression
def test_add_page_when_logged_in(logged_in_api):
    """登录后 → 正常打开"""
    res = logged_in_api.open_add_page()
    assert_status_code(res, 200)


@pytest.mark.regression

# 这里其实temp_product里也用了logged_in_api的夹具，但是，此时setup不会重复执行。它是直接复用第一次的。
# 也就是只会同一个夹具只会setup一次
def test_add_and_find_product(logged_in_api, temp_product, db):
    # ① 商品列表页面上能看到新增的商品
    page = logged_in_api.get_products()
    assert_contains(page.text, temp_product)    # page.text 是响应体转成字符串

    # ② 数据库里真的有一条新增商品数据
    # 使用夹具temp_product，就是拿到临时新建的商品名 name
    rows = db.query_all("SELECT * FROM products WHERE name = ?", (temp_product,))
    assert len(rows) == 1
    assert rows[0]["price"] == 99.9   # 先拿第一行数据，然后通过键“price” 拿到对应的价格值

# 故意写一个reruns的测试用例 demo，为了验证是否会失败自动重试(先注释)
# def test_rerun_demo():
#     import random
#     assert random.random() > 0.5   # 永远为 False。random.random() ：返回：[0.0, 1.0)之间的浮点数，包含0，不包含1