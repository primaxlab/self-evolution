"""Introspection system — self-reflection + self-regulation + growth tracking.

Blueprint alignment: primaxlab/self-evolution 自我意识系统
- 内省调节系统
- 自我认识深度
- 自我调控精度
- 自我完善机制
- 认识水平提升
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class IntrospectionEntry:
    """A single introspection / self-reflection record."""

    id: str
    topic: str  # what was reflected on
    insight: str  # what was learned
    confidence: float = 0.5  # how confident (0–1)
    action_taken: Optional[str] = None  # what was done about it
    outcome: Optional[str] = None  # what happened as a result
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        return asdict(self)


class Introspection:
    """Agent's ability to reflect on its own thoughts, behaviors, and growth.

    This is the "thinking about thinking" system. It records introspection
    entries, tracks self-awareness depth, and self-regulates by comparing
    actual behavior against internal standards.

    Blueprint reference:
      - awareness_system → introspection / self-regulation
      - "内省调节系统" + "自我认识深度" + "自我调控精度"
    """

    def __init__(self, data_dir: str = "/tmp/sevo"):
        self.data_dir = data_dir
        self._file = os.path.join(data_dir, "introspection.json")

        # All introspection entries
        self.entries: list[IntrospectionEntry] = []

        # Self-awareness depth (grows with introspection)
        self.self_awareness_depth: float = 0.30

        # Self-regulation precision (grows with practice)
        self.self_regulation_precision: float = 0.30

        # How many times we've introspected
        self.total_introspections = 0

        self.load()

    # ── persistence ──

    def load(self) -> None:
        os.makedirs(self.data_dir, exist_ok=True)
        if os.path.exists(self._file):
            try:
                with open(self._file) as f:
                    data = json.load(f)
                self.entries = [
                    IntrospectionEntry(**e) for e in data.get("entries", [])
                ]
                self.self_awareness_depth = data.get("self_awareness_depth", 0.30)
                self.self_regulation_precision = data.get(
                    "self_regulation_precision", 0.30
                )
                self.total_introspections = data.get("total_introspections", 0)
            except (json.JSONDecodeError, TypeError):
                pass

    def persist(self) -> None:
        os.makedirs(self.data_dir, exist_ok=True)
        with open(self._file, "w") as f:
            json.dump(
                {
                    "entries": [e.to_dict() for e in self.entries],
                    "self_awareness_depth": self.self_awareness_depth,
                    "self_regulation_precision": self.self_regulation_precision,
                    "total_introspections": self.total_introspections,
                },
                f,
                indent=2,
                ensure_ascii=False,
            )

    # ── introspection operations ──

    def reflect(
        self,
        topic: str,
        insight: str,
        confidence: float = 0.5,
        action_taken: str = None,
    ) -> IntrospectionEntry:
        """Record a new introspection entry.

        Each reflection slightly deepens self-awareness and improves
        self-regulation precision.
        """
        import uuid

        entry = IntrospectionEntry(
            id=f"intro-{uuid.uuid4().hex[:8]}",
            topic=topic,
            insight=insight,
            confidence=confidence,
            action_taken=action_taken,
        )
        self.entries.append(entry)
        self.total_introspections += 1

        # Growth: each introspection deepens awareness (diminishing returns)
        self.self_awareness_depth = min(
            1.0,
            self.self_awareness_depth + 0.02 * (1.0 - self.self_awareness_depth),
        )

        # If action was taken, regulation precision improves more
        if action_taken:
            self.self_regulation_precision = min(
                1.0,
                self.self_regulation_precision
                + 0.03 * (1.0 - self.self_regulation_precision),
            )
        else:
            self.self_regulation_precision = min(
                1.0,
                self.self_regulation_precision
                + 0.01 * (1.0 - self.self_regulation_precision),
            )

        self.persist()
        return entry

    def record_outcome(self, entry_id: str, outcome: str) -> None:
        """Close the feedback loop: what happened after the action."""
        for entry in self.entries:
            if entry.id == entry_id:
                entry.outcome = outcome
                # Positive outcomes boost precision
                positive = any(
                    kw in outcome
                    for kw in ["成功", "有效", "好了", "work", "improved", "better"]
                )
                if positive:
                    self.self_regulation_precision = min(
                        1.0, self.self_regulation_precision + 0.02
                    )
                self.persist()
                return

    # ── queries ──

    def recent_insights(self, limit: int = 5) -> list[dict]:
        """Return the most recent introspection insights."""
        return [
            {
                "topic": e.topic,
                "insight": e.insight,
                "confidence": e.confidence,
                "action": e.action_taken,
                "outcome": e.outcome,
            }
            for e in self.entries[-limit:]
        ]

    def self_improvement_rate(self) -> float:
        """Rate of self-improvement: (entries with action + outcome) / total."""
        if self.total_introspections == 0:
            return 0.0
        acted = sum(
            1
            for e in self.entries
            if e.action_taken is not None and e.outcome is not None
        )
        return round(acted / self.total_introspections, 3)

    # ── snapshot ──

    def snapshot(self) -> dict:
        return {
            "self_awareness_depth": round(self.self_awareness_depth, 2),
            "self_regulation_precision": round(self.self_regulation_precision, 2),
            "total_introspections": self.total_introspections,
            "self_improvement_rate": self.self_improvement_rate(),
        }

    def describe(self) -> str:
        """Human-readable introspection summary."""
        return (
            f"自我认识深度={self.self_awareness_depth:.0%}，"
            f"自我调控精度={self.self_regulation_precision:.0%}，"
            f"已内省{self.total_introspections}次，"
            f"自我完善率={self.self_improvement_rate():.0%}"
        )