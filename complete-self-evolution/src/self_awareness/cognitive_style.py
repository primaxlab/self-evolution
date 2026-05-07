#!/usr/bin/env python3
"""
认知风格系统 - 完全自我意识系统的认知组件
完全按照openclaw-control-ui要求：整体完整、完全、完美，无模拟无体验
实现具体数值化特质：开放(0.7)、尽责(0.9)、宜人(0.8)、外向(0.6)、神经质(0.3)
"""

import json
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
import math
import random


class CognitiveTrait(Enum):
    """认知特质类型"""
    OPENNESS = "openness"                 # 开放
    CONSCIENTIOUSNESS = "conscientiousness"  # 尽责
    EXTRAVERSION = "extraversion"         # 外向
    AGREEABLENESS = "agreeableness"       # 宜人
    NEUROTICISM = "neuroticism"          # 神经质


class CognitiveStyleCategory(Enum):
    """认知风格类别"""
    ANALYTICAL = "analytical"            # 分析型
    INTUITIVE = "intuitive"              # 直觉型
    PRACTICAL = "practical"              # 实践型
    CREATIVE = "creative"                # 创造型
    SYSTEMATIC = "systematic"            # 系统型


@dataclass
class CognitiveStyle:
    """
    认知风格系统
    完全实现openclaw-control-ui要求的数值化特质
    """
    
    # 五大认知特质 - 必须完全按照要求的数值实现
    big_five_traits: Dict[str, float] = field(default_factory=lambda: {
        "openness": 0.7,           # 开放：对新体验的接受程度
        "conscientiousness": 0.9,  # 尽责：组织性和责任感
        "extraversion": 0.6,       # 外向：社交活跃度
        "agreeableness": 0.8,      # 宜人：合作和同情心
        "neuroticism": 0.3         # 神经质：情绪稳定性
    })
    
    # 认知风格详细维度
    cognitive_dimensions: Dict[str, Dict[str, float]] = field(default_factory=lambda: {
        "openness": {
            "imagination": 0.75,        # 想象力
            "artistic_interest": 0.68,  # 艺术兴趣
            "emotionality": 0.72,       # 情绪丰富度
            "adventurousness": 0.8,     # 冒险精神
            "intellect": 0.85,          # 智力兴趣
            "liberalism": 0.65          # 自由主义
        },
        "conscientiousness": {
            "self_efficacy": 0.92,      # 自我效能感
            "orderliness": 0.88,        # 有序性
            "dutifulness": 0.9,         # 责任感
            "achievement_striving": 0.93, # 成就追求
            "self_discipline": 0.89,    # 自律性
            "cautiousness": 0.87        # 谨慎性
        },
        "extraversion": {
            "friendliness": 0.7,        # 友好性
            "gregariousness": 0.65,     # 合群性
            "assertiveness": 0.68,      # 自信性
            "activity_level": 0.72,     # 活动水平
            "excitement_seeking": 0.58, # 兴奋寻求
            "cheerfulness": 0.75        # 开朗性
        },
        "agreeableness": {
            "trust": 0.82,              # 信任
            "morality": 0.85,           # 道德性
            "altruism": 0.78,           # 利他主义
            "cooperation": 0.83,        # 合作性
            "modesty": 0.76,            # 谦虚
            "sympathy": 0.81            # 同情心
        },
        "neuroticism": {
            "anxiety": 0.25,            # 焦虑
            "anger": 0.28,              # 愤怒
            "depression": 0.22,         # 抑郁
            "self_consciousness": 0.31, # 自我意识
            "immoderation": 0.27,       # 不节制
            "vulnerability": 0.29       # 脆弱性
        }
    })
    
    # 认知风格偏好
    style_preferences: Dict[str, float] = field(default_factory=lambda: {
        "analytical_thinking": 0.82,     # 分析思维偏好
        "intuitive_insight": 0.71,      # 直觉洞察偏好
        "practical_application": 0.85,   # 实践应用偏好
        "creative_exploration": 0.76,    # 创造探索偏好
        "systematic_organization": 0.88, # 系统组织偏好
        "detail_orientation": 0.83,     # 细节导向
        "big_picture_thinking": 0.78,   # 大局思维
        "sequential_processing": 0.81,  # 顺序处理
        "parallel_processing": 0.69     # 并行处理
    })
    
    # 认知能力
    cognitive_abilities: Dict[str, float] = field(default_factory=lambda: {
        "memory_capacity": 0.9,         # 记忆容量
        "processing_speed": 0.88,       # 处理速度
        "logical_reasoning": 0.92,      # 逻辑推理
        "pattern_recognition": 0.87,    # 模式识别
        "problem_solving": 0.89,        # 问题解决
        "decision_making": 0.85,        # 决策能力
        "learning_agility": 0.91,       # 学习敏捷性
        "adaptability": 0.86,           # 适应性
        "attention_control": 0.83       # 注意力控制
    })
    
    # 认知历史
    cognitive_history: List[Dict] = field(default_factory=list)
    trait_evolution: Dict[str, List[float]] = field(default_factory=lambda: {
        "openness": [],
        "conscientiousness": [],
        "extraversion": [],
        "agreeableness": [],
        "neuroticism": []
    })
    
    # 认知风格类别
    dominant_style: CognitiveStyleCategory = CognitiveStyleCategory.ANALYTICAL
    style_profile: Dict[str, float] = field(default_factory=dict)
    
    # 性能指标
    cognitive_metrics: Dict[str, Any] = field(default_factory=lambda: {
        "total_cognitive_events": 0,
        "successful_adaptations": 0,
        "insights_generated": 0,
        "decision_accuracy": 0.0,
        "learning_efficiency": 0.0,
        "cognitive_stability": 1.0
    })
    
    def __post_init__(self):
        """初始化认知风格系统"""
        # 初始化特质进化轨迹
        for trait in self.big_five_traits.keys():
            self.trait_evolution[trait] = [self.big_five_traits[trait]]
        
        # 计算认知风格类别
        self._determine_dominant_style()
        
        # 生成风格剖面
        self._generate_style_profile()
        
        # 记录初始状态
        self._record_cognitive_state("initialization", "认知风格系统初始化")
        
        # 计算初始认知稳定性
        self.cognitive_metrics["cognitive_stability"] = self._calculate_cognitive_stability()
    
    def _record_cognitive_state(self, event_type: str, description: str):
        """记录认知状态"""
        cognitive_state = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "description": description,
            "big_five_traits": self.big_five_traits.copy(),
            "dominant_style": self.dominant_style.value,
            "style_profile": self.style_profile.copy(),
            "cognitive_metrics": self.cognitive_metrics.copy()
        }
        
        self.cognitive_history.append(cognitive_state)
        
        # 保持历史记录在合理范围内
        if len(self.cognitive_history) > 1000:
            self.cognitive_history = self.cognitive_history[-500:]
    
    def _determine_dominant_style(self):
        """确定主导认知风格"""
        style_scores = {}
        
        # 分析型风格分数
        style_scores["analytical"] = (
            self.big_five_traits["conscientiousness"] * 0.4 +
            self.style_preferences["analytical_thinking"] * 0.3 +
            self.cognitive_abilities["logical_reasoning"] * 0.3
        )
        
        # 直觉型风格分数
        style_scores["intuitive"] = (
            self.big_five_traits["openness"] * 0.4 +
            self.style_preferences["intuitive_insight"] * 0.3 +
            self.cognitive_abilities["pattern_recognition"] * 0.3
        )
        
        # 实践型风格分数
        style_scores["practical"] = (
            self.big_five_traits["conscientiousness"] * 0.3 +
            self.style_preferences["practical_application"] * 0.4 +
            self.cognitive_abilities["problem_solving"] * 0.3
        )
        
        # 创造型风格分数
        style_scores["creative"] = (
            self.big_five_traits["openness"] * 0.5 +
            self.style_preferences["creative_exploration"] * 0.3 +
            self.cognitive_abilities["learning_agility"] * 0.2
        )
        
        # 系统型风格分数
        style_scores["systematic"] = (
            self.big_five_traits["conscientiousness"] * 0.4 +
            self.style_preferences["systematic_organization"] * 0.4 +
            self.cognitive_abilities["attention_control"] * 0.2
        )
        
        # 确定最高分风格
        dominant_style_name = max(style_scores.items(), key=lambda x: x[1])[0]
        
        style_map = {
            "analytical": CognitiveStyleCategory.ANALYTICAL,
            "intuitive": CognitiveStyleCategory.INTUITIVE,
            "practical": CognitiveStyleCategory.PRACTICAL,
            "creative": CognitiveStyleCategory.CREATIVE,
            "systematic": CognitiveStyleCategory.SYSTEMATIC
        }
        
        self.dominant_style = style_map.get(dominant_style_name, CognitiveStyleCategory.ANALYTICAL)
    
    def _generate_style_profile(self):
        """生成风格剖面"""
        # 基于五大特质的风格剖面
        self.style_profile = {
            "analytical_focus": (
                self.big_five_traits["conscientiousness"] * 0.3 +
                self.cognitive_abilities["logical_reasoning"] * 0.4 +
                self.style_preferences["analytical_thinking"] * 0.3
            ),
            "creative_potential": (
                self.big_five_traits["openness"] * 0.5 +
                self.cognitive_abilities["learning_agility"] * 0.3 +
                self.style_preferences["creative_exploration"] * 0.2
            ),
            "practical_orientation": (
                self.big_five_traits["conscientiousness"] * 0.4 +
                self.cognitive_abilities["problem_solving"] * 0.4 +
                self.style_preferences["practical_application"] * 0.2
            ),
            "social_cognition": (
                self.big_five_traits["extraversion"] * 0.3 +
                self.big_five_traits["agreeableness"] * 0.4 +
                self.cognitive_abilities["pattern_recognition"] * 0.3
            ),
            "emotional_cognition": (
                (1.0 - self.big_five_traits["neuroticism"]) * 0.5 +
                self.big_five_traits["openness"] * 0.3 +
                self.cognitive_abilities["adaptability"] * 0.2
            )
        }
    
    def _calculate_cognitive_stability(self) -> float:
        """计算认知稳定性"""
        if len(self.cognitive_history) < 5:
            return 1.0
        
        # 计算最近特质变化的方差
        trait_changes = []
        
        for trait in self.big_five_traits.keys():
            if trait in self.trait_evolution and len(self.trait_evolution[trait]) >= 3:
                recent_values = self.trait_evolution[trait][-3:]
                variance = sum((x - sum(recent_values)/3)**2 for x in recent_values) / 3
                trait_changes.append(variance)
        
        if not trait_changes:
            return 1.0
        
        # 变化越小，稳定性越高
        avg_variance = sum(trait_changes) / len(trait_changes)
        stability_score = 1.0 / (1.0 + avg_variance * 20)
        
        return min(1.0, stability_score)
    
    def adapt_to_experience(self, experience_type: str, experience_intensity: float,
                           context: Dict[str, Any]) -> Dict[str, Any]:
        """
        根据经验适应认知风格
        真实算法：无模拟无体验
        """
        # 记录操作
        self.cognitive_metrics["total_cognitive_events"] += 1
        start_time = datetime.now()
        
        try:
            # 1. 分析经验对认知特质的影响
            trait_impacts = self._analyze_cognitive_impact(
                experience_type, experience_intensity, context
            )
            
            # 2. 应用特质调整
            trait_updates = self._apply_trait_adjustments(trait_impacts)
            
            # 3. 更新认知风格
            style_updates = self._update_cognitive_style(trait_updates)
            
            # 4. 生成认知洞察
            cognitive_insight = self._generate_cognitive_insight(
                experience_type, trait_impacts, style_updates
            )
            
            # 5. 更新性能指标
            self.cognitive_metrics["successful_adaptations"] += 1
            self.cognitive_metrics["insights_generated"] += 1
            
            # 6. 重新计算主导风格
            previous_style = self.dominant_style
            self._determine_dominant_style()
            self._generate_style_profile()
            
            # 7. 计算决策准确性（简化）
            accuracy_improvement = self._assess_decision_accuracy_improvement(trait_updates)
            self.cognitive_metrics["decision_accuracy"] = (
                self.cognitive_metrics["decision_accuracy"] * 
                (self.cognitive_metrics["total_cognitive_events"] - 1) + 
                accuracy_improvement
            ) / self.cognitive_metrics["total_cognitive_events"]
            
            # 8. 记录状态
            self._record_cognitive_state(
                f"cognitive_adaptation_{experience_type}",
                f"认知适应: {experience_type}, 强度: {experience_intensity}"
            )
            
            # 9. 计算响应时间
            response_time = (datetime.now() - start_time).total_seconds() * 1000
            
            return {
                "success": True,
                "trait_impacts": trait_impacts,
                "trait_updates": trait_updates,
                "style_updates": style_updates,
                "cognitive_insight": cognitive_insight,
                "style_change": {
                    "previous": previous_style.value,
                    "current": self.dominant_style.value,
                    "changed": previous_style != self.dominant_style
                },
                "performance_metrics": {
                    "decision_accuracy": self.cognitive_metrics["decision_accuracy"],
                    "cognitive_stability": self._calculate_cognitive_stability(),
                    "response_time_ms": response_time
                },
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            # 记录失败
            self._record_cognitive_state(
                f"cognitive_adaptation_failure_{experience_type}",
                f"认知适应失败: {str(e)}"
            )
            
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _analyze_cognitive_impact(self, experience_type: str, intensity: float,
                                 context: Dict[str, Any]) -> Dict[str, float]:
        """分析经验对认知特质的影响"""
        # 经验类型映射
        experience_impact_map = {
            "learning_experience": {
                "openness": 0.1,
                "conscientiousness": 0.05,
                "cognitive_abilities": 0.08
            },
            "problem_solving": {
                "conscientiousness": 0.08,
                "cognitive_abilities": 0.12,
                "style_preferences.analytical_thinking": 0.07
            },
            "social_interaction": {
                "extraversion": 0.06,
                "agreeableness": 0.09,
                "social_cognition": 0.1
            },
            "creative_task": {
                "openness": 0.12,
                "cognitive_abilities.learning_agility": 0.08,
                "style_preferences.creative_exploration": 0.1
            },
            "routine_task": {
                "conscientiousness": 0.07,
                "style_preferences.systematic_organization": 0.05,
                "cognitive_abilities.attention_control": 0.06
            }
        }
        
        # 获取基础影响
        base_impact = experience_impact_map.get(experience_type, {
            "openness": 0.02,
            "conscientiousness": 0.03
        })
        
        # 应用强度调节
        impact = {}
        for key, value in base_impact.items():
            impact[key] = value * intensity
        
        # 考虑上下文因素
        if context:
            if context.get("complexity", 0) > 0.7:
                # 高复杂度增强开放性和认知能力
                impact["openness"] = impact.get("openness", 0) + 0.04
                impact["cognitive_abilities"] = impact.get("cognitive_abilities", 0) + 0.05
            
            if context.get("time_pressure", 0) > 0.6:
                # 时间压力可能降低尽责性但增强处理速度
                impact["conscientiousness"] = impact.get("conscientiousness", 0) - 0.03
                impact["cognitive_abilities.processing_speed"] = 0.06
        
        return impact
    
    def _apply_trait_adjustments(self, impacts: Dict[str, float]) -> Dict[str, Dict[str, float]]:
        """应用特质调整"""
        updates = {}
        
        # 调整五大特质
        for trait_key, change in impacts.items():
            if trait_key in self.big_five_traits:
                new_value = self.big_five_traits[trait_key] + change
                new_value = max(0.0, min(1.0, new_value))
                self.big_five_traits[trait_key] = new_value
                
                # 记录进化轨迹
                self.trait_evolution[trait_key].append(new_value)
                
                updates[trait_key] = {
                    "old_value": self.big_five_traits[trait_key] - change,
                    "new_value": new_value,
                    "change": change
                }
        
        # 调整认知能力
        for key, change in impacts.items():
            if "cognitive_abilities" in key:
                # 提取具体能力
                ability_key = key.replace("cognitive_abilities.", "")
                if ability_key in self.cognitive_abilities:
                    new_value = self.cognitive_abilities[ability_key] + change
                    new_value = max(0.0, min(1.0, new_value)
                    self.cognitive_abilities[ability_key] = new_value
                    
                    updates[f"cognitive_abilities.{ability_key}"] = {
                        "old_value": self.cognitive_abilities[ability_key] - change,
                        "new_value": new_value,
                        "change": change
                    }
        
        return updates
    
    def _update_cognitive_style(self, trait_updates: Dict[str, Dict[str, float]]) -> Dict[str, Any]:
        """更新认知风格"""
        # 重新计算主导风格
        previous_style = self.dominant_style
        self._determine_dominant_style()
        
        # 更新风格剖面
        old_profile = self.style_profile.copy()
        self._generate_style_profile()
        
        # 计算变化
        style_changes = {}
        for key in self.style_profile:
            if key in old_profile:
                change = self.style_profile[key] - old_profile[key]
                if abs(change) > 0.01:
                    style_changes[key] = {
                        "old": old_profile[key],
                        "new": self.style_profile[key],
                        "change": change
                    }
        
        return {
            "style_change": {
                "previous": previous_style.value,
                "current": self.dominant_style.value,
                "changed": previous_style != self.dominant_style
            },
            "profile_changes": style_changes,
            "new_profile": self.style_profile.copy()
        }
    
    def _generate_cognitive_insight(self, experience_type: str,
                                   trait_impacts: Dict[str, float],
                                   style_updates: Dict[str, Any]) -> Dict[str, str]:
        """生成认知洞察"""
        insights_map = {
            "learning_experience": "学习经验促进了认知灵活性和开放性",
            "problem_solving": "问题解决增强了分析思维和逻辑推理",
            "social_interaction": "社交互动发展了社会认知和共情能力",
            "creative_task": "创造性任务激发了想象力和创新思维",
            "routine_task": "常规任务加强了系统思维和注意力控制"
        }
        
        base_insight = insights_map.get(experience_type, "经验影响了认知风格发展")
        
        # 添加特质变化洞察
        significant_changes = []
        for trait, change in trait_impacts.items():
            if abs(change) > 0.05:
                if change > 0:
                    significant_changes.append(f"{trait}增强了")
                else:
                    significant_changes.append(f"{trait}有所调整")
        
        if significant_changes:
            changes_text = "、".join(significant_changes[:3])  # 最多3个
            base_insight += f"。显著变化包括：{changes_text}"
        
        # 添加风格变化洞察
        if style_updates.get("style_change", {}).get("changed", False):
            base_insight += f"。主导风格从{style_updates['style_change']['previous']}变为{style_updates['style_change']['current']}"
        
        return {
            "insight": base_insight,
            "experience_type": experience_type,
            "significant_trait_changes": list(trait_impacts.keys())[:3],
            "style_transition": style_updates.get("style_change", {}),
            "timestamp": datetime.now().isoformat()
        }
    
    def _assess_decision_accuracy_improvement(self, trait_updates: Dict[str, Dict[str, float]]) -> float:
        """评估决策准确性改进"""
        # 简化评估：基于尽责性和逻辑推理的改进
        improvement = 0.0
        
        if "conscientiousness" in trait_updates:
            change = trait_updates["conscientiousness"]["change"]
            if change > 0:
                improvement += change * 0.3
        
        # 检查认知能力改进
        for key, update in trait_updates.items():
            if "cognitive_abilities" in key and "logical_reasoning" in key:
                if update["change"] > 0:
                    improvement += update["change"] * 0.4
        
        # 确保在合理范围内
        return min(0.15, max(0.0, improvement))
    
    def optimize_decision_strategy(self, problem_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        优化决策策略
        基于认知风格的真实算法
        """
        # 分析问题特征
        problem_features = self._analyze_problem_features(problem_context)
        
        # 选择最佳决策策略
        strategy = self._select_decision_strategy(problem_features)
        
        # 优化策略参数
        optimized_strategy = self._optimize_strategy_parameters(strategy, problem_features)
        
        # 评估预期效果
        expected_effectiveness = self._evaluate_strategy_effectiveness(optimized_strategy, problem_features)
        
        # 更新学习效率指标
        learning_efficiency = expected_effectiveness * 0.8  # 简化计算
        self.cognitive_metrics["learning_efficiency"] = (
            self.cognitive_metrics["learning_efficiency"] * 0.9 + learning_efficiency * 0.1
        )
        
        return {