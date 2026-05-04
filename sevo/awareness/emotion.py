"""Emotion system — 3D model (valence, arousal, dominance).

Uses a damped-spring model: events shift the state, state decays toward baseline.
"""

import math
from typing import Optional


class EmotionState:
    """Three-dimensional emotion model.

    Dimensions (all float 0.0–1.0):
      - valence:  positive (1.0) → negative (0.0)
      - arousal:  excited (1.0) → calm (0.0)
      - dominance: in-control (1.0) → overwhelmed (0.0)
    """

    # Default baselines
    BASELINE = {"valence": 0.70, "arousal": 0.60, "dominance": 0.55}

    # Decay per update (toward baseline)
    DECAY_RATE = 0.05

    # Keyword → (valence_shift, arousal_shift, dominance_shift)
    KEYWORD_SIGNALS = {
        "谢谢": (+0.08, +0.05, +0.03),
        "好": (+0.05, +0.02, +0.02),
        "棒": (+0.10, +0.08, +0.03),
        "厉害": (+0.08, +0.07, +0.01),
        "爱": (+0.12, +0.05, -0.02),
        "不行": (-0.10, +0.03, -0.08),
        "太慢了": (-0.08, +0.05, -0.06),
        "错了": (-0.12, +0.04, -0.10),
        "失望": (-0.15, -0.05, -0.05),
        "快点": (+0.02, +0.10, -0.04),
        "紧急": (-0.02, +0.15, -0.08),
        "搞不定": (-0.10, +0.06, -0.12),
    }

    def __init__(self):
        self.reset()

    def reset(self) -> None:
        """Set all dimensions to baseline."""
        self._v = self.BASELINE["valence"]
        self._a = self.BASELINE["arousal"]
        self._d = self.BASELINE["dominance"]

    def ingest_interaction(self, text: str) -> dict:
        """Process a user message and update emotional state.

        Returns the change delta for logging.
        """
        dv, da, dd = 0.0, 0.0, 0.0

        # Match keywords
        for keyword, (vd, ad, dd_) in self.KEYWORD_SIGNALS.items():
            if keyword in text:
                dv += vd
                da += ad
                dd += dd_

        # Apply with clamping
        self._v = max(0.0, min(1.0, self._v + dv))
        self._a = max(0.0, min(1.0, self._a + da))
        self._d = max(0.0, min(1.0, self._d + dd))

        # Decay toward baseline
        self._decay()

        return {"valence": dv, "arousal": da, "dominance": dd}

    def snapshot(self) -> dict:
        """Return current emotional state."""
        return {
            "valence": round(self._v, 2),
            "arousal": round(self._a, 2),
            "dominance": round(self._d, 2),
        }

    def dominant_emotion(self) -> str:
        """Classify into coarse emotion label."""
        v, a, d = self._v, self._a, self._d
        if v > 0.75 and a > 0.6:
            return "喜悦"
        if v > 0.6 and a < 0.3:
            return "平静"
        if v < 0.3 and a > 0.6:
            return "焦虑"
        if v < 0.3 and a < 0.3:
            return "低落"
        if a > 0.7:
            return "激动"
        if v > 0.5:
            return "满足"
        return "中性"

    def _decay(self) -> None:
        """Gradually pull toward baseline."""
        attr_map = {"_v": "valence", "_a": "arousal", "_d": "dominance"}
        for attr, key in attr_map.items():
            current = getattr(self, attr)
            baseline = self.BASELINE[key]
            setattr(
                self,
                attr,
                current + (baseline - current) * self.DECAY_RATE,
            )