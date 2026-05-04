"""Tests for memory store."""

import tempfile
from pathlib import Path

from sevo.memory.store import Memory, MemoryStore


def test_store_and_retrieve():
    with tempfile.TemporaryDirectory() as tmp:
        store = MemoryStore(data_dir=tmp)
        store.initialize()

        mem = Memory(
            type="experience",
            content="用户询问了关于Python的内存管理",
            session_id="s1",
            importance=7.0,
            tags=["python", "memory"],
        )
        store.store(mem)

        results = store.retrieve(query="Python", limit=5)
        assert len(results) == 1
        assert "python" in results[0]["tags"]


def test_count():
    with tempfile.TemporaryDirectory() as tmp:
        store = MemoryStore(data_dir=tmp)
        store.initialize()
        assert store.count() == 0

        store.store(Memory(content="test1"))
        store.store(Memory(content="test2", type="error"))
        assert store.count() == 2
        assert store.count(type="error") == 1
        assert store.count(type="experience") == 1


def test_decay():
    with tempfile.TemporaryDirectory() as tmp:
        store = MemoryStore(data_dir=tmp)
        store.initialize()

        # Store a very old, low-importance memory
        mem = Memory(
            content="old low prio",
            importance=2.0,
            timestamp="2024-01-01T00:00:00",
        )
        store.store(mem)

        # And a recent, important one
        mem2 = Memory(
            content="recent important",
            importance=9.0,
        )
        store.store(mem2)

        removed = store.decay(retention_days=365)
        assert removed >= 1  # the old low-prio should be gone
        assert store.count() >= 1  # the important one stays


def test_retrieve_by_type():
    with tempfile.TemporaryDirectory() as tmp:
        store = MemoryStore(data_dir=tmp)
        store.initialize()

        store.store(Memory(content="exp", type="experience"))
        store.store(Memory(content="err", type="error"))
        store.store(Memory(content="insight", type="insight"))

        results = store.retrieve(type="error")
        assert len(results) == 1
        assert results[0]["content"] == "err"