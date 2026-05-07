#!/usr/bin/env python3
"""测试自我进化系统知识库"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.learning.engine import LearningEngine, KnowledgeDomain, LearningStrategy
import asyncio

async def test_knowledge():
    eng = LearningEngine()
    await eng.start_async_session()
    
    # 查看所有知识点
    all_kp = eng.get_relevant_knowledge('', limit=100)
    print(f'知识库总计: {len(all_kp)} 条\n')
    
    # 按领域分组
    domains = {}
    for kp in all_kp:
        d = kp.domain.value
        if d not in domains:
            domains[d] = []
        domains[d].append(kp)
    
    for domain, points in domains.items():
        print(f'[{domain}] ({len(points)}条)')
        for kp in points:
            print(f'  [{kp.confidence:.0%}] {kp.content[:70]}')
        print()
    
    # 查看学习统计
    stats = eng.get_statistics()
    print(f'统计:')
    total = stats.get('total_knowledge_points', 0)
    by_domain = stats.get('knowledge_by_domain', {})
    print(f'  总知识点: {total}')
    print(f'  领域分布: {by_domain}')
    
    # 运行一次进化（knowledge_synthesis）
    print('\n=== 运行新进化 ===')
    task_id = eng.create_learning_task(
        query='LLM推理优化技术',
        strategy=LearningStrategy.KNOWLEDGE_SYNTHESIS,
        domain=KnowledgeDomain.AI_ML,
        priority=8
    )
    results = await eng.execute_learning_task(task_id)
    print(f'进化产出: {len(results)} 个新知识点')
    for kp in results:
        print(f'  [{kp.confidence:.0%}] {kp.content[:80]}')
    
    # 最终统计
    stats2 = eng.get_statistics()
    print(f'\n最终知识库: {stats2["total_knowledge_points"]} 条')

asyncio.run(test_knowledge())
