"""
内置生成器页面对象类
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from base.base_page import BasePage
from config import EXPLICIT_WAIT, EXPLICIT_WAIT_LONG, EXPLICIT_WAIT_SHORT
from utils.logger import get_logger

logger = get_logger(__name__)


class GeneratorPage(BasePage):
    """内置生成器页面"""

    # 定位器
    PAGE_TITLE = (By.XPATH, '//*[contains(text(), "内置生成器") or contains(text(), "使用模板")]')
    
    # Cascader 级联选择器 - 需要点击可见的选择器元素而非隐藏的 input
    GENERATOR_SELECTOR = (By.XPATH, '//input[@id="generator-type"]/ancestor::div[contains(@class, "ant-select-selector")]')
    COUNT_INPUT = (By.ID, 'count-input')
    GENERATE_BUTTON = (By.ID, 'generate-btn')
    RANGE_MIN_INPUT = (By.ID, 'range-min')
    RANGE_MAX_INPUT = (By.ID, 'range-max')
    
    # 数据表格
    DATA_TABLE = (By.XPATH, '//div[contains(@class, "ant-table-wrapper")]')
    TABLE_ROWS = (By.XPATH, '//div[contains(@class, "ant-table-wrapper")]//tbody/tr')
    
    # 错误提示
    ERROR_MESSAGE = (By.XPATH, '//div[contains(@class, "ant-message-error")]')
    SUCCESS_MESSAGE = (By.XPATH, '//div[contains(@class, "ant-message-success")]')
    # 内联表单错误提示
    INLINE_ERROR = (By.XPATH, '//div[contains(@class, "ant-form-item-explain-error")]')

    def select_generator(self, category: str, generator: str) -> None:
        """
        选择生成器

        Args:
            category: 分类名称，如 "个人数据"
            generator: 生成器名称，如 "姓名"
        """
        logger.info(f"选择生成器: {category} -> {generator}")
        
        # 点击级联选择器（可见的选择器元素）
        self.click(self.GENERATOR_SELECTOR)
        
        # 点击分类
        cat_locator = (By.XPATH, f'//li[contains(@class, "ant-cascader-menu-item") and contains(., "{category}")]')
        cat_elem = WebDriverWait(self.driver, EXPLICIT_WAIT).until(
            EC.element_to_be_clickable(cat_locator)
        )
        cat_elem.click()
        
        # 点击生成器
        gen_locator = (By.XPATH, f'//li[contains(@class, "ant-cascader-menu-item") and contains(., "{generator}")]')
        gen_elem = WebDriverWait(self.driver, EXPLICIT_WAIT).until(
            EC.element_to_be_clickable(gen_locator)
        )
        gen_elem.click()

    def set_count(self, count: int) -> None:
        """
        设置生成数量

        Args:
            count: 生成数量
        """
        logger.info(f"设置生成数量: {count}")
        
        # 找到输入框
        count_input = WebDriverWait(self.driver, EXPLICIT_WAIT).until(
            EC.presence_of_element_located(self.COUNT_INPUT)
        )
        
        # 激活输入框并清除现有值
        count_input.click()
        count_input.send_keys(Keys.CONTROL + "a")
        count_input.send_keys(Keys.BACKSPACE)
        
        # 输入新值
        count_input.send_keys(str(count))

    def set_range(self, min_val: float, max_val: float) -> None:
        """
        设置范围参数

        Args:
            min_val: 最小值
            max_val: 最大值
        """
        logger.info(f"设置范围: {min_val} - {max_val}")
        
        # 设置最小值
        if min_val is not None:
            min_input = WebDriverWait(self.driver, EXPLICIT_WAIT).until(
                EC.presence_of_element_located(self.RANGE_MIN_INPUT)
            )
            min_input.click()
            min_input.send_keys(Keys.CONTROL + "a")
            min_input.send_keys(Keys.BACKSPACE)
            min_input.send_keys(str(min_val))
        
        # 设置最大值
        if max_val is not None:
            max_input = WebDriverWait(self.driver, EXPLICIT_WAIT).until(
                EC.presence_of_element_located(self.RANGE_MAX_INPUT)
            )
            max_input.click()
            max_input.send_keys(Keys.CONTROL + "a")
            max_input.send_keys(Keys.BACKSPACE)
            max_input.send_keys(str(max_val))

    def click_generate(self) -> None:
        """点击生成按钮"""
        logger.info("点击生成按钮")
        self.click(self.GENERATE_BUTTON)

    def wait_for_data_generated(self, timeout: int = None) -> bool:
        """
        等待数据生成完成

        Args:
            timeout: 超时时间（秒），默认使用配置中的长超时

        Returns:
            是否成功生成
        """
        if timeout is None:
            timeout = EXPLICIT_WAIT_LONG
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.DATA_TABLE)
            )
            return True
        except Exception as e:
            logger.warning(f"等待数据生成超时: {e}")
            return False

    def get_row_count(self) -> int:
        """
        获取表格行数

        Returns:
            行数
        """
        try:
            rows = self.driver.find_elements(*self.TABLE_ROWS)
            logger.info(f"找到 {len(rows)} 个数据行")
            return len(rows)
        except Exception as e:
            logger.error(f"获取行数量失败: {e}")
            return 0

    def is_error_message_displayed(self, timeout: int = 5) -> bool:
        """
        检查错误信息是否显示

        Args:
            timeout: 超时时间（秒）

        Returns:
            是否显示
        """
        return self.is_element_present(self.ERROR_MESSAGE, timeout=timeout)
    
    def is_inline_error_displayed(self, timeout: int = 5) -> bool:
        """
        检查内联表单错误提示是否显示

        Args:
            timeout: 超时时间（秒）

        Returns:
            是否显示
        """
        return self.is_element_present(self.INLINE_ERROR, timeout=timeout)

    def is_on_generator_page(self) -> bool:
        """
        判断是否在生成器页面

        Returns:
            是否在
        """
        return self.is_element_present(self.PAGE_TITLE, timeout=5)
