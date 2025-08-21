"""
🏠 08. Local MCP Service Integration Practice

Real scenarios for local integration of multiple MCP services, showing why Context Manager is necessary:

Practical problems:
- Need to connect multiple MCP services simultaneously (file system, Git, database, etc.)
- Each connection requires correct lifecycle management
- Ensure all connections are properly closed when an exception occurs
- Resource dependencies and cleanup order

Context Manager solution:
- AsyncExitStack manages multiple MCP connections
- Automatically establish and cleanup process connections
- Exception-safe resource manager
"""

import asyncio
from contextlib import AsyncExitStack, asynccontextmanager
from typing import Dict, Any

# Simulate MCP client session (in real use, import from mcp library)
class MockMCPSession:
    def __init__(self, server_name: str):
        self.server_name = server_name
        self.connected = False
    
    async def connect(self):
        print(f"🔌 Connecting to MCP Service: {self.server_name}")
        await asyncio.sleep(0.1)  # Simulate connection time
        self.connected = True
    
    async def disconnect(self):
        print(f"🔌 Disconnecting MCP Service: {self.server_name}")
        await asyncio.sleep(0.05)  # Simulate disconnection time
        self.connected = False
    
    async def call_tool(self, tool_name: str, params: Dict) -> Dict:
        if not self.connected:
            raise ConnectionError(f"Service {self.server_name} not connected")
        
        result = f"{self.server_name}_{tool_name}_result"
        print(f"   🔧 [{self.server_name}] {tool_name}({params}) -> {result}")
        await asyncio.sleep(0.05)  # Simulate tool execution time
        return {"result": result, "server": self.server_name}

# =============================================================================
# 1. Context Manager for a single MCP Service
# =============================================================================

@asynccontextmanager
async def mcp_server_connection(server_name: str, command: str):
    """Single MCP Service connection manager"""
    session = MockMCPSession(server_name)
    try:
        await session.connect()
        yield session
    finally:
        if session.connected:
            await session.disconnect()

# =============================================================================
# 2. Error Example - problems without using Context Manager
# =============================================================================

async def bad_example_without_context_manager():
    """❌ Bad example: manually managing connections"""
    print("❌ Error Example: manually managing connections")
    print("-" * 40)
    
    # Manually create connections
    fs_session = MockMCPSession("filesystem")
    git_session = MockMCPSession("git")
    db_session = MockMCPSession("database")
    
    try:
        await fs_session.connect()
        await git_session.connect() 
        await db_session.connect()
        
        # Use services
        await fs_session.call_tool("list_files", {"path": "."})
        
        # Simulate error
        raise ValueError("Simulated business logic error")
        
    except Exception as e:
        print(f"💥 Error occurred: {e}")
        print("⚠️ Connections may not have been cleaned up properly!")
    
    # Manual cleanup (easy to forget or make mistakes)
    if fs_session.connected:
        await fs_session.disconnect()
    if git_session.connected:
        await git_session.disconnect()
    if db_session.connected:
        await db_session.disconnect()
    
    print()

# =============================================================================
# 3. Correct Example - Using AsyncExitStack to manage multiple MCP services
# =============================================================================

async def good_example_with_async_exit_stack():
    """✅ Correct example: Using AsyncExitStack to manage multiple MCP services"""
    print("✅ Correct Example: AsyncExitStack manages multiple MCP services")
    print("-" * 50)
    
    async with AsyncExitStack() as stack:
        # Establish multiple MCP connections in order
        fs_session = await stack.enter_async_context(
            mcp_server_connection("filesystem", "npx @mcp/server-filesystem")
        )
        
        git_session = await stack.enter_async_context(
            mcp_server_connection("git", "npx @mcp/server-git")
        )
        
        db_session = await stack.enter_async_context(
            mcp_server_connection("database", "npx @mcp/server-postgres")
        )
        
        print("🚀 All MCP services connected, starting work...")
        
        # Use multiple services collaboratively
        files = await fs_session.call_tool("list_files", {"path": "./src"})
        commits = await git_session.call_tool("git_log", {"limit": 5})
        data = await db_session.call_tool("query", {"sql": "SELECT * FROM users"})
        
        try:
            # Simulate error
            raise ValueError("Simulated business logic error")
        except ValueError as e:
            print(f"💥 Error occurred: {e}")
            print("✅ AsyncExitStack will automatically clean up all connections")
    
    print("🧹 All MCP connections have been safely closed\n")

# =============================================================================
# 4. Real application scenario - local development environment integration
# =============================================================================

