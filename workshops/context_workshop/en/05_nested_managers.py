"""
🔄 05. Nested Composite Context Manager

Demonstrate how to compose multiple Context Managers for complex resource management:
- Budget control + performance monitoring + session management
- Multi-layer nested resource dependencies
- Enterprise-grade comprehensive management

Core: Nested usage of multiple with statements
"""

from contextlib import contextmanager
import time

@contextmanager
def budget_tracker(budget):
    """Budget Tracker Manager"""
    print(f"💰 Budget control: ${budget}")
    tracker = {"budget": budget, "spent": 0}
    try:
        yield tracker
    finally:
        remaining = tracker["budget"] - tracker["spent"]
        print(f"💰 Budget summary: spent ${tracker['spent']:.3f}, remaining ${remaining:.3f}")

@contextmanager
def performance_monitor(task_name):
    """Performance Monitor Manager"""
    print(f"📊 Performance monitoring: {task_name}")
    start = time.time()
    try:
        yield {"task": task_name, "start_time": start}
    finally:
        duration = time.time() - start
        print(f"📊 Performance report: {task_name} took {duration:.2f}s")

@contextmanager
def simple_session(session_id):
    """Simplified Session Manager"""
    print(f"🚀 Session: {session_id}")
    session = {"id": session_id, "operations": []}
    try:
        yield session
    finally:
        print(f"🚀 Session ended: {session_id} ({len(session['operations'])} operations)")

def simulate_llm_call(session, budget, operation):
    """Simulate LLM call"""
    cost = 0.01  # Cost per call
    session["operations"].append(operation)
    budget["spent"] += cost
    print(f"   🤖 Executing: {operation} (Cost: ${cost})")

if __name__ == "__main__":
    print("🔄 Nested Composite Context Manager Demo\n")
    
    # Three-layer nesting: budget + monitoring + session
    with budget_tracker(0.05) as budget:
        with performance_monitor("AI batch processing") as monitor:
            with simple_session("batch-001") as session:
                simulate_llm_call(session, budget, "data analysis")
                simulate_llm_call(session, budget, "report generation")
                simulate_llm_call(session, budget, "result validation")
                
                print(f"   📈 Current spending: ${budget['spent']:.3f}")
    
    print("\n✅ Key Point: Nested Context Manager enables multi-layer resource management and monitoring")