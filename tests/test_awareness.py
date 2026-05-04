"""Tests for awareness system — blueprint-aligned self-awareness module.

All tests use tempfile.TemporaryDirectory for isolation.
"""

import tempfile

import pytest

from sevo.awareness.awareness_system import SelfAwarenessSystem, AwarenessReport
from sevo.awareness.cognitive_style import CognitiveStyle
from sevo.awareness.motivation import MotivationSystem
from sevo.awareness.introspection import Introspection


# ═══════════════════════════════════════════════════════
# CognitiveStyle tests
# ═══════════════════════════════════════════════════════

class TestCognitiveStyle:
    def test_default_profile(self):
        with tempfile.TemporaryDirectory() as tmp:
            cs = CognitiveStyle(data_dir=tmp)
            assert cs.openness == 0.70
            assert cs.conscientiousness == 0.90
            assert cs.agreeableness == 0.80
            assert cs.extraversion == 0.60
            assert cs.neuroticism == 0.30

    def test_nudge_trait(self):
        with tempfile.TemporaryDirectory() as tmp:
            cs = CognitiveStyle(data_dir=tmp)
            cs.nudge_trait("openness", 0.10)
            assert cs.openness == 0.80
            cs.nudge_trait("openness", -0.30)
            assert cs.openness == 0.50

    def test_nudge_clamped(self):
        with tempfile.TemporaryDirectory() as tmp:
            cs = CognitiveStyle(data_dir=tmp)
            cs.nudge_trait("neuroticism", -1.0)
            assert cs.neuroticism == 0.0
            cs.nudge_trait("conscientiousness", 1.0)
            assert cs.conscientiousness == 1.0

    def test_drift_to_baseline(self):
        with tempfile.TemporaryDirectory() as tmp:
            cs = CognitiveStyle(data_dir=tmp)
            cs.nudge_trait("openness", -0.30)  # 0.70 → 0.40
            cs.drift_to_baseline()
            # 0.40 + (0.70-0.40)*0.01 = 0.403
            assert 0.40 < cs.openness < 0.45

    def test_reasoning_and_learning(self):
        with tempfile.TemporaryDirectory() as tmp:
            cs = CognitiveStyle(data_dir=tmp)
            cs.set_reasoning_style("analytical")
            assert cs.profile.reasoning_style == "analytical"
            cs.set_learning_preference("doing")
            assert cs.profile.learning_preference == "doing"

    def test_persistence(self):
        with tempfile.TemporaryDirectory() as tmp:
            cs1 = CognitiveStyle(data_dir=tmp)
            cs1.nudge_trait("openness", 0.05)
            cs1.persist()

            cs2 = CognitiveStyle(data_dir=tmp)
            cs2.load()
            assert cs2.openness == 0.75

    def test_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            cs = CognitiveStyle(data_dir=tmp)
            snap = cs.snapshot()
            assert "ocean" in snap
            assert snap["ocean"]["openness"] == 0.70
            assert snap["reasoning_style"] == "systematic"

    def test_describe(self):
        with tempfile.TemporaryDirectory() as tmp:
            cs = CognitiveStyle(data_dir=tmp)
            desc = cs.describe()
            assert "openness" in desc
            assert "推理" in desc or "reasoning" in desc


# ═══════════════════════════════════════════════════════
# MotivationSystem tests
# ═══════════════════════════════════════════════════════

