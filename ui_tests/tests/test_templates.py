"""
模板管理测试用例
"""
import time
import allure

from pages.home_page import HomePage
from pages.templates_page import TemplatesPage
from pages.generator_page import GeneratorPage
from utils.logger import get_logger

logger = get_logger(__name__)

BASE_URL = "http://localhost:5174"
TEST_TEMPLATE_NAME = "测试模板_自动化测试"
TEST_TEMPLATE_DESC = "这是一个用于自动化测试的模板"


@allure.feature("模板管理")
class TestTemplates:
    """模板管理测试"""

    @allure.story("新建单字段模板")
    @allure.title("TPL-01: 新建单字段模板")
    @allure.description("测试新建一个包含单个字段的模板")
    def test_create_single_field_template(self, driver):
        """新建单字段模板"""
        with allure.step("打开模板管理页面"):
            home_page = HomePage(driver)
            home_page.open(BASE_URL)
            home_page.navigate_to_templates()
            templates_page = TemplatesPage(driver)
            assert templates_page.is_on_templates_page(), "应该跳转到模板管理页面"

        with allure.step("点击新建模板按钮"):
            templates_page.click_new_template()

        with allure.step("填写模板名称和描述"):
            templates_page.fill_template_name(TEST_TEMPLATE_NAME)
            templates_page.fill_template_description(TEST_TEMPLATE_DESC)

        with allure.step("添加字段"):
            templates_page.click_add_field()
            templates_page.select_field_type("姓名")

        with allure.step("保存模板"):
            templates_page.click_save()

        with allure.step("验证保存成功"):
            assert templates_page.wait_for_success_message(timeout=10), "应该显示成功提示"
            time.sleep(1)  # 等待列表刷新
            assert templates_page.find_template_by_name(TEST_TEMPLATE_NAME), "应该在列表中找到新创建的模板"

    @allure.story("新建多字段模板")
    @allure.title("TPL-02: 新建多字段模板")
    @allure.description("测试新建一个包含多个字段的模板")
    def test_create_multi_field_template(self, driver):
        """新建多字段模板"""
        template_name = "多字段测试模板"
        
        with allure.step("打开模板管理页面"):
            home_page = HomePage(driver)
            home_page.open(BASE_URL)
            home_page.navigate_to_templates()
            templates_page = TemplatesPage(driver)

        with allure.step("点击新建模板按钮"):
            templates_page.click_new_template()

        with allure.step("填写模板名称"):
            templates_page.fill_template_name(template_name)

        with allure.step("添加多个字段"):
            templates_page.click_add_field()
            templates_page.select_field_type("姓名")
            
            templates_page.click_add_field()
            templates_page.select_field_type("邮箱", index=1)
            
            templates_page.click_add_field()
            templates_page.select_field_type("手机号", index=2)

        with allure.step("保存模板"):
            templates_page.click_save()

        with allure.step("验证保存成功"):
            assert templates_page.wait_for_success_message(timeout=10), "应该显示成功提示"
            time.sleep(1)
            assert templates_page.find_template_by_name(template_name), "应该在列表中找到新创建的模板"

    @allure.story("编辑已有模板")
    @allure.title("TPL-03: 编辑已有模板")
    @allure.description("测试编辑一个已存在的模板")
    def test_edit_template(self, driver):
        """编辑已有模板"""
        # 先创建一个测试模板
        template_name = "待编辑模板"
        new_template_name = "已编辑模板"
        
        with allure.step("打开模板管理页面"):
            home_page = HomePage(driver)
            home_page.open(BASE_URL)
            home_page.navigate_to_templates()
            templates_page = TemplatesPage(driver)

        with allure.step("创建测试模板"):
            templates_page.click_new_template()
            templates_page.fill_template_name(template_name)
            templates_page.click_add_field()
            templates_page.select_field_type("姓名")
            templates_page.click_save()
            templates_page.wait_for_success_message(timeout=10)
            time.sleep(1)

        with allure.step("编辑模板"):
            templates_page.click_action_menu(0)
            templates_page.click_action_edit()
            templates_page.fill_template_name(new_template_name)
            templates_page.click_save()

        with allure.step("验证编辑成功"):
            assert templates_page.wait_for_success_message(timeout=10), "应该显示成功提示"
            time.sleep(1)
            assert templates_page.find_template_by_name(new_template_name), "应该找到编辑后的模板"

    @allure.story("复制模板")
    @allure.title("TPL-04: 复制模板")
    @allure.description("测试复制一个已存在的模板")
    def test_copy_template(self, driver):
        """复制模板"""
        template_name = "待复制模板"
        
        with allure.step("打开模板管理页面"):
            home_page = HomePage(driver)
            home_page.open(BASE_URL)
            home_page.navigate_to_templates()
            templates_page = TemplatesPage(driver)

        with allure.step("创建测试模板"):
            templates_page.click_new_template()
            templates_page.fill_template_name(template_name)
            templates_page.click_add_field()
            templates_page.select_field_type("姓名")
            templates_page.click_save()
            templates_page.wait_for_success_message(timeout=10)
            time.sleep(1)

        with allure.step("复制模板"):
            templates_page.click_action_menu(0)
            templates_page.click_action_copy()

        with allure.step("验证复制成功"):
            assert templates_page.wait_for_success_message(timeout=10), "应该显示成功提示"
            time.sleep(1)

    @allure.story("使用模板生成数据")
    @allure.title("TPL-05: 使用模板生成数据")
    @allure.description("测试使用已有模板生成数据")
    def test_generate_with_template(self, driver):
        """使用模板生成数据"""
        template_name = "用于生成测试的模板"
        
        with allure.step("打开模板管理页面"):
            home_page = HomePage(driver)
            home_page.open(BASE_URL)
            home_page.navigate_to_templates()
            templates_page = TemplatesPage(driver)

        with allure.step("创建测试模板"):
            templates_page.click_new_template()
            templates_page.fill_template_name(template_name)
            templates_page.click_add_field()
            templates_page.select_field_type("姓名")
            templates_page.click_save()
            templates_page.wait_for_success_message(timeout=10)
            time.sleep(1)

        with allure.step("使用模板生成数据"):
            templates_page.click_action_menu(0)
            templates_page.click_action_generate()

        with allure.step("验证跳转到生成器页面"):
            generator_page = GeneratorPage(driver)
            assert generator_page.is_on_generator_page(), "应该跳转到内置生成器页面"

    @allure.story("删除模板")
    @allure.title("TPL-06: 删除模板")
    @allure.description("测试删除一个已存在的模板")
    def test_delete_template(self, driver):
        """删除模板"""
        template_name = "待删除模板"
        
        with allure.step("打开模板管理页面"):
            home_page = HomePage(driver)
            home_page.open(BASE_URL)
            home_page.navigate_to_templates()
            templates_page = TemplatesPage(driver)

        with allure.step("创建测试模板"):
            templates_page.click_new_template()
            templates_page.fill_template_name(template_name)
            templates_page.click_add_field()
            templates_page.select_field_type("姓名")
            templates_page.click_save()
            templates_page.wait_for_success_message(timeout=10)
            time.sleep(1)

        with allure.step("删除模板"):
            templates_page.click_action_menu(0)
            templates_page.click_action_delete()
            templates_page.confirm_delete()

        with allure.step("验证删除成功"):
            assert templates_page.wait_for_success_message(timeout=10), "应该显示成功提示"
            time.sleep(1)
            assert not templates_page.find_template_by_name(template_name), "应该找不到被删除的模板"

    @allure.story("新建模板不填写名称")
    @allure.title("TPL-08: 新建模板不填写名称")
    @allure.description("测试不填写模板名称应该无法保存")
    def test_create_template_without_name(self, driver):
        """新建模板不填写名称"""
        with allure.step("打开模板管理页面"):
            home_page = HomePage(driver)
            home_page.open(BASE_URL)
            home_page.navigate_to_templates()
            templates_page = TemplatesPage(driver)

        with allure.step("点击新建模板按钮，不填写名称直接保存"):
            templates_page.click_new_template()
            templates_page.click_save()

        with allure.step("验证错误提示"):
            assert templates_page.wait_for_error_message(timeout=10), "应该显示错误提示"

    @allure.story("编辑模板后点击取消")
    @allure.title("TPL-10: 编辑模板后点击取消")
    @allure.description("测试编辑模板后点击取消应该不会保存修改")
    def test_edit_and_cancel(self, driver):
        """编辑模板后点击取消"""
        template_name = "编辑取消测试模板"
        
        with allure.step("打开模板管理页面"):
            home_page = HomePage(driver)
            home_page.open(BASE_URL)
            home_page.navigate_to_templates()
            templates_page = TemplatesPage(driver)

        with allure.step("创建测试模板"):
            templates_page.click_new_template()
            templates_page.fill_template_name(template_name)
            templates_page.click_add_field()
            templates_page.select_field_type("姓名")
            templates_page.click_save()
            templates_page.wait_for_success_message(timeout=10)
            time.sleep(1)

        with allure.step("编辑模板后取消"):
            templates_page.click_action_menu(0)
            templates_page.click_action_edit()
            templates_page.click_cancel()

        with allure.step("验证模板没有改变"):
            assert templates_page.find_template_by_name(template_name), "应该找到原始模板"
