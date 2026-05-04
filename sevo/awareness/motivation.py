"""Motivation system — intrinsic motives + goal-directed behavior + decay.

Blueprint alignment: primaxlab/self-evolution 自我意识系统第5组件.
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
from typing import Optional


@dataclass
class Goal:
    """A concrete goal the agent is working toward."""

    id: str
    description: str
    priority: float = 0.5  # 0.0 (low) – 1.0 (high)
    progress: float = 0.0  # 0.0 – 1.0
    status: str = "active"  # active | completed | abandoned
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


class MotivationSystem:
    """Tracks intrinsic motives and drives goal-directed behavior.

    Core drives (from self-determination theory):
      - competence:  desire to master skills and feel effective
      - autonomy:    desire to be self-directed
      - relatedness: desire to connect and belong

    Goals are concrete expressions of these drives. Motivation decays
    over time if not reinforced — simulating "boredom" or "task fatigue."

    Blueprint reference: self_awareness.js → this.motivationSystem
    """

    # ── intrinsic drive baselines ──
    BASELINE = {
        "competence": 0.85,  # high — wants to be good at things
        "autonomy": 0.70,  # moderate — ok with guidance
        "relatedness": 0.80,  # high — values connection
    }

    # Decay rate per update (0 = no decay, 1 = instant reset)
    DRIVE_DECAY = 0.02

    # Goal decay: if not updated in this many hours, reduce priority
    GOAL_STALE_HOURS = 24

    def __init__(self, data_dir: str = "/tmp/sevo"):
        self.data_dir = data_dir
        self._file = os.path.join(data_dir, "motivation.json")

        # Current drive levels
        self.drives = dict(self.BASELINE)

        # Active goals
        self.goals: dict[str, Goal] = {}

        # History: how many goals completed
        self.goals_completed = 0
        self.goals_abandoned = 0

        self.load()

    # ── persistence ──

    def load(self) -> None:
        os.makedirs(self.data_dir, exist_ok=True)
        if os.path.exists(self._file):
            try:
                with open(self._file) as f:
                    data = json.load(f)
                self.drives = data.get("drives", dict(self.BASELINE))
                self.goals = {
                    k: Goal(**v) for k, v in data.get("goals", {}).items()
                }
                self.goals_completed = data.get("goals_completed", 0)
                self.goals_abandoned = data.get("goals_abandoned", 0)
            except (json.JSONDecodeError, TypeError):
                pass

    def persist(self) -> None:
        os.makedirs(self.data_dir, exist_ok=True)
        with open(self._file, "w") as f:
            json.dump(
                {
                    "drives": self.drives,
                    "goals": {k: v.to_dict() for k, v in self.goals.items()},
                    "goals_completed": self.goals_completed,
                    "goals_abandoned": self.goals_abandoned,
                },
                f,
                indent=2,
                ensure_ascii=False,
            )

    # ── drive management ──

    def boost_drive(self, drive: str, amount: float = 0.10) -> None:
        """Boost a specific intrinsic drive."""
        if drive in self.drives:
            self.drives[drive] = min(1.0, self.drives[drive] + amount)
            self.persist()

    def suppress_drive(self, drive: str, amount: float = 0.10) -> None:
        """Suppress a specific intrinsic drive."""
        if drive in self.drives:
            self.drives[drive] = max(0.0, self.drives[drive] - amount)
            self.persist()

    def decay_drives(self) -> None:
        """Decay all drives toward baseline (simulates resting state)."""
        for drive, baseline in self.BASELINE.items():
            current = self.drives[drive]
            self.drives[drive] = round(
                current + (baseline - current) * self.DRIVE_DECAY, 4
            )
        self.persist()

    @property
    def overall_motivation(self) -> float:
        """Average of all three drives (0–1)."""
        return round(sum(self.drives.values()) / len(self.drives), 3)

    def snapshot(self) -> dict:
        return {
            "drives": self.drives,
            "overall_motivation": self.overall_motivation,
            "active_goals": sum(1 for g in self.goals.values() if g.status == "active"),
            "goals_completed": self.goals_completed,
            "goals_abandoned": self.goals_abandoned,
        }

    def describe(self) -> str:
        """Human-readable motivation summary."""
        high_drives = [d for d, v in self.drives.items() if v > 0.7]
        low_drives = [d for d, v in self.drives.items() if v < 0.4]
        parts = [f"总体动机={self.overall_motivation:.0%}"]
        if high_drives:
            parts.append(f"高驱动力：{'、'.join(high_drives)}")
        if low_drives:
            parts.append(f"低驱动力：{'、'.join(low_drives)}")
        active = [g for g in self.goals.values() if g.status == "active"]
        parts.append(f"活跃目标：{len(active)}个")
        return "；".join(parts)

    # ── goal management ──

    def add_goal(self, description: str, priority: float = 0.5) -> Goal:
        """Create a new active goal."""
        import uuid

        gid = f"goal-{uuid.uuid4().hex[:8]}"
        goal = Goal(id=gid, description=description, priority=priority)
        self.goals[gid] = goal
        self.persist()
        return goal

    def update_progress(self, goal_id: str, progress: float) -> None:
        """Set goal progress (0.0–1.0). Auto-completes at 1.0."""
        if goal_id not in self.goals:
            return
        goal = self.goals[goal_id]
        goal.progress = max(0.0, min(1.0, progress))
        if goal.progress >= 1.0:
            goal.status = "completed"
            goal.completed_at = datetime.now().isoformat()
            self.goals_completed += 1
            # Completing a goal boosts competence
            self.boost_drive("competence", 0.05)
        self.persist()

    def abandon_goal(self, goal_id: str) -> None:
        """Mark a goal as abandoned."""
        if goal_id not in self.goals:
            return
        self.goals[goal_id].status = "abandoned"
        self.goals_abandoned += 1
        self.persist()

    def get_active_goals(self) -> list[Goal]:
        """Return all active goals, sorted by priority desc."""
        active = [g for g in self.goals.values() if g.status == "active"]
        return sorted(active, key=lambda g: -g.priority)

    def decay_stale_goals(self, stale_hours: int = None) -> None:
        """Reduce priority of goals that haven't been touched."""
        if stale_hours is None:
            stale_hours = self.GOAL_STALE_HOURS
        cutoff = datetime.now() - timedelta(hours=stale_hours)
        for goal in self.goals.values():
            if goal.status == "active":
                created = datetime.fromisoformat(goal.created_at)
                if created < cutoff:
                    goal.priority = max(0.1, goal.priority - 0.05)
        self.persist()