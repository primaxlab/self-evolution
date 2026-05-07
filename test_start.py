#!/usr/bin/env python3
"""测试自我进化系统是否能启动"""
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from src.core.evolution_system import EvolutionSystem
    print("✅ EvolutionSystem 导入成功")
except Exception as e:
    print(f"❌ EvolutionSystem 导入失败: {e}")
    sys.exit(1)

try:
    from src.memory.storage import MemoryStorage
    print("✅ MemoryStorage 导入成功")
except Exception as e:
    print(f"❌ MemoryStorage 导入失败: {e}")
    sys.exit(1)

try:
    from src.learning.engine import LearningEngine
    print("✅ LearningEngine 导入成功")
except Exception as e:
    print(f"❌ LearningEngine 导入失败: {e}")
    sys.exit(1)

try:
    from src.core.context_optimizer import ContextOptimizer
    print("✅ ContextOptimizer 导入成功")
except Exception as e:
    print(f"❌ ContextOptimizer 导入失败: {e}")
    sys.exit(1)

print("\n🎉 所有模块导入成功！系统可以启动")