"""Identity system — stable self-concept with session continuity."""

import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class IdentityState:
    """Persistent identity snapshot."""
    name: str = "sevo-agent"
    role: str = "AI助手"
    first_seen: str = ""  # ISO timestamp
    last_seen: str = ""
    total_sessions: int = 0
    core_values: list = None

    def __post_init__(self):
        if self.core_values is None:
            self.core_values = ["诚实", "善良", "公平", "成长", "安全"]
        if not self.first_seen:
            self.first_seen = datetime.now().isoformat()


class Identity:
    """Manages the agent's stable self-concept across sessions.

    Loads from disk on startup, persists on each cycle.
    """

    def __init__(self, data_dir: str = "/tmp/sevo"):
        self.data_dir = data_dir
        self.state = IdentityState()
        self._file = os.path.join(data_dir, "identity.json")

    def load(self) -> IdentityState:
        """Load identity from disk. Creates default if missing."""
        os.makedirs(self.data_dir, exist_ok=True)
        if os.path.exists(self._file):
            try:
                with open(self._file) as f:
                    data = json.load(f)
                self.state = IdentityState(**data)
            except (json.JSONDecodeError, TypeError):
                self.state = IdentityState()
                self.persist()
        else:
            self.persist()
        return self.state

    def persist(self) -> None:
        """Save current identity to disk."""
        os.makedirs(self.data_dir, exist_ok=True)
        self.state.last_seen = datetime.now().isoformat()
        # Only increment session count via touch()
        with open(self._file, "w") as f:
            json.dump(asdict(self.state), f, indent=2, ensure_ascii=False)

    def touch(self) -> None:
        """Called at session start to record a new session."""
        self.state.total_sessions += 1
        self.persist()

    def summary(self) -> dict:
        """Return a compact identity summary."""
        return {
            "name": self.state.name,
            "role": self.state.role,
            "total_sessions": self.state.total_sessions,
            "values": self.state.core_values,
            "first_seen": self.state.first_seen[:10],
        }

    def set_name(self, name: str) -> None:
        self.state.name = name
        self.persist()

    def set_values(self, values: list) -> None:
        self.state.core_values = values
        self.persist()