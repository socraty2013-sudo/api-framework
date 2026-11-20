# 读取 csv 文件的测试数据并返回

import csv,yaml
from pathlib import Path
from openpyxl import load_workbook

DATA_DIR = Path(__file__).resolve().parent.parent/"data"

def read_csv(filename):
    path = DATA_DIR/filename
    with open(path, encoding="utf-8", newline="") as f:    # newline 它让 Python 别动我的换行符（如有），交给 csv 模块自己判断。
        return list(csv.DictReader(f))     # DictReader:把「表头」和「每一行」拼成字典，一行变成一个字典。

def read_yaml(filename):
    path = DATA_DIR/filename
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def read_excel(filename, sheet=None):
    path = DATA_DIR / filename

    # `wb`：openpyxl 的工作簿对象（Excel 文件）
    # data_only=True 单元格里是公式时，读公式算出来的结果，不读公式本身
    wb = load_workbook(path, read_only=True, data_only=True)

    # 三元表达式。如果调用函数时，传入的 `sheet` 有值（不为空、不是 None）→ ws = 指定工作表
    # 如果传入`sheet` 是空 / None → ws = 默认激活工作表
    ws = wb[sheet] if sheet else wb.active

    rows = list(ws.values)     # 把整个 sheet 的所有行吐出来，每行是一个元组，然后转成 list
    header = rows[0]
    return [dict(zip(header, row)) for row in rows[1:]]   # zip 按位置配对两个序列,得到的是元组，后转成字典



if __name__ == '__main__':
    print(read_csv("login_cases.csv"))
    print(read_yaml("login_cases.yaml"))

