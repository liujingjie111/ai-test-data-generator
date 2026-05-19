"""
截图工具类
用于测试过程中的截图功能，支持成功和失败截图
"""
import os
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Optional

import allure
from selenium.webdriver.remote.webdriver import WebDriver


def capture_screenshot(
    driver: WebDriver,
    test_name: str,
    status: str = "success",
    attach_to_allure: bool = True
) -> Optional[str]:
    """
    捕获当前页面截图

    Args:
        driver: Selenium WebDriver 对象
        test_name: 测试用例名称
        status: 截图状态 ("success" 或 "failure")
        attach_to_allure: 是否附加到 Allure 报告

    Returns:
        截图文件路径，失败返回 None
    """
    try:
        # 创建截图目录
        screenshot_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'screenshots',
            status
        )
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)

        # 中文状态描述映射
        status_map = {
            'success': '成功',
            'failure': '失败'
        }
        status_cn = status_map.get(status, status)

        # 使用北京时间（东八区）
        beijing_tz = ZoneInfo('Asia/Shanghai')
        now = datetime.now(beijing_tz)
        timestamp = now.strftime("%Y年%m月%d日%H时%M分%S秒")

        # 生成截图文件名
        screenshot_name = f"{test_name}_{status_cn}_{timestamp}.png"
        screenshot_path = os.path.join(screenshot_dir, screenshot_name)

        # 保存截图
        driver.save_screenshot(screenshot_path)

        # 附加到 Allure 报告
        if attach_to_allure:
            with open(screenshot_path, 'rb') as f:
                allure.attach(
                    f.read(),
                    name=screenshot_name,
                    attachment_type=allure.attachment_type.PNG
                )

        return screenshot_path

    except Exception as e:
        print(f"截图失败: {str(e)}")
        return None
