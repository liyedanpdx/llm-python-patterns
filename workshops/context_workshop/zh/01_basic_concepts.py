"""
🎯 01. Context Manager 基础概念

Context Manager 是 Python with 语句背后的机制，确保资源正确获取和释放。
核心模式：setup -> use -> cleanup，即使发生异常也会执行清理工作。

实际应用：文件操作、数据库连接、临时配置、时间测量等。
"""

import time
from contextlib import contextmanager

@contextmanager
def simple_timer(task_name):
    """最简单的计时器 Context Manager"""
    print(f"⏰ 开始: {task_name}")
    start = time.time()
    try:
        yield start  # yield 前是 setup，后是 cleanup
    finally:
        print(f"✅ 完成: {task_name} ({time.time() - start:.2f}s)")

@contextmanager  
def temp_config(config, key, value):
    """临时修改配置，退出时自动恢复"""
    original = config.get(key)
    config[key] = value
    print(f"🔄 临时设置 {key}={value}")
    try:
        yield config
    finally:
        config[key] = original
        print(f"🔄 恢复 {key}={original}")

if __name__ == "__main__":
    print("🎯 Context Manager 基础演示\n")
    
    # 1. 基础计时器
    with simple_timer("数据处理") as start:
        time.sleep(0.1)
        print(f"   开始时间: {start:.2f}")
    
    # 2. 临时配置
    config = {"debug": False}
    print(f"\n原始配置: {config}")
    with temp_config(config, "debug", True):
        print(f"临时配置: {config}")
    print(f"恢复配置: {config}")
    
    print("\n✅ 关键要点：yield 分隔 setup/cleanup，finally 确保清理执行")