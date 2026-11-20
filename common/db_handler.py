# 数据库连接及执行配置

import sqlite3

from config import config


class DBHandler:
    def __init__(self, db_path=None):
        self.db_path = db_path or config["db_path"]    # 不传就用配置里的路径

    def query_all(self, sql, params=()):  # 第二个参数建议写成这种 params=()，() 想单一占位符?传空。调用传参，第二个参数用("xxxx",）的方式
        """查多条，返回字典列表。

        db.query_all("SELECT * FROM users WHERE username = ?", ("admin",))
        → [{'id': 1, 'username': 'admin', 'password': '123456'}]
        """
        conn = sqlite3.connect(self.db_path)           # sqlite 是文件型库，给路径就连上
        conn.row_factory = sqlite3.Row                 # 让每行能按字段名取 row["username"]；不设只能 row[1]。row_factory是 conn下的属性，去接收字段名取列的作用（还是没搞懂，就搞不懂为啥要这样写）
        rows = conn.execute(sql, params).fetchall()    # params 按顺序填给 ?；fetchall 取全部（fetchone 取一行，fetchmany(n) 取 n 行）
        conn.close()                                   # 查询不需要 commit
        return [dict(r) for r in rows]                 # Row 对象转普通字典，方便取值、序列化

    def execute(self, sql, params=()):
        """增删改，返回受影响行数。

        db.execute("DELETE FROM products WHERE id = ?", (5,))
        → 1 表示删掉一行；0 表示没有这条记录
        """
        conn = sqlite3.connect(self.db_path)
        cur = conn.execute(sql, params)                # execute()内部生成游标，游标执行 sql，同时返回游标存到cur，rowcount 从它上面取
        conn.commit()                                  # 不提交，数据不会写进文件
        conn.close()
        return cur.rowcount                            # 实际改了几行；属性，不加括号
