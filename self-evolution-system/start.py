#!/usr/bin/env python3
"""自我进化系统启动脚本"""
import asyncio
import sys
import os
import json
from datetime import datetime

# 设置UTF-8编码
sys.stdout.reconfigure(encoding='utf-8')
os.environ['PYTHONIOENCODING'] = 'utf-8'

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.core.evolution_system import EvolutionSystem

async def main():
    """主函数"""
    print("\n" + "="*70)
    print("SELF-EVOLUTION SYSTEM - 完整解决OpenClaw上下文超限问题")
    print("="*70)

    system = EvolutionSystem("config/settings.yaml")
    try:
        print("\n[Phase 1] System initialization")
        await system.initialize()
        print("System initialized")

        state = system.get_system_state()
        print(f"\nInitial state:")
        print(f"  Session ID: {system.session_id}")
        print(f"  System version: {system.config.get('system', {}).get('version', '1.0.0')}")

        print("\n[Phase 2] Solving context overflow...")
        solution = await system.solve_context_overflow()

        print(f"\nSolution report:")
        print(f"  Detected tokens: {solution['detected_tokens']}")
        print(f"  Target: {solution['target_tokens']}")
        print(f"  Solutions applied: {', '.join(solution['solutions_applied'])}")
        print(f"  Final tokens: {solution['final_tokens']}")
        print(f"  Compression ratio: {solution['compression_ratio']:.1%}")
        print(f"  Integrity: {solution['integrity']:.1%}")

        if solution["success"]:
            print("\nSUCCESS: Context overflow resolved!")
        else:
            print("\nWARNING: Problem not fully resolved")

        print("\n[Phase 3] Running full evolution...")
        evolution_result = await system.evolve("full")
        if evolution_result["success"]:
            print("Full evolution completed")
        else:
            print(f"Evolution failed: {evolution_result['error']}")

        print("\n[Done] System running")

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await system.shutdown()
        print("\nSystem shutdown complete")

if __name__ == "__main__":
    asyncio.run(main())