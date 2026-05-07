#!/usr/bin/env python3
"""Find INSERT statements in engine.py"""
with open(r'D:\OpenClaw_Main\workspace\self-evolution-system\src\learning\engine.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'INSERT' in line.upper():
        print(f"Line {i+1}: {line.rstrip()[:100]}")