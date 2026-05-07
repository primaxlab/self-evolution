#!/usr/bin/env python3
"""Find close() calls in evolution_system.py"""
with open(r'D:\OpenClaw_Main\workspace\self-evolution-system\src\core\evolution_system.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '.close()' in line:
        print(f"Line {i+1}: {line.rstrip()[:100]}")