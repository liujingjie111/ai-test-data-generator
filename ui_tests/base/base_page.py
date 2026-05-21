"""
基础页面类
所有页面对象的基类，包含通用的元素定位和操作方法
"""
from typing import List, Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from config import BASE_URL, EXPLICIT_WAIT
from utils.logger import get_logger


logger = get_logger(__name__)


class BasePage:
    """基础页面类"""

    def __init__(self, driver: WebDriver, base_url: str = None):
        """
        初始化基础页面

        Args:
            driver: Selenium WebDriver 对象
            base_url: 基础 URL，默认从配置读取
        """
        self.driver = driver
        self.base_url = base_url or BASE_URL
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT)

    def open(self, url: str = "") -> None:
        """
        打开页面

        Args:
            url: 相对或绝对 URL
        """
        if url.startswith("http"):
            full_url = url
        else:
            full_url = f"{self.base_url}{url}"
        logger.info(f"打开页面: {full_url}")
        self.driver.get(full_url)

    def find_element(self, locator: tuple) -> WebElement:
        """
        查找单个元素

        Args:
            locator: 定位器元组，如 (By.ID, "id")

        Returns:
            找到的 WebElement
        """
        logger.debug(f"查找元素: {locator}")
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator: tuple) -> List[WebElement]:
        """
        查找多个元素

        Args:
            locator: 定位器元组

        Returns:
            WebElement 列表
        """
        logger.debug(f"查找多个元素: {locator}")
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator: tuple) -> None:
        """
        点击元素（等待元素可点击后再点击）

        Args:
            locator: 定位器元组
        """
        element = self.wait_for_element_clickable(locator)
        logger.info(f"点击元素: {locator}")
        element.click()

    def click_by_element(self, element: WebElement) -> None:
        """
        直接点击 WebElement 对象（避免每次重新查找）

        Args:
            element: WebElement 对象
        """
        logger.info(f"点击元素: tag={element.tag_name}, text={element.text[:30]}")
        element.click()

    def click_and_retry(self, locator: tuple, retries: int = 3) -> None:
        """
        带重试的点击，适用于 Ant Design 等动态组件

        Args:
            locator: 定位器元组
            retries: 重试次数
        """
        for attempt in range(retries):
            try:
                element = self.wait_for_element_clickable(locator)
                element.click()
                return
            except Exception as e:
                if attempt == retries - 1:
                    raise
                logger.warning(f"点击失败(第{attempt + 1}次)，重试: {e}")

    def send_keys(self, locator: tuple, text: str, clear: bool = True) -> None:
        """
        输入文本

        Args:
            locator: 定位器元组
            text: 要输入的文本
            clear: 是否先清空内容
        """
        element = self.wait_for_element_clickable(locator)
        if clear:
            element.clear()
        logger.info(f"输入文本: {text} 到元素: {locator}")
        element.send_keys(text)

    def get_text(self, locator: tuple) -> str:
        """
        获取元素文本

        Args:
            locator: 定位器元组

        Returns:
            元素文本
        """
        text = self.find_element(locator).text
        logger.debug(f"获取元素文本: {text}")
        return text

    def is_element_present(self, locator: tuple, timeout: int = 3) -> bool:
        """
        检查元素是否存在

        Args:
            locator: 定位器元组
            timeout: 超时时间（秒）

        Returns:
            是否存在
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except Exception:
            return False

    def is_element_visible(self, locator: tuple, timeout: int = 3) -> bool:
        """
        检查元素是否可见

        Args:
            locator: 定位器元组
            timeout: 超时时间（秒）

        Returns:
            是否可见
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except Exception:
            return False

    def wait_for_element_clickable(self, locator: tuple, timeout: int = 10) -> WebElement:
        """
        等待元素可点击

        Args:
            locator: 定位器元组
            timeout: 超时时间（秒）

        Returns:
            WebElement
        """
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_for_element_visible(self, locator: tuple, timeout: int = 10) -> WebElement:
        """
        等待元素可见

        Args:
            locator: 定位器元组
            timeout: 超时时间（秒）

        Returns:
            WebElement
        """
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_text(self, locator: tuple, text: str, timeout: int = 10) -> bool:
        """
        等待元素包含指定文本

        Args:
            locator: 定位器元组
            text: 期望的文本
            timeout: 超时时间（秒）

        Returns:
            是否匹配
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.text_to_be_present_in_element(locator, text)
            )
            return True
        except Exception:
            return False

    def switch_to_frame(self, locator: tuple) -> None:
        """
        切换到 iframe

        Args:
            locator: iframe 定位器
        """
        frame = self.find_element(locator)
        self.driver.switch_to.frame(frame)
        logger.info("切换到 iframe")

    def switch_to_default_content(self) -> None:
        """切换回默认内容"""
        self.driver.switch_to.default_content()
        logger.info("切换回默认内容")

    def execute_script(self, script: str, *args):
        """
        执行 JavaScript 脚本

        Args:
            script: JavaScript 脚本
            *args: 脚本参数

        Returns:
            脚本执行结果
        """
        return self.driver.execute_script(script, *args)

    def scroll_to_element(self, locator: tuple) -> None:
        """
        滚动到元素位置

        Args:
            locator: 定位器元组
        """
        element = self.find_element(locator)
        self.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        logger.info(f"滚动到元素: {locator}")

    def hover(self, locator: tuple) -> None:
        """
        鼠标悬停

        Args:
            locator: 定位器元组
        """
        element = self.find_element(locator)
        ActionChains(self.driver).move_to_element(element).perform()
        logger.info(f"鼠标悬停到元素: {locator}")

    def get_attribute(self, locator: tuple, attribute: str) -> str:
        """
        获取元素属性

        Args:
            locator: 定位器元组
            attribute: 属性名

        Returns:
            属性值
        """
        return self.find_element(locator).get_attribute(attribute)

    def accept_alert(self, timeout: int = 5) -> None:
        """
        接受警告框

        Args:
            timeout: 超时时间（秒）
        """
        alert = WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
        alert.accept()
        logger.info("接受警告框")

    def dismiss_alert(self, timeout: int = 5) -> None:
        """
        取消警告框

        Args:
            timeout: 超时时间（秒）
        """
        alert = WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
        alert.dismiss()
        logger.info("取消警告框")

    def refresh(self) -> None:
        """刷新页面"""
        self.driver.refresh()
        logger.info("刷新页面")

    def get_current_url(self) -> str:
        """获取当前 URL"""
        return self.driver.current_url
