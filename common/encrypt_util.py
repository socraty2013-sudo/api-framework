# encrypt util：加密工具

import hashlib, hmac

# (text: str)	text 是参数名；
# : str 是说「这个参数应该是字符串」。类型注解--参数注解，声明 text 是字符串（仅注解，不是语法必需，写不写都能跑）
# -> str 是说「这个函数会返回字符串」。类型注解--返回值注解，声明函数返回字符串（仅注解。不是语法必需，写不写都能跑）
# 类型注解（type hints）—— Python 3.5 以后加的，不是语法必需，写不写都能跑。

# 属于哈希，输出数据长度：32位十六进制
def md5(text: str) -> str:
    """把明文内容通过 MD5 算成固定长度（32 位十六进制）的摘要，同样输入永远得到同样输出。"""

    #.encode() —— md5 只吃 bytes，不吃 str，必须先编码
    #.hexdigest() —— 把二进制摘要转成 32 位十六进制字符串（接口传的就是这个）
    #不调 .hexdigest() 拿到的是 bytes，塞进表单会出错
    md5_str = hashlib.md5(text.encode()).hexdigest()
    return md5_str


# 和 MD5同事哈希，输出数据长度：64 位十六进制。用法和 MD5 完全相同
def sha256(text: str) -> str:
    """把明文内容通过 MD5 算成固定长度（32 位十六进制）的摘要，同样输入永远得到同样输出。"""

    #.encode() —— md5 只吃 bytes，不吃 str，必须先编码
    #.hexdigest() —— 把二进制摘要转成 32 位十六进制字符串（接口传的就是这个）
    #不调 .hexdigest() 拿到的是 bytes，塞进表单会出错
    sha256_str = hashlib.sha256(text.encode()).hexdigest()
    return sha256_str

# HMAC（Hash-based Message Authentication Code）：基于哈希的消息认证码 -- 真实项目用这个
# HMAC-SHA256 = 用 SHA256 这个哈希算法，套上 HMAC 规则，带上密钥计算。
def hmac_sha256(key: str, msg: str) -> str:
    # 三个参数：密钥、消息、哈希算法。
    hmac_str = hmac.new(key.encode(), msg.encode(), hashlib.sha256).hexdigest()
    return hmac_str

if __name__ == '__main__':
    print(md5("123456"))
    print(len(md5("123456")))