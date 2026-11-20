"""商品列表页的页面对象"""

from common.ui_utils import wait_element, click
from pages.locators.product_locators import ProductLocators

class ProductsListPage:
    def __init__(self, driver):
    # 把浏览器遥控器存到对象上，这个类的每个方法都能用 self.driver 拿到它
       self.driver = driver

    def open(self, base_url):
        """浏览器打开首页"""
        self.driver.get(base_url + "/")

    def wait_loaded(self):
        """等页面刷出来"""
        wait_element(self.driver, ProductLocators.PAGE_TITLE)

    def click(self, name):
        """点某个商品名"""

        # ⬇️click() 中，定位器本身接收的就是元组，一个整体，故无需加*号解包成两个参数
        click(self.driver, ProductLocators.product_link(name))

    def has_add_link(self):
        """看有没有新增入口"""

        # ⬇️find_elements无法接收整个元组，需用*号解包成两个独立的参数，再传入
        els = self.driver.find_elements(*ProductLocators.ADD_LINK)
        return len(els) > 0    # 能找到元素就返回 True，找不到返回 False（返回布尔值）

