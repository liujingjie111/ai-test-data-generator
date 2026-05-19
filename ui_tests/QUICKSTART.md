# 快速启动指南

## 前置条件

确保以下服务正在运行：

1. **前端服务** (已在 terminal 22 运行): `http://localhost:5174`
2. **后端服务** (已在 terminal 16 运行): `http://localhost:8000`

## 步骤 1: 进入 ui_tests 目录

```bash
cd D:\Users\679\Desktop\ai-test-data-generator\ui_tests
```

## 步骤 2: 运行测试（使用便捷脚本）

### 查看可用模块
```bash
python run_tests.py -l
```

### 运行所有测试
```bash
python run_tests.py
```

### 运行特定模块
```bash
# 只运行内置生成器测试
python run_tests.py -m test_generator

# 只运行模板管理测试
python run_tests.py -m test_templates
```

## 步骤 3: 查看报告（使用便捷脚本）

测试完成后，可以使用以下方式查看报告：

### 在线报告（推荐）
```bash
python generate_online_report.py
```
这会启动本地服务器并自动在浏览器中打开报告，按 Ctrl+C 停止服务器。

### 离线报告
```bash
python generate_offline_report.py
```
这会生成静态 HTML 报告，打开 `allure-report/index.html` 即可查看。

## （可选）使用原始 pytest 命令

如果您想使用原始的 pytest 命令，也是可以的：

```bash
# 运行所有测试
pytest --alluredir=allure-results

# 查看在线报告
allure serve allure-results

# 生成离线报告
allure generate allure-results -o allure-report --clean
```

## 注意事项

- 测试会自动清理包含 "test" 或 "测试" 的模板，请确保不要有重要的测试模板
- 每次测试运行都会自动截图（成功和失败都有），截图文件使用中文和北京时间命名
- 每次运行测试前会自动清理旧的报告和截图
- 测试期间浏览器窗口会自动打开和关闭

## 常见问题

### 问: 找不到数据库表?
答: 确保后端服务已经初始化了数据库（运行过至少一次）

### 问: 测试超时?
答: 可能是页面加载太慢，检查前端和后端是否正常响应

### 问: Allure 相关脚本找不到 Allure?
答: 脚本默认会查找 `D:\allure-2.39.0\bin\allure.bat`，如果您的 Allure 在其他位置，可以使用 `--allure-path` 参数指定：
```bash
python generate_offline_report.py --allure-path "您的路径\allure.bat"
```
