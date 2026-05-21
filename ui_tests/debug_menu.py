"""调试脚本：测试删除确认弹窗"""
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
    driver.get(BASE_URL + "/templates")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "模板管理")]')))
    print("✅ 已打开模板管理页面")

    # 创建模板
    rows = driver.find_elements(By.XPATH, "//div[contains(@class, 'ant-table-wrapper')]//tbody//tr")
    if not rows:
        new_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(., "新建模板")]')))
        new_btn.click()
        name_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="请输入模板名称"]')))
        name_input.send_keys("删除调试模板")
        add_field = driver.find_element(By.XPATH, '//button[contains(., "添加字段")]')
        add_field.click()
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".ant-modal-wrap:not([style*='display: none']) .ant-card-small")))
        save_btn = driver.find_element(By.XPATH, '//button[contains(@class, "ant-btn-primary")]//span[text()="保存"]/..')
        save_btn.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "ant-message-success")]')))
        print("✅ 模板已创建")

    # 点击操作菜单
    rows = driver.find_elements(By.XPATH, "//div[contains(@class, 'ant-table-wrapper')]//tbody//tr")
    cells = rows[0].find_elements(By.TAG_NAME, "td")
    action_cell = cells[-1]
    ActionChains(driver).move_to_element(action_cell).perform()
    buttons = action_cell.find_elements(By.TAG_NAME, "button")
    buttons[-1].click()
    print("✅ 已点击操作菜单")

    # 等待下拉菜单
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".ant-dropdown:not(.ant-dropdown-hidden)"))
    )
    print("✅ 下拉菜单已出现")

    # 点击删除
    del_item = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//*[contains(@class, 'ant-dropdown-menu-item') and contains(., '删除')]"))
    )
    del_item.click()
    print("✅ 已点击删除菜单项")

    # 检查确认弹窗
    import time
    time.sleep(0.5)
    
    confirm_info = driver.execute_script("""
        // 查找 Modal.confirm 生成的结构
        const confirmModals = document.querySelectorAll('.ant-modal-confirm');
        let result = '';
        confirmModals.forEach((m, i) => {
            const style = m.closest('.ant-modal-wrap')?.getAttribute('style') || '';
            const title = m.querySelector('.ant-modal-confirm-title');
            const content = m.querySelector('.ant-modal-confirm-content');
            const btns = m.querySelectorAll('.ant-modal-confirm-btns button');
            let btnInfo = '';
            btns.forEach((b, j) => {
                btnInfo += `  Button ${j}: class="${b.className}", text="${b.textContent.trim()}"\\n`;
            });
            result += `Confirm ${i}: style=${style}, title=${title?.textContent}, content=${content?.textContent}\\n${btnInfo}\\n`;
        });
        
        // 也检查 modal-root
        const roots = document.querySelectorAll('.ant-modal-root');
        roots.forEach((r, i) => {
            const wrap = r.querySelector('.ant-modal-wrap');
            const style = wrap?.getAttribute('style') || '';
            const isConfirm = r.querySelector('.ant-modal-confirm');
            result += `Root ${i}: style=${style}, isConfirm=${!!isConfirm}\\n`;
        });
        
        return result || 'no confirm dialogs or roots found';
    """)
    print(f"\n📄 确认弹窗信息:\n{confirm_info}")

    # 尝试查找确定按钮
    try:
        ok_btn = driver.find_element(By.XPATH, "//button[contains(@class, 'ant-btn-primary') and contains(., '确定')]")
        print(f"✅ 找到确定按钮: {ok_btn.text}")
        ok_btn.click()
        print("✅ 已点击确定")
    except Exception as e:
        print(f"❌ 找不到确定按钮: {e}")
        # 尝试更简单的XPath
        try:
            ok_btn = driver.find_element(By.XPATH, "//button[contains(@class, 'ant-btn-primary')]")
            print(f"✅ 找到普通primary按钮: {ok_btn.text}")
        except Exception as e2:
            print(f"❌ 也找不到: {e2}")

    print("\n✅ 调试完成")

finally:
    driver.quit()