class TestMotivationSystem:
    def test_initial_drives(self):
        with tempfile.TemporaryDirectory() as tmp:
            ms = MotivationSystem(data_dir=tmp)
            assert ms.drives["competence"] == 0.85
            assert ms.drives["autonomy"] == 0.70
            assert ms.drives["relatedness"] == 0.80

    def test_boost_drive(self):
        with tempfile.TemporaryDirectory() as tmp:
            ms = MotivationSystem(data_dir=tmp)
            ms.boost_drive("competence", 0.10)
            assert ms.drives["competence"] == 0.95

    def test_boost_clamped(self):
        with tempfile.TemporaryDirectory() as tmp:
            ms = MotivationSystem(data_dir=tmp)
            ms.boost_drive("competence", 0.30)
            assert ms.drives["competence"] == 1.0

    def test_suppress_drive(self):
        with tempfile.TemporaryDirectory() as tmp:
            ms = MotivationSystem(data_dir=tmp)
            ms.suppress_drive("relatedness", 0.20)
            assert round(ms.drives["relatedness"], 1) == 0.6

    def test_decay_drives(self):
        with tempfile.TemporaryDirectory() as tmp:
            ms = MotivationSystem(data_dir=tmp)
            ms.boost_drive("competence", 0.10)  # 0.85 → 0.95
            ms.decay_drives()
            # 0.95 + (0.85 - 0.95) * 0.02 = 0.948
            assert ms.drives["competence"] < 0.95

    def test_overall_motivation(self):
        with tempfile.TemporaryDirectory() as tmp:
            ms = MotivationSystem(data_dir=tmp)
            expected = round((0.85 + 0.70 + 0.80) / 3, 3)
            assert ms.overall_motivation == expected

    def test_goal_management(self):
        with tempfile.TemporaryDirectory() as tmp:
            ms = MotivationSystem(data_dir=tmp)
            goal = ms.add_goal("学习 Python", priority=0.8)
            assert goal.status == "active"

            active = ms.get_active_goals()
            assert len(active) == 1
            assert active[0].priority == 0.8

    def test_goal_completion(self):
        with tempfile.TemporaryDirectory() as tmp:
            ms = MotivationSystem(data_dir=tmp)
            goal = ms.add_goal("完成测试")
            ms.update_progress(goal.id, 1.0)
            assert goal.status == "completed"
            assert ms.goals_completed == 1
            # Completing goal boosts competence
            assert ms.drives["competence"] > 0.85

    def test_goal_abandon(self):
        with tempfile.TemporaryDirectory() as tmp:
            ms = MotivationSystem(data_dir=tmp)
            goal = ms.add_goal("废弃项目")
            ms.abandon_goal(goal.id)
            assert goal.status == "abandoned"
            assert ms.goals_abandoned == 1

    def test_persistence(self):
        with tempfile.TemporaryDirectory() as tmp:
            ms1 = MotivationSystem(data_dir=tmp)
            ms1.add_goal("测试持久化", priority=0.9)
            ms1.persist()

            ms2 = MotivationSystem(data_dir=tmp)
            ms2.load()
            active = ms2.get_active_goals()
            assert len(active) == 1

    def test_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            ms = MotivationSystem(data_dir=tmp)
            snap = ms.snapshot()
            assert "drives" in snap
            assert "overall_motivation" in snap
            assert snap["active_goals"] == 0


# ═══════════════════════════════════════════════════════
# Introspection tests
# ═══════════════════════════════════════════════════════

class TestIntrospection:
    def test_initial_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            it = Introspection(data_dir=tmp)
            assert it.self_awareness_depth == 0.30
            assert it.self_regulation_precision == 0.30
            assert it.total_introspections == 0

    def test_reflect(self):
        with tempfile.TemporaryDirectory() as tmp:
            it = Introspection(data_dir=tmp)
            entry = it.reflect("为什么回答不够好", "应该先搜索再回答",
                               confidence=0.7, action_taken="先搜索")
            assert entry.topic == "为什么回答不够好"
            assert entry.confidence == 0.7
            assert it.total_introspections == 1
            assert it.self_awareness_depth > 0.30
            # With action, regulation improves
            assert it.self_regulation_precision > 0.302

    def test_reflect_without_action(self):
        with tempfile.TemporaryDirectory() as tmp:
            it = Introspection(data_dir=tmp)
            # Baseline: precision is 0.30
            baseline = it.self_regulation_precision
            it.reflect("随便想想", "没想明白", confidence=0.3)
            # Without action, regulation improves by 0.01*(1-precision)
            assert it.self_regulation_precision > baseline

    def test_reflect_can_reach_high_values(self):
        with tempfile.TemporaryDirectory() as tmp:
            it = Introspection(data_dir=tmp)
            # Many reflections with actions should raise awareness
            for i in range(50):
                it.reflect(f"topic{i}", f"insight{i}", action_taken="act")
            assert it.self_awareness_depth > 0.7
            assert it.self_regulation_precision > 0.7

    def test_record_outcome(self):
        with tempfile.TemporaryDirectory() as tmp:
            it = Introspection(data_dir=tmp)
            entry = it.reflect("问题A", "洞察A", action_taken="改了")
            precision_before = it.self_regulation_precision
            it.record_outcome(entry.id, "成功！效果很好")
            assert it.self_regulation_precision > precision_before

    def test_recent_insights(self):
        with tempfile.TemporaryDirectory() as tmp:
            it = Introspection(data_dir=tmp)
            for i in range(10):
                it.reflect(f"topic {i}", f"insight {i}")
            recent = it.recent_insights(limit=3)
            assert len(recent) == 3

    def test_self_improvement_rate(self):
        with tempfile.TemporaryDirectory() as tmp:
            it = Introspection(data_dir=tmp)
            assert it.self_improvement_rate() == 0.0
            e1 = it.reflect("t1", "i1", action_taken="do X")
            it.record_outcome(e1.id, "成功")
            e2 = it.reflect("t2", "i2")  # no action
            # 1 acted out of 2 = 0.5
            assert it.self_improvement_rate() == 0.5

    def test_persistence(self):
        with tempfile.TemporaryDirectory() as tmp:
            it1 = Introspection(data_dir=tmp)
            it1.reflect("测试", "洞察测试", action_taken="执行")
            it1.persist()

            it2 = Introspection(data_dir=tmp)
            it2.load()
            assert it2.total_introspections == 1

    def test_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            it = Introspection(data_dir=tmp)
            snap = it.snapshot()
            assert "self_awareness_depth" in snap
            assert "self_regulation_precision" in snap


