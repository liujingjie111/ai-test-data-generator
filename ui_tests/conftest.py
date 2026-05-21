"""
pytest 配置文件
包含测试前后置操作和通用 fixture
"""
import pytest
import os
import sys
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import allure

# 添加项目根目录到 Python 路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'ui_tests'))

from utils.logger import get_logger
from utils.screenshot import capture_screenshot
from config import IMPLICIT_WAIT

logger = get_logger(__name__)

# 截图目录
SCREENSHOT_DIR = os.path.join(current_dir, 'screenshots')
SUCCESS_SCREENSHOT_DIR = os.path.join(SCREENSHOT_DIR, 'success')
FAILURE_SCREENSHOT_DIR = os.path.join(SCREENSHOT_DIR, 'failure')

# 创建截图目录
for dir_path in [SUCCESS_SCREENSHOT_DIR, FAILURE_SCREENSHOT_DIR]:
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def cleanup_screenshots():
    """
    清理旧的截图文件
    """
    logger.info("清理旧的截图文件...")
    
    for dir_path in [SUCCESS_SCREENSHOT_DIR, FAILURE_SCREENSHOT_DIR]:
        if os.path.exists(dir_path):
            for filename in os.listdir(dir_path):
                file_path = os.path.join(dir_path, filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                        logger.info(f"已删除: {file_path}")
                except Exception as e:
                    logger.error(f"删除文件失败 {file_path}: {e}")
    
    logger.info("旧截图清理完成！")


@pytest.fixture(scope='session', autouse=True)
def cleanup_before_tests():
    """
    测试会话开始前的清理工作
    """
    # 清理旧截图
    cleanup_screenshots()


@pytest.fixture(scope='session')
def driver():
    """
    WebDriver fixture - 提供浏览器实例

    Returns:
        WebDriver 实例
    """
    logger.info("正在初始化 WebDriver...")
    
    chrome_options = Options()
    
    # 配置选项（不使用无头模式，方便调试）
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    # 设置窗口大小
    chrome_options.add_argument('--window-size=1920,1080')
    
    # 配置下载目录
    download_dir = os.path.join(current_dir, 'downloads')
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    
    prefs = {
        'download.default_directory': download_dir,
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
    }
    chrome_options.add_experimental_option('prefs', prefs)
    
    try:
        logger.info("正在尝试启动 Chrome 浏览器...")
        
        # 使用已存在的 ChromeDriver
        chromedriver_path = r"C:/Users/679/AppData/Local/Programs/Python/Python313/chromedriver.exe"
        logger.info(f"使用 ChromeDriver 路径: {chromedriver_path}")
        
        # 初始化 WebDriver
        driver = webdriver.Chrome(
            service=Service(chromedriver_path),
            options=chrome_options
        )
        
        # 设置隐式等待（全局兜底等待）
        driver.implicitly_wait(IMPLICIT_WAIT)
        
        logger.info("WebDriver 初始化成功！")
        
        yield driver
        
        # 测试结束后关闭浏览器
        logger.info("正在关闭 WebDriver...")
        driver.quit()
        logger.info("WebDriver 已关闭！")
    except Exception as e:
        logger.error(f"WebDriver 初始化失败: {str(e)}")
        raise


@pytest.fixture(scope='function', autouse=True)
def test_screenshot(driver, request):
    """
    测试用例前后置截图

    Args:
        driver: WebDriver 实例
        request: pytest 请求对象
    """
    test_name = request.node.name
    logger.info(f"开始执行测试: {test_name}")
    
    yield
    
    # 测试结束后截图
    if hasattr(request.node, 'rep_call') and not request.node.rep_call.passed:
        # 测试失败
        logger.error(f"测试 {test_name} 失败，正在截图...")
        screenshot_path = capture_screenshot(
            driver,
            test_name,
            'failure',
            attach_to_allure=True
        )
        if screenshot_path:
            logger.info(f"失败截图已保存: {screenshot_path}")
    else:
        # 测试成功
        logger.info(f"测试 {test_name} 成功，正在截图...")
        screenshot_path = capture_screenshot(
            driver,
            test_name,
            'success',
            attach_to_allure=True
        )
        if screenshot_path:
            logger.info(f"成功截图已保存: {screenshot_path}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    捕获测试结果，用于判断是否需要截图

    Args:
        item: 测试项
        call: 调用对象
    """
    outcome = yield
    rep = outcome.get_result()
    
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(scope='function', autouse=True)
def cleanup_test_data():
    """
    测试前后清理测试数据
    """
    from utils.db_utils import cleanup_test_templates
    
    logger.info("清理旧的测试模板...")
    cleanup_test_templates()
    
    yield
    
    # 测试后再次清理
    logger.info("测试结束，清理测试数据...")
    cleanup_test_templates()
