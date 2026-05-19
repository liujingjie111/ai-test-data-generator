"""
模板管理页面对象类
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from base.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class TemplatesPage(BasePage):
    """模板管理页面"""

    # 定位器
    # 页面标题
    PAGE_TITLE = (By.XPATH, '//*[contains(text(), "模板管理")]')

    # 新建模板按钮
    NEW_TEMPLATE_BUTTON = (By.XPATH, '//button[contains(., "新建模板")]')

    # 模板表格
    TEMPLATE_TABLE = (By.XPATH, '//div[contains(@class, "ant-table-wrapper")]')
    TEMPLATE_ROWS = (By.XPATH, '//div[contains(@class, "ant-table-wrapper")]//tbody/tr')

    # 模板编辑弹窗
    MODAL_TITLE = (By.XPATH, '//div[contains(@class, "ant-modal-title")]')
    MODAL_NAME_INPUT = (By.XPATH, '//input[@placeholder="请输入模板名称"] | //label[text()="模板名称"]/following::input[1]')
    MODAL_DESC_INPUT = (By.XPATH, '//textarea[@placeholder="请输入模板描述"] | //label[text()="描述"]/following::textarea[1]')

    # 字段配置
    ADD_FIELD_BUTTON = (By.XPATH, '//button[contains(., "添加字段")]')
    FIELD_CARDS = (By.XPATH, '//div[contains(@class, "ant-card")]')
    FIELD_TYPE_SELECT = (By.XPATH, '(//div[contains(@class, "ant-select")])[1]')
    FIELD_LABEL_INPUT = (By.XPATH, '(//input[@placeholder="请输入字段标签"])[1]')
    FIELD_DELETE_BUTTON = (By.XPATH, '(//button[contains(@class, "ant-btn-dangerous")])[1]')

    # 弹窗按钮
    SAVE_BUTTON = (By.XPATH, '//button[contains(., "保存") and @type="button"] | //button[text()="保存"]')
    CANCEL_BUTTON = (By.XPATH, '//button[contains(., "取消") and @type="button"] | //button[text()="取消"]')

    # 确认删除弹窗
    CONFIRM_DELETE_MODAL = (By.XPATH, '//div[contains(@class, "ant-modal-confirm-body")]')
    CONFIRM_DELETE_OK = (By.XPATH, '//button[contains(@class, "ant-btn-primary") and .//span[text()="确定"]]')
    CONFIRM_DELETE_CANCEL = (By.XPATH, '//button[not(contains(@class, "ant-btn-primary")) and .//span[text()="取消"]]')

    # 操作菜单
    ACTION_MENU_BUTTON = (By.XPATH, '(//button[contains(@type, "text")]//*[contains(@class, "anticon-ellipsis")])[1]')
    ACTION_GENERATE = (By.XPATH, '//div[contains(@class, "ant-dropdown-menu-item") and .//span[text()="生成数据"]]')
    ACTION_EDIT = (By.XPATH, '//div[contains(@class, "ant-dropdown-menu-item") and .//span[text()="编辑"]]')
    ACTION_COPY = (By.XPATH, '//div[contains(@class, "ant-dropdown-menu-item") and .//span[text()="复制"]]')
    ACTION_DELETE = (By.XPATH, '//div[contains(@class, "ant-dropdown-menu-item") and .//span[text()="删除"]]')

    # 消息提示
    SUCCESS_MESSAGE = (By.XPATH, '//div[contains(@class, "ant-message-success")]')
    ERROR_MESSAGE = (By.XPATH, '//div[contains(@class, "ant-message-error")]')

    def __init__(self, driver):
        super().__init__(driver)

    def click_new_template(self) -> None:
        """点击新建模板按钮"""
        logger.info("点击新建模板按钮")
        self.click(self.NEW_TEMPLATE_BUTTON)

    def fill_template_name(self, name: str) -> None:
        """
        填写模板名称

        Args:
            name: 模板名称
        """
        logger.info(f"填写模板名称: {name}")
        self.send_keys(self.MODAL_NAME_INPUT, name)

    def fill_template_description(self, description: str) -> None:
        """
        填写模板描述

        Args:
            description: 描述
        """
        logger.info(f"填写模板描述: {description}")
        self.send_keys(self.MODAL_DESC_INPUT, description)

    def click_add_field(self) -> None:
        """点击添加字段按钮"""
        logger.info("点击添加字段按钮")
        self.click(self.ADD_FIELD_BUTTON)
        time.sleep(0.5)

    def select_field_type(self, field_type: str, index: int = 0) -> None:
        """
        选择字段类型

        Args:
            field_type: 字段类型，如 "name", "email"
            index: 字段索引，默认为 0（第一个字段）
        """
        logger.info(f"选择字段类型: {field_type}")
        
        # 点击类型选择器
        select_locator = (By.XPATH, f'(//div[contains(@class, "ant-select")])[{index + 1}]')
        self.click(select_locator)
        time.sleep(0.5)
        
        # 选择类型
        option_locator = (By.XPATH, f'//div[contains(@class, "ant-select-item-option") and text()="{field_type}"]')
        self.click(option_locator)
        time.sleep(0.5)

    def fill_field_label(self, label: str, index: int = 0) -> None:
        """
        填写字段标签

        Args:
            label: 标签文本
            index: 字段索引，默认为 0
        """
        logger.info(f"填写字段标签: {label}")
        label_input_locator = (By.XPATH, f'(//input[@placeholder="请输入字段标签"])[{index + 1}]')
        self.send_keys(label_input_locator, label)

    def delete_field(self, index: int = 0) -> None:
        """
        删除字段

        Args:
            index: 字段索引，默认为 0
        """
        logger.info(f"删除字段: {index}")
        delete_button_locator = (By.XPATH, f'(//button[contains(@class, "ant-btn-dangerous")])[{index + 1}]')
        self.click(delete_button_locator)
        time.sleep(0.5)

    def click_save(self) -> None:
        """点击保存按钮"""
        logger.info("点击保存按钮")
        self.click(self.SAVE_BUTTON)

    def click_cancel(self) -> None:
        """点击取消按钮"""
        logger.info("点击取消按钮")
        self.click(self.CANCEL_BUTTON)

    def get_template_count(self) -> int:
        """
        获取模板数量

        Returns:
            模板数量
        """
        if self.is_element_present(self.TEMPLATE_TABLE):
            rows = self.find_elements(self.TEMPLATE_ROWS)
            return len(rows)
        return 0

    def find_template_by_name(self, name: str) -> bool:
        """
        根据名称查找模板

        Args:
            name: 模板名称

        Returns:
            是否找到
        """
        template_name_locator = (By.XPATH, f'//table//td[text()="{name}"]')
        return self.is_element_present(template_name_locator)

    def click_action_menu(self, index: int = 0) -> None:
        """
        点击模板操作菜单

        Args:
            index: 模板索引，默认为 0（第一个）
        """
        logger.info(f"点击第 {index + 1} 个模板的操作菜单")
        action_button_locator = (By.XPATH, f'(//button[contains(@type, "text")]//*[contains(@class, "anticon-ellipsis")])[{index + 1}]')
        self.click(action_button_locator)
        time.sleep(0.5)

    def click_action_generate(self) -> None:
        """点击操作菜单中的生成数据"""
        logger.info("点击生成数据")
        self.click(self.ACTION_GENERATE)

    def click_action_edit(self) -> None:
        """点击操作菜单中的编辑"""
        logger.info("点击编辑")
        self.click(self.ACTION_EDIT)

    def click_action_copy(self) -> None:
        """点击操作菜单中的复制"""
        logger.info("点击复制")
        self.click(self.ACTION_COPY)

    def click_action_delete(self) -> None:
        """点击操作菜单中的删除"""
        logger.info("点击删除")
        self.click(self.ACTION_DELETE)

    def confirm_delete(self) -> None:
        """确认删除"""
        logger.info("确认删除")
        self.wait_for_element_clickable(self.CONFIRM_DELETE_OK, timeout=5)
        self.click(self.CONFIRM_DELETE_OK)

    def cancel_delete(self) -> None:
        """取消删除"""
        logger.info("取消删除")
        self.wait_for_element_clickable(self.CONFIRM_DELETE_CANCEL, timeout=5)
        self.click(self.CONFIRM_DELETE_CANCEL)

    def wait_for_success_message(self, timeout: int = 10) -> bool:
        """
        等待成功消息

        Args:
            timeout: 超时时间

        Returns:
            是否显示
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.SUCCESS_MESSAGE)
            )
            return True
        except Exception:
            return False

    def wait_for_error_message(self, timeout: int = 10) -> bool:
        """
        等待错误消息

        Args:
            timeout: 超时时间

        Returns:
            是否显示
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.ERROR_MESSAGE)
            )
            return True
        except Exception:
            return False

    def is_on_templates_page(self) -> bool:
        """
        判断是否在模板管理页面

        Returns:
            是否在
        """
        return self.is_element_present(self.PAGE_TITLE, timeout=5)
