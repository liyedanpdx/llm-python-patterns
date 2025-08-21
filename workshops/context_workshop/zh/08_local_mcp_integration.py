"""
🏠 08. 本地 MCP 服务集成实战

本地集成多个 MCP 服务的实际场景，展示为什么 Context Manager 是必需的：

实际问题：
- 需要同时连接多个 MCP 服务器（文件系统、Git、数据库等）
- 每个连接都需要正确的生命周期管理
- 异常时确保所有连接正确关闭
- 资源依赖和清理顺序

Context Manager 解决方案：
- AsyncExitStack 管理多个 MCP 连接
- 自动处理连接建立和清理
- 异常安全的资源管理
"""

import asyncio
from contextlib import AsyncExitStack, asynccontextmanager
from typing import Dict, Any

# 模拟 MCP 客户端会话（实际使用时从 mcp 库导入）
class MockMCPSession:
    def __init__(self, server_name: str):
        self.server_name = server_name
        self.connected = False
    
    async def connect(self):
        print(f"🔌 连接到 MCP 服务器: {self.server_name}")
        await asyncio.sleep(0.1)  # 模拟连接时间
        self.connected = True
    
    async def disconnect(self):
        print(f"🔌 断开 MCP 服务器: {self.server_name}")
        await asyncio.sleep(0.05)  # 模拟断连时间
        self.connected = False
    
    async def call_tool(self, tool_name: str, params: Dict) -> Dict:
        if not self.connected:
            raise ConnectionError(f"服务器 {self.server_name} 未连接")
        
        result = f"{self.server_name}_{tool_name}_result"
        print(f"   🔧 [{self.server_name}] {tool_name}({params}) -> {result}")
        await asyncio.sleep(0.05)  # 模拟工具执行时间
        return {"result": result, "server": self.server_name}

# =============================================================================
# 1. 单个 MCP 服务器的 Context Manager
# =============================================================================

@asynccontextmanager
async def mcp_server_connection(server_name: str, command: str):
    """单个 MCP 服务器连接管理器"""
    session = MockMCPSession(server_name)
    try:
        await session.connect()
        yield session
    finally:
        if session.connected:
            await session.disconnect()

# =============================================================================
# 2. 错误示例 - 不使用 Context Manager 的问题
# =============================================================================

async def bad_example_without_context_manager():
    """❌ 不好的例子：不使用 Context Manager"""
    print("❌ 错误示例：手动管理连接")
    print("-" * 40)
    
    # 手动创建连接
    fs_session = MockMCPSession("filesystem")
    git_session = MockMCPSession("git")
    db_session = MockMCPSession("database")
    
    try:
        await fs_session.connect()
        await git_session.connect() 
        await db_session.connect()
        
        # 使用服务
        await fs_session.call_tool("list_files", {"path": "."})
        
        # 模拟错误
        raise ValueError("模拟业务逻辑错误")
        
    except Exception as e:
        print(f"💥 发生错误: {e}")
        print("⚠️ 连接可能没有正确清理！")
    
    # 手动清理（很容易忘记或出错）
    if fs_session.connected:
        await fs_session.disconnect()
    if git_session.connected:
        await git_session.disconnect()
    if db_session.connected:
        await db_session.disconnect()
    
    print()

# =============================================================================
# 3. 正确示例 - 使用 AsyncExitStack 管理多个 MCP 服务
# =============================================================================

async def good_example_with_async_exit_stack():
    """✅ 正确示例：使用 AsyncExitStack 管理多个 MCP 服务"""
    print("✅ 正确示例：AsyncExitStack 管理多个 MCP 服务")
    print("-" * 50)
    
    async with AsyncExitStack() as stack:
        # 按顺序建立多个 MCP 连接
        fs_session = await stack.enter_async_context(
            mcp_server_connection("filesystem", "npx @mcp/server-filesystem")
        )
        
        git_session = await stack.enter_async_context(
            mcp_server_connection("git", "npx @mcp/server-git")
        )
        
        db_session = await stack.enter_async_context(
            mcp_server_connection("database", "npx @mcp/server-postgres")
        )
        
        print("🚀 所有 MCP 服务已连接，开始工作...")
        
        # 使用多个服务协同工作
        files = await fs_session.call_tool("list_files", {"path": "./src"})
        commits = await git_session.call_tool("git_log", {"limit": 5})
        data = await db_session.call_tool("query", {"sql": "SELECT * FROM users"})
        
        try:
            # 模拟错误
            raise ValueError("模拟业务逻辑错误")
        except ValueError as e:
            print(f"💥 发生错误: {e}")
            print("✅ AsyncExitStack 会自动清理所有连接")
    
    print("🧹 所有 MCP 连接已安全关闭\n")

# =============================================================================
# 4. 实际应用场景 - 本地开发环境集成
# =============================================================================

