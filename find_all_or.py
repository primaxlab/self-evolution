#!/usr/bin/env python3
"""Find all SQL OR occurrences in engine.py"""
with open(r'D:\OpenClaw_Main\workspace\self-evolution-system\src\learning\engine.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    # Look for SQL keywords near OR
    if ' OR ' in line.upper() or line.strip().startswith('OR '):
        print(f"Line {i+1}: {line.rstrip()[:120]}")