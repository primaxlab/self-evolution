#!/usr/bin/env python3
"""Fix indentation in storage.py"""
file_path = r'D:\OpenClaw_Main\workspace\self-evolution-system\src\memory\storage.py'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find and fix lines 555-560 area
for i, line in enumerate(lines):
    if 'escaped = mem.content.replace' in line:
        lines[i] = '        escaped = mem.content.replace("\'", "\'\'")\n'
        print(f"Fixed line {i+1}")
    if 'f.write(f" NULL' in line and i > 553 and i < 565:
        lines[i] = '        f.write(f" NULL,\n")\n'
        print(f"Fixed line {i+1}")

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("Done!")