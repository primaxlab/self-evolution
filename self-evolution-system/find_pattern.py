#!/usr/bin/env python3
"""Find and fix datetime issue"""
with open(r'D:\OpenClaw_Main\workspace\self-evolution-system\src\core\evolution_system.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the problematic area
if 'get_system_state().__dict__' in content:
    idx = content.find('get_system_state().__dict__')
    print("Found at index", idx)
    print("Context:")
    print(repr(content[idx-200:idx+200]))
else:
    print("Not found")