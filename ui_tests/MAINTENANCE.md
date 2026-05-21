# UI 自动化测试维护指南

## 目录结构

```
ui_tests/
├── config.py              # 全局配置文件（URL、超时、测试数据）
├── conftest.py            # pytest 全局 fixture（driver、截图、数据清理）
├── run_tests.py           # 测试运行入口脚本
├── MAINTENANCE.md         # 本维护指南
├── base/
│   ├── __init__.py
│   └── base_page.py       # 基础页面类（通用方法封装）
├── pages/
│   ├── __init__.py
│   ├── home_page.py       # 首页页面对象
│   ├── templates_page.py  # 模板管理页面对象
│   └── generator_page.py  # 内置生成器页面对象
├── tests/
│   ├── __init__.py
│   ├── test_templates.py  # 模板管理测试用例
│   └── test_generator.py  # 内置生成器测试用例
├── utils/
│   ├── __init__.py
│   ├── logger.py          # 日志工具
│   ├── screenshot.py      # 截图工具
│   └── db_utils.py        # 数据库清理工具
├── screenshots/           # 截图输出目录（自动生成）
│   ├── success/
│   └── failure/
└── downloads/             # 文件下载目录（自动生成）
```

## 开发规范

### 1. 技术栈约束

- 只使用 **Selenium 原生 API**，禁止直接写 JS 操作元素
  - 例外：Ant Design 特殊组件（Select下拉框、Input等），需在代码注释中说明原因
- 禁止使用 `time.sleep()`，必须使用 `WebDriverWait` + `expected_conditions`
- 测试框架：pytest + Allure
- 断言必须有真实校验逻辑，禁止 `assert True` 或 `pass`

### 2. 元素定位优先级

1. `data-testid` 属性（优先让开发添加）
2. `id` 属性（唯一、稳定）
3. `name` 属性
4. `css_selector`（简短、稳定，不用复杂层级）
5. `XPath`（最后备选，禁止绝对路径、禁止索引如 `div[3]`）

定位器必须保证唯一性，不允许模糊匹配导致多选。

### 3. 等待规范

| 等待类型 | 配置项 | 默认值 | 适用场景 |
|---------|--------|--------|---------|
| 隐式等待 | `IMPLICIT_WAIT` | 5s | 全局兜底，在 conftest.py 中设置 |
| 显式等待 | `EXPLICIT_WAIT` | 10s | 大多数元素可见/可点击等待 |
| 短等待 | `EXPLICIT_WAIT_SHORT` | 5s | 快速操作确认 |
| 长等待 | `EXPLICIT_WAIT_LONG` | 30s | 数据生成、文件下载等耗时操作 |

示例：
```python
# 正确：显式等待
WebDriverWait(self.driver, EXPLICIT_WAIT).until(
    EC.element_to_be_clickable((By.ID, "btn-login"))
)

# 错误：强制等待
time.sleep(3)  # 禁止
```

### 4. 用例设计规范

- 每个用例独立：独立驱动、独立数据、独立清理
- 结构：前置操作 → 核心步骤 → 结果断言 → 后置清理
- 必须包含正常场景 + 异常场景
- 命名规范：`test_模块_功能_场景`

### 5. Page Object 模式

每个页面对象必须继承 `BasePage`，封装元素的定位和操作，不暴露元素细节给测试用例。

```python
class TemplatesPage(BasePage):
    # 在类顶部定义定位器
    NEW_TEMPLATE_BUTTON = (By.XPATH, "//button[...]")
    
    def click_new_template(self) -> None:
        """点击新建模板按钮"""
        self.click(self.NEW_TEMPLATE_BUTTON)
```

### 6. 断言规范

所有断言必须明确，包含错误提示信息：

```python
# 正确
assert templates_page.wait_for_success_message(), "模板保存应该显示成功提示"
assert templates_page.find_template_by_name(name), "列表中应找到创建的模板"

# 错误
assert True  # 禁止
pass  # 禁止
```

## 配置文件说明

所有可变参数集中在 `config.py` 中管理：

```python
# 服务器配置
BASE_URL = "http://localhost:5174"

# 超时配置
IMPLICIT_WAIT = 5       # 隐式等待
EXPLICIT_WAIT = 10      # 显式等待
EXPLICIT_WAIT_SHORT = 5 # 短等待
EXPLICIT_WAIT_LONG = 30 # 长等待

# 测试数据
TEMPLATE_NAMES = {
    "single": "测试模板_自动化测试",
    # ...
}
```

新增可变参数时，统一添加到 `config.py`，不要在测试代码中硬编码。

## 新增测试用例流程

1. **确定页面对象**：如果需要的新页面不在 `pages/` 中，创建新的 Page 类
2. **编写 Page 类**：封装元素定位器和操作方法
3. **编写测试用例**：在 `tests/` 中创建或扩展现有测试类
4. **添加清理逻辑**：在 `db_utils.py` 中添加数据清理规则
5. **运行验证**：使用 `run_tests.py` 执行测试
6. **提交代码**：遵循命名规范和注释标准

## 脚本更新流程

1. 修改前在 `config.py` 中确认/更新测试数据
2. 修改 Page 类中的定位器或操作方法
3. 更新对应的测试用例
4. 运行测试验证功能正常
5. 清理不再使用的代码（如旧的定位器、废弃的方法）

## 常见问题排查

| 问题 | 排查方向 |
|------|---------|
| 元素找不到 | 1. 检查等待时间是否足够<br>2. 检查是否存在 iframe<br>3. 检查元素是否动态渲染<br>4. 检查定位器是否唯一 |
| 测试不稳定（偶发失败） | 1. 检查是否使用了 `time.sleep`<br>2. 检查等待条件是否合适<br>3. 检查是否有异步加载未等待 |
| 下拉框选择错位 | 检查是否在操作前关闭了其他下拉框 |
| 数据库清理不干净 | 检查 `db_utils.py` 中的过滤条件是否覆盖所有测试模板 |

## 运行测试

```bash
# 确保后端和前端服务已启动

# 运行所有测试
cd ui_tests
python run_tests.py

# 运行指定测试文件
pytest tests/test_templates.py -v

# 运行指定测试用例
pytest tests/test_templates.py::TestTemplates::test_edit_template -v

# 生成 Allure 报告
pytest --alluredir=./allure-results
allure serve ./allure-results
```