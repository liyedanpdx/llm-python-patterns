# 🔧 Python Context Manager Workshop

## 📚 简介

本 workshop 通过 5 个渐进式模块，教你掌握 Python Context Manager 的核心概念和实用技巧，特别适用于 LLM 应用开发。

## 🎯 学习路径

### 01. 基础概念 (`01_basic_concepts.py`)
- Context Manager 的工作原理
- `@contextmanager` 装饰器使用
- setup -> use -> cleanup 模式
- 基础计时器和临时配置示例

**运行：** `python 01_basic_concepts.py`

### 02. LLM 会话管理 (`02_llm_session_manager.py`)
- LLM 会话生命周期管理
- Token 计算和成本追踪
- 异常处理和状态恢复
- 生产级应用示例

**运行：** `python 02_llm_session_manager.py`

### 03. 异步管理器 (`03_async_manager.py`)
- `@asynccontextmanager` 使用
- GPU 资源池管理
- 异步 LLM 会话处理
- 并发任务协调

**运行：** `python 03_async_manager.py`

### 04. 智能感知 (`04_smart_session.py`)
- `contextvars` 全局状态管理
- 自动会话感知机制
- 无需手动传递参数
- 灵感来源：llamabot 项目

**运行：** `python 04_smart_session.py`

### 05. 嵌套组合 (`05_nested_managers.py`)
- 多层 Context Manager 嵌套
- 预算控制 + 性能监控 + 会话管理
- 企业级系统资源管理
- 复杂场景的最佳实践

**运行：** `python 05_nested_managers.py`

### 06. MCP 协议实现 (`06_mcp_implementation.md`)
- Model Context Protocol 详细解析
- 企业级 AI 上下文管理标准
- 多传输层支持（stdio/SSE/WebSocket）
- AsyncExitStack 高级资源管理模式
- 与 llamabot、OpenAI SDK 的对比分析

**阅读：** 查看 `06_mcp_implementation.md` 文档

### 07. AsyncExitStack vs @asynccontextmanager (`07_asyncexitstack_vs_asynccontextmanager.py`)
- 两种异步上下文管理方式的详细对比
- 单个资源 vs 多个资源管理
- 动态资源管理和错误处理
- 组合使用的最佳实践

**运行：** `python 07_asyncexitstack_vs_asynccontextmanager.py`

### 08. 本地 MCP 集成实战 (`08_local_mcp_integration.py`)
- 本地集成多个 MCP 服务的实际场景
- 开发环境和生产环境的服务编排
- Context Manager 在 MCP 集成中的必要性
- 错误示例 vs 正确示例对比

**运行：** `python 08_local_mcp_integration.py`

### 09. 设计模式分析 (`09_design_patterns_analysis.md`)
- Context Manager 中体现的设计模式深度解析
- Template Method、Builder、Composite 等模式协同
- 企业级架构中的模式应用价值
- 多模式协同的设计思想和实践指导

**阅读：** 查看 `09_design_patterns_analysis.md` 文档

## 🚀 快速开始

```bash
# 克隆项目
cd workshops/context_workshop

# 按顺序运行所有模块
python 01_basic_concepts.py
python 02_llm_session_manager.py
python 03_async_manager.py
python 04_smart_session.py
python 05_nested_managers.py
```

## 💡 实际应用场景

- **文件操作**：`with open() as f`
- **数据库连接**：会话管理和事务控制
- **LLM API 调用**：成本追踪和会话管理
- **GPU 资源**：异步资源池管理
- **临时配置**：测试环境配置切换
- **性能监控**：自动计时和资源统计

## 🔗 相关项目

- **llamabot**：使用 PromptRecorder Context Manager 自动记录 LLM 对话
- **OpenAI Agents SDK**：RunContextWrapper 管理 LLM 运行时上下文
- **Model Context Protocol (MCP)**：Anthropic 开放标准，企业级 AI 上下文管理协议
- **FastMCP**：简化 MCP 服务器开发的 Python 框架

## ✅ 关键要点

1. **Context Manager** 确保资源的正确获取和释放
2. **yield 语句** 分隔 setup 和 cleanup 阶段
3. **finally 块** 保证清理代码始终执行
4. **异步支持** 适用于高并发和资源密集型场景
5. **contextvars** 实现全局状态感知和自动上下文传递
6. **嵌套组合** 提供强大的多层资源管理能力
7. **MCP 协议** 标准化的企业级 AI 上下文管理解决方案
8. **设计模式协同** Context Manager 是多个设计模式优雅组合的典型范例

这些模式在生产环境中被 llamabot、OpenAI SDK、Model Context Protocol 等知名项目广泛使用！

## 🎯 设计模式精髓

Context Manager 体现了多个经典设计模式的协同应用：

- **Template Method** - 定义固定的资源管理算法骨架（Setup → Use → Cleanup）
- **Builder Pattern** - AsyncExitStack 逐步构建复杂资源结构
- **Composite Pattern** - 嵌套结构形成层次化的资源管理树
- **Facade Pattern** - 为复杂子系统提供简化的统一接口
- **Strategy Pattern** - 不同场景下的不同资源管理策略
- **Observer Pattern** - 监控和观察资源使用状态
- **Factory Pattern** - 动态创建适合的资源管理器

这种**多模式协同**的设计思想是现代企业级软件架构的核心理念！