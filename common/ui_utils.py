"""UI 通用动作：创建浏览器、等元素、点击、输入"""
import os

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import config

# 默认最多等几秒，从配置里读（base.yaml 的 timeout: 10）
DEFAULT_TIMEOUT = config.get("timeout", 10)


def get_driver(browser=None):
    """创建浏览器。选择顺序：函数参数 > 环境变量 BROWSER > 配置文件 > 默认 chrome"""

    # config.get(key, default): 字典里有 browser 这个 key：返回它对应的值; 没有，不会抛 KeyError，直接返回第二个参数，也就是默认值chrome
    browser = browser or os.environ.get("BROWSER") or config.get("browser", "chrome")

    # 无头模式 = 不弹真窗口，后台跑。调试阶段先注释掉，肉眼能看到浏览器在动
    # 以后放 CI 里跑，把这行打开
    # options.add_argument("--headless=new")

    if browser == "firefox":
        return webdriver.Firefox()
    if browser == "edge":
        return webdriver.Edge()
    return webdriver.Chrome()


def wait_element(driver, locator, timeout=DEFAULT_TIMEOUT):
    """等元素出现并且可见，返回该元素。超时就抛 TimeoutException"""
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(locator)
    )

def click(driver, locator, timeout=DEFAULT_TIMEOUT):
    """等元素可见后点击它"""
    wait_element(driver, locator, timeout).click()

def input_text(driver, locator, text, timeout=DEFAULT_TIMEOUT):
    """等元素可见后，先清空再输入"""
    el = wait_element(driver, locator, timeout)
    el.clear()
    el.send_keys(text)

def get_text(driver, locator, timeout=DEFAULT_TIMEOUT):
    """等元素可见后，取它的文字"""
    return wait_element(driver, locator, timeout).text

def wait_url_changes(driver, old_url, timeout=DEFAULT_TIMEOUT):
    """等浏览器地址变了。点完按钮会跳转时用：先记下旧地址，点，再等它变"""

    # EC.url_changes(old_url)：Selenium 内置条件，意思是「当前地址和 old_url 不一样了」
    WebDriverWait(driver, timeout).until(EC.url_changes(old_url))