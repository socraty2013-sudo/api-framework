"""UI 相关的 fixture"""

import os
import allure
import pytest
from common.ui_utils import get_driver

# 截图存放目录
SCREENSHOT_DIR = os.path.join("output", "screenshots")

@pytest.fixture
def driver():
    """每个用例一个全新的浏览器；用例结束无论成败都关掉"""
    d = get_driver()
    yield d
    d.quit()


# @pytest.hookimpl 是 pytest 自带的装饰器，作用是调节钩子的行为。hookwrapper=True 是它最常用的参数。
# 翻译成人话：告诉 pytest「我这个函数不是普通钩子，我要包住你的执行过程，等你干完再把结果给我」。

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # 这是pytest自带钩子：每一条用例执行完、准备生成结果报告的时候自动跑
    # hookwrapper=True 代表包装模式：先等pytest跑完用例，我们再拿结果做处理，必须搭配yield
    # item：当前正在跑的这条用例对象
    # call：pytest内部记录本次运行信息的对象，本例没直接使用

    """钩子：UI 用例失败就截图并挂进 Allure"""

    # yield：在这里暂停，把执行权交给pytest（无需带内容），让pytest先把用例完整跑完（「你去生成报告吧」）
    # pytest 把结果（成功失败，还包含异常信息、时长等）装进 outcome 还回来
    # 代码才会继续执行yield后面的内容
    outcome = yield
    # 从outcome里面取出这条用例最终的执行结果信息，存到report
    report = outcome.get_result()

    # 一条用例分3个阶段：setup前置、call跑测试代码、teardown后置清理
    # report.when 用来判断当前是哪个阶段
    # 我们只关心【真正跑测试代码（call阶段）】并且是失败的情况
    # 只要不是call阶段，或者用例没有失败，直接return退出函数，不截图
    if report.when != "call" or not report.failed:
        return

    # item.funcargs：当前这条用例能拿到的所有fixture变量，是字典
    # 尝试获取driver（浏览器对象），接口用例没有driver，拿出来就是None
    d = item.funcargs.get("driver")
    # 如果拿不到浏览器对象，说明不是UI用例，直接退出，不截图防止报错
    if d is None:
        return

    # 文件夹不存在就创建；exist_ok=True：文件夹已经存在时不会抛出报错
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    # 拼接截图完整保存路径，截图文件名使用当前用例的名字
    path = os.path.join(SCREENSHOT_DIR, f"{item.name}.png")
    # 调用selenium浏览器对象，对当前页面截图并保存到上面路径
    d.save_screenshot(path)

    # 将截图文件附加到allure报告中，打开报告就能直接查看这张失败截图
    allure.attach.file(path, name="失败截图", attachment_type=allure.attachment_type.PNG)


"""
report.when      # "call" 才继续
report.failed    # True 才继续
item.name        # 当前用例名
item.funcargs    # 当前用例拿到的夹具，字典
"""
