# UI 自动化测试

这是智能测试数据生成平台的 UI 自动化测试项目，使用 pytest + Selenium + Allure 框架，采用 Page Object 设计模式。

## 目录结构

```
ui_tests/
├── __init__.py
├── conftest.py              # pytest 配置文件
├── pytest.ini               # pytest 配置
├── requirements.txt         # 依赖包
├── README.md                # 本文件
├── QUICKSTART.md            # 快速启动指南
├── run_tests.py             # 运行测试用例脚本
├── generate_offline_report.py # 生成离线报告脚本
├── generate_online_report.py  # 生成在线报告脚本
├── test_data_generator.db   # 测试数据库
├── .pytest_cache/           # pytest 缓存目录
├── __pycache__/             # Python 缓存目录
├── logs/                    # 日志目录
├── screenshots/             # 截图目录
│   ├── success/             # 成功截图
│   └── failure/             # 失败截图
├── data/                    # 测试数据目录
├── downloads/               # 下载目录
├── allure-results/          # Allure 测试结果目录
├── allure-report/           # Allure 离线报告目录
├── base/                    # 基础页面类
│   ├── __init__.py
│   └── base_page.py         # 所有页面的基类
├── pages/                   # 页面对象
│   ├── __init__.py
│   ├── home_page.py         # 首页
│   ├── generator_page.py    # 内置生成器页
│   └── templates_page.py    # 模板管理页
├── tests/                   # 测试用例
│   ├── __init__.py
│   ├── test_generator.py    # 内置生成器测试
│   └── test_templates.py    # 模板管理测试
└── utils/                   # 工具类
    ├── __init__.py
    ├── logger.py            # 日志工具
    ├── db_utils.py          # 数据库清理工具
    └── screenshot.py        # 截图工具
```

## 环境准备

### 1. 安装 Python 依赖

```bash
cd ui_tests
pip install -r requirements.txt
```

### 2. 安装 Allure

需要提前下载并配置 Allure，你可以按照以下步骤安装：

1. 下载 Allure：https://github.com/allure-framework/allure2/releases
2. 解压到某个目录，例如：`D:\allure-2.39.0`
3. 将 `D:\allure-2.39.0\bin` 添加到系统环境变量 PATH

或者直接使用你的本地已安装的 Allure（如果在 `D:\allure-2.39.0\bin`）。

### 3. 安装 Chrome 浏览器

确保你已经安装了 Chrome 浏览器（Selenium 需要使用）。

### 4. 确保项目服务正在运行

在运行测试前，确保：
- 前端服务正在运行：`http://localhost:5174`
- 后端服务正在运行：`http://localhost:8000`

## 运行测试

### 方式 1: 运行所有测试并生成 Allure 报告

```bash
cd ui_tests
pytest --alluredir=allure-results
```

### 方式 2: 运行特定测试文件

```bash
# 只运行内置生成器测试
pytest tests/test_generator.py --alluredir=allure-results

# 只运行模板管理测试
pytest tests/test_templates.py --alluredir=allure-results
```

### 方式 3: 运行特定测试用例

```bash
pytest tests/test_generator.py::TestGenerator::test_name_generator --alluredir=allure-results
```

## 查看 Allure 报告

在测试运行完成后，可以使用以下命令生成并查看测试报告：

```bash
# 生成报告
allure generate allure-results -o allure-report --clean

# 打开报告（会自动在浏览器中打开）
allure open allure-report
```

或者直接合并生成和查看：

```bash
allure serve allure-results
```

## 测试覆盖

### 内置生成器测试
- ✅ GEN-01: 姓名生成器正常生成数据
- ✅ GEN-02: 邮箱生成器正常生成数据
- ✅ GEN-03: 手机号生成器正常生成数据
- ✅ GEN-04: 带范围参数的年龄生成器
- ✅ GEN-07: 不选择生成器直接生成
- ✅ GEN-08: 生成数量超出上限(100001条)
- ✅ GEN-09: 生成数量为0或负数
- ✅ GEN-11: 范围参数最小值大于最大值

### 模板管理测试
- ✅ TPL-01: 新建单字段模板
- ✅ TPL-02: 新建多字段模板
- ✅ TPL-03: 编辑已有模板
- ✅ TPL-04: 复制模板
- ✅ TPL-05: 使用模板生成数据
- ✅ TPL-06: 删除模板
- ✅ TPL-08: 新建模板不填写名称
- ✅ TPL-10: 编辑模板后点击取消

## 注意事项

1. **数据清理**：每个测试都会在开始和结束时清理测试模板（名称中包含"test"或"测试"的模板）
2. **自动清理**：每次运行测试前会自动清理旧的 Allure 报告和截图
3. **截图**：
   - 无论测试成功或失败都会自动截图
   - 截图保存到 `screenshots/success/` 和 `screenshots/failure/` 目录
   - 截图文件名采用中文命名格式，包含测试名称和北京时间
   - 截图会附加到 Allure 报告中
4. **日志**：日志会输出到控制台和 `logs/` 目录下的文件
5. **浏览器窗口大小**：默认使用 1920x1080 分辨率
6. **Allure 路径**：脚本默认会查找常见的 Allure 安装路径，也可以通过 `--allure-path` 参数指定

## 技术栈

- **测试框架**: pytest 7.4.3
- **UI 自动化**: Selenium 4.15.2
- **报告工具**: Allure 2.39.0
- **设计模式**: Page Object Model (POM)
- **浏览器管理**: webdriver-manager 4.0.1

---

## 最新优化（2026-05）

本次对自动化测试框架进行了系统性优化，主要改进包括：

### 配置集中管理
- 创建 [`config.py`](config.py) 统一管理 BASE_URL、超时时间、测试数据等可变参数
- 消除所有硬编码，支持多环境切换

### 强制等待消除
- 移除全部 `time.sleep()`，统一使用 `WebDriverWait` + `expected_conditions`
- 分级超时配置：隐式等待 5s、显式等待 10s、长等待 30s

### 元素定位增强
- 修复 Ant Design 5 组件定位：`contains(text())` → `contains(.)` 解决文本嵌套问题
- 修复 Cascader 级联选择器定位（隐藏 input → 可见 selector）
- 解决 Select 下拉框选择错位问题（新增 `_close_all_dropdowns()` 方法）

### 断言强化
- 替换所有 `assert True` / `pass` 弱断言
- 添加实际业务逻辑校验：模板名称存在、字段数量正确、成功提示显示等

### 其他改进
- 日志系统：分级日志输出到控制台和文件
- 失败自动截图：Allure 报告自动附带截图
- 数据库清理增强：测试前后自动清理测试数据
- 维护指南：[MAINTENANCE.md](MAINTENANCE.md) 规范后续开发流程
