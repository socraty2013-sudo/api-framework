import sys
import allure
import pytest
from common.assert_util import assert_status_code
from common.file_handler import read_csv,read_yaml,read_excel


csv_rows = read_csv("login_cases.csv")
yaml_rows = read_yaml("login_cases.yaml")
excel_rows = read_excel("login_cases.xlsx")

# 其实三中格式的数据驱动，对于用例本身来说，读取得到的数据内容和格式都是相同的。这里写三个方法纯粹为了示意。
@allure.feature("登录模块")
@allure.story("参数化登录")
@allure.title("登录 - {case[case_name]}")
@pytest.mark.parametrize("case", csv_rows, ids=[r["case_name"] for r in csv_rows] )
def test_login_csv(api,case):
    res = api.login(case["username"], case["password"])
    assert_status_code(res, int(case["expect_code"]))    # csv 的字段默认为字符串，这里真实请求返回的 code 为int 类型，故 csv 文件的字符串要转成 int，否则断言失败

@pytest.mark.skipif(sys.version_info > (3, 10), reason="需要 Python 3.10+")    # 满足条件：python 版本< 3.10 时，则跳过
@pytest.mark.parametrize("case", yaml_rows, ids=[r["case_name"] for r in yaml_rows] )
def test_login_yaml(api,case):
    res = api.login(case["username"], case["password"])
    assert_status_code(res, case["expect_code"])        # yaml 数据文件内部需要定好数据类型，故断言时，无需额外的调整数据类型

@pytest.mark.skip
@pytest.mark.parametrize("case", excel_rows, ids=[r["case_name"] for r in csv_rows] )
def test_login_excel(api,case):
    res = api.login(case["username"], case["password"])
    assert_status_code(res, int(case["expect_code"]))    # csv 的字段默认为字符串，这里真实请求返回的 code 为int 类型，故 csv 文件的字符串要转成 int，否则断言失败

