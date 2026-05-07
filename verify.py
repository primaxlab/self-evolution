"""Verify all modules import successfully."""

import sys

# Add package source root so 'import memory' etc. works
sys.path.insert(0, "D:/OpenClaw_Main/workspace/self-evolution-system/src")
sys.path.insert(0, "D:/OpenClaw_Main/workspace/complete-self-evolution/src")

# sys.path must contain the PARENT of each package root, not the package dir itself
# memory.storage -> from self-evolution-system/ (not src/)
sys.path.insert(0, "D:/OpenClaw_Main/workspace/self-evolution-system")
# self_awareness.* -> from complete-self-evolution/ (not src/)
sys.path.insert(0, "D:/OpenClaw_Main/workspace/complete-self-evolution")

modules = [
    ("memory.storage", "src/memory/"),
    ("learning.engine", "src/learning/"),
    ("core.context_optimizer", "src/core/"),
    ("core.evolution_system", "src/core/"),
    ("iteration.engine", "src/iteration/"),
    ("personality.engine", "src/personality/"),
    ("safety.engine", "src/safety/"),
    ("self_awareness.personality_core",
     "complete-self-evolution/src/self_awareness/"),
    ("self_awareness.emotional_intelligence",
     "complete-self-evolution/src/self_awareness/"),
    ("self_awareness.cognitive_style",
     "complete-self-evolution/src/self_awareness/"),
]

ok, fail = 0, 0
for mod, hint in modules:
    try:
        __import__(mod)
        ok += 1
        print(f"  OK    {mod}")
    except Exception as e:
        fail += 1
        print(f"  FAIL  {mod}  <- {e}")

print(f"\nRESULT: {ok} passed, {fail} failed")

# Also try constructing the key classes
from memory.storage import MemoryStorage
from learning.engine import LearningEngine
from core.context_optimizer import ContextOptimizer
from core.evolution_system import EvolutionSystem
from iteration.engine import IterationEngine
from personality.engine import PersonalityEngine
from safety.engine import SafetyEngine
from self_awareness.personality_core import PersonalityCore
from self_awareness.emotional_intelligence import EmotionalIntelligence
from self_awareness.cognitive_style import CognitiveStyle
print("OK - All classes constructed successfully")