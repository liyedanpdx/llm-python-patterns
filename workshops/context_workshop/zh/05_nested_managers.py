"""
🔄 05. 嵌套组合 Context Manager

演示如何组合多个 Context Manager 实现复杂的资源管理，如：
- 预算控制 + 性能监控 + 会话管理
- 多层嵌套的资源依赖
- 企业级系统的综合管理

核心：多个 with 语句的嵌套使用
"""

from contextlib import contextmanager
import time

@contextmanager
def budget_tracker(budget):
    """预算追踪管理器"""
    print(f"💰 预算控制: ${budget}")
    tracker = {"budget": budget, "spent": 0}
    try:
        yield tracker
    finally:
        remaining = tracker["budget"] - tracker["spent"]
        print(f"💰 预算结算: 花费 ${tracker['spent']:.3f}, 剩余 ${remaining:.3f}")

@contextmanager
def performance_monitor(task_name):
    """性能监控管理器"""
    print(f"📊 性能监控: {task_name}")
    start = time.time()
    try:
        yield {"task": task_name, "start_time": start}
    finally:
        duration = time.time() - start
        print(f"📊 性能报告: {task_name} 耗时 {duration:.2f}s")

@contextmanager
def simple_session(session_id):
    """简化的会话管理器"""
    print(f"🚀 会话: {session_id}")
    session = {"id": session_id, "operations": []}
    try:
        yield session
    finally:
        print(f"🚀 会话结束: {session_id} ({len(session['operations'])} 操作)")

def simulate_llm_call(session, budget, operation):
    """模拟 LLM 调用"""
    cost = 0.01  # 每次调用成本
    session["operations"].append(operation)
    budget["spent"] += cost
    print(f"   🤖 执行: {operation} (成本: ${cost})")

if __name__ == "__main__":
    print("🔄 嵌套组合 Context Manager 演示\n")
    
    # 三层嵌套：预算 + 监控 + 会话
    with budget_tracker(0.05) as budget:
        with performance_monitor("AI批处理") as monitor:
            with simple_session("batch-001") as session:
                simulate_llm_call(session, budget, "数据分析")
                simulate_llm_call(session, budget, "报告生成")
                simulate_llm_call(session, budget, "结果验证")
                
                print(f"   📈 当前花费: ${budget['spent']:.3f}")
    
    print("\n✅ 关键要点：嵌套 Context Manager 实现多层资源管理和监控")