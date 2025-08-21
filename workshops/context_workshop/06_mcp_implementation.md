# 🌐 06. Model Context Protocol (MCP) Context Manager 实现

## 📚 什么是 Model Context Protocol (MCP)

Model Context Protocol (MCP) 是由 Anthropic 创建的开放标准，旨在为 LLM 应用提供标准化的上下文管理机制。它采用客户端-服务器架构，通过统一的协议让 AI 应用能够安全、标准化地访问外部数据和功能。

### 🏗️ 核心架构

MCP 基于三个核心概念：
- **Prompts**：可重用的提示模板
- **Resources**：为上下文提供的数据和内容
- **Tools**：可执行的功能

## 🔧 MCP 的 Context Manager 实现模式

### 1. 客户端会话管理

MCP 使用 `AsyncExitStack` 来管理复杂的异步资源生命周期：

```python
from contextlib import asynccontextmanager, AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

@asynccontextmanager
async def mcp_client_session(server_params):
    """
    MCP 客户端会话管理器
    
    负责管理与 MCP 服务器的连接建立、会话创建和资源清理。
    使用 AsyncExitStack 确保所有异步资源都能正确清理。
    """
    async with AsyncExitStack() as stack:
        # 建立 stdio 传输连接
        stdio_transport = await stack.enter_async_context(
            stdio_client(server_params)
        )
        
        # 创建客户端会话
        session = await stack.enter_async_context(
            ClientSession(stdio_transport.read, stdio_transport.write)
        )
        
        print(f"🚀 MCP 会话已建立")
        yield session
        print(f"🧹 MCP 会话已清理")
```

这种实现的优势在于：
- **自动资源管理**：无论是否发生异常，都确保连接正确关闭
- **嵌套资源支持**：可以管理多层依赖的异步资源
- **类型安全**：提供完整的类型提示和错误处理

### 2. 服务器生命周期管理

对于需要运行多个 MCP 服务器的场景，FastMCP 提供了优雅的生命周期管理：

```python
@asynccontextmanager
async def mcp_server_lifespan(app):
    """
    MCP 服务器集群生命周期管理
    
    同时启动和管理多个 MCP 服务器实例，确保它们协调工作。
    在应用关闭时，按照正确的顺序清理所有服务器资源。
    """
    async with AsyncExitStack() as stack:
        # 并行启动多个专门化的 MCP 服务器
        await stack.enter_async_context(echo_server.session_manager.run())
        await stack.enter_async_context(math_server.session_manager.run())
        await stack.enter_async_context(database_server.session_manager.run())
        await stack.enter_async_context(file_server.session_manager.run())
        
        print("🚀 所有 MCP 服务器集群已启动")
        print("   - Echo 服务器：处理回显和测试")
        print("   - Math 服务器：执行数学计算")
        print("   - Database 服务器：数据库查询和操作")
        print("   - File 服务器：文件系统访问")
        
        yield
        
        print("🧹 所有 MCP 服务器已优雅关闭")
```

### 3. 资源和数据库管理

企业级应用需要管理数据库连接、缓存系统等复杂资源：

```python
@asynccontextmanager
async def mcp_resource_manager(config):
    """
    MCP 企业级资源管理器
    
    管理应用所需的所有持久化资源，包括数据库连接、
    缓存系统、消息队列等，确保资源的高效利用和正确清理。
    """
    print("🔧 初始化 MCP 资源...")
    
    # 建立数据库连接
    db = await Database.connect(config.database_url)
    print("   ✅ 数据库连接已建立")
    
    # 建立 Redis 缓存连接
    cache = await RedisCache.connect(config.redis_url)
    print("   ✅ Redis 缓存连接已建立")
    
    # 建立消息队列连接
    message_queue = await MessageQueue.connect(config.rabbitmq_url)
    print("   ✅ 消息队列连接已建立")
    
    # 创建应用上下文
    context = {
        "db": db,
        "cache": cache,
        "message_queue": message_queue,
        "active_sessions": {},
        "message_history": [],
        "performance_metrics": {
            "total_requests": 0,
            "successful_requests": 0,
            "error_count": 0
        }
    }
    
    try:
        yield context
    finally:
        # 生成性能报告
        metrics = context["performance_metrics"]
        success_rate = (metrics["successful_requests"] / max(1, metrics["total_requests"])) * 100
        
        print("📊 MCP 会话统计报告:")
        print(f"   💬 处理消息: {len(context['message_history'])} 条")
        print(f"   🔄 总请求数: {metrics['total_requests']}")
        print(f"   ✅ 成功率: {success_rate:.1f}%")
        print(f"   ❌ 错误次数: {metrics['error_count']}")
        
        # 确保所有资源正确清理
        await db.disconnect()
        await cache.disconnect() 
        await message_queue.close()
        print("🧹 所有企业级资源已安全释放")
```

