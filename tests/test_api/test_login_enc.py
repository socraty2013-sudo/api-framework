# 加密登录测试用例
import pytest
from common.assert_util import assert_status_code


@pytest.mark.parametrize("username,password,expect_code",[
    ("admin_enc", "123456", 302),
    ("admin_enc", "wrong", 200),
    ("nobody", "123456", 200),
])

def test_login_enc(api,username,password,expect_code):
    res = api.login_enc(username, password)   # 传参直接传明文，login_enc 方法内部会md5后再传
    assert_status_code(res, expect_code)

# 另外一组数据，需验证无需 md5() 时，是否能正常登录（应该无法登录，停留在登录页）。
# 故这里绕过 login_enc() 的方法（因为用它会自动 md5 ），直接调用最初始client 请求。
def test_login_without_enc(api):
    res = api.client.post("/login_enc", data={"username":"admin_enc", "password":"123456"})
    assert_status_code(res, 200)