#!/usr/bin/env python3
"""Check whitespace in storage.py"""
with open(r'D:\OpenClaw_Main\workspace\self-evolution-system\src\memory\storage.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(536, 578):
    line = lines[i]
    leading = len(line) - len(line.lstrip())
    print(f"Line {i+1}: indent={leading} | {line.rstrip()[:70]}")