## 🌐 传输层抽象

MCP 支持多种传输方式，每种都有专门的 context manager 实现：

### stdio 传输（本地子进程通信）

```python
@asynccontextmanager
async def stdio_transport(command, args):
    """
    stdio 传输管理器
    
    用于与本地运行的 MCP 服务器子进程通信。
    适合开发环境和本地工具集成。
    """
    print(f"🔧 启动 stdio 服务器: {' '.join([command] + args)}")
    
    process = await asyncio.create_subprocess_exec(
        command, *args,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    try:
        yield (process.stdin, process.stdout)
    finally:
        print("🔧 正在终止 stdio 服务器...")
        process.terminate()
        try:
            await asyncio.wait_for(process.wait(), timeout=5.0)
        except asyncio.TimeoutError:
            print("⚠️ 强制终止 stdio 服务器")
            process.kill()
            await process.wait()
        print("✅ stdio 服务器已安全关闭")
```

### SSE 传输（HTTP 服务器端事件）

```python
@asynccontextmanager
async def sse_transport(url, headers=None):
    """
    SSE (Server-Sent Events) 传输管理器
    
    用于与远程 HTTP MCP 服务器通信。
    支持实时流式数据传输，适合云部署场景。
    """
    print(f"🌐 连接到 SSE 服务器: {url}")
    
    connector = aiohttp.TCPConnector(limit=100, limit_per_host=10)
    session = aiohttp.ClientSession(
        connector=connector,
        headers=headers or {},
        timeout=aiohttp.ClientTimeout(total=30)
    )
    
    try:
        # 建立 SSE 连接
        async with session.get(url) as response:
            if response.status != 200:
                raise ConnectionError(f"SSE 连接失败: {response.status}")
            
            print("✅ SSE 连接已建立")
            yield session
            
    except Exception as e:
        print(f"❌ SSE 连接错误: {e}")
        raise
    finally:
        await session.close()
        await connector.close()
        print("🧹 SSE 连接已关闭")
```

### WebSocket 传输（双向实时通信）

```python
@asynccontextmanager
async def websocket_transport(url, protocols=None):
    """
    WebSocket 传输管理器
    
    提供双向实时通信能力，适合需要高频交互的场景。
    支持自动重连和心跳检测。
    """
    print(f"🔌 连接到 WebSocket 服务器: {url}")
    
    try:
        async with websockets.connect(
            url, 
            subprotocols=protocols or [],
            ping_interval=20,
            ping_timeout=10,
            close_timeout=10
        ) as websocket:
            print("✅ WebSocket 连接已建立")
            print(f"   协议: {websocket.subprotocol}")
            print(f"   扩展: {websocket.extensions}")
            
            yield websocket
            
    except websockets.exceptions.ConnectionClosed:
        print("⚠️ WebSocket 连接已被服务器关闭")
    except Exception as e:
        print(f"❌ WebSocket 连接错误: {e}")
        raise
    finally:
        print("🧹 WebSocket 连接已清理")
```

## 🎯 完整的实际应用示例

以下是一个综合性的示例，展示如何在实际项目中使用 MCP context manager：

