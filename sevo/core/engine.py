"""Evolution engine — the central orchestrator.

Blueprint alignment: primaxlab/self-evolution 核心编排
- Uses SelfAwarenessSystem (6-component facade) instead of individual sub-components
- EvolutionReport expanded to include full awareness snapshot
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional

from sevo.awareness.awareness_system import SelfAwarenessSystem
from sevo.memory.store import MemoryStore
from sevo.learning.extractor import ExperienceExtractor

DEFAULT_DATA_DIR = "/tmp/sevo"


class EvolutionStage(Enum):
    """Evolution stages from emergence to transcendence.

    Blueprint alignment: index.py → EvolutionStage
    """

    FOUNDATIONAL = "foundational"  # 基础能力建立 (0–15 cycles)
    CONSCIOUSNESS = "consciousness"  # 意识觉醒 (16–40)
    LEARNING = "learning"  # 自主学习 (41–80)
    ITERATION = "iteration"  # 迭代优化 (81–120)
    MATURITY = "maturity"  # 成熟稳定 (121–180)
    TRANSCENDENCE = "transcendence"  # 超越进化 (181+)


@dataclass
class EvolutionReport:
    """Result of one full evolution cycle.

    Blueprint alignment: index.py → cycle report structure.
    """

    timestamp: datetime = field(default_factory=datetime.now)
    cycle_number: int = 0
    stage: EvolutionStage = EvolutionStage.FOUNDATIONAL

    # ── Sub-system snapshots ──
    identity_summary: dict = field(default_factory=dict)
    emotional_snapshot: dict = field(default_factory=dict)
    motivation_snapshot: dict = field(default_factory=dict)
    introspection_snapshot: dict = field(default_factory=dict)
    awareness_composite: float = 0.0

    # ── Cycle metrics ──
    memories_count: int = 0
    experiences_extracted: int = 0
    improvements: list = field(default_factory=list)
    duration_ms: float = 0.0

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp.isoformat(),
            "cycle_number": self.cycle_number,
            "stage": self.stage.value,
            "identity": self.identity_summary,
            "emotional": self.emotional_snapshot,
            "motivation": self.motivation_snapshot,
            "introspection": self.introspection_snapshot,
            "awareness_composite": self.awareness_composite,
            "memories_count": self.memories_count,
            "experiences_extracted": self.experiences_extracted,
            "duration_ms": self.duration_ms,
        }


class EvolutionEngine:
    """Central engine that orchestrates all six core systems.

    Blueprint alignment: CompleteSelfEvolutionSystem from index.py.
    Uses SelfAwarenessSystem as the unified awareness layer.
    """

    def __init__(self, data_dir: str = DEFAULT_DATA_DIR):
        self.data_dir = data_dir

        # ── Core subsystems ──
        self.awareness = SelfAwarenessSystem(data_dir=data_dir)
        self.memory = MemoryStore(data_dir=data_dir)
        self.extractor = ExperienceExtractor()

        # ── Runtime state ──
        self.session_id = ""
        self.cycle_count = 0
        self.stage = EvolutionStage.FOUNDATIONAL
        self.start_time = datetime.now()

    # ── lifecycle ──

    def bootstrap(self, session_id: str = None) -> EvolutionReport:
        """Load persistent state and prepare for a new session.

        Blueprint alignment: index.py → start_evolution()
        """
        self.awareness.bootstrap(session_id)
        self.memory.initialize()

        if session_id:
            self.session_id = session_id
        else:
            self.session_id = f"sevo_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        self.start_time = datetime.now()
        return self._build_report(0)

    def run_cycle(
        self,
        user_message: Optional[str] = None,
        assistant_response: Optional[str] = None,
        context: Optional[dict] = None,
    ) -> EvolutionReport:
        """Run one complete evolution cycle.

        This is the main entry point called each conversation turn.
        It mirrors blueprint's _run_real_evolution_cycle() structure:
          1. Awareness check (emotion + value + cognitive nudge)
          2. Experience extraction → memory
          3. Introspection (self-reflection)
          4. Stage evolution

        Args:
            user_message: The user's latest message.
            assistant_response: The assistant's response.
            context: Extra context dict.
        """
        t0 = datetime.now()
        self.cycle_count += 1

        # 1. Ingest interaction through awareness system
        if user_message:
            self.awareness.ingest_interaction(user_message, assistant_response or "")

        # 2. Decay: emotion + motivation + cognitive drift toward baseline
        self.awareness.emotion._decay()
        self.awareness.motivation.decay_drives()
        self.awareness.cognitive.drift_to_baseline()

        # 3. Extract experience from the exchange → store in memory
        experience_count = 0
        if user_message and assistant_response:
            experiences = self.extractor.extract(
                user_message=user_message,
                assistant_response=assistant_response,
                session_id=self.session_id,
            )
            for exp in experiences:
                self.memory.store(exp)
            experience_count = len(experiences)

        # 4. Self-reflect (introspection) — every 5 cycles
        if self.cycle_count % 5 == 0 and user_message and assistant_response:
            self.awareness.self_reflect(
                topic=f"对话#{self.cycle_count}",
                insight=f"处理了用户消息: {user_message[:50]}...",
                confidence=0.6,
            )

        # 5. Persist identity snapshot
        self.awareness.identity.persist()

        # 6. Evolve stage if thresholds met
        self._evolve_stage()

        duration = (datetime.now() - t0).total_seconds() * 1000
        return self._build_report(experience_count, duration)

    # ── status / report ──

    def status(self) -> dict:
        """Return current system state as a dict."""
        return {
            "session_id": self.session_id,
            "cycle_count": self.cycle_count,
            "stage": self.stage.value,
            "uptime": str(datetime.now() - self.start_time),
            "awareness": self.awareness.snapshot(),
            "memory": self.memory.stats(),
        }

    def generate_awareness_report(self) -> dict:
        """Generate comprehensive awareness report (blueprint-compatible)."""
        report = self.awareness.generate_report()
        return report.to_dict()

    # ── Internal ──

    def _evolve_stage(self) -> None:
        """Advance evolution stage based on cycle count thresholds.

        Blueprint alignment: index.py → _update_real_evolution_stage()
        """
        thresholds = [
            (0, EvolutionStage.FOUNDATIONAL),
            (15, EvolutionStage.CONSCIOUSNESS),
            (40, EvolutionStage.LEARNING),
            (80, EvolutionStage.ITERATION),
            (120, EvolutionStage.MATURITY),
            (180, EvolutionStage.TRANSCENDENCE),
        ]
        # Find the highest threshold we've crossed
        current_prev = self.stage
        for threshold, stage in thresholds:
            if self.cycle_count >= threshold:
                self.stage = stage
        if self.stage != current_prev and self.cycle_count > 0:
            # Log stage transition (could trigger introspection)
            pass

    def _build_report(
        self, experience_count: int, duration_ms: float = 0.0
    ) -> EvolutionReport:
        awareness = self.awareness.snapshot()
        return EvolutionReport(
            cycle_number=self.cycle_count,
            stage=self.stage,
            identity_summary=awareness["identity"],
            emotional_snapshot=awareness["emotional"],
            motivation_snapshot=awareness["motivation"],
            introspection_snapshot=awareness["introspection"],
            awareness_composite=self.awareness.generate_report().composite_score,
            memories_count=self.memory.count(),
            experiences_extracted=experience_count,
            duration_ms=duration_ms,
        )