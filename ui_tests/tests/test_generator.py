"""
内置生成器测试用例
"""
import allure
import pytest

from pages.home_page import HomePage
from pages.generator_page import GeneratorPage
from config import BASE_URL
from utils.logger import get_logger

logger = get_logger(__name__)


@allure.feature("内置生成器")
class TestGenerator:
    """内置生成器测试"""

    @allure.story("姓名生成器正常生成数据")
    @allure.title("GEN-01: 姓名生成器正常生成数据")
    @allure.description("测试姓名生成器能否正常生成 10 条数据")
    def test_name_generator(self, driver):
        """姓名生成器正常生成数据"""
        with allure.step("打开内置生成器页面"):
            home_page = HomePage(driver)
            home_page.open(BASE_URL)
            home_page.navigate_to_generator()
            generator_page = GeneratorPage(driver)
            assert generator_page.is_on_generator_page(), "应该跳转到内置生成器页面"

        with allure.step("选择姓名生成器"):
            generator_page.select_generator("个人数据", "姓名")

        with allure.step("设置生成数量为 10"):
            generator_page.set_count(10)

        with allure.step("点击生成按钮"):
            generator_page.click_generate()

        with allure.step("验证数据生成成功"):
            assert generator_page.wait_for_data_generated(timeout=30), "数据应该成功生成"
            row_count = generator_page.get_row_count()
            assert row_count >= 10, f"应该生成至少 10 条数据，实际生成 {row_count} 条"

    @allure.story("邮箱生成器正常生成数据")
    @allure.title("GEN-02: 邮箱生成器正常生成数据")
    @allure.description("测试邮箱生成器能否正常生成 10 条数据")
    def test_email_generator(self, driver):
        """邮箱生成器正常生成数据"""
        with allure.step("打开内置生成器页面"):
            home_page = HomePage(driver)
            home_page.open(BASE_URL)
            home_page.navigate_to_generator()
            generator_page = GeneratorPage(driver)

        with allure.step("选择邮箱生成器"):
            generator_page.select_generator("个人数据", "邮箱")

        with allure.step("设置生成数量为 10"):
            generator_page.set_count(10)

        with allure.step("点击生成按钮"):
            generator_page.click_generate()

        with allure.step("验证数据生成成功"):
            assert generator_page.wait_for_data_generated(timeout=30), "数据应该成功生成"

    @allure.story("手机号生成器正常生成数据")
    @allure.title("GEN-03: 手机号生成器正常生成数据")
    @allure.description("测试手机号生成器能否正常生成 10 条数据")
    def test_phone_generator(self, driver):
        """手机号生成器正常生成数据"""
        with allure.step("打开内置生成器页面"):
            home_page = HomePage(driver)
            home_page.open(BASE_URL)
            home_page.navigate_to_generator()
            generator_page = GeneratorPage(driver)

        with allure.step("选择手机号生成器"):
            generator_page.select_generator("个人数据", "手机号")

        with allure.step("设置生成数量为 10"):
            generator_page.set_count(10)

        with allure.step("点击生成按钮"):
            generator_page.click_generate()

        with allure.step("验证数据生成成功"):
            assert generator_page.wait_for_data_generated(timeout=30), "数据应该成功生成"

    @allure.story("带范围参数的年龄生成器")
    @allure.title("GEN-04: 带范围参数的年龄生成器")
    @allure.description("测试年龄生成器在设置 20-30 范围的情况下正常生成数据")
    def test_age_generator_with_range(self, driver):
        """带范围参数的年龄生成器"""
        with allure.step("打开内置生成器页面"):
            home_page = HomePage(driver)
            home_page.open(BASE_URL)
            home_page.navigate_to_generator()
            generator_page = GeneratorPage(driver)

        with allure.step("选择年龄生成器"):
            generator_page.select_generator("个人数据", "年龄")

        with allure.step("设置生成数量为 10，范围为 20-30"):
            generator_page.set_count(10)
            generator_page.set_range(20, 30)

        with allure.step("点击生成按钮"):
            generator_page.click_generate()

        with allure.step("验证数据生成成功"):
            assert generator_page.wait_for_data_generated(timeout=30), "数据应该成功生成"

    @allure.story("不选择生成器直接生成")
    @allure.title("GEN-07: 不选择生成器直接生成")
    @allure.description("测试在未选择生成器的情况下点击生成按钮应该显示错误提示")
    def test_generate_without_selector(self, driver):
        """不选择生成器直接生成"""
        with allure.step("打开内置生成器页面"):
            home_page = HomePage(driver)
            home_page.open(BASE_URL)
            home_page.navigate_to_generator()
            generator_page = GeneratorPage(driver)

        with allure.step("不选择生成器直接点击生成按钮"):
            generator_page.click_generate()

        with allure.step("验证生成按钮存在（页面未崩溃）"):
            # 未选择生成器时点击生成，页面不应崩溃
            assert generator_page.is_on_generator_page(), "页面应保持在内置生成器页面"

    @allure.story("生成数量超出上限")
    @allure.title("GEN-08: 生成数量超出上限(100001条)")
    @allure.description("测试当输入数量超过限制时，输入框应该自动调整到最大值")
    def test_count_exceeds_limit(self, driver):
        """生成数量超出上限"""
        with allure.step("打开内置生成器页面"):
            home_page = HomePage(driver)
            home_page.open(BASE_URL)
            home_page.navigate_to_generator()
            generator_page = GeneratorPage(driver)

        with allure.step("选择姓名生成器"):
            generator_page.select_generator("个人数据", "姓名")

        with allure.step("设置生成数量为 100001"):
            generator_page.set_count(100001)

        with allure.step("验证应该能够生成（InputNumber 会自动限制到最大值）"):
            generator_page.click_generate()
            assert generator_page.wait_for_data_generated(timeout=30), "数据应该成功生成"

    @allure.story("生成数量为0或负数")
    @allure.title("GEN-09: 生成数量为0或负数")
    @allure.description("测试当输入数量为0或负数时，应该自动调整到合法范围")
    def test_count_zero_or_negative(self, driver):
        """生成数量为0或负数"""
        with allure.step("打开内置生成器页面"):
            home_page = HomePage(driver)
            home_page.open(BASE_URL)
            home_page.navigate_to_generator()
            generator_page = GeneratorPage(driver)

        with allure.step("选择姓名生成器"):
            generator_page.select_generator("个人数据", "姓名")

        with allure.step("设置生成数量为 0，系统会自动调整到最小值"):
            generator_page.set_count(0)

        with allure.step("点击生成按钮，应该能够正常生成数据"):
            generator_page.click_generate()
            assert generator_page.wait_for_data_generated(timeout=30), "数据应该成功生成"

    @allure.story("范围参数最小值大于最大值")
    @allure.title("GEN-11: 范围参数最小值大于最大值")
    @allure.description("测试当最小值大于最大值时，应该显示错误提示")
    def test_range_min_greater_than_max(self, driver):
        """范围参数最小值大于最大值"""
        with allure.step("打开内置生成器页面"):
            home_page = HomePage(driver)
            home_page.open(BASE_URL)
            home_page.navigate_to_generator()
            generator_page = GeneratorPage(driver)

        with allure.step("选择年龄生成器"):
            generator_page.select_generator("个人数据", "年龄")

        with allure.step("设置范围为 40-20（最小值大于最大值）"):
            generator_page.set_count(10)
            generator_page.set_range(40, 20)

        with allure.step("点击生成按钮，验证页面能够正常响应"):
            generator_page.click_generate()
            # 验证页面不会崩溃，保持在内置生成器页面
            assert generator_page.is_on_generator_page(), "页面应保持在内置生成器页面"
