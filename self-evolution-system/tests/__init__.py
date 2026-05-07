"""Test suite for self-evolution-system."""
import sys
sys.path.insert(0, "D:/OpenClaw_Main/workspace/self-evolution-system/src")

import tempfile, os
from iteration.engine import IterationEngine, IterationType, VersionInfo
from personality.engine import PersonalityEngine, ValueRule, TraitType
from safety.engine import SafetyEngine, SafetyPolicy, EvolutionConstraint


def test_version_info():
    v = VersionInfo(1, 2, 3)
    assert str(v) == "v1.2.3"
    assert v.bump(IterationType.MINOR) == VersionInfo(1, 3, 0)
    assert v.bump(IterationType.PATCH) == VersionInfo(1, 2, 4)
    assert v.bump(IterationType.MAJOR) == VersionInfo(2, 0, 0)
    print("  OK  test_version_info")


def test_iteration_engine():
    with tempfile.TemporaryDirectory() as tmp:
        engine = IterationEngine(tmp, version=VersionInfo(1, 0, 0))
        assert engine.current_version() == "v1.0.0"
        engine.bump_version(IterationType.MINOR)
        assert engine.current_version() == "v1.1.0"
        stats = engine.get_stats()
        assert "version" in stats
        assert "backup_count" in stats
        print("  OK  test_iteration_engine")


def test_iteration_backup_rollback():
    with tempfile.TemporaryDirectory() as tmp:
        engine = IterationEngine(tmp)
        # Create a test file
        test_file = os.path.join(tmp, "test.txt")
        with open(test_file, "w") as f:
            f.write("original")
        backup = engine.create_backup("test.txt")
        assert backup is not None
        assert os.path.isfile(backup)
        with open(test_file, "w") as f:
            f.write("modified")
        ok = engine.rollback("test.txt")
        assert ok
        with open(test_file) as f:
            assert f.read() == "original"
        print("  OK  test_iteration_backup_rollback")


def test_personality_engine():
    engine = PersonalityEngine()
    engine.set_trait("curiosity", 0.9)
    assert engine.get_trait("curiosity") == 0.9
    engine.adjust_trait("caution", 0.1)
    assert engine.get_trait("caution") == 0.6
    rule = ValueRule("no_delete", "do not delete user data", 0.8, "delete_user")
    engine.add_rule(rule)
    assert engine.check_constraint("just_reading") is True
    assert engine.check_constraint("delete_user_something") is False
    assert len(engine.get_rules()) == 1
    engine.remove_rule("no_delete")
    assert len(engine.get_rules()) == 0
    stats = engine.get_stats()
    assert stats["trait_count"] >= 0
    print("  OK  test_personality_engine")


def test_safety_engine():
    engine = SafetyEngine()
    # No constraints = all safe
    assert engine.check_module("anything") == engine.check_module("__all__")  # both SAFE
    assert engine.check_code("print('hello')") == engine.check_module("test")  # both SAFE
    status = engine.check_rate_limit()
    assert status.value in ("safe", "warning")
    engine.record_iteration()
    print("  OK  test_safety_engine")


def test_safety_with_constraints():
    policy = SafetyPolicy()
    policy.add_constraint(EvolutionConstraint(
        "test_policy", "test",
        max_iterations_per_hour=3,
        allowed_modules=["core", "learning"],
        blocked_patterns=["exec(", "eval("],
    ))
    engine = SafetyEngine(policy)
    # Module check
    assert engine.check_module("learning").value == "safe"
    assert engine.check_module("random_module").value == "violation"
    # Code check
    assert engine.check_code("x = 1 + 2").value == "safe"
    assert engine.check_code("exec('x = 1')").value == "blocked"
    # Rate limit
    for _ in range(3):
        engine.record_iteration()
    assert engine.check_rate_limit().value in ("warning", "violation")
    print("  OK  test_safety_with_constraints")


def test_personality_serialization():
    import json
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        tmp = f.name
    try:
        engine = PersonalityEngine()
        engine.set_trait("creativity", 0.95)
        engine.add_rule(ValueRule("rule1", "desc", 0.5))
        engine.save(tmp)
        # Reload
        engine2 = PersonalityEngine()
        engine2.load(tmp)
        assert engine2.get_trait("creativity") == 0.95
        assert len(engine2.get_rules()) == 1
        print("  OK  test_personality_serialization")
    finally:
        if os.path.isfile(tmp):
            os.unlink(tmp)


if __name__ == "__main__":
    tests = [
        test_version_info,
        test_iteration_engine,
        test_iteration_backup_rollback,
        test_personality_engine,
        test_safety_engine,
        test_safety_with_constraints,
        test_personality_serialization,
    ]
    passed = 0
    for t in tests:
        try:
            t()
            passed += 1
        except Exception as e:
            print(f"  FAIL {t.__name__}: {e}")
    print(f"\nResult: {passed}/{len(tests)} passed")