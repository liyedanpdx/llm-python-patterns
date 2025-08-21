"""
🤖 02. LLM Session Manager

Using Context Manager to manage LLM session lifecycle, including:
- Automatic initialization and cleanup
- Token calculation and cost tracking  
- Exception handling and state recovery

Real applications: chatbots, batch processing, cost monitoring
"""

from contextlib import contextmanager

@contextmanager
def llm_session(session_id, max_tokens=100):
    """LLM Session Manager"""
    print(f"🚀 Starting session: {session_id}")
    session = {"id": session_id, "messages": [], "tokens": 0, "max_tokens": max_tokens}
    try:
        yield session
        print(f"✅ Session completed: {session['id']}")
    except Exception as e:
        print(f"❌ Session error: {e}")
        raise
    finally:
        # Session statistics and cleanup
        cost = session["tokens"] * 0.002 / 1000
        print(f"📊 Stats: {len(session['messages'])} messages, {session['tokens']} tokens, ${cost:.4f}")

def add_message(session, role, content):
    """Add message to session"""
    tokens = len(content) // 4  # Simple token estimation
    session["messages"].append({"role": role, "content": content})
    session["tokens"] += tokens
    
    if session["tokens"] > session["max_tokens"]:
        print(f"⚠️ Token limit exceeded: {session['tokens']}/{session['max_tokens']}")
    
    print(f"💬 {role}: {content[:30]}... ({tokens} tokens)")

if __name__ == "__main__":
    print("🤖 LLM Session Manager Demo\n")
    
    # Basic session
    with llm_session("chat-001") as session:
        add_message(session, "user", "What is Context Manager?")
        add_message(session, "assistant", "Context Manager ensures proper resource management")
    
    # Exception handling
    try:
        with llm_session("error-demo") as session:
            add_message(session, "user", "Test message")
            raise ValueError("Simulated API error")
    except ValueError:
        print("✅ Exception handled, session properly cleaned up")
    
    print("\n✅ Key Point: Automatically manage session lifecycle, ensure resource cleanup and cost tracking")