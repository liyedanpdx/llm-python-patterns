# 🌐 06. Model Context Protocol (MCP) Context Manager Implementation

## 📚 What is Model Context Protocol (MCP)

Model Context Protocol (MCP) is an open standard created by Anthropic to provide standardized context management mechanisms for LLM applications. It adopts a client-server architecture that allows AI applications to securely and standardly access external data and functionality through unified protocols.

### 🏗️ Core Architecture

MCP is based on three core concepts:

* **Prompts**: Reusable prompt templates
* **Resources**: Data and content provided for context
* **Tools**: Executable functionality

## 🔧 MCP Context Manager Implementation Patterns

### 1. Client Session Management

MCP uses `AsyncExitStack` to manage complex async resource lifecycles:

```python
from contextlib import asynccontextmanager, AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

@asynccontextmanager
async def mcp_client_session(server_params):
    """
    MCP Client Session Manager
    
    Responsible for establishing the connection to the MCP server, 
    creating the session, and cleaning up resources.
    Uses AsyncExitStack to ensure proper cleanup of all async resources.
    """
    async with AsyncExitStack() as stack:
        # Establish stdio transport connection
        stdio_transport = await stack.enter_async_context(
            stdio_client(server_params)
        )
        
        # Create client session
        session = await stack.enter_async_context(
            ClientSession(stdio_transport.read, stdio_transport.write)
        )
        
        print(f"🚀 MCP session established")
        yield session
        print(f"🧹 MCP session cleaned up")
```

Advantages of this implementation:

* **Automatic resource management**: Ensures connections are closed properly even when exceptions occur
* **Nested resource support**: Can manage multilayer asynchronous resources
* **Type safety**: Provides complete type hints and error handling

### 2. Server Lifecycle Management

For scenarios requiring multiple MCP servers, FastMCP provides graceful lifecycle management:

```python
@asynccontextmanager
async def mcp_server_lifespan(app):
    """
    MCP Server Cluster Lifecycle Manager
    
    Starts and manages multiple MCP server instances simultaneously, ensuring coordinated operation.
    Cleans up all server resources in the correct order when the application closes.
    """
    async with AsyncExitStack() as stack:
        # Start multiple specialized MCP servers in parallel
        await stack.enter_async_context(echo_server.session_manager.run())
        await stack.enter_async_context(math_server.session_manager.run())
        await stack.enter_async_context(database_server.session_manager.run())
        await stack.enter_async_context(file_server.session_manager.run())
        
        print("🚀 All MCP servers started")
        print("   - Echo Server: Handles echo and testing")
        print("   - Math Server: Performs mathematical calculations")
        print("   - Database Server: Database queries and operations")
        print("   - File Server: File system access")
        
        yield
        
        print("🧹 All MCP servers gracefully shut down")
```

### 3. Resource and Database Management

Enterprise-level applications need to manage databases, caches, and other complex resources:

```python
@asynccontextmanager
async def mcp_resource_manager(config):
    """
    MCP Enterprise Resource Manager
    
    Manages all persistent resources needed by the application, including database connections,
    cache systems, message queues, etc., ensuring efficient use and proper cleanup.
    """
    print("🔧 Initializing MCP resources...")
    
    # Establish database connection
    db = await Database.connect(config.database_url)
    print("   ✅ Database connection established")
    
    # Establish Redis cache connection
    cache = await RedisCache.connect(config.redis_url)
    print("   ✅ Redis cache connection established")
    
    # Establish message queue connection
    message_queue = await MessageQueue.connect(config.rabbitmq_url)
    print("   ✅ Message queue connection established")
    
    # Create application context
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
        # Generate performance report
        metrics = context["performance_metrics"]
        success_rate = (metrics["successful_requests"] / max(1, metrics["total_requests"])) * 100
        
        print("📊 MCP Session Report:")
        print(f"   💬 Messages processed: {len(context['message_history'])}")
        print(f"   🔄 Total requests: {metrics['total_requests']}")
        print(f"   ✅ Success rate: {success_rate:.1f}%")
        print(f"   ❌ Error count: {metrics['error_count']}")
        
        # Ensure proper cleanup
        await db.disconnect()
        await cache.disconnect() 
        await message_queue.close()
        print("🧹 All enterprise resources safely released")
```

## 🌐 Transport Layer Abstraction

MCP supports multiple transport methods, each with its own context manager implementation:

### stdio Transport (Local Subprocess Communication)

```python
@asynccontextmanager
async def stdio_transport(command, args):
    """
    stdio Transport Manager
    
    Used for communication with locally running MCP server subprocesses.
    Suitable for development and local tool integration.
    """
    print(f"🔧 Starting stdio server: {' '.join([command] + args)}")
    
    process = await asyncio.create_subprocess_exec(
        command, *args,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    try:
        yield (process.stdin, process.stdout)
    finally:
        print("🔧 Terminating stdio server...")
        process.terminate()
        try:
            await asyncio.wait_for(process.wait(), timeout=5.0)
        except asyncio.TimeoutError:
            print("⚠️ Forcing stdio server termination")
            process.kill()
            await process.wait()
        print("✅ stdio server safely shut down")
```

### SSE Transport (HTTP Server-Sent Events)

