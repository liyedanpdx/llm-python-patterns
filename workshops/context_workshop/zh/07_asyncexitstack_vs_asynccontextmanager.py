"""
🔧 AsyncExitStack vs @asynccontextmanager 对比

AsyncExitStack 和 @asynccontextmanager 的关系：
- @asynccontextmanager: 创建单个异步上下文管理器
- AsyncExitStack: 管理多个异步上下文管理器的组合

实际关系：AsyncExitStack 内部使用多个 @asynccontextmanager 创建的对象
"""

import asyncio
from contextlib import asynccontextmanager, AsyncExitStack

# =============================================================================
# 1. 单个资源管理 - @asynccontextmanager
# =============================================================================

@asynccontextmanager
async def database_connection(db_name):
    """单个数据库连接管理器"""
    print(f"🔌 连接数据库: {db_name}")
    await asyncio.sleep(0.1)  # 模拟连接时间
    connection = f"DB_{db_name}_connection"
    try:
        yield connection
    finally:
        print(f"🔌 关闭数据库: {db_name}")
        await asyncio.sleep(0.05)  # 模拟关闭时间

@asynccontextmanager
async def redis_cache(cache_name):
    """单个 Redis 缓存管理器"""
    print(f"⚡ 连接缓存: {cache_name}")
    await asyncio.sleep(0.1)
    cache = f"CACHE_{cache_name}_connection"
    try:
        yield cache
    finally:
        print(f"⚡ 关闭缓存: {cache_name}")
        await asyncio.sleep(0.05)

@asynccontextmanager
async def message_queue(queue_name):
    """单个消息队列管理器"""
    print(f"📬 连接队列: {queue_name}")
    await asyncio.sleep(0.1)
    queue = f"QUEUE_{queue_name}_connection"
    try:
        yield queue
    finally:
        print(f"📬 关闭队列: {queue_name}")
        await asyncio.sleep(0.05)

# =============================================================================
# 2. 传统嵌套方式 - 多个 @asynccontextmanager
# =============================================================================

async def traditional_nested_approach():
    """传统的嵌套 async with 方式"""
    print("📍 传统嵌套方式:")
    print("-" * 30)
    
    async with database_connection("users") as db:
        async with redis_cache("session") as cache:
            async with message_queue("notifications") as queue:
                print(f"✅ 使用资源: {db}, {cache}, {queue}")
                await asyncio.sleep(0.1)  # 模拟工作
    print()

# =============================================================================
# 3. AsyncExitStack 方式 - 动态管理多个资源
# =============================================================================

async def async_exit_stack_approach():
    """AsyncExitStack 动态管理多个资源"""
    print("📍 AsyncExitStack 方式:")
    print("-" * 30)
    
    async with AsyncExitStack() as stack:
       # 动态添加多个异步上下文管理器
        db = await stack.enter_async_context(database_connection("users"))
        cache = await stack.enter_async_context(redis_cache("session"))
        queue = await stack.enter_async_context(message_queue("notifications"))
         
        print(f"✅ 使用资源: {db}, {cache}, {queue}")
        await asyncio.sleep(0.1)  # 模拟工作
    print()

# =============================================================================
# 4. AsyncExitStack 的动态特性
# =============================================================================

async def dynamic_resource_management():
    """展示 AsyncExitStack 的动态特性"""
    print("📍 动态资源管理:")
    print("-" * 30)
    
    async with AsyncExitStack() as stack:
        resources = []
        
        # 根据条件动态添加资源
        configs = [
            ("primary_db", "database"),
            ("user_cache", "cache"),
            ("email_queue", "queue")
        ]
        
        for name, resource_type in configs:
            if resource_type == "database":
                resource = await stack.enter_async_context(database_connection(name))
            elif resource_type == "cache":
                resource = await stack.enter_async_context(redis_cache(name))
            elif resource_type == "queue":
                resource = await stack.enter_async_context(message_queue(name))
            
            resources.append(resource)
            print(f"   ➕ 动态添加: {resource}")
        
        print(f"✅ 管理 {len(resources)} 个动态资源")
        await asyncio.sleep(0.1)
    print()

# =============================================================================
# 5. 组合使用 - AsyncExitStack 管理自定义 @asynccontextmanager
# =============================================================================

@asynccontextmanager
async def application_context(app_name):
    """应用级上下文管理器 - 内部使用 AsyncExitStack"""
    print(f"🚀 启动应用: {app_name}")
    
    async with AsyncExitStack() as stack:
        # 应用需要的所有资源
        db = await stack.enter_async_context(database_connection("app_db"))
        cache = await stack.enter_async_context(redis_cache("app_cache"))
        queue = await stack.enter_async_context(message_queue("app_queue"))
        
        # 创建应用上下文
        app_context = {
            "name": app_name,
            "database": db,
            "cache": cache,
            "message_queue": queue,
            "startup_time": asyncio.get_event_loop().time()
        }
        
        try:
            yield app_context
        finally:
            uptime = asyncio.get_event_loop().time() - app_context["startup_time"]
            print(f"🚀 应用 {app_name} 运行了 {uptime:.2f} 秒")

async def combined_approach():
    """组合使用两种方式"""
    print("📍 组合使用方式:")
    print("-" * 30)
    
    # 外层使用 AsyncExitStack 管理多个应用
    async with AsyncExitStack() as stack:
        # 每个应用内部使用 @asynccontextmanager + AsyncExitStack
        app1 = await stack.enter_async_context(application_context("WebServer"))
        app2 = await stack.enter_async_context(application_context("APIGateway"))
        
        print(f"✅ 运行应用: {app1['name']} 和 {app2['name']}")
        await asyncio.sleep(0.2)
    print()

# =============================================================================
# 6. 错误处理对比
# =============================================================================

async def error_handling_comparison():
    """错误处理对比"""
    print("📍 错误处理对比:")
    print("-" * 30)
    
    # AsyncExitStack 的错误处理
    try:
        async with AsyncExitStack() as stack:
            db = await stack.enter_async_context(database_connection("test_db"))
            cache = await stack.enter_async_context(redis_cache("test_cache"))
            
            print("⚠️ 模拟错误...")
            raise ValueError("测试错误")
            
    except ValueError as e:
        print(f"✅ 错误已捕获: {e}")
        print("   所有资源仍然正确清理")
    
    print()

# =============================================================================
# 主程序
# =============================================================================

async def main():
    print("🔧 AsyncExitStack vs @asynccontextmanager 对比演示")
    print("=" * 60)
    
    await traditional_nested_approach()
    await async_exit_stack_approach()
    await dynamic_resource_management()
    await combined_approach()
    await error_handling_comparison()
    
    print("📚 关键区别总结:")
    print("✅ @asynccontextmanager: 创建单个异步上下文管理器")
    print("✅ AsyncExitStack: 管理多个异步上下文管理器")
    print("✅ 关系: AsyncExitStack 使用 @asynccontextmanager 创建的对象")
    print("✅ 优势: AsyncExitStack 支持动态添加和复杂的资源管理")

if __name__ == "__main__":
    asyncio.run(main())