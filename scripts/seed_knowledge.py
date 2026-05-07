#!/usr/bin/env python3
"""知识库种子脚本 - 为自我进化系统预制基础知识"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.learning.engine import LearningEngine, LearningStrategy, KnowledgeDomain, KnowledgePoint
import hashlib
from datetime import datetime
import json

SEED_KNOWLEDGE = [
    # AI/ML 领域
    ("Transformer架构的核心是多头自注意力机制，通过QKV矩阵计算注意力权重",
     KnowledgeDomain.AI_ML, KnowledgeDomain.AI_ML, ["transformer", "attention", "deep-learning"]),
    ("上下文压缩的三种策略：结构化压缩（保留骨架）、语义压缩（保留含义）、混合压缩（平衡）",
     KnowledgeDomain.AI_ML, KnowledgeDomain.TECHNOLOGY, ["context", "compression", "optimization"]),
    ("知识蒸馏是将大模型知识迁移到小模型的技术，保持输出分布相似",
     KnowledgeDomain.AI_ML, KnowledgeDomain.AI_ML, ["distillation", "model-compression"]),
    ("强化学习通过奖励信号引导模型行为，PPO算法是当前最主流的RLHF方法",
     KnowledgeDomain.AI_ML, KnowledgeDomain.AI_ML, ["reinforcement-learning", "ppo", "rlhf"]),
    ("大语言模型的温度参数控制输出随机性：低温=确定性强，高温=创造性高",
     KnowledgeDomain.AI_ML, KnowledgeDomain.AI_ML, ["temperature", "sampling", "llm"]),
    ("RAG架构通过向量检索增强LLM的知识覆盖，有效消除幻觉问题",
     KnowledgeDomain.AI_ML, KnowledgeDomain.TECHNOLOGY, ["rag", "retrieval", "knowledge-base"]),
    ("Few-shot学习通过提供少量范例让LLM理解任务，优于Zero-shot但需要更多上下文",
     KnowledgeDomain.AI_ML, KnowledgeDomain.AI_ML, ["few-shot", "prompt-engineering", "in-context-learning"]),
    ("Chain-of-Thought提示通过逐步推理提升复杂问题的准确率，适合数学和逻辑任务",
     KnowledgeDomain.AI_ML, KnowledgeDomain.AI_ML, ["cot", "reasoning", "prompt"]),

    # 编程领域
    ("Python异步编程使用async/await语法，核心事件循环通过asyncio.get_event_loop()管理",
     KnowledgeDomain.PROGRAMMING, KnowledgeDomain.PROGRAMMING, ["python", "async", "event-loop"]),
    ("SQLite的WAL模式提升并发读写性能，通过PRAGMA journal_mode=WAL启用",
     KnowledgeDomain.PROGRAMMING, KnowledgeDomain.PROGRAMMING, ["sqlite", "wal", "database"]),
    ("上下文管理器使用with语句，__enter__和__exit__方法分别处理资源的获取和释放",
     KnowledgeDomain.PROGRAMMING, KnowledgeDomain.PROGRAMMING, ["context-manager", "python"]),
    ("Type hint在Python 3.5+引入，通过typing模块提供类型检查支持，提升代码可维护性",
     KnowledgeDomain.PROGRAMMING, KnowledgeDomain.PROGRAMMING, ["type-hint", "python", "typing"]),
    ("装饰器是Python的函数式编程特性，通过@语法糖实现AOP功能（日志、缓存、鉴权）",
     KnowledgeDomain.PROGRAMMING, KnowledgeDomain.PROGRAMMING, ["decorator", "python", "aop"]),
    ("元类（Metaclass）是Python中控制类创建的高级特性，type的所有子类都可以作为元类",
     KnowledgeDomain.PROGRAMMING, KnowledgeDomain.PROGRAMMING, ["metaclass", "python", "oop"]),
    ("包管理工具pip使用requirements.txt管理依赖，支持版本锁定和依赖解析",
     KnowledgeDomain.PROGRAMMING, KnowledgeDomain.PROGRAMMING, ["pip", "package", "dependency"]),
    ("Git的rebase和merge是两种合并策略：rebase保持线性历史，merge保留分支拓扑",
     KnowledgeDomain.PROGRAMMING, KnowledgeDomain.PROGRAMMING, ["git", "rebase", "merge"]),

    # 技术领域
    ("OpenClaw的上下文窗口限制在160K tokens左右，超限后会丢失早期对话信息",
     KnowledgeDomain.TECHNOLOGY, KnowledgeDomain.TECHNOLOGY, ["openclaw", "context-window"]),
    ("智能上下文压缩通过识别信息密度，保留核心语义，移除冗余内容，压缩率可达50-70%",
     KnowledgeDomain.TECHNOLOGY, KnowledgeDomain.TECHNOLOGY, ["compression", "context", "optimization"]),
    ("记忆系统通过重要性评分和访问频率进行分层管理，确保关键信息不被遗忘",
     KnowledgeDomain.TECHNOLOGY, KnowledgeDomain.TECHNOLOGY, ["memory", "importance", "forgetting"]),
    ("WebSocket长连接支持全双工通信，适合实时推送场景，比HTTP轮询效率高",
     KnowledgeDomain.TECHNOLOGY, KnowledgeDomain.TECHNOLOGY, ["websocket", "realtime", "communication"]),
    ("Docker容器通过cgroups和namespaces实现资源隔离，比虚拟机更轻量",
     KnowledgeDomain.TECHNOLOGY, KnowledgeDomain.TECHNOLOGY, ["docker", "container", "isolation"]),
    ("代理服务器（Proxy）通过中间层转发请求，可以实现访问控制、缓存和负载均衡",
     KnowledgeDomain.TECHNOLOGY, KnowledgeDomain.TECHNOLOGY, ["proxy", "network", "forward"]),
    ("HTTP/2多路复用允许在单一TCP连接上并行多个请求，解决队头阻塞问题",
     KnowledgeDomain.TECHNOLOGY, KnowledgeDomain.TECHNOLOGY, ["http2", "multiplexing", "protocol"]),
    ("向量数据库通过embedding相似度搜索实现语义级检索，比关键词搜索更准确",
     KnowledgeDomain.TECHNOLOGY, KnowledgeDomain.TECHNOLOGY, ["vector-db", "embedding", "search"]),
]

def seed():
    eng = LearningEngine()
    count = 0
    
    for idx, (content, domain, src_domain, tags) in enumerate(SEED_KNOWLEDGE):
        kp_id = f"seed_kp_{idx:03d}_{hashlib.md5(content.encode()).hexdigest()[:8]}"
        
        kp = KnowledgePoint(
            id=kp_id,
            content=content,
            source=f"seed_knowledge_base_v1/{domain.value}",
            domain=domain,
            confidence=0.85,
            tags=tags,
            verified=True,
            verification_sources=["seed_knowledge_base"],
            verification_count=1,
            usage_count=0,
            relevance_score=0.7,
        )
        
        eng._save_knowledge_point(kp)
        eng.knowledge_base[kp_id] = kp
        count += 1
    
    eng.db_conn.commit()
    print(f"种子知识库已加载: {count} 个知识点")
    
    # 验证
    stats = eng.get_statistics()
    print(f"知识库统计: {stats['total_knowledge_points']} 知识点")
    print(f"领域分布: {stats.get('knowledge_by_domain', {})}")
    
    eng.close()
    return count

if __name__ == "__main__":
    seed()
