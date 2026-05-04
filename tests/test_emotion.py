"""Tests for emotion system."""

from sevo.awareness.emotion import EmotionState


def test_initial_state():
    e = EmotionState()
    s = e.snapshot()
    assert s["valence"] == 0.70
    assert s["arousal"] == 0.60
    assert s["dominance"] == 0.55


def test_positive_interaction():
    e = EmotionState()
    e.ingest_interaction("谢谢，太棒了！")
    s = e.snapshot()
    assert s["valence"] > 0.70  # should increase


def test_negative_interaction():
    e = EmotionState()
    e.ingest_interaction("错了，很失望")
    s = e.snapshot()
    assert s["valence"] < 0.70  # should decrease


def test_dominant_emotion():
    e = EmotionState()
    e._v = 0.9
    e._a = 0.8
    assert e.dominant_emotion() == "喜悦"

    e._v = 0.2
    e._a = 0.7
    assert e.dominant_emotion() == "焦虑"


def test_decay():
    e = EmotionState()
    # Override to extreme values
    e._v = 0.9
    e._a = 0.9
    e._d = 0.9

    # Multiple calls to decay gradually
    for _ in range(10):
        e._decay()

    s = e.snapshot()
    # Should be closer to baseline
    assert s["valence"] < 0.9
    assert s["arousal"] < 0.9


def test_reset():
    e = EmotionState()
    e._v = 0.1
    e.reset()
    assert e._v == 0.70