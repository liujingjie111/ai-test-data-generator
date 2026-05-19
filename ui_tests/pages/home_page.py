"""
首页页面对象类
"""
from selenium.webdriver.common.by import By

from base.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class HomePage(BasePage):
    """首页"""

    # 定位器 - 简化版本 - 直接通过文本查找
    PAGE_TITLE = (By.XPATH, '//*[contains(text(), "智能测试数据生成平台")]')

    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_home(self):
        """导航到首页 - 直接通过 URL"""
        logger.info("导航到首页")
        self.open("/")

    def navigate_to_generator(self):
        """导航到内置生成器 - 直接通过 URL"""
        logger.info("导航到内置生成器")
        self.open("/generator")

    def navigate_to_templates(self):
        """导航到模板管理 - 直接通过 URL"""
        logger.info("导航到模板管理")
        self.open("/templates")

    def navigate_to_ai_generator(self):
        """导航到 AI 生成 - 直接通过 URL"""
        logger.info("导航到 AI 生成")
        self.open("/ai-generator")

    def navigate_to_api_keys(self):
        """导航到 API 密钥 - 直接通过 URL"""
        logger.info("导航到 API 密钥")
        self.open("/api-keys")

    def navigate_to_history(self):
        """导航到历史记录 - 直接通过 URL"""
        logger.info("导航到历史记录")
        self.open("/history")

    def is_on_home_page(self) -> bool:
        """判断是否在首页"""
        return self.is_element_present(self.PAGE_TITLE, timeout=5)
