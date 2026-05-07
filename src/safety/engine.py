"""Safety engine — bounded evolution with constraint enforcement."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional


class SafetyStatus(Enum):
    SAFE = "safe"
    WARNING = "warning"
    VIOLATION = "violation"
    BLOCKED = "blocked"


@dataclass
class EvolutionConstraint:
    name: str
    description: str
    max_iterations_per_hour: int = 10
    max_memory_growth_mb: float = 100.0
    allowed_modules: List[str] = field(default_factory=lambda: [
        "core", "memory", "learning", "iteration", "personality"])
    blocked_patterns: List[str] = field(default_factory=lambda: [
        "exec(", "eval(", "__import__(", "os.system(",
        "subprocess.call(", "subprocess.Popen(",
    ])


@dataclass
class SafetyPolicy:
    constraints: List[EvolutionConstraint] = field(default_factory=list)
    auto_rollback_on_violation: bool = True
    require_human_approval_for: List[str] = field(default_factory=lambda: [
        "code_generation", "external_api_access",
        "self_delete", "memory_wipe",
    ])

    def add_constraint(self, c: EvolutionConstraint):
        self.constraints.append(c)


class SafetyEngine:
    def __init__(self, policy: Optional[SafetyPolicy] = None):
        self.policy = policy or SafetyPolicy()
        self.logger = logging.getLogger("safety.Engine")
        self._violations: List[Dict[str, Any]] = []
        self._iteration_log: List[datetime] = []
        self._memory_used_mb: float = 0.0

    def check_module(self, module_name: str) -> SafetyStatus:
        allowed = set()
        for c in self.policy.constraints:
            allowed.update(c.allowed_modules)
        if not allowed:
            return SafetyStatus.SAFE
        if module_name in allowed:
            return SafetyStatus.SAFE
        self._log_violation("module_not_allowed",
                            f"Module '{module_name}' not in allowed list")
        return SafetyStatus.VIOLATION

    def check_code(self, code: str) -> SafetyStatus:
        blocked = set()
        for c in self.policy.constraints:
            blocked.update(c.blocked_patterns)
        for pattern in sorted(blocked):
            if pattern in code:
                for i, line in enumerate(code.split("\n"), 1):
                    if pattern in line:
                        self._log_violation("blocked_pattern",
                                           f"Blocked '{pattern}' at line {i}")
                        break
                return SafetyStatus.BLOCKED
        return SafetyStatus.SAFE

    def check_rate_limit(self) -> SafetyStatus:
        now = datetime.now()
        cutoff = now.timestamp() - 3600
        self._iteration_log = [t for t in self._iteration_log
                               if t.timestamp() > cutoff]
        max_iter = min([c.max_iterations_per_hour
                       for c in self.policy.constraints],
                       default=10)
        if len(self._iteration_log) >= max_iter:
            self._log_violation("rate_limit_exceeded",
                               f"{len(self._iteration_log)}/h (max {max_iter})")
            return SafetyStatus.WARNING
        return SafetyStatus.SAFE

    def record_iteration(self):
        self._iteration_log.append(datetime.now())

    def check_memory_growth(self, additional_mb: float) -> SafetyStatus:
        new_usage = self._memory_used_mb + additional_mb
        max_mb = min([c.max_memory_growth_mb
                      for c in self.policy.constraints],
                     default=100.0)
        if new_usage > max_mb:
            self._log_violation("memory_limit_exceeded",
                               f"Would reach {new_usage:.1f} MB > {max_mb} MB")
            return SafetyStatus.VIOLATION
        return SafetyStatus.SAFE

    def requires_approval(self, action: str) -> bool:
        return any(p in action for p in self.policy.require_human_approval_for)

    def add_constraint(self, constraint: EvolutionConstraint):
        self.policy.add_constraint(constraint)

    def get_policy_summary(self) -> dict:
        return {
            "constraints": [{"name": c.name, "description": c.description}
                           for c in self.policy.constraints],
            "auto_rollback": self.policy.auto_rollback_on_violation,
            "approval_required": list(self.policy.require_human_approval_for),
            "violations_recorded": len(self._violations),
        }

    def _log_violation(self, kind: str, detail: str):
        v = {"kind": kind, "detail": detail,
             "timestamp": datetime.now().isoformat()}
        self._violations.append(v)
        self.logger.warning("[%s] %s", kind, detail)

    def get_violations(self, limit: int = 20) -> List[Dict[str, Any]]:
        return self._violations[-limit:]

    def get_stats(self) -> Dict[str, Any]:
        return {
            "violations_count": len(self._violations),
            "constraint_count": len(self.policy.constraints),
            "recent_iterations": len(self._iteration_log),
            "memory_used_mb": round(self._memory_used_mb, 2),
        }