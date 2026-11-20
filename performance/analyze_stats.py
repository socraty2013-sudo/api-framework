"""分析 locust 阶梯加压结果：每个用户数阶段只取最后 N 秒稳态，输出对比表。

用法：python performance/analyze_stats.py [history.csv]
"""
import csv
import sys

# 运行脚本时如果传了第 1 个参数，就用这个参数作为文件路径；不传参数，就用后面这个默认 csv 路径
# `sys.argv[0]` 是脚本文件名，`sys.argv[1]` 是第一个传入参数
# 三元表达式：if 条件成立（运行脚本时，除了脚本名之外，带了别的参数，总参数（含脚本）＞1个），则Path=sys.argv[1]，否则走右边Path=右边 csv路径
# 举例：python test.py abc.csv——py 文件为 argv[0]；csv为argv[1]。如果则这个参数，if 判断是成立的。
PATH = sys.argv[1] if len(sys.argv) > 1 else "output/perf/shape_stats_history.csv"
TAIL = int(sys.argv[2]) if len(sys.argv) > 2 else 20

MIN_SECONDS = 30   # 样本不足 30 秒的阶段直接跳过（那是爬坡瞬间，不是稳态）

rows = list(csv.DictReader(open(PATH)))

# 按 User Count 分组，保持出现顺序
stages = {}
order = []
for r in rows:
    u = int(r["User Count"])
    if u not in stages:
        stages[u] = []
        order.append(u)
    stages[u].append(r)


def avg_pct(seg, key):
    """平均分位数；跳过 N/A"""
    vals = [float(r[key]) for r in seg if r[key] != "N/A"]
    return sum(vals) / len(vals) if vals else 0.0

# 用户数':>5: 用户数：表头名称之一；>: 右对齐；5: 当前文字占 5 个字符
print(f"{'用户数':>5}  {'QPS':>7}  {'P50':>5}  {'P95':>5}  {'P99':>5}  {'反推RT':>8}")
print("-" * 48)
for u in order:
    seg = stages[u]
    if len(seg) < MIN_SECONDS:
        continue
    tail = seg[-TAIL:]
    qps = sum(float(r["Requests/s"]) for r in tail) / len(tail)
    rt = u / qps * 1000 if qps else 0
    print(f"{u:>5}  {qps:>7.0f}  {avg_pct(tail,'50%'):>5.0f}  "
          f"{avg_pct(tail,'95%'):>5.0f}  {avg_pct(tail,'99%'):>5.0f}  {rt:>6.1f}ms")
