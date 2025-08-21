"""
🧠 04. Smart Session Manager (contextvars)

Using contextvars for global state awareness, internal functions automatically 
get current session context. Inspired by llamabot's PromptRecorder.

Features:
- No need to manually pass session parameters
- Internal functions auto-detect current session  
- Support nested sessions and state isolation
"""

import contextvars
from contextlib import contextmanager

# Global context variables
current_session = contextvars.ContextVar('current_session', default=None)
current_model = contextvars.ContextVar('current_model', default='gpt-3.5-turbo')

@contextmanager
def smart_session(session_id, model="gpt-4"):
    """Smart session manager - auto-set global context"""
    print(f"🧠 Smart session: {session_id}")
    session = {"id": session_id, "calls": [], "model": model}
    
    # Set context variables
    session_token = current_session.set(session)
    model_token = current_model.set(model)
    
    try:
        yield session
    finally:
        # Restore context variables
        current_session.reset(session_token)
        current_model.reset(model_token)
        print(f"📝 Auto-recorded {len(session['calls'])} calls")

def smart_llm_call(prompt):
    """Smart LLM call - auto-detect current session"""
    session = current_session.get()
    model = current_model.get()
    
    if session:
        session["calls"].append({"prompt": prompt, "model": model})
        print(f"🤖 [{model}] {prompt[:20]}... (recorded)")
    else:
        print(f"🤖 [{model}] {prompt[:20]}... (standalone call)")
    
    return f"AI response: {prompt}"

if __name__ == "__main__":
    print("🧠 Smart Session Manager Demo\n")
    
    # 1. Smart session - auto recording
    with smart_session("auto-chat", "gpt-4") as session:
        smart_llm_call("What is contextvars?")
        smart_llm_call("How to apply in LLM?")
        smart_llm_call("Any real use cases?")
    
    # 2. Outside session call
    smart_llm_call("This call won't be recorded")
    
    # 3. Nested sessions
    with smart_session("outer-session"):
        smart_llm_call("Outer session")
        with smart_session("inner-session"):
            smart_llm_call("Inner session")
        smart_llm_call("Back to outer")
    
    print("\n✅ Key Point: contextvars enables global state awareness, internal functions auto-get context")