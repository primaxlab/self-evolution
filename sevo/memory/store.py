"""Memory store — SQLite-backed persistent memory with retrieval and decay."""

import json
import os
import sqlite3
import threading
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional


@dataclass
class Memory:
    """A single memory record."""
    id: str = ""
    type: str = "experience"  # experience, knowledge, preference, error, insight
    content: str = ""
    session_id: str = ""
    importance: float = 5.0  # 0–10
    timestamp: str = ""
    tags: list = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()
        if not self.id:
            self.id = f"mem_{datetime.now().strftime('%Y%m%d%H%M%S')}_{os.urandom(4).hex()}"


class MemoryStore:
    """SQLite-backed memory store with decay and relevance retrieval."""

    def __init__(self, data_dir: str = "/tmp/sevo"):
        self.data_dir = data_dir
        self.db_path = os.path.join(data_dir, "memory.db")
        self._lock = threading.Lock()

    def initialize(self) -> None:
        """Create tables if they don't exist."""
        os.makedirs(self.data_dir, exist_ok=True)
        with self._get_conn() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id TEXT PRIMARY KEY,
                    type TEXT NOT NULL DEFAULT 'experience',
                    content TEXT NOT NULL,
                    session_id TEXT DEFAULT '',
                    importance REAL DEFAULT 5.0,
                    timestamp TEXT NOT NULL,
                    tags TEXT DEFAULT '[]',
                    metadata TEXT DEFAULT '{}'
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_memories_type
                ON memories(type)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_memories_timestamp
                ON memories(timestamp DESC)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_memories_importance
                ON memories(importance DESC)
            """)
            conn.commit()

    def store(self, memory: Memory) -> None:
        """Persist a memory record."""
        with self._get_conn() as conn:
            conn.execute(
                """INSERT OR REPLACE INTO memories
                   (id, type, content, session_id, importance, timestamp, tags, metadata)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    memory.id,
                    memory.type,
                    memory.content,
                    memory.session_id,
                    memory.importance,
                    memory.timestamp,
                    json.dumps(memory.tags, ensure_ascii=False),
                    json.dumps(memory.metadata, ensure_ascii=False),
                ),
            )
            conn.commit()

    def retrieve(self, query: str = None, type: str = None, limit: int = 10) -> list[dict]:
        """Retrieve memories by keyword match and optional type filter.

        Basic substring match — for MVP. Upgrade path: embedding similarity.
        """
        sql = "SELECT * FROM memories WHERE 1=1"
        params = []

        if query:
            sql += " AND content LIKE ?"
            params.append(f"%{query}%")

        if type:
            sql += " AND type = ?"
            params.append(type)

        sql += " ORDER BY importance DESC, timestamp DESC LIMIT ?"
        params.append(limit)

        with self._get_conn() as conn:
            rows = conn.execute(sql, params).fetchall()

        return [self._row_to_dict(r) for r in rows]

    def decay(self, retention_days: int = 30) -> int:
        """Remove memories older than retention_days with importance < 3.

        Returns number of deleted records.
        """
        cutoff = (datetime.now() - timedelta(days=retention_days)).isoformat()
        with self._get_conn() as conn:
            cur = conn.execute(
                "DELETE FROM memories WHERE timestamp < ? AND importance < 3.0",
                (cutoff,),
            )
            conn.commit()
            return cur.rowcount

    def count(self, type: str = None) -> int:
        """Total memory count, optionally filtered by type."""
        if type:
            sql = "SELECT COUNT(*) FROM memories WHERE type = ?"
            params = (type,)
        else:
            sql = "SELECT COUNT(*) FROM memories"
            params = ()
        with self._get_conn() as conn:
            row = conn.execute(sql, params).fetchone()
            return row[0] if row else 0

    def stats(self) -> dict:
        """Return memory system statistics."""
        total = self.count()
        by_type = {}
        for t in ("experience", "knowledge", "preference", "error", "insight"):
            c = self.count(type=t)
            if c > 0:
                by_type[t] = c
        return {"total": total, "by_type": by_type}

    # ── Internal ──

    def _get_conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def _row_to_dict(row) -> dict:
        d = dict(row)
        d["tags"] = json.loads(d.get("tags", "[]"))
        d["metadata"] = json.loads(d.get("metadata", "{}"))
        return d