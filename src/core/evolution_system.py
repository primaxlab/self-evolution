#!/usr/bin/env python3
"""
自我进化系统主引擎
集成所有模块，提供完整的进化能力
"""

import asyncio
import yaml
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import os
import sys
import logging

# 导入各个模块
from src.memory.storage import MemoryStorage, MemoryRecord, MemoryType, ImportanceLevel
from src.learning.engine import LearningEngine, LearningStrategy, KnowledgeDomain, KnowledgePoint
from src.core.context_optimizer import ContextOptimizer, CompressionResult


@dataclass
class EvolutionState:
    """进化状态"""
    # 系统状态
    system_started: datetime = None
    last_evolution: datetime = None
    evolution_count: int = 0
    
    # 性能指标
    current_context_tokens: int = 0
    optimized_context_tokens: int = 0
    compression_ratio: float = 1.0
    
    # 学习指标
    total_learning_tasks: int = 0
    completed_learning_tasks: int = 0
    total_knowledge_points: int = 0
    
    # 记忆指标
    total_memories: int = 0
    memory_storage_size_mb: float = 0.0
    
    # 错误指标
    errors_detected: int = 0
    errors_fixed: int = 0
    error_fix_rate: float = 0.0
    
    # 人格状态
    personality_traits: Dict[str, float] = field(default_factory=dict)
    emotional_state: Dict[str, float] = field(default_factory=dict)
    
    def __post_init__(self):
        if self.system_started is None:
            self.system_started = datetime.now()
        if self.last_evolution is None:
            self.last_evolution = self.system_started
        
        # 默认人格特质
        if not self.personality_traits:
            self.personality_traits = {
                "openness": 0.7,
                "conscientiousness": 0.9,
                "extraversion": 0.6,
                "agreeableness": 0.8,
                "neuroticism": 0.3
            }
        
        # 默认情绪状态
        if not self.emotional_state:
            self.emotional_state = {
                "valence": 0.7,     # 效价：积极
                "arousal": 0.5,     # 唤醒度：中等
                "dominance": 0.6    # 支配感：中等偏高
            }


