"""
UI 自动化测试全局配置
集中管理所有可变参数，避免硬编码
"""
import os

# ============================================================
# 服务器配置
# ============================================================
BASE_URL = "http://localhost:5174"

# ============================================================
# 超时配置（秒）
# ============================================================
IMPLICIT_WAIT = 5
EXPLICIT_WAIT = 10
EXPLICIT_WAIT_SHORT = 5
EXPLICIT_WAIT_LONG = 30

# ============================================================
# 浏览器配置
# ============================================================
CHROME_DRIVER_PATH = r"C:/Users/679/AppData/Local/Programs/Python/Python313/chromedriver.exe"
BROWSER_WINDOW_WIDTH = 1920
BROWSER_WINDOW_HEIGHT = 1080

# ============================================================
# 测试数据
# ============================================================
TEMPLATE_NAMES = {
    "single": "测试模板_自动化测试",
    "multi": "多字段测试模板",
    "edit": "待编辑模板",
    "copy": "待复制模板",
    "generate": "用于生成测试的模板",
    "delete": "待删除模板",
    "edit_cancel": "编辑取消测试模板",
}
TEMPLATE_DESC = "这是一个用于自动化测试的模板"

# ============================================================
# 目录路径
# ============================================================
UI_TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOT_DIR = os.path.join(UI_TESTS_DIR, "screenshots")
LOG_DIR = os.path.join(UI_TESTS_DIR, "logs")
DOWNLOAD_DIR = os.path.join(UI_TESTS_DIR, "downloads")

# ============================================================
# 数据库
# ============================================================
BACKEND_DIR = os.path.join(os.path.dirname(UI_TESTS_DIR), "backend")