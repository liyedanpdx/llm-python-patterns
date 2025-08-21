"""
🤖 02. LLM 会话管理器

使用 Context Manager 管理 LLM 会话的生命周期，包括：
- 自动初始化和清理
- Token 计算和成本追踪  
- 异常处理和状态恢复

实际应用：客服机器人、批处理任务、成本监控
"""

from contextlib import contextmanager

@contextmanager
def llm_session(session_id, max_tokens=100):
    """LLM 会话管理器"""
    print(f"🚀 启动会话: {session_id}")
    session = {"id": session_id, "messages": [], "tokens": 0, "max_tokens": max_tokens}
    try:
        yield session
        print(f"✅ 会话完成: {session['id']}")
    except Exception as e:
        print(f"❌ 会话异常: {e}")
        raise
    finally:
        # 会话统计和清理
        cost = session["tokens"] * 0.002 / 1000
        print(f"📊 统计: {len(session['messages'])} 消息, {session['tokens']} tokens, ${cost:.4f}")

def add_message(session, role, content):
    """添加消息到会话"""
    tokens = len(content) // 4  # 简单 token 估算
    session["messages"].append({"role": role, "content": content})
    session["tokens"] += tokens
    
    if session["tokens"] > session["max_tokens"]:
        print(f"⚠️ Token 超限: {session['tokens']}/{session['max_tokens']}")
    
    print(f"💬 {role}: {content[:30]}... ({tokens} tokens)")

if __name__ == "__main__":
    print("🤖 LLM 会话管理器演示\n")
    
    # 基础会话
    with llm_session("chat-001") as session:
        add_message(session, "user", "什么是 Context Manager？")
        add_message(session, "assistant", "Context Manager 确保资源正确管理")
    
    # 异常处理
    try:
        with llm_session("error-demo") as session:
            add_message(session, "user", "测试消息")
            raise ValueError("模拟API错误")
    except ValueError:
        print("✅ 异常已处理，会话正确清理")
    
    print("\n✅ 关键要点：自动管理会话生命周期，确保资源清理和成本追踪")