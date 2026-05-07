"""Iteration engine — version bumps, backups, rollback, async iteration cycle."""

from __future__ import annotations

import json
import logging
import os
import shutil
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any, Dict, List, Optional


class IterationType(Enum):
    PATCH = auto()   # bug-fix, no new feature
    MINOR = auto()   # new feature, backward-compatible
    MAJOR = auto()   # breaking change or major redesign


@dataclass
class VersionInfo:
    major: int = 1
    minor: int = 0
    patch: int = 0

    def __str__(self) -> str:
        return f"v{self.major}.{self.minor}.{self.patch}"

    def bump(self, it_type: IterationType) -> "VersionInfo":
        if it_type == IterationType.MAJOR:
            return VersionInfo(self.major + 1, 0, 0)
        if it_type == IterationType.MINOR:
            return VersionInfo(self.major, self.minor + 1, 0)
        return VersionInfo(self.major, self.minor, self.patch + 1)


@dataclass
class IterationSnapshot:
    version: str
    timestamp: str
    changes_summary: str = ""
    regression_passed: bool = True


class IterationEngine:
    def __init__(self, workspace_root: str, version: Optional[VersionInfo] = None):
        self._root = workspace_root
        self._version = version or VersionInfo()
        self._logger = logging.getLogger("iteration.Engine")
        self._history: List[Dict[str, Any]] = []

        self._backup_dir = os.path.join(workspace_root, ".iteration_backups")
        os.makedirs(self._backup_dir, exist_ok=True)

        self._snapshots_dir = os.path.join(workspace_root, ".iteration_snapshots")
        os.makedirs(self._snapshots_dir, exist_ok=True)

    def current_version(self) -> str:
        return str(self._version)

    def bump_version(self, it_type: IterationType) -> str:
        old = str(self._version)
        self._version = self._version.bump(it_type)
        self._record("version_bump", {"from": old, "to": str(self._version),
                                      "type": it_type.name})
        return str(self._version)

    def create_backup(self, file_path: str) -> Optional[str]:
        if not os.path.isabs(file_path):
            file_path = os.path.join(self._root, file_path)
        if not os.path.isfile(file_path):
            return None
        backup_id = uuid.uuid4().hex[:8]
        backup_name = f"{os.path.basename(file_path)}_{backup_id}.bak"
        backup_path = os.path.join(self._backup_dir, backup_name)
        try:
            shutil.copy2(file_path, backup_path)
            self._record("backup_created", {"file": file_path,
                                             "backup": backup_path})
            return backup_path
        except Exception as e:
            self._logger.error("Backup failed for %s: %s", file_path, e)
            return None

    def rollback(self, file_path: str) -> bool:
        if not os.path.isabs(file_path):
            file_path = os.path.join(self._root, file_path)
        basename = os.path.basename(file_path)
        candidates = [
            f for f in os.listdir(self._backup_dir)
            if f.startswith(basename) and f.endswith(".bak")
        ]
        if not candidates:
            return False
        candidates.sort(reverse=True)
        backup_path = os.path.join(self._backup_dir, candidates[0])
        try:
            shutil.copy2(backup_path, file_path)
            self._record("rollback", {"file": file_path,
                                       "backup": backup_path})
            return True
        except Exception as e:
            self._logger.error("Rollback failed for %s: %s", file_path, e)
            return False

    def save_snapshot(self, changes_summary: str = "",
                     regression_passed: bool = True) -> str:
        snap_id = uuid.uuid4().hex[:8]
        snap: IterationSnapshot = IterationSnapshot(
            version=str(self._version),
            timestamp=datetime.now().isoformat(),
            changes_summary=changes_summary,
            regression_passed=regression_passed,
        )
        path = os.path.join(self._snapshots_dir, f"{snap_id}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"version": snap.version,
                       "timestamp": snap.timestamp,
                       "changes_summary": snap.changes_summary,
                       "regression_passed": snap.regression_passed,
                       "snap_id": snap_id}, f, ensure_ascii=False)
        self._record("snapshot_saved", {"version": snap.version,
                                         "path": path})
        return path

    def list_snapshots(self) -> List[Dict[str, Any]]:
        result = []
        for fname in os.listdir(self._snapshots_dir):
            if fname.endswith(".json"):
                try:
                    with open(os.path.join(self._snapshots_dir, fname),
                              encoding="utf-8") as f:
                        result.append(json.load(f))
                except Exception:
                    pass
        return sorted(result, key=lambda x: x.get("timestamp", ""), reverse=True)

    def run_regression_check(self) -> bool:
        """Stub: return True. Replace with actual test runner integration."""
        return True

    def execute_iteration_cycle(self,
                                changes_summary: str = "") -> Dict[str, Any]:
        """Run one full iteration cycle: backup -> regression -> snapshot."""
        ok = self.run_regression_check()
        self.save_snapshot(changes_summary, ok)
        self._record("iteration_cycle", {"passed": ok,
                                         "version": str(self._version)})
        return {"ok": ok, "version": str(self._version),
                "snapshot_count": len(os.listdir(self._snapshots_dir))}

    def get_stats(self) -> Dict[str, Any]:
        return {
            "version": str(self._version),
            "backup_count": len(os.listdir(self._backup_dir)),
            "snapshot_count": len(os.listdir(self._snapshots_dir)),
            "history_entries": len(self._history),
        }

    def _record(self, kind: str, data: Dict[str, Any]):
        entry = {"kind": kind, "timestamp": datetime.now().isoformat(),
                 **data}
        self._history.append(entry)
        self._logger.info("[%s] %s", kind, data)