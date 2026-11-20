# api-framework

基于 pytest 的接口 / UI 自动化测试框架，覆盖数据驱动、多环境配置、日志、Allure 报告与性能压测。

被测系统：[ecommerce-tests](https://github.com/socraty2013-sudo/ecommerce-tests)（Flask + SQLite，默认端口 5050）。

## 能力一览

| 能力 | 实现方式 |
| --- | --- |
| 用例分层 | `tests/test_api`（接口）/ `tests/test_ui`（UI），共 23 条 |
| fixture 分层 | 接口 / 数据库 / UI 三组 fixture 拆在 `tests/fixtures/`，由 `pytest_plugins` 统一加载 |
| 业务封装 | `common/business_api.py` 把「登录、加购、下单」这类业务动作包成方法，用例不直接拼 URL |
| 请求层 | `common/api_client.py` 封装 `requests.Session`，统一 base_url、超时与日志 |
| 数据驱动 | `data/` 下 csv / yaml / xlsx，`parametrize` 批量喂用例 |
| 多环境 | `config/` 下 base + dev / uat，用 `ENV` 环境变量切换 |
| 失败重试 | `pytest-rerunfailures`，全局 2 次、间隔 1 秒 |
| 报告 | Allure，失败自动附日志 |
| 性能测试 | `performance/locustfile.py`，Locust 搭阶梯加压 |

## 快速开始

**前置条件**：本框架与被测系统 `ecommerce-tests` 放在同一个父目录下：

```
PycharmProjects/
├── api-framework/
└── ecommerce-tests/
```

数据库路径按 `../ecommerce-tests/ecommerce_dev.db` 解析，目录结构不符时需要改 `config/dev.yaml`。

### 1. 启动被测系统

```bash
cd ../ecommerce-tests
.venv/bin/python -m flask run --port=5050
```

### 2. 安装依赖

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. 运行用例

```bash
pytest                        # 全部
pytest tests/test_api         # 只跑接口层
pytest tests/test_ui          # 只跑 UI 层
pytest -m smoke               # 只跑冒烟
ENV=uat pytest                # 切到 uat 环境
pytest -n auto                # 并行执行
```

UI 层需要本机有 Chrome 与对应的 chromedriver。

## 目录结构

```
api-framework/
├── config/          多环境配置（base.yaml + dev/uat.yaml）
├── common/          公共工具层
│   ├── api_client.py      请求封装
│   ├── business_api.py    业务动作封装
│   ├── db_handler.py      数据库操作
│   ├── encrypt_util.py    md5 / sha256 / hmac
│   ├── file_handler.py    csv / yaml / excel 读取
│   ├── logger.py          日志
│   ├── assert_util.py     断言工具
│   └── ui_utils.py        浏览器驱动与常用操作
├── data/            数据驱动的测试数据
├── pages/           UI 页面对象（POM）
│   ├── locators/          元素定位器
│   ├── login_page.py
│   └── product_list_page.py
├── performance/     Locust 压测脚本、统计分析与报告
├── tests/           用例与 fixture
│   ├── fixtures/          api / db / ui 三组 fixture
│   ├── test_api/
│   └── test_ui/
└── output/          运行产物（报告 / 日志 / 截图，不进版本库）
```

## 分层设计

自下而上五层，上层只调下层：

```
用例（tests/）        写业务断言，不关心怎么发请求
    ↓
业务封装（business_api）  一个方法 = 一个业务动作
    ↓
请求层（api_client）      统一 base_url、超时、会话
    ↓
数据协议（requests / selenium）
    ↓
被测系统（ecommerce-tests）
```

用例里不出现 URL，也不出现裸 `requests` 调用——换接口地址只改配置，换请求方式只改封装层。

## 多环境

`config/base.yaml` 放公共配置，`config/dev.yaml`、`config/uat.yaml` 放差异项，加载时后者覆盖前者。

```bash
ENV=uat pytest      # 环境变量决定读哪份
```

`db_path` 在 yaml 里写相对路径，代码按项目根目录解析成绝对路径；也支持用 `DB_PATH` 环境变量强制覆盖。

## 测试数据

| 文件 | 用途 |
| --- | --- |
| `data/login_cases.csv` | 登录场景参数化 |
| `data/login_cases.yaml` | 同上，yaml 写法 |
| `data/login_cases.xlsx` | 同上，excel 写法 |
| `data/add_product_flow.yaml` | 加购流程步骤数据 |

## 报告

```bash
pytest --alluredir=output/allure-results
allure serve output/allure-results
```

## 性能测试

```bash
locust -f performance/locustfile.py --host=http://127.0.0.1:5050
```

打开 `http://localhost:8089` 配置并发与加压曲线；统计结果用 `performance/analyze_stats.py` 提取稳态数据。
