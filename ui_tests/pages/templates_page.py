"""
模板管理页面对象类
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from base.base_page import BasePage
from config import EXPLICIT_WAIT, EXPLICIT_WAIT_SHORT
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
    # 使用字段标签来计数（只有字段卡片才有字段标签输入框）
    FIELD_SELECTORS = (By.XPATH, '//div[contains(@class, "ant-modal-wrap") and contains(@style, "display: block")]//div[contains(@class, "ant-select-selector")]')
    FIELD_TYPE_SELECT = (By.XPATH, '(//div[contains(@class, "ant-select")])[1]')
    FIELD_LABEL_INPUT = (By.XPATH, '(//input[@placeholder="请输入字段标签"])[1]')
    FIELD_DELETE_BUTTON = (By.XPATH, '(//button[contains(@class, "ant-btn-dangerous")])[1]')

    # 弹窗按钮
    # 使用包含"保存"文本的主要按钮
    SAVE_BUTTON = (By.XPATH, "//button[contains(@class, 'ant-btn-primary') and contains(., '保')]")
    CANCEL_BUTTON = (By.XPATH, "//button[contains(., '取') and not(contains(@class, 'ant-btn-primary'))]")

    # 确认删除弹窗
    CONFIRM_DELETE_MODAL = (By.XPATH, '//div[contains(@class, "ant-modal-confirm-body")]')
    CONFIRM_DELETE_OK = (By.XPATH, '//button[contains(@class, "ant-btn-primary") and contains(., "确")]')
    CONFIRM_DELETE_CANCEL = (By.XPATH, '//button[contains(., "取") and not(contains(@class, "ant-btn-primary"))]')

    # 操作菜单
    # 使用更简单的方式找到操作按钮 - 只要是在表格行中的按钮就行
    ACTION_MENU_BUTTON = (By.XPATH, '(//button[@type="text"])[1]')
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
        try:
            element = self.wait_for_element_clickable(self.MODAL_NAME_INPUT)
            element.clear()
            element.send_keys(name)
        except Exception as e:
            logger.warning(f"标准方式失败，尝试JavaScript: {e}")
            try:
                element = self.find_element(self.MODAL_NAME_INPUT)
                self.driver.execute_script("arguments[0].value = '';", element)
                self.driver.execute_script(f"arguments[0].value = '{name}';", element)
                self.driver.execute_script("arguments[0].dispatchEvent(new Event('input'));", element)
                self.driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", element)
            except Exception as e2:
                logger.error(f"JavaScript也失败: {e2}")
                raise

    def fill_template_description(self, description: str) -> None:
        """
        填写模板描述

        Args:
            description: 描述
        """
        logger.info(f"填写模板描述: {description}")
        try:
            self.send_keys(self.MODAL_DESC_INPUT, description)
        except Exception as e:
            logger.warning(f"标准方式失败，尝试JavaScript: {e}")
            # 使用 JavaScript 直接设置值
            elements = self.driver.find_elements(*self.MODAL_DESC_INPUT)
            if elements:
                self.driver.execute_script("arguments[0].value = '';", elements[0])
                self.driver.execute_script("arguments[0].value = arguments[1];", elements[0], description)
                # 触发 change 事件
                self.driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", elements[0])

    def click_add_field(self, current_field_count: int = None) -> int:
        """
        点击添加字段按钮，并等待新字段卡片出现

        Args:
            current_field_count: 当前字段数量（不含外层包装卡片）。如果不传，自动检测。

        Returns:
            新添加字段的索引（从 0 开始）
        """
        logger.info("点击添加字段按钮")

        if current_field_count is None:
            js_count = """
                const visibleModal = document.querySelector('.ant-modal-wrap:not([style*="display: none"])');
                return visibleModal ? visibleModal.querySelectorAll('.ant-card-small').length : 0;
            """
            current_field_count = self.driver.execute_script(js_count)

        logger.info(f"当前字段数量: {current_field_count}")

        add_btn = self.find_element(self.ADD_FIELD_BUTTON)
        add_btn.click()

        WebDriverWait(self.driver, EXPLICIT_WAIT).until(
            lambda d: d.execute_script("""
                const visibleModal = document.querySelector('.ant-modal-wrap:not([style*="display: none"])');
                return visibleModal ? visibleModal.querySelectorAll('.ant-card-small').length : 0;
            """) > current_field_count
        )

        logger.info(f"新字段已出现")
        self.scroll_to_bottom()
        new_field_index = current_field_count
        logger.info(f"新添加字段的索引: {new_field_index}")
        return new_field_index
    
    def scroll_to_bottom(self) -> None:
        """滚动模态框内容到底部"""
        logger.info("滚动到模态框底部")
        try:
            # 查找模态框内容区域
            modal_body = self.driver.find_element(By.CSS_SELECTOR, ".ant-modal-body")
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", modal_body)
        except Exception as e:
            logger.warning(f"滚动失败: {e}")

    def select_field_type(self, field_type: str, index: int = 0) -> None:
        """
        选择字段类型

        Args:
            field_type: 字段类型名称
            index: 字段索引，默认为 0（第一个字段）
        """
        logger.info(f"========== 选择字段类型: {field_type}, 索引: {index} ==========")
        
        # 关键修复：先关闭所有可能还开着的下拉框，避免选项错位
        self._close_all_dropdowns()
        
        # 使用 JavaScript 找到目标选择器并滚动到视图中（只滚动模态框内部，不滚动整个页面）
        js_find_selector = f"""
            const allWrappers = document.querySelectorAll('.ant-modal-wrap');
            let visibleModal = null;
            for (const wrapper of allWrappers) {{
                const style = wrapper.getAttribute('style') || '';
                if (!style.includes('display: none')) {{
                    visibleModal = wrapper;
                    break;
                }}
            }}
            if (!visibleModal) return 'error: no visible modal';
            
            const fieldCards = visibleModal.querySelectorAll('.ant-card-small');
            if (fieldCards.length <= {index}) return 'error: index out of range, count=' + fieldCards.length;
            
            let info = 'Total field cards: ' + fieldCards.length + ', target index: {index}\\n';
            fieldCards.forEach((card, i) => {{
                const selector = card.querySelector('.ant-select-selector');
                const currentValue = selector ? selector.textContent.trim() : 'N/A';
                info += '  Card ' + i + ': value=' + currentValue + '\\n';
            }});
            
            const targetCard = fieldCards[{index}];
            const typeSelector = targetCard.querySelector('.ant-select-selector');
            if (!typeSelector) return 'error: no selector in target card';
            
            // 只滚动模态框内部的滚动条，不滚动整个页面
            const modalBody = visibleModal.querySelector('.ant-modal-body');
            if (modalBody) {{
                const cardTop = typeSelector.offsetTop;
                const cardHeight = typeSelector.offsetHeight;
                const modalScrollTop = modalBody.scrollTop;
                const modalHeight = modalBody.clientHeight;
                
                // 如果元素在可视区域外，才滚动
                if (cardTop < modalScrollTop || cardTop + cardHeight > modalScrollTop + modalHeight) {{
                    modalBody.scrollTop = cardTop - modalHeight / 2 + cardHeight / 2;
                }}
            }}
            
            return 'success\\n' + info;
        """
        result = self.driver.execute_script(js_find_selector)
        logger.info(f"JS 定位结果:\n{result}")

        if result is None or result.startswith('error:'):
            logger.error(f"未找到可见模态框或索引 {index} 超出范围: {result}")
            raise Exception(f"未找到可见模态框或字段索引 {index} 超出范围: {result}")

        # 使用 Selenium 找到精确的可见模态框中的字段卡片选择器
        # 关键：只选择可见模态框中 .ant-card-small 内的 .ant-select-selector
        try:
            visible_wrappers = self.driver.find_elements(
                By.XPATH, '//div[contains(@class, "ant-modal-wrap") and not(contains(@style, "display: none"))]'
            )
            if not visible_wrappers:
                raise Exception("未找到可见模态框")
            visible_wrapper = visible_wrappers[0]

            small_cards = visible_wrapper.find_elements(By.CSS_SELECTOR, '.ant-card-small')
            if len(small_cards) <= index:
                raise Exception(f"索引 {index} 超出范围，只有 {len(small_cards)} 个字段卡片")

            target_card = small_cards[index]
            type_selector = target_card.find_element(By.CSS_SELECTOR, '.ant-select-selector')

            logger.info(f"目标元素标签: {type_selector.tag_name}")
            logger.info(f"目标元素文本: {type_selector.text}")
            logger.info(f"目标元素位置: x={type_selector.location['x']}, y={type_selector.location['y']}")

            type_selector.click()
            logger.info(f"成功点击索引 {index} 的选择器")
        except Exception as e:
            logger.error(f"点击选择器失败: {e}")
            raise

        # 等待下拉选项出现（只等待当前打开的下拉框）
        try:
            WebDriverWait(self.driver, EXPLICIT_WAIT_SHORT).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[contains(@class, "ant-select-dropdown") and not(contains(@class, "ant-select-dropdown-hidden"))]//div[contains(@class, "ant-select-item-option")]')
                )
            )
            logger.info("下拉选项已出现")
        except Exception as e:
            logger.error(f"下拉选项未出现: {e}")
            raise

        # 关键修复：只查找当前可见下拉框中的选项，避免点到其他下拉框的选项
        option_xpaths = [
            f'//div[contains(@class, "ant-select-dropdown") and not(contains(@class, "ant-select-dropdown-hidden"))]//div[contains(@class, "ant-select-item-option") and .//div[text()="{field_type}"]]',
            f'//div[contains(@class, "ant-select-dropdown") and not(contains(@class, "ant-select-dropdown-hidden"))]//div[contains(@class, "ant-select-item-option") and contains(text(), "{field_type}")]',
        ]

        option_found = False
        for xpath in option_xpaths:
            options = self.driver.find_elements(By.XPATH, xpath)
            if options:
                logger.info(f"使用 XPath 找到选项: {xpath}")
                WebDriverWait(self.driver, EXPLICIT_WAIT_SHORT).until(
                    EC.element_to_be_clickable(options[0])
                )
                # 使用 JavaScript 点击选项（Ant Design 下拉选项元素可能不可直接交互）
                self.driver.execute_script("arguments[0].click();", options[0])
                option_found = True
                break

        if not option_found:
            logger.error(f"没有找到类型选项: {field_type}")
            raise Exception(f"没有找到字段类型选项: {field_type}")

        # Ant Design 的 Select 下拉框需要手动关闭
        WebDriverWait(self.driver, EXPLICIT_WAIT_SHORT).until(
            EC.invisibility_of_element_located(
                (By.CSS_SELECTOR, '.ant-select-dropdown:not(.ant-select-dropdown-hidden)')
            )
        )

        logger.info(f"========== 字段类型选择完成: {field_type} ==========")

    def _close_all_dropdowns(self) -> None:
        """关闭所有可能还开着的下拉框，避免选项错位"""
        logger.info("关闭所有下拉框")
        body = self.driver.find_element(By.TAG_NAME, 'body')
        body.send_keys('\ue00c')
        try:
            WebDriverWait(self.driver, EXPLICIT_WAIT_SHORT).until(
                EC.invisibility_of_element_located(
                    (By.CSS_SELECTOR, '.ant-select-dropdown:not(.ant-select-dropdown-hidden)')
                )
            )
        except Exception:
            logger.warning("下拉框未自动关闭，点击 body 强制关闭")
            body.click()

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
        self.click_and_retry(delete_button_locator)

    def click_save(self) -> None:
        """点击保存按钮"""
        logger.info("点击保存按钮")
        self.scroll_to_bottom()
        save_btn = WebDriverWait(self.driver, EXPLICIT_WAIT).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class, 'ant-btn-primary') and .//span[contains(text(), '保')]]")
            )
        )
        save_btn.click()
        try:
            WebDriverWait(self.driver, EXPLICIT_WAIT).until(
                EC.invisibility_of_element_located(self.MODAL_TITLE)
            )
            logger.info("模态框已关闭")
        except Exception:
            logger.info("模态框未关闭（可能已有消息提示）")

    def click_cancel(self) -> None:
        """点击取消按钮"""
        logger.info("点击取消按钮")
        cancel_btn = WebDriverWait(self.driver, EXPLICIT_WAIT_SHORT).until(
            EC.element_to_be_clickable(self.CANCEL_BUTTON)
        )
        cancel_btn.click()

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

    def wait_for_template_gone(self, name: str, timeout: int = 10) -> bool:
        """
        等待模板名称从表格中消失（删除后表格刷新需要时间）

        Args:
            name: 模板名称
            timeout: 超时时间

        Returns:
            是否已消失
        """
        try:
            template_name_locator = (By.XPATH, f'//table//td[text()="{name}"]')
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(template_name_locator)
            )
            return True
        except Exception:
            return False

    def _click_dropdown_menu_item(self, item_text: str) -> None:
        """
        点击下拉菜单中的指定菜单项（通用方法）
        等待菜单出现后，查找匹配文本的菜单项并点击

        Args:
            item_text: 菜单项文本（如"编辑"、"删除"）
        """
        logger.info(f"点击下拉菜单项: {item_text}")
        menu_item_xpath = f"//*[contains(@class, 'ant-dropdown-menu-item') and contains(., '{item_text}')]"
        menu_item = WebDriverWait(self.driver, EXPLICIT_WAIT).until(
            EC.element_to_be_clickable((By.XPATH, menu_item_xpath))
        )
        menu_item.click()

    def click_action_menu(self, index: int = 0, template_name: str = None) -> None:
        """
        点击模板操作菜单

        Args:
            index: 模板索引，默认为 0（第一个）
            template_name: 可选，指定要操作的模板名称
        """
        logger.info(f"点击第 {index + 1} 个模板的操作菜单")
        if template_name:
            logger.info(f"查找模板: {template_name}")

        table_rows = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'ant-table-wrapper')]//tbody//tr")
        target_row = None

        if template_name:
            for row in table_rows:
                if template_name in row.text:
                    target_row = row
                    logger.info(f"找到模板: {template_name}")
                    break

        if not target_row and len(table_rows) > index:
            target_row = table_rows[index]
            logger.info(f"使用索引 {index} 的模板")

        if target_row:
            cells = target_row.find_elements(By.TAG_NAME, "td")
            if cells:
                action_cell = cells[-1]
                ActionChains(self.driver).move_to_element(action_cell).perform()
                buttons = action_cell.find_elements(By.TAG_NAME, "button")
                if buttons:
                    buttons[-1].click()
                    return

        logger.warning("未找到目标行或操作按钮")

    def click_action_generate(self) -> None:
        """点击操作菜单中的生成数据"""
        self._click_dropdown_menu_item("生成数据")

    def click_action_edit(self) -> None:
        """点击操作菜单中的编辑"""
        self._click_dropdown_menu_item("编辑")
        # 等待编辑模态框完全打开（Ant Design 模态框有打开动画）
        WebDriverWait(self.driver, EXPLICIT_WAIT).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class, "ant-modal-title") and contains(text(), "编辑模板")]')
            )
        )

    def click_action_copy(self) -> None:
        """点击操作菜单中的复制"""
        self._click_dropdown_menu_item("复制")

    def click_action_delete(self) -> None:
        """点击操作菜单中的删除"""
        self._click_dropdown_menu_item("删除")

    def confirm_delete(self) -> None:
        """确认删除"""
        logger.info("确认删除")
        # 先等待确认弹窗出现
        WebDriverWait(self.driver, EXPLICIT_WAIT).until(
            EC.visibility_of_element_located(self.CONFIRM_DELETE_MODAL)
        )
        confirm_btn = WebDriverWait(self.driver, EXPLICIT_WAIT).until(
            EC.element_to_be_clickable(self.CONFIRM_DELETE_OK)
        )
        confirm_btn.click()

    def cancel_delete(self) -> None:
        """取消删除"""
        logger.info("取消删除")
        cancel_btn = WebDriverWait(self.driver, EXPLICIT_WAIT_SHORT).until(
            EC.element_to_be_clickable(self.CONFIRM_DELETE_CANCEL)
        )
        cancel_btn.click()

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

    def get_template_info(self, template_name: str) -> dict:
        """
        获取模板的详细信息

        Args:
            template_name: 模板名称

        Returns:
            包含模板信息的字典
        """
        logger.info(f"获取模板信息: {template_name}")

        table_rows = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'ant-table-wrapper')]//tbody//tr")
        
        for row in table_rows:
            try:
                if template_name in row.text:
                    # 获取这一行的所有单元格
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if len(cells) >= 3:
                        info = {
                            "name": cells[0].text.strip(),
                            "description": cells[1].text.strip() if len(cells) > 1 else "",
                            "field_count": int(cells[2].text.strip()) if len(cells) > 2 else 0
                        }
                        logger.info(f"找到模板信息: {info}")
                        return info
            except Exception as e:
                logger.warning(f"解析行失败: {e}")
        
        return {"name": "", "description": "", "field_count": 0}
