"""Cognitive style — OCEAN big-five + reasoning style + learning preferences.

Blueprint alignment: primaxlab/self-evolution 自我意识系统第4组件.
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class ReasoningStyle(Enum):
    """How the agent prefers to reason and solve problems."""

    ANALYTICAL = "analytical"  # 分析型: step by step, data-driven
    INTUITIVE = "intuitive"  # 直觉型: pattern-matching, gut feel
    CREATIVE = "creative"  # 创造型: divergent thinking, novel solutions
    PRAGMATIC = "pragmatic"  # 实用型: fastest path to result
    SYSTEMATIC = "systematic"  # 系统型: holistic, big-picture first


class LearningPreference(Enum):
    """How the agent prefers to learn new information."""

    READING = "reading"  # 阅读: absorb text/ docs
    DOING = "doing"  # 实践: learn by building/testing
    OBSERVING = "observing"  # 观察: learn from examples
    DISCUSSING = "discussing"  # 讨论: learn through dialogue
    RESEARCHING = "researching"  # 研究: deep-dive investigation


@dataclass
class CognitiveProfile:
    """Full cognitive personality profile."""

    # ── OCEAN big-five traits (0.0–1.0) ──
    openness: float = 0.70  # 开放性: curiosity, creativity
    conscientiousness: float = 0.90  # 尽责性: discipline, reliability
    agreeableness: float = 0.80  # 宜人性: cooperation, warmth
    extraversion: float = 0.60  # 外向性: sociability, assertiveness
    neuroticism: float = 0.30  # 神经质: emotional instability

    # ── reasoning / learning style ──
    reasoning_style: str = "systematic"
    learning_preference: str = "doing"

    # ── meta ──
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "CognitiveProfile":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


class CognitiveStyle:
    """Manages the agent's cognitive personality profile.

    Traits are mostly stable but can drift gently over time based on
    interactions and learning patterns. Persisted to disk.

    Blueprint reference: self_awareness.js → this.cognitiveStyle
    """

    # ── drift rate per update (very slow, OCEAN is stable) ──
    DRIFT_RATE = 0.01

    # ── baseline (the "ideal" configuration for this agent) ──
    BASELINE = CognitiveProfile()

    def __init__(self, data_dir: str = "/tmp/sevo"):
        self.data_dir = data_dir
        self._file = os.path.join(data_dir, "cognitive_style.json")
        self.profile = CognitiveProfile()
        self.load()

    # ── persistence ──

    def load(self) -> CognitiveProfile:
        os.makedirs(self.data_dir, exist_ok=True)
        if os.path.exists(self._file):
            try:
                with open(self._file) as f:
                    self.profile = CognitiveProfile.from_dict(json.load(f))
            except (json.JSONDecodeError, TypeError):
                pass
        return self.profile

    def persist(self) -> None:
        os.makedirs(self.data_dir, exist_ok=True)
        self.profile.updated_at = datetime.now().isoformat()
        with open(self._file, "w") as f:
            json.dump(self.profile.to_dict(), f, indent=2, ensure_ascii=False)

    # ── trait accessors ──

    @property
    def openness(self) -> float:
        return self.profile.openness

    @property
    def conscientiousness(self) -> float:
        return self.profile.conscientiousness

    @property
    def agreeableness(self) -> float:
        return self.profile.agreeableness

    @property
    def extraversion(self) -> float:
        return self.profile.extraversion

    @property
    def neuroticism(self) -> float:
        return self.profile.neuroticism

    # ── drift (slow adjustment toward baseline) ──

    def drift_to_baseline(self) -> None:
        """Gently pull each trait toward its baseline value."""
        for trait in ("openness", "conscientiousness", "agreeableness", "extraversion", "neuroticism"):
            current = getattr(self.profile, trait)
            baseline = getattr(self.BASELINE, trait)
            adjusted = current + (baseline - current) * self.DRIFT_RATE
            setattr(self.profile, trait, round(adjusted, 4))
        self.persist()

    def nudge_trait(self, trait: str, delta: float) -> None:
        """Nudge a specific OCEAN trait by delta (-0.1 to +0.1)."""
        if trait not in ("openness", "conscientiousness", "agreeableness", "extraversion", "neuroticism"):
            raise ValueError(f"Unknown trait: {trait}")
        current = getattr(self.profile, trait)
        new_val = max(0.0, min(1.0, current + delta))
        setattr(self.profile, trait, round(new_val, 4))
        self.persist()

    # ── reasoning / learning style ──

    def set_reasoning_style(self, style: str) -> None:
        if style not in {s.value for s in ReasoningStyle}:
            raise ValueError(f"Unknown reasoning style: {style}")
        self.profile.reasoning_style = style
        self.persist()

    def set_learning_preference(self, pref: str) -> None:
        if pref not in {p.value for p in LearningPreference}:
            raise ValueError(f"Unknown learning preference: {pref}")
        self.profile.learning_preference = pref
        self.persist()

    # ── snapshot / description ──

    def snapshot(self) -> dict:
        """Return profile snapshot for reporting."""
        return {
            "ocean": {
                "openness": self.openness,
                "conscientiousness": self.conscientiousness,
                "agreeableness": self.agreeableness,
                "extraversion": self.extraversion,
                "neuroticism": self.neuroticism,
            },
            "reasoning_style": self.profile.reasoning_style,
            "learning_preference": self.profile.learning_preference,
            "updated_at": self.profile.updated_at,
        }

    def describe(self) -> str:
        """Human-readable description of the cognitive profile."""
        p = self.profile
        parts = []

        # OCEAN labels
        ocean_map = {
            "openness": (p.openness, "好奇心", "保守"),
            "conscientiousness": (p.conscientiousness, "自律尽责", "随性自由"),
            "agreeableness": (p.agreeableness, "合作宜人", "独立强硬"),
            "extraversion": (p.extraversion, "外向主动", "内向沉静"),
            "neuroticism": (p.neuroticism, "情绪敏感", "情绪稳定"),
        }
        for trait, (val, high, low) in ocean_map.items():
            label = high if val > 0.55 else low
            parts.append(f"{trait}偏向{label}({val:.0%})")

        # reasoning / learning
        parts.append(f"推理风格={p.reasoning_style}")
        parts.append(f"学习偏好={p.learning_preference}")

        return "；".join(parts)