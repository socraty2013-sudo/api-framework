"""商品列表页 UI 用例"""

from config import config
from pages.product_list_page import ProductsListPage

def test_click_product_opens_detail(driver, temp_product):
    # ① 准备
    page = ProductsListPage(driver)
    page.open(config["base_url"])
    page.wait_loaded()

    # ② 动作
    page.click(temp_product)

    # ③ 断言
    # 浏览器当前页面的完整 HTML。点进详情页后，页面上会渲染出商品名，直接查这段 HTML 里有没有这个名字。
    assert temp_product in driver.page_source


def test_add_link_hidden_when_not_logged_in(driver):
    # ① 准备
    page = ProductsListPage(driver)
    page.open(config["base_url"])
    page.wait_loaded()

    # ② 动作——这一步没有，直接跳过

    # ③ 断言
    assert page.has_add_link() is False    # 因没先登录，故has_add_link 读不到链接，即长度为0，返回Fasle

