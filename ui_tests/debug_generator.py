"""调试脚本：测试内置生成器页面 Cascader 选择"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from config import BASE_URL

driver = webdriver.Chrome()
driver.implicitly_wait(5)
driver.maximize_window()

try:
    driver.get(BASE_URL + "/generator")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "生成器")]')))
    print("✅ 已打开内置生成器页面")

    # 获取页面HTML结构
    html = driver.execute_script("return document.querySelector('#generator-type')?.outerHTML || 'not found'")
    print(f"\n📄 Cascader HTML:\n{html}")

    # 点击级联选择器
    cascader = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "generator-type")))
    cascader.click()
    print("\n✅ 已点击级联选择器")

    # 等待弹窗出现
    import time
    time.sleep(1)

    # 获取弹窗HTML
    popup_html = driver.execute_script("""
        const menus = document.querySelector('.ant-cascader-menus');
        if (menus) return menus.outerHTML;
        const dropdown = document.querySelector('.ant-select-dropdown');
        if (dropdown) return dropdown.outerHTML;
        const popup = document.querySelector('.ant-cascader-dropdown');
        if (popup) return popup.outerHTML;
        return 'no cascader popup found';
    """)
    print(f"\n📄 Cascader 弹窗 HTML:\n{popup_html[:3000]}")

    # 尝试不同XPath查找菜单项
    print("\n🔍 测试不同XPath:")
    
    xpaths = [
        ("//*[text()='个人数据']", "text() exact"),
        ("//*[contains(text(), '个人数据')]", "contains(text())"),
        ("//*[contains(., '个人数据')]", "contains(.)"),
        ("//li[contains(@class, 'ant-cascader-menu-item') and contains(., '个人数据')]", "li class + contains"),
    ]
    
    for xpath, name in xpaths:
        try:
            el = driver.find_element(By.XPATH, xpath)
            print(f"  ✅ {name}: tag={el.tag_name}, text='{el.text[:30]}', clickable={el.is_enabled() and el.is_displayed()}")
        except Exception as e:
            print(f"  ❌ {name}: {type(e).__name__}")

    print("\n✅ 调试完成")

finally:
    driver.quit()