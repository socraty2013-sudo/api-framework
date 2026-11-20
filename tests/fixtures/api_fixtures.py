#  conftest: pytest 的特殊文件名：放在哪个目录，就管那个目录及以下的所有用例。（这里用了 pytest_plugins，所以全局可用。各取所需）
import uuid
import pytest
from common.business_api import BusinessApi


#  Python 装饰器的通用规则：不带参数用裸的，带参数必须加括号
@pytest.fixture
def api():
    """每个用例拿到一个全新的 BusinessApi"""
    return BusinessApi()


@pytest.fixture()
def logged_in_api(api):
    """先登录，再把这个已登录的实例交出去"""
    api.login()  # 这行没收返回值 —— 因为这里需要的是它的副作用（cookie 存进去了），不是响应内容。
    yield api  # 这里返回的是 BusinessApi 实例（属于对象），这个实例内部最深的处 requests.Session 的 cookies 里带有登录态
    api.logout()

@pytest.fixture
def temp_product(logged_in_api, db):
    """造一个临时商品，用例跑完自动删除"""
    name = f"自动化测试商品_{uuid.uuid4().hex[:8]}"   # 每次产出一个不重复的 8 位串，保证这次造的一定是新的
    logged_in_api.add_product(name, 99.9, 10)

    yield name

    rows = db.query_all("SELECT * FROM products WHERE name = ?", (name,))
    for row in rows:
        logged_in_api.delete_product(row["id"])