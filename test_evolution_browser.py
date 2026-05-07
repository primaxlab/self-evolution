#!/usr/bin/env python3
"""测试浏览器研究 + 知识库增长"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.learning.engine import LearningEngine, LearningStrategy, KnowledgeDomain
from src.memory.storage import MemoryStorage, MemoryRecord, MemoryType, ImportanceLevel
from src.core.evolution_system import EvolutionSystem
import asyncio

async def main():
    print('=' * 60)
    print('自我进化系统 - 进化能力全面测试')
    print('=' * 60)
    
    system = EvolutionSystem("config/settings.yaml")
    await system.initialize()
    
    # 查看初始知识库
    stats_before = system.learning_engine.get_statistics()
    print(f'\n进化前知识库: {stats_before["total_knowledge_points"]} 条')
    
    # 测试1: knowledge_synthesis (有种子知识)
    print('\n--- 测试1: 知识合成进化 ---')
    kp1 = await system.learn_from_query(
        query='深度学习模型优化最佳实践',
        strategy=LearningStrategy.KNOWLEDGE_SYNTHESIS,
        domain=KnowledgeDomain.AI_ML
    )
    print(f'  获得 {len(kp1)} 个知识点')
    
    # 测试2: 浏览器研究 (自动降级到冷启动)
    print('\n--- 测试2: 浏览器研究 (优雅降级) ---')
    kp2 = await system.learn_from_query(
        query='分布式系统可靠性设计模式',
        strategy=LearningStrategy.BROWSER_RESEARCH,
        domain=KnowledgeDomain.TECHNOLOGY
    )
    print(f'  获得 {len(kp2)} 个知识点')
    
    # 测试3: 再次知识合成 (现在有更多知识可合成)
    print('\n--- 测试3: 基于已有知识的二次合成 ---')
    kp3 = await system.learn_from_query(
        query='AI系统自我优化方法',
        strategy=LearningStrategy.KNOWLEDGE_SYNTHESIS,
        domain=KnowledgeDomain.AI_ML
    )
    print(f'  获得 {len(kp3)} 个知识点')
    
    # 查看进化后知识库
    stats_after = system.learning_engine.get_statistics()
    print(f'\n进化后知识库: {stats_after["total_knowledge_points"]} 条')
    print(f'  本次进化新增: {stats_after["total_knowledge_points"] - stats_before["total_knowledge_points"]} 条')
    print(f'  领域分布: {stats_after["knowledge_by_domain"]}')
    
    # 查看系统状态
    state = system.get_system_state()
    print(f'\n系统状态:')
    print(f'  进化次数: {state.evolution_count}')
    print(f'  学习任务: {state.completed_learning_tasks}/{state.total_learning_tasks}')
    print(f'  总知识量: {state.total_knowledge_points}')
    
    await system.shutdown()
    print('\n测试完成！')

asyncio.run(main())
