"""Tests for Sevo core engine."""

import tempfile
from pathlib import Path

from sevo.core.engine import EvolutionEngine, EvolutionStage


def test_bootstrap_creates_identity():
    with tempfile.TemporaryDirectory() as tmp:
        engine = EvolutionEngine(data_dir=tmp)
        report = engine.bootstrap(session_id="test-001")
        assert engine.session_id == "test-001"
        assert report.stage == EvolutionStage.FOUNDATIONAL
        # bootstrap touch() is called via awareness.bootstrap() → identity.touch()
        assert engine.awareness.identity.state.total_sessions == 1


def test_run_cycle_extracts_experience():
    with tempfile.TemporaryDirectory() as tmp:
        engine = EvolutionEngine(data_dir=tmp)
        engine.bootstrap(session_id="test-002")

        report = engine.run_cycle(
            user_message="你好，这个系统太棒了！",
            assistant_response="谢谢！我会继续努力的。",
        )
        # Should have extracted at least an experience memory
        assert report.experiences_extracted > 0
        assert engine.memory.count() > 0
        assert engine.cycle_count == 1


def test_emotion_changes_with_input():
    with tempfile.TemporaryDirectory() as tmp:
        engine = EvolutionEngine(data_dir=tmp)
        engine.bootstrap()

        before = engine.awareness.emotion.snapshot()

        # Positive message
        engine.run_cycle(
            user_message="太棒了谢谢！",
            assistant_response="不客气！",
        )

        after = engine.awareness.emotion.snapshot()
        # Valence should increase (keywords: 谢谢 + 棒)
        assert after["valence"] >= before["valence"]


def test_stage_evolution():
    with tempfile.TemporaryDirectory() as tmp:
        engine = EvolutionEngine(data_dir=tmp)
        engine.bootstrap()

        # Simulate many cycles
        for i in range(16):
            engine.cycle_count = i + 1
            engine._evolve_stage()

        assert engine.stage == EvolutionStage.CONSCIOUSNESS


def test_memory_persistence():
    with tempfile.TemporaryDirectory() as tmp:
        # First session
        engine = EvolutionEngine(data_dir=tmp)
        engine.bootstrap(session_id="s1")
        engine.run_cycle(
            user_message="测试记忆持久化",
            assistant_response="记忆已存储",
        )
        count1 = engine.memory.count()

        # Second session — should find previous memories
        engine2 = EvolutionEngine(data_dir=tmp)
        engine2.bootstrap(session_id="s2")
        count2 = engine2.memory.count()

        # Memory should persist across sessions
        assert count2 > 0