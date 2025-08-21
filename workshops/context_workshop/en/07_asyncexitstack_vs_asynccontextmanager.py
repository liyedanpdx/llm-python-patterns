"""
🔧 AsyncExitStack vs @asynccontextmanager Comparison

Relationship between AsyncExitStack and @asynccontextmanager:
- @asynccontextmanager: Creates a single async context manager
- AsyncExitStack: Manages combinations of multiple async context managers

Actual relationship: AsyncExitStack internally uses multiple objects created by @asynccontextmanager
"""

import asyncio
from contextlib import asynccontextmanager, AsyncExitStack

# =============================================================================
# 1. Single Resource Manager - @asynccontextmanager
# =============================================================================

@asynccontextmanager
async def database_connection(db_name):
    """Single database connection manager"""
    print(f"🔌 Connecting to database: {db_name}")
    await asyncio.sleep(0.1)  # Simulate connection time
    connection = f"DB_{db_name}_connection"
    try:
        yield connection
    finally:
        print(f"🔌 Closing database: {db_name}")
        await asyncio.sleep(0.05)  # Simulate closing time

@asynccontextmanager
async def redis_cache(cache_name):
    """Single Redis cache manager"""
    print(f"⚡ Connecting to cache: {cache_name}")
    await asyncio.sleep(0.1)
    cache = f"CACHE_{cache_name}_connection"
    try:
        yield cache
    finally:
        print(f"⚡ Closing cache: {cache_name}")
        await asyncio.sleep(0.05)

@asynccontextmanager
async def message_queue(queue_name):
    """Single message queue manager"""
    print(f"📬 Connecting to queue: {queue_name}")
    await asyncio.sleep(0.1)
    queue = f"QUEUE_{queue_name}_connection"
    try:
        yield queue
    finally:
        print(f"📬 Closing queue: {queue_name}")
        await asyncio.sleep(0.05)

# =============================================================================
# 2. Traditional Nested Approach - Multiple @asynccontextmanager
# =============================================================================

async def traditional_nested_approach():
    """Traditional nested async with approach"""
    print("📍 Traditional nested approach:")
    print("-" * 30)
    
    async with database_connection("users") as db:
        async with redis_cache("session") as cache:
            async with message_queue("notifications") as queue:
                print(f"✅ Using resources: {db}, {cache}, {queue}")
                await asyncio.sleep(0.1)  # Simulate work
    print()

# =============================================================================
# 3. AsyncExitStack Approach - Dynamic Management of Multiple Resources
# =============================================================================

async def async_exit_stack_approach():
    """AsyncExitStack dynamically manages multiple resources"""
    print("📍 AsyncExitStack approach:")
    print("-" * 30)
    
    async with AsyncExitStack() as stack:
       # Dynamically add multiple async context managers
        db = await stack.enter_async_context(database_connection("users"))
        cache = await stack.enter_async_context(redis_cache("session"))
        queue = await stack.enter_async_context(message_queue("notifications"))
         
        print(f"✅ Using resources: {db}, {cache}, {queue}")
        await asyncio.sleep(0.1)  # Simulate work
    print()

# =============================================================================
# 4. Dynamic Features of AsyncExitStack
# =============================================================================

async def dynamic_resource_management():
    """Demonstrate dynamic features of AsyncExitStack"""
    print("📍 Dynamic resource management:")
    print("-" * 30)
    
    async with AsyncExitStack() as stack:
        resources = []
        
        # Dynamically add resources based on conditions
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
            print(f"   ➕ Dynamically added: {resource}")
        
        print(f"✅ Managing {len(resources)} dynamic resources")
        await asyncio.sleep(0.1)
    print()

# =============================================================================
# 5. Combined Usage - AsyncExitStack Managing Custom @asynccontextmanager
# =============================================================================

@asynccontextmanager
async def application_context(app_name):
    """Application-level context manager - internally uses AsyncExitStack"""
    print(f"🚀 Starting application: {app_name}")
    
    async with AsyncExitStack() as stack:
        # All resources needed by the application
        db = await stack.enter_async_context(database_connection("app_db"))
        cache = await stack.enter_async_context(redis_cache("app_cache"))
        queue = await stack.enter_async_context(message_queue("app_queue"))
        
        # Create application context
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
            print(f"🚀 Application {app_name} ran for {uptime:.2f} seconds")

async def combined_approach():
    """Combined usage of both approaches"""
    print("📍 Combined usage approach:")
    print("-" * 30)
    
    # Outer layer uses AsyncExitStack to manage multiple applications
    async with AsyncExitStack() as stack:
        # Each application internally uses @asynccontextmanager + AsyncExitStack
        app1 = await stack.enter_async_context(application_context("WebServer"))
        app2 = await stack.enter_async_context(application_context("APIGateway"))
        
        print(f"✅ Running applications: {app1['name']} and {app2['name']}")
        await asyncio.sleep(0.2)
    print()

# =============================================================================
# 6. Error Handling Comparison
# =============================================================================

async def error_handling_comparison():
    """Error handling comparison"""
    print("📍 Error handling comparison:")
    print("-" * 30)
    
    # AsyncExitStack error handling
    try:
        async with AsyncExitStack() as stack:
            db = await stack.enter_async_context(database_connection("test_db"))
            cache = await stack.enter_async_context(redis_cache("test_cache"))
            
            print("⚠️ Simulating error...")
            raise ValueError("Test error")
            
    except ValueError as e:
        print(f"✅ Error caught: {e}")
        print("   All resources still properly cleaned up")
    
    print()

# =============================================================================
# 主程序
# =============================================================================

async def main():
    print("🔧 AsyncExitStack vs @asynccontextmanager ComparisonDemo")
    print("=" * 60)
    
    await traditional_nested_approach()
    await async_exit_stack_approach()
    await dynamic_resource_management()
    await combined_approach()
    await error_handling_comparison()
    
    print("📚 Key differences summary:")
    print("✅ @asynccontextmanager: Creates single async context manager")
    print("✅ AsyncExitStack: Manages multiple async context managers")
    print("✅ Relationship: AsyncExitStack uses objects created by @asynccontextmanager")
    print("✅ Advantage: AsyncExitStack supports dynamic addition and complex resource management")

if __name__ == "__main__":
    asyncio.run(main())