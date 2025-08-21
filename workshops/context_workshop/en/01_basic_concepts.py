"""
🎯 01. Context Manager Fundamentals

Context Manager is the mechanism behind Python's with statement, ensuring proper resource 
acquisition and release. Core pattern: setup -> use -> cleanup, cleanup executes even if exceptions occur.

Real applications: file operations, database connections, temporary configurations, timing measurements, etc.
"""

import time
from contextlib import contextmanager

@contextmanager
def simple_timer(task_name):
    """Simplest timer Context Manager"""
    print(f"⏰ Starting: {task_name}")
    start = time.time()
    try:
        yield start  # setup before yield, cleanup after
    finally:
        print(f"✅ Completed: {task_name} ({time.time() - start:.2f}s)")

@contextmanager  
def temp_config(config, key, value):
    """Temporarily modify config, auto-restore on exit"""
    original = config.get(key)
    config[key] = value
    print(f"🔄 Temp setting {key}={value}")
    try:
        yield config
    finally:
        config[key] = original
        print(f"🔄 Restored {key}={original}")

if __name__ == "__main__":
    print("🎯 Context Manager Basic Demo\n")
    
    # 1. Basic timer
    with simple_timer("data processing") as start:
        time.sleep(0.1)
        print(f"   Start time: {start:.2f}")
    
    # 2. Temporary config
    config = {"debug": False}
    print(f"\nOriginal config: {config}")
    with temp_config(config, "debug", True):
        print(f"Temp config: {config}")
    print(f"Restored config: {config}")
    
    print("\n✅ Key Point: yield separates setup/cleanup, finally ensures cleanup execution")