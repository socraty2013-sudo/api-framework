# 断言工具：失败时只有知道哪个接口、返回了什么

def assert_status_code(res, expected):
    """断言 HTTP 状态码，失败时把接口现场带出来"""

    # ↓【assert 条件, 报错信息】：“条件”为假时才会走报错信息。此时，这里的“报错信息”会代替来 assert 默认的 AssertionError 显示
    assert res.status_code == expected,(
        f"状态码不符 | 期望 {expected!r} | 实际 {res.status_code!r} | "    # !r 叫 repr 转换，就是让值按「代码里的样子」显示，不做处理。(下同)
        
        # !r 是 Python f-string 里的转换标记，等价于调用 `repr()`
        # repr()的作用是：尽量还原这个对象的“字面形式”。举例：f"{变量!r}" = f"{repr(变量)}"，会将格式化前的内容的比如空格/换行符这种保留下来
        f"{res.request.method} {res.url} | 响应体 {res.text[:200]!r}"
    )

def assert_contains(text, expected):
    """断言文本里包含某段内容"""
    assert  expected in text,(
        f"内容不存在 | 期望包含 {expected!r} | 实际 {text [:200]!r}"
    )