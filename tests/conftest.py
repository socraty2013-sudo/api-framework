import os


# 国内网络访问 GitHub 版本清单极慢，Selenium Manager 会卡死在联网查版本这一步
# 强制离线模式：只用 PATH 里已装好的 chromedriver，不联网
os.environ["SE_OFFLINE"] = "true"


# 【pytest_plugins】 是一个专门写在 conftest.py 里的变量，值是列表，列表里面填模块名字符串。
    # 作用：告诉 pytest，自动去加载这些模块里写好的 fixture、钩子函数
    # pytest_plugins 只能放在【最顶层】的 conftest.py（tests/conftest.py）
    # 非最顶层的 conftest 不能写这个，写了直接报错。
pytest_plugins=[
    "tests.fixtures.api_fixtures",
    "tests.fixtures.db_fixtures",
    "tests.fixtures.ui_fixtures",
]