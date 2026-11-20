import pytest
from common.file_handler import read_yaml


flows = read_yaml("add_product_flow.yaml")

@pytest.mark.parametrize("flow", flows, ids=[f["case_name"] for f in flows])
def test_flow(logged_in_api, flow):
    last = None

    """
       ⬇️flow["steps"]得到的数据如下：
       [
           {'action': 'add_product', 'name': 'yaml测试商品_001', 'price': 99.9, 'stock': 10},
           {'action': 'get_products'},
        ]
       """
    # 遍历时，逐条读取上面的数据
    for step in flow["steps"]:
        params = dict(step)                   # 复制一份，不改原始数据（将 step 转成字典）
        data = params.pop("action")         # 遍拿掉字典中的一个元素：action，剩下的就是方法参数，并把参数赋值给 data

        # 举例：getattr(api, "add_product") = api.add_product； getattr(api, "login")() = api.login()
        # ⬇️等价于：logged_in_api.add_product(name="yaml测试商品_001", price=99.9, stock=10)
        last = getattr(logged_in_api, data)(**params)     # 先按名字找到方法，再用 ** 把字典拆成关键字参数传进去。


    name = flow["steps"][0]["name"]
    assert name in last.text