@asynccontextmanager
async def local_dev_environment():
    """Local development environment MCP service integration"""
    print("🏠 Setting up local development environment...")
    
    async with AsyncExitStack() as stack:
        # All MCP services required for development environment
        services = {}
        
        # File system service - code file management
        services["filesystem"] = await stack.enter_async_context(
            mcp_server_connection("filesystem", "npx @mcp/server-filesystem /project")
        )
        
        # Git service - version control
        services["git"] = await stack.enter_async_context(
            mcp_server_connection("git", "npx @mcp/server-git --repo /project")
        )
        
        # Database service - local test data
        services["database"] = await stack.enter_async_context(
            mcp_server_connection("database", "npx @mcp/server-postgres postgresql://localhost:5432/devdb")
        )
        
        # Fetch service - test data acquisition
        services["fetch"] = await stack.enter_async_context(
            mcp_server_connection("fetch", "npx @mcp/server-fetch")
        )
        
        # Development environment context
        dev_context = {
            "services": services,
            "project_path": "/project",
            "environment": "development",
            "started_at": asyncio.get_event_loop().time()
        }
        
        print("✅ Local development environment ready")
        yield dev_context
        
        uptime = asyncio.get_event_loop().time() - dev_context["started_at"]
        print(f"🏠 Development environment ran for {uptime:.2f} seconds")

async def development_workflow():
    """Development workflow example"""
    print("🔧 Development workflow demo")
    print("-" * 30)
    
    async with local_dev_environment() as env:
        services = env["services"]
        
        # 1. Check project status
        print("📋 Step 1: Check project status")
        files = await services["filesystem"].call_tool("list_files", {"path": "./src"})
        status = await services["git"].call_tool("git_status", {})
        
        # 2. Fetch external data
        print("📋 Step 2: Fetch test data")
        api_data = await services["fetch"].call_tool("fetch", {"url": "https://api.example.com/test"})
        
        # 3. Update database
        print("📋 Step 3: Update test database")
        await services["database"].call_tool("execute", {
            "sql": "INSERT INTO test_data (data) VALUES ($1)",
            "params": [api_data]
        })
        
        # 4. Commit changes
        print("📋 Step 4: Commit code changes")
        await services["git"].call_tool("git_add", {"files": ["test_data.sql"]})
        await services["git"].call_tool("git_commit", {"message": "Add test data"})
        
        print("✅ Development workflow completed")
    
    print()

# =============================================================================
# 5. Production environment integration scenario
# =============================================================================

async def production_mcp_integration():
    """Production environment MCP service integration"""
    print("🏭 Production environment MCP integration demo")
    print("-" * 40)
    
    async with AsyncExitStack() as stack:
        # Production environment MCP service config
        production_services = {}
        
        # Monitoring and logging
        production_services["monitoring"] = await stack.enter_async_context(
            mcp_server_connection("monitoring", "mcp-server-prometheus")
        )
        
        # Database cluster
        production_services["primary_db"] = await stack.enter_async_context(
            mcp_server_connection("primary_db", "mcp-server-postgres-primary")
        )
        
        production_services["read_replica"] = await stack.enter_async_context(
            mcp_server_connection("read_replica", "mcp-server-postgres-replica")
        )
        
        # Cache service
        production_services["redis"] = await stack.enter_async_context(
            mcp_server_connection("redis", "mcp-server-redis")
        )
        
        # Message queue
        production_services["rabbitmq"] = await stack.enter_async_context(
            mcp_server_connection("rabbitmq", "mcp-server-rabbitmq")
        )
        
        print("🚀 All production environment services connected")
        
        # Simulate production workload
        tasks = []
        for i in range(3):
            task = asyncio.create_task(
                simulate_production_workload(production_services, f"batch-{i}")
            )
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        print(f"📊 Processed {len(results)} batch tasks")
    
    print("🏭 Production environment safely closed\n")

async def simulate_production_workload(services: Dict, batch_id: str):
    """Simulate production workload"""
    # Read data
    data = await services["read_replica"].call_tool("query", {
        "sql": f"SELECT * FROM orders WHERE batch_id = '{batch_id}'"
    })
    
    # Process and cache
    await services["redis"].call_tool("set", {
        "key": f"processed_{batch_id}",
        "value": data
    })
    
    # Send message
    await services["rabbitmq"].call_tool("publish", {
        "queue": "processed_orders",
        "message": {"batch_id": batch_id, "status": "completed"}
    })
    
    return f"batch_{batch_id}_completed"

# =============================================================================
# Main program
# =============================================================================

async def main():
    print("🏠 Local MCP Service Integration Practice Demo")
    print("=" * 60)
    print("💡 Demonstrating why local integration of multiple MCP services requires Context Manager\n")
    
    # Demo bad approach
    await bad_example_without_context_manager()
    
    # Demo correct approach
    await good_example_with_async_exit_stack()
    
    # Real application scenarios
    await development_workflow()
    await production_mcp_integration()
    
    print("📚 Key Points:")
    print("✅ When integrating multiple MCP services locally, Context Manager is essential")
    print("✅ AsyncExitStack automatically manages lifecycles of multiple connections")
    print("✅ Ensures exception safety and proper resource cleanup")
    print("✅ Supports complex service dependencies and composition")
    print("✅ Simplifies service orchestration for both development and production environments")

if __name__ == "__main__":
    asyncio.run(main())
