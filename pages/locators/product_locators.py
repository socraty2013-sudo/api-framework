"""商品列表页的元素定位器"""

from selenium.webdriver.common.by import By

class ProductLocators:
    """商品列表页的元素定位器"""

    # ① 页面标题：用来确认页面加载完（常量）
    PAGE_TITLE = (By.TAG_NAME, "h1")

    # ② 「新增商品」链接：登录后才显示，未登录不该有（常量）
    ADD_LINK = (By.LINK_TEXT, "新增商品")

    # ③ 商品名链接：动态的文字，必须写成方法：调用时才把 name 填进去（不是常量）
    @staticmethod
    def product_link(name):
        return (By.LINK_TEXT, name)