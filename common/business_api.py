# 业务层干的活：把「接口」包成「业务动作」。用例里只写 api.login()，不关心底下怎么发的。

from config import config
from common.api_client import ApiClient
from common.encrypt_util import md5

class BusinessApi:
    def __init__(self, client=None):
        # BusinessApi 自己不发请求，它手里握着一个 ApiClient，活都交给它干。client=None 是留个口子：以后想换别的 client 实现，可以传进来。
        # ApiClient 是类本身（模板），ApiClient() 是拿模板造出来的一个实例（真东西）。括号 = 执行构造函数。
        self.client = client or ApiClient()

    def login(self, username=None, password=None):
        """登录：不传账号就用配置里的"""
        username = username or config["user"]["username"]
        password = password or config["user"]["password"]
        return self.client.post("/login", data= {"username":username, "password":password})

    def logout(self):
        """退出登录"""
        return self.client.get("/logout")

    def get_products(self):
        """商品列表页"""
        return self.client.get("/")

    def add_product(self, name, price, stock):
        """新增商品"""
        return self.client.post("/products/add", data={"name":name, "price":price, "stock":stock})

    def get_product(self, product_id):
        """商品详情"""
        return self.client.get(f"/products/{product_id}")

    def delete_product(self, product_id):
        """删除商品"""
        return self.client.post(f"/products/{product_id}/delete")

    def open_add_page(self):
        """打开新增商品页（需要先登录）"""
        return self.client.get("/products/add")

    def login_enc(self, username=None, password=None):
        """加密登录：密码先 md5 再传"""
        username = username or config["user_enc"]["username"]
        password = password or config["user_enc"]["password"]
        return self.client.post("/login_enc",data={"username":username, "password":md5(password)})



if __name__ == '__main__':
   test = BusinessApi()
   print(BusinessApi.login_enc())