#!/usr/bin/env python3
"""Find SQL OR error in engine.py"""
with open(r'D:\OpenClaw_Main\workspace\self-evolution-system\src\learning\engine.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if ' OR ' in line and ('SELECT' in line or 'WHERE' in line):
        print(f"Line {i+1}: {line.rstrip()}")