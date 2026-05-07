#!/usr/bin/env python3
"""Fix shutdown indentation properly"""
with open(r'D:\OpenClaw_Main\workspace\self-evolution-system\src\core\evolution_system.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Fix lines 615-630 to have correct try-block indentation (12 spaces)
# Currently they are at 8 spaces

for i in range(615, 631):
    if lines[i].strip():  # Don't modify empty lines
        lines[i] = '            ' + lines[i].lstrip()

with open(r'D:\OpenClaw_Main\workspace\self-evolution-system\src\core\evolution_system.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("Fixed indentation!")