@asynccontextmanager
async def local_dev_environment():
    """本地开发环境的 MCP 服务集成"""
    print("🏠 设置本地开发环境...")
    
    async with AsyncExitStack() as stack:
        # 开发环境需要的所有 MCP 服务
        services = {}
        
        # 文件系统服务 - 代码文件管理
        services["filesystem"] = await stack.enter_async_context(
            mcp_server_connection("filesystem", "npx @mcp/server-filesystem /project")
        )
        
        # Git 服务 - 版本控制
        services["git"] = await stack.enter_async_context(
            mcp_server_connection("git", "npx @mcp/server-git --repo /project")
        )
        
        # 数据库服务 - 本地测试数据
        services["database"] = await stack.enter_async_context(
            mcp_server_connection("database", "npx @mcp/server-postgres postgresql://localhost:5432/devdb")
        )
        
        # 网页抓取服务 - 测试数据获取
        services["fetch"] = await stack.enter_async_context(
            mcp_server_connection("fetch", "npx @mcp/server-fetch")
        )
        
        # 开发环境上下文
        dev_context = {
            "services": services,
            "project_path": "/project",
            "environment": "development",
            "started_at": asyncio.get_event_loop().time()
        }
        
        print("✅ 本地开发环境就绪")
        yield dev_context
        
        uptime = asyncio.get_event_loop().time() - dev_context["started_at"]
        print(f"🏠 开发环境运行了 {uptime:.2f} 秒")

async def development_workflow():
    """开发工作流示例"""
    print("🔧 开发工作流演示")
    print("-" * 30)
    
    async with local_dev_environment() as env:
        services = env["services"]
        
        # 1. 检查项目状态
        print("📋 步骤 1: 检查项目状态")
        files = await services["filesystem"].call_tool("list_files", {"path": "./src"})
        status = await services["git"].call_tool("git_status", {})
        
        # 2. 获取外部数据
        print("📋 步骤 2: 获取测试数据")
        api_data = await services["fetch"].call_tool("fetch", {"url": "https://api.example.com/test"})
        
        # 3. 更新数据库
        print("📋 步骤 3: 更新测试数据库")
        await services["database"].call_tool("execute", {
            "sql": "INSERT INTO test_data (data) VALUES ($1)",
            "params": [api_data]
        })
        
        # 4. 提交更改
        print("📋 步骤 4: 提交代码更改")
        await services["git"].call_tool("git_add", {"files": ["test_data.sql"]})
        await services["git"].call_tool("git_commit", {"message": "Add test data"})
        
        print("✅ 开发工作流完成")
    
    print()

# =============================================================================
# 5. 生产环境集成场景
# =============================================================================

async def production_mcp_integration():
    """生产环境的 MCP 服务集成"""
    print("🏭 生产环境 MCP 集成演示")
    print("-" * 40)
    
    async with AsyncExitStack() as stack:
        # 生产环境的 MCP 服务配置
        production_services = {}
        
        # 监控和日志
        production_services["monitoring"] = await stack.enter_async_context(
            mcp_server_connection("monitoring", "mcp-server-prometheus")
        )
        
        # 数据库集群
        production_services["primary_db"] = await stack.enter_async_context(
            mcp_server_connection("primary_db", "mcp-server-postgres-primary")
        )
        
        production_services["read_replica"] = await stack.enter_async_context(
            mcp_server_connection("read_replica", "mcp-server-postgres-replica")
        )
        
        # 缓存服务
        production_services["redis"] = await stack.enter_async_context(
            mcp_server_connection("redis", "mcp-server-redis")
        )
        
        # 消息队列
        production_services["rabbitmq"] = await stack.enter_async_context(
            mcp_server_connection("rabbitmq", "mcp-server-rabbitmq")
        )
        
        print("🚀 生产环境所有服务已连接")
        
        # 模拟生产工作负载
        tasks = []
        for i in range(3):
            task = asyncio.create_task(
                simulate_production_workload(production_services, f"batch-{i}")
            )
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        print(f"📊 处理了 {len(results)} 个批次任务")
    
    print("🏭 生产环境已安全关闭\n")

async def simulate_production_workload(services: Dict, batch_id: str):
    """模拟生产工作负载"""
    # 读取数据
    data = await services["read_replica"].call_tool("query", {
        "sql": f"SELECT * FROM orders WHERE batch_id = '{batch_id}'"
    })
    
    # 处理并缓存
    await services["redis"].call_tool("set", {
        "key": f"processed_{batch_id}",
        "value": data
    })
    
    # 发送消息
    await services["rabbitmq"].call_tool("publish", {
        "queue": "processed_orders",
        "message": {"batch_id": batch_id, "status": "completed"}
    })
    
    return f"batch_{batch_id}_completed"

# =============================================================================
# 主程序
# =============================================================================

async def main():
    print("🏠 本地 MCP 服务集成实战演示")
    print("=" * 60)
    print("💡 展示为什么本地集成多个 MCP 服务需要 Context Manager\n")
    
    # 演示错误做法
    await bad_example_without_context_manager()
    
    # 演示正确做法
    await good_example_with_async_exit_stack()
    
    # 实际应用场景
    await development_workflow()
    await production_mcp_integration()
    
    print("📚 关键要点:")
    print("✅ 本地集成多个 MCP 服务时，Context Manager 是必需的")
    print("✅ AsyncExitStack 自动管理多个连接的生命周期")
    print("✅ 确保异常安全和资源正确清理")
    print("✅ 支持复杂的服务依赖和组合")
    print("✅ 简化开发和生产环境的服务编排")

if __name__ == "__main__":
    asyncio.run(main())