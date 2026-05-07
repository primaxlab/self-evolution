#!/usr/bin/env python3
"""Check structure"""
with open(r'D:\OpenClaw_Main\workspace\self-evolution-system\src\core\evolution_system.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Check line 612-640 to understand the structure
for i in range(610, 645):
    indent = len(lines[i]) - len(lines[i].lstrip())
    print(f"Line {i+1} ({indent}): {lines[i].rstrip()[:90]}")