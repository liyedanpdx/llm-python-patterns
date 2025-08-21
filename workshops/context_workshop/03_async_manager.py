"""
⚡ 03. 异步 Context Manager

异步 Context Manager 适用于需要异步资源管理的场景，如：
- GPU 资源池管理
- 异步网络连接
- 并发任务协调

核心：使用 @asynccontextmanager 装饰器和 async with 语句
"""

import asyncio
from contextlib import asynccontextmanager

@asynccontextmanager
async def gpu_resource(gpu_id):
    """GPU 资源管理器"""
    print(f"🔧 分配 GPU-{gpu_id}")
    await asyncio.sleep(0.1)  # 模拟异步资源分配
    try:
        yield f"GPU-{gpu_id}"
    finally:
        print(f"🔧 释放 GPU-{gpu_id}")
        await asyncio.sleep(0.05)  # 模拟异步清理

@asynccontextmanager
async def async_llm_session(session_id):
    """异步 LLM 会话管理器"""
    print(f"🚀 异步启动: {session_id}")
    session = {"id": session_id, "tasks": []}
    try:
        yield session
        print(f"✅ 异步完成: {session_id}")
    finally:
        print(f"📊 处理了 {len(session['tasks'])} 个任务")

async def process_llm_query(session, query):
    """模拟异步 LLM 查询处理"""
    session["tasks"].append(query)
    print(f"   🔄 处理: {query}")
    await asyncio.sleep(0.1)  # 模拟异步处理时间
    return f"回复: {query}"

async def main():
    print("⚡ 异步 Context Manager 演示\n")
    
    # 1. GPU 资源管理
    async with gpu_resource("A100") as gpu:
        print(f"   使用 {gpu} 进行计算")
        await asyncio.sleep(0.05)
    
    # 2. 异步会话处理
    async with async_llm_session("async-chat") as session:
        tasks = [
            process_llm_query(session, "查询A"),
            process_llm_query(session, "查询B"),
            process_llm_query(session, "查询C")
        ]
        results = await asyncio.gather(*tasks)
        print(f"   📈 并发结果: {len(results)} 个")
    
    print("\n✅ 关键要点：async with 管理异步资源，支持并发处理")

if __name__ == "__main__":
    asyncio.run(main())