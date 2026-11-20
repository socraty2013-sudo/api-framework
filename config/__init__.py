import os
from pathlib import Path   # pathlib 是 python 3.4+ 获取目录路径的内置标准库，Path是路径对象
import yaml


# ① 当前跑的是哪个环境：去环境变量里找 ENV，找不到就当 dev
ENV = os.environ.get("ENV", "dev")

# ② 项目根目录的绝对路径
 # 同 os.path.join("a", b.txt)  → 得到 a/b.txt
 # `Path(__file__)`：获取当前文件路径`，.resolve()`：拿到绝对完整真实路径，`.parent`：取**上一级目录**
BASE_DIR = Path(__file__).resolve().parent.parent


# ③ 把环境先关的yaml读成字典
def _load(name):
    """读 config /环境.yaml，返回字典"""
    with open(BASE_DIR / "config" / f"{name}.yaml", encoding="utf-8") as f:    # 拼路径。Path 对象用 / 连接

        # safe_load(f) 读到空文件时，返回None，就变成了None or {}
        # 在Python `or` 运算规则中, 先评估左侧（None）是否为真（`None`、`0`、`""`、`[]`、`{}`都不为真），故丢弃，直接走右侧{}。故如读到文件为空，则还是兜底返回（空）字典
        # 如果左侧不为None，则不继续走右侧{}，直接返回读取的内容
        return yaml.safe_load(f) or {}


# ④ 合并读取到的base+环境.yaml的两个字典（递归函数：函数内部自己调自己）
def deep_merge(base,override):
    """递归合并：两边的值都是字典就钻进去合，否则后者覆盖前者"""
    result = dict(base)     # 复制一份 base。这样后面改 result，不会动到传进来的 base（不污染调用方的数据）
    for key, value in override.items():    # 遍历覆盖方override（也就是 uat）的每个键值对
        """
        遍历uat.yaml（举例），得到：
        1.第一轮：key = "base_url", value = "http://uat.example.com"
        2.第二轮：key = "user", value = {"username": "uat_admin"}
        """
        # 第一轮执行：if 条件直接 False，走 else：result["base_url"] = "http://uat.example.com"
        # 第二轮执行：if 条件为 True，得到：{'user': {'username': 'uat_admin'}} ，走deepmerge

        # isinstance(value, dict) → 判断上一行中value，也就是：{'username': 'uat_admin'}，是否是字典。
        # isinstance((result.get(key), dict) → 从uat中取到当前轮的key，然后去result（复制的base）中，看是否能找到同名的key，找到后，判断对应值是否为字典。
        # 仅覆盖和被覆盖方，都同是字典类型时，才递归合并内层字段。出现不是字典，则无法合并，走else覆盖
        if isinstance(value, dict) and isinstance(result.get(key), dict):     # 判断这一对是不是"两边都是字典"。isinstance(x, dict) 问"x 是字典吗"
            result[key] = deep_merge(result[key], value)      # 不要直接拿覆盖方（比如uat）的 value 覆盖。把这两个子字典丢进 deep_merge 再合并一次（函数自己调自己，这就是"递归"）
        else:

            # 直接用 覆盖方（比如uat）的 value，覆盖掉 result中同名 [key]的 value，不拆开里面。
            # 如果 result 中没这个该 [key]，则新增该 键值对（没花括号，不是字典，是字符串）
            result[key] = value

    return result


# ⑤ 最终配置：base.yaml 打底，当前环境的 yaml 覆盖
# 都用_load()方法去读取yaml文件，返回【字典】（一个直接读base，另一个读命令输入的环境名称，然后根据环境名称去找对应的yaml）
config = deep_merge(_load("base"), _load(ENV))

# ⑥ 路径兜底
#    问题：yaml 里如果写成 /Users/yaben/... 这种绝对路径，换台机器、进 CI 就找不到文件了
#    做法：yaml 里写【相对路径】，这里按【项目根目录】把它拼成绝对路径
#          项目不管克隆到哪，只要和 ecommerce-tests 是同级目录，路径就成立
#    另外留一个环境变量 DB_PATH，CI 里想指到别的位置时，设它就能盖掉 yaml 的值
if os.environ.get("DB_PATH"):
    config["db_path"] = os.environ["DB_PATH"]

if config.get("db_path") and not Path(config["db_path"]).is_absolute():
    config["db_path"] = str((BASE_DIR / config["db_path"]).resolve())