# ═══════════════════════════════════════════════════════
# SelfAwarenessSystem (integration) tests
# ═══════════════════════════════════════════════════════

class TestSelfAwarenessSystem:
    def test_bootstrap(self):
        with tempfile.TemporaryDirectory() as tmp:
            system = SelfAwarenessSystem(data_dir=tmp)
            system.bootstrap("test-session")
            assert system.identity.state.name == "sevo-agent"

    def test_ingest_interaction_emotional(self):
        with tempfile.TemporaryDirectory() as tmp:
            system = SelfAwarenessSystem(data_dir=tmp)
            system.ingest_interaction("爸爸说谢谢！太棒了！")
            snap = system.emotion.snapshot()
            assert snap["valence"] > 0.70

    def test_ingest_interaction_values(self):
        with tempfile.TemporaryDirectory() as tmp:
            system = SelfAwarenessSystem(data_dir=tmp)
            system.ingest_interaction("太棒了！完美！")
            new_consistency = system.values.identity_consistency()
            assert new_consistency == 1.0

    def test_ingest_interaction_correction(self):
        with tempfile.TemporaryDirectory() as tmp:
            system = SelfAwarenessSystem(data_dir=tmp)
            system.ingest_interaction("你搞错了，不是这样的")
            assert system.values.violations["诚实"] > 0

    def test_self_reflect(self):
        with tempfile.TemporaryDirectory() as tmp:
            system = SelfAwarenessSystem(data_dir=tmp)
            result = system.self_reflect(
                "为什么慢", "因为没缓存",
                confidence=0.8, action="加缓存"
            )
            assert "entry_id" in result
            assert system.introspection.total_introspections == 1

    def test_generate_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            system = SelfAwarenessSystem(data_dir=tmp)
            system.bootstrap()
            report = system.generate_report()
            assert isinstance(report, AwarenessReport)
            assert 0.0 <= report.composite_score <= 1.0
            assert len(report.strengths) > 0

    def test_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            system = SelfAwarenessSystem(data_dir=tmp)
            snap = system.snapshot()
            assert "identity" in snap
            assert "emotional" in snap
            assert "dominant_emotion" in snap
            assert "motivation" in snap
            assert "introspection" in snap

    def test_full_cycle_integration(self):
        """Simulate a complete interaction cycle through awareness system."""
        with tempfile.TemporaryDirectory() as tmp:
            system = SelfAwarenessSystem(data_dir=tmp)
            system.bootstrap("session-1")

            interactions = [
                ("你好！", "你好，有什么可以帮你的？"),
                ("帮我写个函数", "好的，函数已生成。"),
                ("太棒了！谢谢！", "不客气！"),
                ("这里好像有问题", "让我检查一下...确实有bug，已修复。"),
                ("完美解决了！", "很高兴能帮到你！"),
            ]

            for user_msg, asst_msg in interactions:
                system.ingest_interaction(user_msg, asst_msg)

            report = system.generate_report()
            assert report.composite_score > 0.0
            assert system.emotion.dominant_emotion() in [
                "喜悦", "满足", "平静", "中性", "激动"
            ]
            assert sum(system.values.upholds.values()) > 0
            assert system.identity.state.total_sessions == 1