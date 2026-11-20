from locust import HttpUser,between,task,events,LoadTestShape
import uuid
from common.db_handler import DBHandler


class MyShape(LoadTestShape):
    stages = [
        {"duration": 60, "users": 10, "spawn_rate": 5},    # spawn_rate  是每秒爬升几个用户，这里是每秒启动 5 个用户
        {"duration": 120, "users": 20, "spawn_rate": 10},
        {"duration": 180, "users": 40, "spawn_rate": 10},
        {"duration": 240, "users": 80, "spawn_rate": 20},
    ]

    def tick(self):
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage["duration"]:
                return stage["users"], stage["spawn_rate"]
        return None

class LoginUser(HttpUser):
    host = "http://127.0.0.1:5050"      # 被测系统地址
    # wait_time = between(1, 3)

    # on_start: locust 预留的【固定方法名】，每个虚拟用户创建时【自动执行一次】
    # 写在 HttpUser 子类里，方法名必须叫 on_start
    # 不加 @task。加了它就变成循环任务，逻辑就错了
    # self.client：locust 内置的 HTTP 客户端。本质是 requests.Session
    # on_start 里登录成功后，服务器返回的 cookie 被 Session 自动存下来，之后所有 self.client.get(...) 都会自动带上这个 cookie
    # def on_start(self) -> None:
    #     self.client.post("/login", data={"username":"admin", "password":"123456"})     # self.client: locust 内置的 HTTP 客户端，用法和 requests 一模一样。封装了所有统计数字都从它这里来


    # @task
    # def add_product(self):
    #     self.client.post("/products/add", data={
    #         "name":f"perf_{uuid.uuid4().hex[:8]}",
    #         "price":"99",
    #         "stock":"100",
    #     })


    @task
    def browse(self):
        self.client.get("/")

# events.test_stop	事件名：整个测试结束时触发一次
# .add_listener	方法：往这个事件上挂一个函数
# environment 函数第一个参数：locust 运行环境对象（含用户数、统计信息等），必须占位
# **kwargs	兜底参数，locust 可能传别的关键字参数进来，防止报错
@events.test_stop.add_listener
def cleanup(environment, **kwargs):
    db = DBHandler()

    # db.execute() 返回 rowcount（影响行数），正好拿来打印删了几条
    # ? 是 sqlite 驱动的参数占位符**，**不是字符串拼接**，目的就是防御 SQL 注入。
    # 第二个参数必须是元组：（"pref_%",) 后一定要加逗号，表示为元组，否则只是字符串
    # SQL 的 LIKE 里 _ 是通配符，代表【任意单个字符】。所以 LIKE 'perf_%' 里的 _ 会匹配 perf 后面任意一个字符，perfa123 也会被匹配到（这里了解就好了）
    deleted = db.execute("DELETE FROM products WHERE name Like ?", ("perf_%", ))
    print(f"\n[清理] 删除压测数据 {deleted} 条")



"""
locust的具体信息在命令行或locust 网页上配置，部分常用参数：

    locust -f xxx/locustfile.py :启动 locust，并指定目录及脚本
    -H: --host;    
    -P : --web-port。默认 8089，8089被占用后改它
    -u: --users
    -r: 每秒新增用户数
    -t: 执行脚本总时长
    --headless: 无头模式，不打开网页，纯终端跑
    --autostart: locust 的命令行参数，作用一句话——让网页启动后自动开跑，不用点 Start（此时打开网页可直接进入数据页）
    --autoquit:  配合--autostart：跑完 X 秒后整个进程退出。不加的话跑完网页还挂着
"""




