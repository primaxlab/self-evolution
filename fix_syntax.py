#!/usr/bin/env python3
"""Fix indentation in storage.py"""
file_path = r'D:\OpenClaw_Main\workspace\self-evolution-system\src\memory\storage.py'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find and fix the problematic lines around 555-560
for i, line in enumerate(lines):
    if 'escaped = mem.content.replace' in line:
        # Ensure proper indentation (8 spaces for inside for loop)
        lines[i] = '        escaped = mem.content.replace("\'", "\'\'")\n'
        print(f"Fixed line {i+1}")
    if i > 0 and 'f.write(f" \'{escaped}\'", in line:
        lines[i] = '        f.write(f" \'{escaped}\',\\n")\n'
        print(f"Fixed line {i+1}")

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("Done!")