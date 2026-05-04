#!/usr/bin/env python3
"""Sevo CLI — command-line interface for the self-evolution system."""

import argparse
import json
import sys

from sevo.core.engine import EvolutionEngine


def main():
    p = argparse.ArgumentParser(
        prog="sevo",
        description="Sevo — Complete Self-Evolution System",
    )
    sub = p.add_subparsers(dest="command")

    # ── run ──
    run_p = sub.add_parser("run", help="Start interactive evolution session")
    run_p.add_argument("--data-dir", default="/tmp/sevo", help="Data directory")

    # ── status ──
    sub.add_parser("status", help="Show current system status")

    # ── memory ──
    mem_p = sub.add_parser("memory", help="Query memory store")
    mem_p.add_argument("query", nargs="?", help="Search keyword")
    mem_p.add_argument("--type", "-t", help="Filter by type")
    mem_p.add_argument("--limit", "-n", type=int, default=10, help="Max results")
    mem_p.add_argument("--data-dir", default="/tmp/sevo")

    # ── decay ──
    dec_p = sub.add_parser("decay", help="Run memory decay cleanup")
    dec_p.add_argument("--days", type=int, default=30, help="Retention days")
    dec_p.add_argument("--data-dir", default="/tmp/sevo")

    args = p.parse_args()

    if args.command == "run":
        _run_interactive(args)
    elif args.command == "status":
        _show_status(args)
    elif args.command == "memory":
        _query_memory(args)
    elif args.command == "decay":
        _run_decay(args)
    else:
        p.print_help()


def _run_interactive(args):
    engine = EvolutionEngine(data_dir=args.data_dir)
    report = engine.bootstrap()
    print(f"🧬 Sevo v0.1.0 — Session: {engine.session_id}")
    print(f"📊 Stage: {report.stage.value} | Memories: {report.memories_count}")
    print()
    print("Type messages to simulate interactions, or /quit to exit.")
    print("Commands: /status, /memory <query>, /quit")
    print()

    while True:
        try:
            user_input = input("👤 > ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not user_input:
            continue

        if user_input == "/quit":
            break
        elif user_input == "/status":
            status = engine.status()
            print(json.dumps(status, indent=2, ensure_ascii=False))
            continue
        elif user_input.startswith("/memory"):
            query = user_input.replace("/memory", "").strip()
            memories = engine.memory.retrieve(query=query or None, limit=5)
            for m in memories:
                print(f"  [{m['type']}] {m['content'][:80]}")
            continue

        # Simulate assistant response (MVP: echo reflection)
        assistant_response = f"收到: {user_input} (session={engine.session_id})"

        report = engine.run_cycle(
            user_message=user_input,
            assistant_response=assistant_response,
        )

        print(f"🤖 > {assistant_response}")
        print(f"   [🧠 emotion={engine.awareness.emotion.dominant_emotion()} "
              f"mem={report.memories_count} exp={report.experiences_extracted}]")

    # Final persist
    engine.awareness.identity.persist()
    print(f"\n👋 Session {engine.session_id} ended.")
    print(f"   {engine.memory.count()} memories stored.")


def _show_status(args):
    engine = EvolutionEngine()
    engine.bootstrap()
    print(json.dumps(engine.status(), indent=2, ensure_ascii=False))


def _query_memory(args):
    store = __import__("sevo.memory.store", fromlist=["MemoryStore"]).MemoryStore(
        data_dir=args.data_dir
    )
    store.initialize()
    results = store.retrieve(query=args.query, type=args.type, limit=args.limit)
    for m in results:
        ts = m["timestamp"][:19]
        print(f"[{m['id']}] [{m['type']}] {ts} ★{m['importance']:.0f}")
        print(f"  {m['content'][:120]}")
        print()


def _run_decay(args):
    store = __import__("sevo.memory.store", fromlist=["MemoryStore"]).MemoryStore(
        data_dir=args.data_dir
    )
    store.initialize()
    before = store.count()
    removed = store.decay(retention_days=args.days)
    after = store.count()
    print(f"Decay: {before} → {after} ({removed} removed, {args.days}d retention)")


if __name__ == "__main__":
    main()