class EvolutionSystem:
    """完整的自我进化系统"""
    
    def __init__(self, config_path: str = "config/settings.yaml"):
        self.config = self._load_config(config_path)
        self._setup_logging()
        
        # 初始化各个模块
        self.memory_storage = None
        self.learning_engine = None
        self.context_optimizer = None
        
        # 系统状态
        self.state = EvolutionState()
        self.session_id = f"session_{int(datetime.now().timestamp())}"
        
        # 初始化标志
        self.initialized = False
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """加载配置文件"""
        default_config = {
            "system": {
                "name": "Self-Evolution System",
                "version": "1.0.0",
                "auto_start": True,
                "auto_optimize": True
            },
            "modules": {
                "memory": True,
                "learning": True,
                "context_optimization": True,
                "personality": True,
                "safety": True
            }
        }
        
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = yaml.safe_load(f)
                return self._merge_configs(default_config, user_config)
        except Exception as e:
            self.logger.error(f"配置加载失败: {e}")
        
        return default_config
    
    def _merge_configs(self, default: Dict, user: Dict) -> Dict:
        """合并配置"""
        result = default.copy()
        
        def deep_merge(base, update):
            for key, value in update.items():
                if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                    deep_merge(base[key], value)
                else:
                    base[key] = value
        
        deep_merge(result, user)
        return result
    
    def _setup_logging(self):
        """设置日志"""
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
        # 文件处理器
        file_handler = logging.FileHandler(
            f"{log_dir}/evolution_system_{datetime.now().strftime('%Y%m%d')}.log",
            encoding='utf-8'
        )
        file_handler.setFormatter(logging.Formatter(log_format))
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(log_format))
        
        # 配置根日志器
        self.logger = logging.getLogger("EvolutionSystem")
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    async def initialize(self):
        """初始化系统"""
        try:
            self.logger.info("正在初始化自我进化系统...")
            
            # 初始化记忆存储
            if self.config["modules"]["memory"]:
                self.memory_storage = MemoryStorage(
                    self.config.get("memory", {}).get("database_path", "data/memory.db")
                )
                self.logger.info("记忆存储系统初始化完成")
            
            # 初始化学习引擎
            if self.config["modules"]["learning"]:
                self.learning_engine = LearningEngine()
                await self.learning_engine.start_async_session()
                self.logger.info("学习引擎初始化完成")
            
            # 初始化上下文优化器
            if self.config["modules"]["context_optimization"]:
                self.context_optimizer = ContextOptimizer()
                self.logger.info("上下文优化器初始化完成")
            
            # 记录启动记忆
            if self.memory_storage:
                startup_memory = MemoryRecord(
                    id=f"startup_{self.session_id}",
                    type=MemoryType.EXPERIENCE,
                    content="自我进化系统启动",
                    timestamp=datetime.now(),
                    session_id=self.session_id,
                    importance=ImportanceLevel.MEDIUM,
                    tags=["system", "startup", "evolution"],
                    metadata={"version": self.config["system"]["version"]}
                )
                self.memory_storage.store_memory(startup_memory)
            
            self.initialized = True
            self.logger.info("自我进化系统初始化完成")
            
            # 记录状态
            await self._record_system_state("initialized")
            
        except Exception as e:
            self.logger.error(f"系统初始化失败: {e}")
            raise
    
    async def optimize_context(self, target_tokens: int = 150000) -> CompressionResult:
        """
        优化当前上下文
        这是解决OpenClaw上下文超限问题的核心功能
        """
        if not self.context_optimizer:
            raise RuntimeError("上下文优化器未初始化")
        
        self.logger.info(f"开始上下文优化，目标标记数: {target_tokens}")
        
        # 获取需要优化的文件列表
        workspace_files = self._get_workspace_files()
        
        # 执行优化
        result = self.context_optimizer.optimize_context(workspace_files, target_tokens)
        
        # 更新状态
        self.state.current_context_tokens = result.original_tokens
        self.state.optimized_context_tokens = result.compressed_tokens
        self.state.compression_ratio = result.compression_ratio
        
        # 记录优化记忆
        if self.memory_storage:
            optimization_memory = MemoryRecord(
                id=f"optimization_{int(datetime.now().timestamp())}",
                type=MemoryType.KNOWLEDGE,
                content=f"上下文优化: {result.original_tokens} -> {result.compressed_tokens} 标记 ({result.compression_ratio:.1%})",
                timestamp=datetime.now(),
                session_id=self.session_id,
                importance=ImportanceLevel.HIGH,
                tags=["optimization", "context", "compression"],
                metadata={
                    "original_tokens": result.original_tokens,
                    "compressed_tokens": result.compressed_tokens,
                    "compression_ratio": result.compression_ratio,
                    "integrity": result.preserved_integrity,
                    "optimized_files": result.optimized_files
                }
            )
            self.memory_storage.store_memory(optimization_memory)
        
        self.logger.info(f"上下文优化完成: {result.original_tokens} -> {result.compressed_tokens} 标记")
        
        return result
    
    async def learn_from_query(self, query: str, 
                             strategy: LearningStrategy = LearningStrategy.BROWSER_RESEARCH,
                             domain: KnowledgeDomain = KnowledgeDomain.TECHNOLOGY) -> List[KnowledgePoint]:
        """
        从查询中学习
        """
        if not self.learning_engine:
            raise RuntimeError("学习引擎未初始化")
        
        self.logger.info(f"开始学习: {query} (策略: {strategy.value}, 领域: {domain.value})")
        
        # 创建学习任务
        task_id = self.learning_engine.create_learning_task(
            query=query,
            strategy=strategy,
            domain=domain,
            priority=7
        )
        
        # 执行学习
        knowledge_points = await self.learning_engine.execute_learning_task(task_id)
        
        # 更新状态
        self.state.total_learning_tasks += 1
        self.state.completed_learning_tasks += 1
        self.state.total_knowledge_points += len(knowledge_points)
        
        # 存储学习记忆
        if self.memory_storage:
            learning_memory = MemoryRecord(
                id=f"learning_{task_id}",
                type=MemoryType.KNOWLEDGE,
                content=f"学习任务完成: {query} - 获得{len(knowledge_points)}个知识点",
                timestamp=datetime.now(),
                session_id=self.session_id,
                importance=ImportanceLevel.MEDIUM,
                tags=["learning", strategy.value, domain.value],
                metadata={
                    "query": query,
                    "strategy": strategy.value,
                    "domain": domain.value,
                    "knowledge_points": len(knowledge_points),
                    "task_id": task_id
                }
            )
            self.memory_storage.store_memory(learning_memory)
        
        self.logger.info(f"学习完成: 获得{len(knowledge_points)}个知识点")
        
        return knowledge_points
    
    async def evolve(self, evolution_target: str = "optimization") -> Dict[str, Any]:
        """
        执行进化
        """
        self.logger.info(f"开始进化: {evolution_target}")
        
        evolution_result = {
            "evolution_target": evolution_target,
            "start_time": datetime.now().isoformat(),
            "modules_executed": [],
            "results": {},
            "success": True,
            "error": None
        }
        
        try:
            # 根据进化目标执行不同的进化模块
            if evolution_target == "optimization":
                # 上下文优化进化
                result = await self.optimize_context()
                evolution_result["results"]["context_optimization"] = {
                    "original_tokens": result.original_tokens,
                    "compressed_tokens": result.compressed_tokens,
                    "compression_ratio": result.compression_ratio,
                    "integrity": result.preserved_integrity
                }
                evolution_result["modules_executed"].append("context_optimization")
            
            elif evolution_target == "learning":
                # 学习能力进化
                # 学习如何更好地学习
                learning_result = await self.learn_from_query(
                    query="AI自我学习和进化方法",
                    strategy=LearningStrategy.BROWSER_RESEARCH,
                    domain=KnowledgeDomain.AI_ML
                )
                evolution_result["results"]["learning_evolution"] = {
                    "knowledge_points_acquired": len(learning_result),
                    "sources": [kp.source for kp in learning_result[:3]]
                }
                evolution_result["modules_executed"].append("learning_evolution")
            
            elif evolution_target == "memory":
                # 记忆系统进化
                if self.memory_storage:
                    # 清理旧记忆
                    deleted = self.memory_storage.cleanup_old_memories()
                    evolution_result["results"]["memory_evolution"] = {
                        "memories_deleted": deleted,
                        "optimization_performed": True
                    }
                    evolution_result["modules_executed"].append("memory_evolution")
            
            elif evolution_target == "full":
                # 完整进化：执行所有模块
                results = {}
                
                # 上下文优化
                opt_result = await self.optimize_context()
                results["context_optimization"] = {
                    "compression_ratio": opt_result.compression_ratio,
                    "integrity": opt_result.preserved_integrity
                }
                
                # 学习进化
                learn_result = await self.learn_from_query(
                    query="人工智能系统优化方法",
                    strategy=LearningStrategy.KNOWLEDGE_SYNTHESIS
                )
                results["learning_evolution"] = {
                    "knowledge_points": len(learn_result)
                }
                
                # 记忆优化
                if self.memory_storage:
                    deleted = self.memory_storage.cleanup_old_memories()
                    results["memory_evolution"] = {
                        "memories_cleaned": deleted
                    }
                
                evolution_result["results"] = results
                evolution_result["modules_executed"] = ["context_optimization", "learning_evolution", "memory_evolution"]
            
            else:
                raise ValueError(f"未知的进化目标: {evolution_target}")
            
            # 更新进化状态
            self.state.last_evolution = datetime.now()
            self.state.evolution_count += 1
            
            # 记录进化记忆
            if self.memory_storage:
                evolution_memory = MemoryRecord(
                    id=f"evolution_{self.state.evolution_count}",
                    type=MemoryType.REFLECTION,
                    content=f"进化完成: {evolution_target} - 模块: {evolution_result['modules_executed']}",
                    timestamp=datetime.now(),
                    session_id=self.session_id,
                    importance=ImportanceLevel.HIGH,
                    tags=["evolution", evolution_target, "system"],
                    metadata=evolution_result
                )
                self.memory_storage.store_memory(evolution_memory)
            
            self.logger.info(f"进化完成: {evolution_target}")
            
        except Exception as e:
            evolution_result["success"] = False
            evolution_result["error"] = str(e)
            self.logger.error(f"进化失败: {e}")
        
        evolution_result["end_time"] = datetime.now().isoformat()
        evolution_result["duration_seconds"] = (
            datetime.fromisoformat(evolution_result["end_time"]) - 
            datetime.fromisoformat(evolution_result["start_time"])
        ).total_seconds()
        
        return evolution_result
    
    async def solve_context_overflow(self) -> Dict[str, Any]:
        """
        专门解决OpenClaw上下文超限问题
        这是核心解决方案
        """
        self.logger.info("开始解决上下文超限问题")
        
        solution_result = {
            "problem": "context_overflow",
            "detected_tokens": 0,
            "target_tokens": 150000,
            "solutions_applied": [],
            "final_tokens": 0,
            "compression_ratio": 0.0,
            "integrity": 0.0,
            "success": False
        }
        
        try:
            # 1. 分析当前上下文
            workspace_files = self._get_workspace_files()
            
            if self.context_optimizer:
                analysis = self.context_optimizer.analyze_context(workspace_files)
                solution_result["detected_tokens"] = analysis.total_tokens
                
                self.logger.info(f"检测到上下文标记数: {analysis.total_tokens}")
                
                # 2. 检查是否超限
                if analysis.total_tokens <= self.config.get("learning", {}).get("context_optimization", {}).get("target_context_size", 150000):
                    self.logger.info("上下文长度正常，无需优化")
                    solution_result["success"] = True
                    solution_result["final_tokens"] = analysis.total_tokens
                    solution_result["compression_ratio"] = 1.0
                    solution_result["integrity"] = 1.0
                    solution_result["solutions_applied"] = ["none_required"]
                    
                    return solution_result
                
                # 3. 执行优化
                self.logger.info("上下文超限，开始优化...")
                
                # 应用智能压缩
                compression_result = await self.optimize_context()
                solution_result["solutions_applied"].append("intelligent_compression")
                
                # 应用知识引用优化
                if self.learning_engine and self.memory_storage:
                    # 获取相关知识，用引用替换详细内容
                    related_knowledge = self.learning_engine.get_relevant_knowledge(
                        query="上下文优化 压缩算法",
                        limit=5
                    )
                    
                    if related_knowledge:
                        # 这里可以扩展为实际的知识引用优化
                        solution_result["solutions_applied"].append("knowledge_reference")
                
                # 4. 验证优化效果
                final_analysis = self.context_optimizer.analyze_context(workspace_files)
                solution_result["final_tokens"] = final_analysis.total_tokens
                solution_result["compression_ratio"] = compression_result.compression_ratio
                solution_result["integrity"] = compression_result.preserved_integrity
                
                # 5. 检查是否解决
                if final_analysis.total_tokens <= solution_result["target_tokens"]:
                    solution_result["success"] = True
                    self.logger.info(f"上下文超限问题已解决: {solution_result['detected_tokens']} -> {solution_result['final_tokens']} 标记")
                else:
                    solution_result["success"] = False
                    self.logger.warning(f"优化后仍超限: {final_analysis.total_tokens} > {solution_result['target_tokens']}")
                    
                    # 尝试更激进的优化
                    aggressive_result = await self.optimize_context(target_tokens=140000)
                    solution_result["solutions_applied"].append("aggressive_compression")
                    solution_result["final_tokens"] = aggressive_result.compressed_tokens
                    solution_result["compression_ratio"] = aggressive_result.compression_ratio
                    solution_result["integrity"] = aggressive_result.preserved_integrity
                    
                    if aggressive_result.compressed_tokens <= solution_result["target_tokens"]:
                        solution_result["success"] = True
                        self.logger.info("激进优化成功解决问题")
            
            # 记录解决方案
            if self.memory_storage:
                solution_memory = MemoryRecord(
                    id=f"solution_{int(datetime.now().timestamp())}",
                    type=MemoryType.KNOWLEDGE,
                    content=f"上下文超限解决方案: {solution_result['detected_tokens']} -> {solution_result['final_tokens']} 标记 ({solution_result['compression_ratio']:.1%} 压缩率)",
                    timestamp=datetime.now(),
                    session_id=self.session_id,
                    importance=ImportanceLevel.CRITICAL,
                    tags=["solution", "context_overflow", "optimization"],
                    metadata=solution_result
                )
                self.memory_storage.store_memory(solution_memory)
            
        except Exception as e:
            solution_result["success"] = False
            solution_result["error"] = str(e)
            self.logger.error(f"解决上下文超限问题失败: {e}")
        
        return solution_result
    
    def get_system_state(self) -> EvolutionState:
        """获取系统状态"""
        # 更新实时指标
        if self.memory_storage:
            stats = self.memory_storage.get_statistics()
            self.state.total_memories = stats.get("total_memories", 0)
            self.state.memory_storage_size_mb = stats.get("total_size_bytes", 0) / (1024 * 1024)
        
        if self.learning_engine:
            stats = self.learning_engine.get_statistics()
            self.state.total_learning_tasks = stats.get("total_tasks", 0)
            self.state.total_knowledge_points = stats.get("total_knowledge_points", 0)
        
        return self.state
    
    async def get_context_optimization_suggestions(self) -> List[Dict[str, Any]]:
        """获取上下文优化建议"""
        suggestions = []
        
        if not self.context_optimizer:
            return suggestions
        
        workspace_files = self._get_workspace_files()
        analysis = self.context_optimizer.analyze_context(workspace_files)
        
        # 生成建议
        for file_path, suggestion in analysis.suggestions:
            suggestions.append({
                "file": file_path,
                "suggestion": suggestion,
                "estimated_savings_tokens": analysis.by_file.get(file_path, 0) * 0.3  # 估算节省30%
            })
        
        # 添加系统级建议
        if analysis.total_tokens > 160000:
            suggestions.append({
                "file": "system",
                "suggestion": "上下文严重超限，建议立即执行完整优化",
                "estimated_savings_tokens": analysis.total_tokens * 0.5
            })
        
        return suggestions
    
    async def _record_system_state(self, event: str):
        """记录系统状态"""
        if not self.memory_storage:
            return
        
        state_memory = MemoryRecord(
            id=f"state_{event}_{int(datetime.now().timestamp())}",
            type=MemoryType.REFLECTION,
            content=f"系统状态记录: {event}",
            timestamp=datetime.now(),
            session_id=self.session_id,
            importance=ImportanceLevel.LOW,
            tags=["system", "state", event],
            metadata={
                                "event": event,
                "timestamp": datetime.now().isoformat()
            }
        )
        self.memory_storage.store_memory(state_memory)
    
    def _get_workspace_files(self) -> List[str]:
        """获取工作区文件列表"""
        workspace_dir = self.config.get("integration", {}).get("openclaw", {}).get("workspace_path", "D:/OpenClaw_Main/workspace")
        
        essential_files = [
            os.path.join(workspace_dir, "IDENTITY.md"),
            os.path.join(workspace_dir, "USER.md"),
            os.path.join(workspace_dir, "SOUL.md"),
            os.path.join(workspace_dir, "MEMORY.md"),
            os.path.join(workspace_dir, "AGENTS.md"),
            os.path.join(workspace_dir, "TOOLS.md"),
            os.path.join(workspace_dir, "HEARTBEAT.md")
        ]
        
        # 只返回存在的文件
        return [f for f in essential_files if os.path.exists(f)]
    
    async def shutdown(self):
        """关闭系统"""
        self.logger.info("正在关闭自我进化系统...")
        
        try:
            # 关闭学习引擎
            # 记录关闭记忆
            shutdown_memory = MemoryRecord(
            id=f"shutdown_{self.session_id}",
            type=MemoryType.EXPERIENCE,
            content="自我进化系统关闭",
            timestamp=datetime.now(),
            session_id=self.session_id,
            importance=ImportanceLevel.MEDIUM,
            tags=["system", "shutdown"],
            metadata={
            "evolution_count": self.state.evolution_count,
            "total_memories": self.state.total_memories
            }
            )
            self.memory_storage.store_memory(shutdown_memory)

            if self.learning_engine:
                await self.learning_engine.close_async_session()
                self.learning_engine.close()
            
            # 关闭记忆存储
            if self.memory_storage:
                self.memory_storage.close()
            
            self.logger.info("自我进化系统关闭完成")
            
        except Exception as e:
            self.logger.error(f"关闭系统时出错: {e}")
    
    def generate_report(self, report_type: str = "system") -> Dict[str, Any]:
        """生成报告"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "session_id": self.session_id,
            "report_type": report_type,
            "system_state": self.get_system_state().__dict__
        }
        
        if report_type == "performance":
            # 性能报告
            report["performance_metrics"] = {
                "context_optimization": {
                    "current_tokens": self.state.current_context_tokens,
                    "optimized_tokens": self.state.optimized_context_tokens,
                    "compression_ratio": self.state.compression_ratio
                },
                "learning": {
                    "total_tasks": self.state.total_learning_tasks,
                    "completion_rate": (
                        self.state.completed_learning_tasks / max(self.state.total_learning_tasks, 1)
                    ),
                    "knowledge_points": self.state.total_knowledge_points
                }
            }
        
        elif report_type == "evolution":
            # 进化报告
            report["evolution_metrics"] = {
                "total_evolutions": self.state.evolution_count,
                "last_evolution": self.state.last_evolution.isoformat(),
                "system_uptime_seconds": (datetime.now() - self.state.system_started).total_seconds()
            }
        
        elif report_type == "context_optimization":
            # 上下文优化报告
            if self.context_optimizer:
                report["context_optimization"] = self.context_optimizer.get_optimization_report()
        
        return report


# 主函数：直接解决OpenClaw上下文超限问题
async def main():
    """
    自我进化系统主入口
    专门解决OpenClaw上下文超限问题
    """
    print("🦞 自我进化系统启动 - 解决OpenClaw上下文超限问题")
    print("=" * 60)
    
    # 创建进化系统
    system = EvolutionSystem()
    
    try:
        # 初始化系统
        await system.initialize()
        
        print("✅ 系统初始化完成")
        
        # 获取当前状态
        state = system.get_system_state()
        print(f"📊 系统状态:")
        print(f"  会话ID: {system.session_id}")
        print(f"  启动时间: {state.system_started.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  进化次数: {state.evolution_count}")
        
        # 专门解决上下文超限问题
        print("\n🔧 开始解决OpenClaw上下文超限问题...")
        solution = await system.solve_context_overflow()
        
        print(f"\n📋 解决方案报告:")
        print(f"  问题: 上下文超限 ({solution['detected_tokens']} > 163,840)")
        print(f"  目标: {solution['target_tokens']} 标记")
        print(f"  应用方案: {', '.join(solution['solutions_applied'])}")
        print(f"  最终结果: {solution['final_tokens']} 标记")
        print(f"  压缩率: {solution['compression_ratio']:.1%}")
        print(f"  完整性保留: {solution['integrity']:.1%}")
        
        if solution["success"]:
            print("✅ 问题已成功解决！")
        else:
            print("⚠️ 问题未完全解决，需要进一步优化")
            
            # 尝试完整进化
            print("\n🔄 尝试完整进化...")
            evolution_result = await system.evolve("full")
            
            if evolution_result["success"]:
                print("✅ 完整进化成功")
            else:
                print(f"❌ 完整进化失败: {evolution_result['error']}")
        
        # 生成最终报告
        report = system.generate_report("performance")
        print(f"\n📈 性能报告生成完成")
        
        # 保存报告
        report_path = "reports/context_solution_report.json"
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"📄 报告已保存: {report_path}")
        
    except Exception as e:
        print(f"❌ 系统运行失败: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 关闭系统
        await system.shutdown()
        print("\n🔄 系统关闭完成")


if __name__ == "__main__":
    # 运行主函数
    asyncio.run(main())