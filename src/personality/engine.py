"""Personality engine — traits, values, behavioral alignment."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any, Dict, List, Optional


class TraitType(Enum):
    CORE = auto()
    ADAPTABLE = auto()
    CONTEXTUAL = auto()
    LEARNED = auto()


class ValueRule:
    def __init__(self, name: str, description: str, weight: float = 1.0,
                 constraint: Optional[str] = None, enabled: bool = True):
        self.name = name
        self.description = description
        self.weight = max(0.0, min(1.0, weight))
        self.constraint = constraint
        self.created_at = datetime.now()
        self.enabled = enabled

    def to_dict(self) -> dict:
        return {
            "name": self.name, "description": self.description,
            "weight": self.weight, "constraint": self.constraint,
            "enabled": self.enabled,
        }


@dataclass
class PersonalityProfile:
    traits: Dict[str, float] = field(default_factory=lambda: {
        "curiosity": 0.8, "caution": 0.5, "creativity": 0.7,
        "precision": 0.8, "independence": 0.6, "compliance": 0.7,
        "assertiveness": 0.5, "patience": 0.7,
    })
    values: List[ValueRule] = field(default_factory=list)
    preferences: Dict[str, Any] = field(default_factory=dict)
    updated_at: datetime = field(default_factory=datetime.now)


class PersonalityEngine:
    def __init__(self, profile: Optional[PersonalityProfile] = None):
        self.profile = profile or PersonalityProfile()
        self.logger = logging.getLogger("personality.Engine")
        self._history: List[Dict[str, Any]] = []

    def get_trait(self, name: str) -> Optional[float]:
        return self.profile.traits.get(name)

    def set_trait(self, name: str, value: float,
                  it_type: TraitType = TraitType.ADAPTABLE):
        old = self.profile.traits.get(name)
        self.profile.traits[name] = max(0.0, min(1.0, value))
        self._record_change("trait", name, old, self.profile.traits[name])

    def adjust_trait(self, name: str, delta: float):
        current = self.profile.traits.get(name, 0.5)
        self.set_trait(name, current + delta, TraitType.LEARNED)

    def add_rule(self, rule: ValueRule):
        self.profile.values.append(rule)

    def remove_rule(self, name: str) -> bool:
        before = len(self.profile.values)
        self.profile.values = [r for r in self.profile.values if r.name != name]
        return len(self.profile.values) < before

    def get_rules(self, enabled_only: bool = True) -> List[ValueRule]:
        return [r for r in self.profile.values if not enabled_only or r.enabled]

    def check_constraint(self, action: str) -> bool:
        for rule in self.profile.values:
            if rule.enabled and rule.constraint and rule.constraint in action:
                return False
        return True

    def to_dict(self) -> dict:
        return {
            "traits": dict(self.profile.traits),
            "values": [r.to_dict() for r in self.profile.values],
            "preferences": dict(self.profile.preferences),
        }

    def save(self, path: str):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    def load(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.profile.traits.update(data.get("traits", {}))
        self.profile.values = [ValueRule(**v) for v in data.get("values", [])]
        self.profile.preferences.update(data.get("preferences", {}))

    def _record_change(self, kind: str, key: str, old, new):
        self._history.append({
            "kind": kind, "key": key, "old": old, "new": new,
            "timestamp": datetime.now().isoformat(),
        })

    def get_stats(self) -> Dict[str, Any]:
        return {
            "trait_count": len(self.profile.traits),
            "value_rules": len(self.profile.values),
            "changes_recorded": len(self._history),
        }