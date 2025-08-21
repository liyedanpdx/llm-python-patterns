"""
🧠 04. 智能会话管理器 (contextvars)

使用 contextvars 实现全局状态感知，内部函数自动获取当前会话上下文。
灵感来源：llamabot 项目的 PromptRecorder

特点：
- 无需手动传递 session 参数
- 内部函数自动感知当前会话  
- 支持嵌套会话和状态隔离
"""

import contextvars
from contextlib import contextmanager

# 全局上下文变量
current_session = contextvars.ContextVar('current_session', default=None)
current_model = contextvars.ContextVar('current_model', default='gpt-3.5-turbo')

@contextmanager
def smart_session(session_id, model="gpt-4"):
    """智能会话管理器 - 自动设置全局上下文"""
    print(f"🧠 智能会话: {session_id}")
    session = {"id": session_id, "calls": [], "model": model}
    
    # 设置上下文变量
    session_token = current_session.set(session)
    model_token = current_model.set(model)
    
    try:
        yield session
    finally:
        # 恢复上下文变量
        current_session.reset(session_token)
        current_model.reset(model_token)
        print(f"📝 自动记录了 {len(session['calls'])} 次调用")

def smart_llm_call(prompt):
    """智能 LLM 调用 - 自动感知当前会话"""
    session = current_session.get()
    model = current_model.get()
    
    if session:
        session["calls"].append({"prompt": prompt, "model": model})
        print(f"🤖 [{model}] {prompt[:20]}... (已记录)")
    else:
        print(f"🤖 [{model}] {prompt[:20]}... (独立调用)")
    
    return f"AI回复: {prompt}"

if __name__ == "__main__":
    print("🧠 智能会话管理器演示\n")
    
    # 1. 智能会话 - 自动记录
    with smart_session("auto-chat", "gpt-4") as session:
        smart_llm_call("什么是 contextvars？")
        smart_llm_call("如何在 LLM 中应用？")
        smart_llm_call("有什么实际案例？")
    
    # 2. 会话外调用
    smart_llm_call("这个调用不会被记录")
    
    # 3. 嵌套会话
    with smart_session("outer-session"):
        smart_llm_call("外层会话")
        with smart_session("inner-session"):
            smart_llm_call("内层会话")
        smart_llm_call("回到外层")
    
    print("\n✅ 关键要点：contextvars 实现全局状态感知，内部函数自动获取上下文")