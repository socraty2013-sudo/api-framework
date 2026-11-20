# 请求层干的活：让所有 HTTP 请求走同一个出口，地址、超时、登录态在这儿统一处理。

import requests

from config import config

class ApiClient:
    def __init__(self, base_url=None):
        self.base_url = base_url or config["base_url"]      # base_url or config["base_url"]：传了就用自己的，没传（None）就取配置里的。
        self.session = requests.Session()

    def get(self, path, **kwargs):

        # 调用方没传 allow_redirects → 这里设成 False
        # 调用方传了 → 保留调用方的值，不覆盖（ 下方 post 同理）
        kwargs.setdefault("allow_redirects", False)   # 默认时，allow_redirects=Flase，不允许重定向

        # 设置默认的请求等待响应时间上限为10s，如果请求时有传入，则直接使用，忽略默认的10s
        # 如果不写这一行，请求的接口不响应时，会无限期等待。
        # 加了后，默认状态下，如果请求等待10s无响应，则直接抛 ReadTimeout
        # 但如果此时传了 timeout = None，则请求无响应时，还是会无限等待（正常不会这么写）
        kwargs.setdefault("timeout", config["timeout"])
        return self.session.get(self.base_url + path, **kwargs)

    def post(self, path, data=None, **kwargs):
        kwargs.setdefault("allow_redirects", False)
        kwargs.setdefault("timeout", config["timeout"])
        return self.session.post(self.base_url + path, data=data, **kwargs)
