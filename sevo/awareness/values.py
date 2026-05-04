"""Value system — core values and consistency tracking."""


class ValueSystem:
    """Stable values with drift detection.

    Core values anchor the agent's behavior. Consistency
    is measured by how closely outputs align with values.
    """

    CORE_VALUES = ["诚实", "善良", "公平", "成长", "安全"]

    def __init__(self):
        self.values = list(self.CORE_VALUES)
        # How many times each value was violated (self-reported)
        self.violations = {v: 0 for v in self.CORE_VALUES}
        # How many times each value was upheld
        self.upholds = {v: 0 for v in self.CORE_VALUES}

    def snapshot(self) -> dict:
        return {
            "values": self.values,
            "violations": self.violations,
            "upholds": self.upholds,
        }

    def identity_consistency(self) -> float:
        """Compute overall consistency score (0–1).

        High score = values are upheld much more than violated.
        """
        total_upheld = sum(self.upholds.values())
        total_violated = sum(self.violations.values())
        total = total_upheld + total_violated
        if total == 0:
            return 1.0
        return round(total_upheld / total, 3)

    def record_uphold(self, value: str) -> None:
        """Record that a core value was upheld."""
        if value in self.upholds:
            self.upholds[value] += 1

    def record_violation(self, value: str) -> None:
        """Record that a core value was violated."""
        if value in self.violations:
            self.violations[value] += 1