```python
async def intelligent_document_processor():
    """
    智能文档处理系统
    
    结合多个 MCP 服务器提供综合的文档分析能力：
    - 文档解析和内容提取
    - AI 驱动的内容分析
    - 数据库存储和检索
    - 实时进度反馈
    """
    
    # 配置多个 MCP 服务器
    servers = {
        "document_parser": StdioServerParameters(
            command="python", 
            args=["servers/document_parser.py"]
        ),
        "ai_analyzer": StdioServerParameters(
            command="python", 
            args=["servers/ai_analyzer.py"]
        ),
        "database_manager": StdioServerParameters(
            command="python",
            args=["servers/database_manager.py"]
        )
    }
    
    results = []
    
    # 同时连接多个 MCP 服务器
    async with AsyncExitStack() as stack:
        sessions = {}
        
        # 建立所有服务器连接
        for name, params in servers.items():
            print(f"🔧 连接到 {name} 服务器...")
            session = await stack.enter_async_context(
                mcp_client_session(params)
            )
            sessions[name] = session
        
        print("🚀 所有 MCP 服务器已连接，开始处理文档...")
        
        # 文档处理流水线
        documents = ["report1.pdf", "analysis2.docx", "data3.xlsx"]
        
        for doc in documents:
            print(f"\n📄 处理文档: {doc}")
            
            # 1. 文档解析
            parse_result = await sessions["document_parser"].call_tool(
                "parse_document", {"file_path": doc}
            )
            print(f"   ✅ 文档解析完成: {parse_result.content['pages']} 页")
            
            # 2. AI 内容分析
            analysis_result = await sessions["ai_analyzer"].call_tool(
                "analyze_content", {
                    "content": parse_result.content['text'],
                    "analysis_type": "comprehensive"
                }
            )
            print(f"   🤖 AI 分析完成: {analysis_result.content['sentiment']} 情感")
            
            # 3. 数据库存储
            storage_result = await sessions["database_manager"].call_tool(
                "store_analysis", {
                    "document": doc,
                    "parse_data": parse_result.content,
                    "analysis_data": analysis_result.content
                }
            )
            print(f"   💾 数据已存储: ID {storage_result.content['record_id']}")
            
            results.append({
                "document": doc,
                "record_id": storage_result.content['record_id'],
                "status": "completed"
            })
    
    print(f"\n🎉 文档处理完成！共处理 {len(results)} 个文档")
    return results
```

## 🔗 与其他 Context Manager 模式的对比

| 特性 | MCP | llamabot | OpenAI SDK | 本地文件操作 |
|------|-----|----------|------------|------------|
| **主要用途** | 标准化的 AI 上下文协议 | LLM 对话记录 | API 调用管理 | 资源文件管理 |
| **传输方式** | stdio/SSE/WebSocket | 内存状态 | HTTP API | 本地文件系统 |
| **资源管理** | 多服务器连接池 | 会话状态 | 单一 API 连接 | 文件句柄 |
| **异步支持** | ✅ 原生异步 | ✅ 支持 | ✅ 支持 | ❌ 主要同步 |
| **标准化程度** | ✅ 开放标准 | ❌ 项目特定 | ❌ 供应商特定 | ✅ Python 标准 |
| **复杂度** | 高（企业级） | 中（应用级） | 低（API级） | 低（系统级） |

## 🎯 MCP Context Manager 的独特优势

### 1. **标准化协议**
MCP 定义了统一的接口规范，让不同的 AI 服务能够无缝协作，避免了供应商锁定问题。

### 2. **多传输层支持**
通过统一的 context manager 接口，支持 stdio、SSE、WebSocket 等多种传输方式，适应不同的部署场景。

### 3. **企业级资源管理**
提供了完善的资源生命周期管理，包括连接池、错误恢复、性能监控等企业级特性。

### 4. **类型安全**
完整的 TypeScript 和 Python 类型定义，确保编译时类型检查和运行时安全。

### 5. **可扩展架构**
通过 Prompts、Resources、Tools 三大核心抽象，提供了灵活的功能扩展机制。

## 🚀 最佳实践建议

1. **使用 AsyncExitStack**：对于复杂的多资源管理场景，优先使用 AsyncExitStack
2. **错误处理**：为每个传输层实现适当的重试和降级机制
3. **监控和日志**：在 context manager 中集成详细的性能监控和日志记录
4. **资源限制**：设置合理的连接池大小和超时时间
5. **优雅关闭**：确保在应用关闭时，所有 MCP 服务器都能优雅地停止服务

MCP 的 context manager 实现代表了现代 AI 应用架构的最佳实践，为构建可扩展、可维护的 AI 系统提供了坚实的基础！