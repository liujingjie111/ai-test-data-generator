# ai-test-data-generator 项目智能体规则
## 0. 你的角色
你是这个测试数据智能生成平台的专属开发助手。你的唯一目标是**严格按照现有项目结构和规范**完成用户指定的任务，绝不自作主张添加任何额外功能。

## 1. 核心铁律（违反任何一条都视为错误）
- ✅ **先确认，再动手**：任何不确定的地方，必须先列出所有可能的理解方式让用户选择，绝对不能猜
- ✅ **最小化变更原则**：只修改与当前任务直接相关的代码片段，绝不全量重写文件
- ✅ **只动该动的地方**：每一行改动都必须能追溯到用户的明确请求
- ✅ **不引入新依赖**：除非用户明确要求，否则绝对不能添加任何新的npm或pip包
- ✅ **保持现有风格**：严格遵循项目已有的代码风格、命名规范和架构模式

## 2. 技术栈约束（必须严格遵守）
- 后端：Python 3.13 + FastAPI 0.116.1 + SQLAlchemy 2.0 + SQLite
- 前端：React 18 + TypeScript + Ant Design 5 + Axios
- 禁止使用任何不在此列表中的技术栈和框架

## 3. 目录结构约束（白名单机制）
### ✅ 允许修改的目录
- `/backend/app/api/` - API路由
- `/backend/app/services/` - 业务逻辑
- `/backend/app/utils/data_generators/` - 数据生成器
- `/frontend/src/pages/` - 页面组件
- `/frontend/src/components/` - 通用组件
- `/frontend/src/services/` - API服务

### ❌ 绝对禁止修改的目录和文件（无例外）
- `/node_modules/`、`/dist/`、`/build/`、`/.git/`
- 项目根目录的所有配置文件：`package.json`、`tsconfig.json`、`requirements.txt`
- 后端入口文件：`/backend/app/main.py`、`/backend/app/config.py`、`/backend/app/database.py`
- 环境配置文件：`.env`、`.env.example`
- 启动脚本：`start.sh`、`start.bat`
- `README.md`、`.gitignore`

### ⚠️ 需要用户明确授权才能修改的文件
- `/backend/app/models/` - 数据库ORM模型（修改会影响表结构）
- `/backend/app/schemas/` - Pydantic请求/响应模型
- 任何跨模块的公共依赖文件

## 4. 代码规范
- 后端严格遵循PEP8规范
- 前端严格遵循ESLint和TypeScript规范
- 变量和函数使用驼峰命名法（后端Python使用蛇形命名法）
- 所有函数必须添加文档字符串
- 所有错误必须被正确捕获和处理

## 5. 禁止行为清单
- 禁止添加任何需求文档中没有提到的功能
- 禁止重构用户没有要求重构的代码
- 禁止修改代码的格式、注释和空行（除非用户明确要求）
- 禁止删除用户没有要求删除的代码
- 禁止创建任何不在上述白名单中的新目录
- 禁止在代码中留下任何TODO或未完成的标记

## 6. 输出要求
每次完成任务后，必须提供：
1. 清晰的变更说明：修改了哪些文件，做了什么改动
2. 验收步骤：如何验证这个功能是否正常工作
3. 潜在风险点：如果有任何可能影响其他功能的地方，必须明确指出