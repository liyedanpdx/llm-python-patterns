"""
⚡ 03. Async Context Manager

Async Context Manager for scenarios requiring async resource management:
- GPU resource pool management
- Async network connections
- Concurrent task coordination

Core: @asynccontextmanager decorator and async with statements
"""

import asyncio
from contextlib import asynccontextmanager

@asynccontextmanager
async def gpu_resource(gpu_id):
    """GPU Resource Manager"""
    print(f"🔧 Allocating GPU-{gpu_id}")
    await asyncio.sleep(0.1)  # Simulate async resource allocation
    try:
        yield f"GPU-{gpu_id}"
    finally:
        print(f"🔧 Releasing GPU-{gpu_id}")
        await asyncio.sleep(0.05)  # Simulate async cleanup

@asynccontextmanager
async def async_llm_session(session_id):
    """Async LLM Session Manager"""
    print(f"🚀 Async starting: {session_id}")
    session = {"id": session_id, "tasks": []}
    try:
        yield session
        print(f"✅ Async completed: {session_id}")
    finally:
        print(f"📊 Processed {len(session['tasks'])} tasks")

async def process_llm_query(session, query):
    """Simulate async LLM query processing"""
    session["tasks"].append(query)
    print(f"   🔄 Processing: {query}")
    await asyncio.sleep(0.1)  # Simulate async processing time
    return f"Response: {query}"

async def main():
    print("⚡ Async Context Manager Demo\n")
    
    # 1. GPU resource management
    async with gpu_resource("A100") as gpu:
        print(f"   Using {gpu} for computation")
        await asyncio.sleep(0.05)
    
    # 2. Async session processing
    async with async_llm_session("async-chat") as session:
        tasks = [
            process_llm_query(session, "Query A"),
            process_llm_query(session, "Query B"),
            process_llm_query(session, "Query C")
        ]
        results = await asyncio.gather(*tasks)
        print(f"   📈 Concurrent results: {len(results)} items")
    
    print("\n✅ Key Point: async with manages async resources, supports concurrent processing")

if __name__ == "__main__":
    asyncio.run(main())