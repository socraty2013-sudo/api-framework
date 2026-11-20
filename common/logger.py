# 日志器 logger 的创建及相关配置

import logging
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"       # `resolve()`：把路径转成绝对真实路径,自动处理 `.`、`..`、软链接，返回干净的绝对路径。
LOG_DIR =OUTPUT_DIR / "logs"

# parents=True：父级（output）必须存在，如不存在，创建目录时会报错 ; exist_ok=True：目录不在就建；已存在也不报错
LOG_DIR.mkdir(parents=True, exist_ok=True)

def get_logger(name="api-framework"):
    logger = logging.getLogger(name)     # 拿到一个 Logger 实例，变量名叫 logger
    if logger.handlers:           # 已经配过了就直接返回，别重复加
        return logger

    logger.setLevel(logging.INFO)

    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s  | %(message)s")

    sh = logging.StreamHandler()       # 送到终端
    sh.setFormatter(fmt)
    logger.addHandler(sh)

    fh = logging.FileHandler(LOG_DIR / "run.log", encoding="utf-8")    # 送到文件
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    return logger