```python
@asynccontextmanager
async def sse_transport(url, headers=None):
    """
    SSE (Server-Sent Events) Transport Manager
    
    Used for communication with remote HTTP MCP servers.
    Supports real-time streaming, suitable for cloud deployment.
    """
    print(f"🌐 Connecting to SSE server: {url}")
    
    connector = aiohttp.TCPConnector(limit=100, limit_per_host=10)
    session = aiohttp.ClientSession(
        connector=connector,
        headers=headers or {},
        timeout=aiohttp.ClientTimeout(total=30)
    )
    
    try:
        async with session.get(url) as response:
            if response.status != 200:
                raise ConnectionError(f"SSE connection failed: {response.status}")
            
            print("✅ SSE connection established")
            yield session
            
    except Exception as e:
        print(f"❌ SSE connection error: {e}")
        raise
    finally:
        await session.close()
        await connector.close()
        print("🧹 SSE connection closed")
```

### WebSocket Transport (Bidirectional Real-Time Communication)

```python
@asynccontextmanager
async def websocket_transport(url, protocols=None):
    """
    WebSocket Transport Manager
    
    Provides bidirectional real-time communication, suitable for high-frequency interaction.
    Supports auto-reconnect and heartbeat detection.
    """
    print(f"🔌 Connecting to WebSocket server: {url}")
    
    try:
        async with websockets.connect(
            url, 
            subprotocols=protocols or [],
            ping_interval=20,
            ping_timeout=10,
            close_timeout=10
        ) as websocket:
            print("✅ WebSocket connection established")
            print(f"   Protocol: {websocket.subprotocol}")
            print(f"   Extensions: {websocket.extensions}")
            
            yield websocket
            
    except websockets.exceptions.ConnectionClosed:
        print("⚠️ WebSocket connection closed by server")
    except Exception as e:
        print(f"❌ WebSocket connection error: {e}")
        raise
    finally:
        print("🧹 WebSocket connection cleaned up")
```

## 🎯 Complete Real Application Examples

Example showing how to use MCP context managers in practice:

```python
async def intelligent_document_processor():
    """
    Intelligent Document Processing System
    
    Combines multiple MCP servers to provide comprehensive document analysis:
    - Document parsing and content extraction
    - AI-driven content analysis
    - Database storage and retrieval
    - Real-time progress feedback
    """
    
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
    
    async with AsyncExitStack() as stack:
        sessions = {}
        
        for name, params in servers.items():
            print(f"🔧 Connecting to {name} server...")
            session = await stack.enter_async_context(
                mcp_client_session(params)
            )
            sessions[name] = session
        
        print("🚀 All MCP servers connected, starting document processing...")
        
        documents = ["report1.pdf", "analysis2.docx", "data3.xlsx"]
        
        for doc in documents:
            print(f"\n📄 Processing document: {doc}")
            
            parse_result = await sessions["document_parser"].call_tool(
                "parse_document", {"file_path": doc}
            )
            print(f"   ✅ Parsing completed: {parse_result.content['pages']} pages")
            
            analysis_result = await sessions["ai_analyzer"].call_tool(
                "analyze_content", {
                    "content": parse_result.content['text'],
                    "analysis_type": "comprehensive"
                }
            )
            print(f"   🤖 AI analysis completed: {analysis_result.content['sentiment']} sentiment")
            
            storage_result = await sessions["database_manager"].call_tool(
                "store_analysis", {
                    "document": doc,
                    "parse_data": parse_result.content,
                    "analysis_data": analysis_result.content
                }
            )
            print(f"   💾 Data stored: ID {storage_result.content['record_id']}")
            
            results.append({
                "document": doc,
                "record_id": storage_result.content['record_id'],
                "status": "completed"
            })
    
    print(f"\n🎉 Document processing finished! Total {len(results)} documents processed")
    return results
```

## 🔗 Comparison with Other Context Manager Patterns

| Feature                 | MCP                              | llamabot                 | OpenAI SDK            | Local File Ops         |
| ----------------------- | -------------------------------- | ------------------------ | --------------------- | ---------------------- |
| **Main Purpose**        | Standardized AI context protocol | LLM conversation records | API call management   | Resource file handling |
| **Transport**           | stdio/SSE/WebSocket              | In-memory state          | HTTP API              | Local file system      |
| **Resource Management** | Multi-server connection pool     | Session state            | Single API connection | File handles           |
| **Async Support**       | ✅ Native async                   | ✅ Supported              | ✅ Supported           | ❌ Mostly sync          |
| **Standardization**     | ✅ Open standard                  | ❌ Project-specific       | ❌ Vendor-specific     | ✅ Python standard      |
| **Complexity**          | High (enterprise)                | Medium (app-level)       | Low (API-level)       | Low (system-level)     |

## 🎯 Unique Advantages of MCP Context Manager

1. **Standardized Protocol**: Defines unified interfaces for seamless AI service collaboration, avoiding vendor lock-in.
2. **Multi-Transport Support**: Unified context manager interface for stdio, SSE, WebSocket, adaptable to different deployment scenarios.
3. **Enterprise Resource Management**: Full lifecycle management including connection pools, error recovery, performance monitoring.
4. **Type Safety**: Complete TypeScript and Python type definitions for compile-time checks and runtime safety.
5. **Extensible Architecture**: Prompts, Resources, Tools abstractions provide flexible extension mechanisms.

## 🚀 Best Practice Recommendations

1. **Use AsyncExitStack** for complex multi-resource management
2. **Error Handling**: Implement retries and fallbacks for each transport layer
3. **Monitoring & Logging**: Integrate detailed performance monitoring and logging in context managers
4. **Resource Limits**: Configure proper pool sizes and timeouts
5. **Graceful Shutdown**: Ensure all MCP servers shut down properly when application ends

MCP context manager implementation represents best practices in modern AI application architecture, providing a solid foundation for building scalable and maintainable AI systems!