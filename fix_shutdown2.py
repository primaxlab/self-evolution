#!/usr/bin/env python3
"""Fix shutdown indentation"""
with open(r'D:\OpenClaw_Main\workspace\self-evolution-system\src\core\evolution_system.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Check around line 614
for i in range(612, 625):
    print(f"Line {i+1}: indent={len(lines[i])-len(lines[i].lstrip())} | {lines[i].rstrip()[:80]}")