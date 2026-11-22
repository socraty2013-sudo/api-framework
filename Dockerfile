# 造镜像的说明书

# 地基：官方 Python 3.11 精简版，约 150MB
FROM python:3.11-slim

# 容器里的工作目录，后面所有命令都在这里执行
WORKDIR /app

# ① 先只拷依赖清单(和代码分开拷贝，避免修改代码后，这部分缓存也消失了，每次都要重新安装依赖)
COPY requirements.txt .

# ② 再装依赖
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# ③ 最后拷全部代码
COPY . .

# 容器启动时默认跑接口用例
CMD ["pytest", "tests/test_api", "-v"]
