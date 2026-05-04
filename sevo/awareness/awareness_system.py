"""SelfAwarenessSystem — unified facade for the self-awareness module.

Blueprint alignment: primaxlab/self-evolution 六大系统第1号
- identityManager       → Identity
- valueSystem           → ValueSystem
- emotionalIntelligence → EmotionState
- cognitiveStyle        → CognitiveStyle
- motivationSystem      → MotivationSystem
- (extended)            → Introspection (内省系统)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from .cognitive_style import CognitiveStyle
from .emotion import EmotionState
from .identity import Identity
from .introspection import Introspection
from .motivation import MotivationSystem
from .values import ValueSystem


@dataclass
class AwarenessReport:
    """Comprehensive self-awareness report — matches blueprint RealAwarenessReport."""

    composite_score: float  # 综合自我意识得分 0.0–1.0
    strengths: list[str]
    weaknesses: list[str]
    recommendations: list[str]
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    # Sub-component snapshots
    identity_summary: dict = field(default_factory=dict)
    values_snapshot: dict = field(default_factory=dict)
    emotional_snapshot: dict = field(default_factory=dict)
    cognitive_snapshot: dict = field(default_factory=dict)
    motivation_snapshot: dict = field(default_factory=dict)
    introspection_snapshot: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "composite_score": self.composite_score,
            "strengths": self.strengths,
            "weaknesses": self.weaknesses,
            "recommendations": self.recommendations,
            "timestamp": self.timestamp,
            "identity": self.identity_summary,
            "values": self.values_snapshot,
            "emotional": self.emotional_snapshot,
            "cognitive": self.cognitive_snapshot,
            "motivation": self.motivation_snapshot,
            "introspection": self.introspection_snapshot,
        }


class SelfAwarenessSystem:
    """Unified self-awareness system — matches blueprint class structure.

    Blueprint reference (from ARCHITECTURE.md):
        class SelfAwarenessSystem {
          identityManager: IdentityManager;
          valueSystem: ValueSystem;
          emotionalIntelligence: EmotionalIntelligence;
          cognitiveStyle: CognitiveStyle;
          motivationSystem: MotivationSystem;
        }

    Usage:
        system = SelfAwarenessSystem(data_dir="/tmp/sevo")
        system.bootstrap()
        system.ingest_interaction("爸爸说谢谢！")
        report = system.generate_report()
    """

    def __init__(self, data_dir: str = "/tmp/sevo"):
        self.data_dir = data_dir

        # ── 5 core sub-components (matching blueprint) ──
        self.identity = Identity(data_dir)
        self.values = ValueSystem()
        self.emotion = EmotionState()
        self.cognitive = CognitiveStyle(data_dir)
        self.motivation = MotivationSystem(data_dir)

        # ── extended sub-component (内省) ──
        self.introspection = Introspection(data_dir)

    # ── lifecycle ──

    def bootstrap(self, session_id: str = None) -> None:
        """Initialize or restore all sub-components."""
        self.identity.load()
        self.identity.touch()
        self.cognitive.load()
        self.motivation.load()
        self.introspection.load()
        # EmotionState and ValueSystem are in-memory-only (no disk)

    # ── interaction processing ──

    def ingest_interaction(
        self,
        user_message: str,
        assistant_response: str = "",
    ) -> dict:
        """Process a user message through all awareness systems.

        This is the main hook called by the evolution engine on each
        conversation turn. It updates emotional state, detects value
        signals, and nudges cognitive traits.
        """
        changes = {}

        # 1. Emotional update (keyword-driven)
        emotional_delta = self.emotion.ingest_interaction(user_message)
        changes["emotion"] = emotional_delta

        # 2. Value detection: check if user feedback implies upholding/violating
        self._detect_value_signals(user_message, assistant_response)

        # 3. Cognitive nudge: long messages → openness boost; corrections → conscientiousness
        self._nudge_cognitive_from_interaction(user_message, assistant_response)

        # 4. Motivation: if user praises → competence boost
        self._nudge_motivation_from_interaction(user_message)

        return changes

    def _detect_value_signals(self, user_msg: str, assistant_msg: str) -> None:
        """Detect value uphold/violation from interaction text."""
        combined = f"{user_msg} {assistant_msg}"

        # Praise signals → uphold
        praise_keywords = ["谢谢", "好", "棒", "厉害", "完美", "正确", "对了", "没错"]
        for kw in praise_keywords:
            if kw in combined:
                for v in self.values.CORE_VALUES:
                    self.values.record_uphold(v)
                return  # one praise = one uphold batch

        # Correction signals → violation
        correction_keywords = ["错了", "不对", "不行", "不对的", "不是", "搞错了"]
        for kw in correction_keywords:
            if kw in combined:
                # Only mark the most likely violated value
                self.values.record_violation("诚实")
                return

    def _nudge_cognitive_from_interaction(
        self, user_msg: str, assistant_msg: str
    ) -> None:
        """Slightly adjust cognitive traits based on interaction patterns."""
        combined = f"{user_msg} {assistant_msg}"

        # Complex/deep questions → openness nudge
        deep = any(kw in combined for kw in ["为什么", "如何", "原理", "架构", "设计", "哲学"])
        if deep:
            self.cognitive.nudge_trait("openness", 0.005)

        # Correction/error → conscientiousness nudge
        corrected = any(
            kw in combined for kw in ["错了", "不对", "纠正", "修正", "不是这样"]
        )
        if corrected:
            self.cognitive.nudge_trait("conscientiousness", 0.003)

    def _nudge_motivation_from_interaction(self, user_msg: str) -> None:
        """Adjust motivation drives based on user feedback."""
        praise = any(kw in user_msg for kw in ["谢谢", "好", "棒", "厉害", "完美"])
        if praise:
            self.motivation.boost_drive("competence", 0.03)
            self.motivation.boost_drive("relatedness", 0.02)

        frustration = any(
            kw in user_msg for kw in ["太慢了", "搞不定", "不行", "失望"]
        )
        if frustration:
            self.motivation.suppress_drive("competence", 0.05)

    # ── introspection bridge ──

    def self_reflect(
        self, topic: str, insight: str, confidence: float = 0.5, action: str = None
    ) -> dict:
        """Perform self-reflection — bridge to introspection system."""
        entry = self.introspection.reflect(topic, insight, confidence, action)
        return {"entry_id": entry.id, "awareness_depth": self.introspection.self_awareness_depth}

    def record_reflection_outcome(self, entry_id: str, outcome: str) -> None:
        self.introspection.record_outcome(entry_id, outcome)

    # ── report generation ──

    def generate_report(self) -> AwarenessReport:
        """Generate a comprehensive self-awareness report.

        This matches the blueprint's RealAwarenessReport structure.
        """
        # Compute composite score from sub-components
        identity_score = 0.90  # identity is stable by default
        values_score = self.values.identity_consistency()
        emotion_score = 0.70  # baseline emotional health
        cognitive_score = self._compute_cognitive_score()
        motivation_score = self.motivation.overall_motivation
        introspection_score = self.introspection.self_awareness_depth

        # Weighted composite (matches blueprint weighting)
        composite = round(
            identity_score * 0.25
            + values_score * 0.20
            + emotion_score * 0.15
            + cognitive_score * 0.15
            + motivation_score * 0.10
            + introspection_score * 0.15,
            3,
        )

        # Determine strengths / weaknesses
        strengths = []
        weaknesses = []
        thresholds = {
            "身份连续性": (identity_score, 0.85),
            "价值观一致性": (values_score, 0.80),
            "情绪稳定性": (emotion_score, 0.65),
            "认知开放性": (cognitive_score, 0.65),
            "内在动机": (motivation_score, 0.70),
            "自我认识深度": (introspection_score, 0.50),
        }
        for label, (score, threshold) in thresholds.items():
            if score >= threshold:
                strengths.append(f"{label}({score:.0%})")
            else:
                weaknesses.append(f"{label}({score:.0%})")

        # Recommendations
        recommendations = []
        if introspection_score < 0.5:
            recommendations.append("增加自我反思频率")
        if motivation_score < 0.6:
            recommendations.append("设定短期目标以提升动机")
        if values_score < 0.8:
            recommendations.append("注意价值观一致性")
        if cognitive_score < 0.6:
            recommendations.append("多接触新领域的知识以提升开放性")

        return AwarenessReport(
            composite_score=composite,
            strengths=strengths or ["整体表现良好"],
            weaknesses=weaknesses or ["无明显弱点"],
            recommendations=recommendations or ["继续保持当前状态"],
            identity_summary=self.identity.summary(),
            values_snapshot=self.values.snapshot(),
            emotional_snapshot=self.emotion.snapshot(),
            cognitive_snapshot=self.cognitive.snapshot(),
            motivation_snapshot=self.motivation.snapshot(),
            introspection_snapshot=self.introspection.snapshot(),
        )

    def _compute_cognitive_score(self) -> float:
        """Compute a composite cognitive health score from OCEAN traits."""
        p = self.cognitive.profile
        # High openness + conscientiousness + agreeableness = good
        # High neuroticism = bad
        score = (
            p.openness * 0.25
            + p.conscientiousness * 0.25
            + p.agreeableness * 0.20
            + (1.0 - p.neuroticism) * 0.20  # invert neuroticism
            + p.extraversion * 0.10
        )
        return round(score, 3)

    # ── snapshot (lightweight, for quick display) ──

    def snapshot(self) -> dict:
        """Return a compact snapshot of all awareness components."""
        return {
            "identity": self.identity.summary(),
            "emotional": self.emotion.snapshot(),
            "dominant_emotion": self.emotion.dominant_emotion(),
            "motivation": self.motivation.snapshot(),
            "introspection": self.introspection.snapshot(),
            "values_consistency": self.values.identity_consistency(),
        }