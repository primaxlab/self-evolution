#!/usr/bin/env python3
"""Fix export_memories indentation"""
file_path = r'D:\OpenClaw_Main\workspace\self-evolution-system\src\memory\storage.py'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Fix lines in export_memories function
i = 0
while i < len(lines):
    line = lines[i]
    if 'for mem in memories:' in line:
        # Found the for loop, next lines need 8 space indent until we hit non-indented content
        i += 1
        while i < len(lines):
            stripped = lines[i].strip()
            if stripped == '' or stripped.startswith('#'):
                i += 1
                continue
            if stripped.startswith('def ') or stripped.startswith('class '):
                break
            # These lines need 8 space indent
            if lines[i][0:8].strip() == '':  # not already indented
                lines[i] = '        ' + lines[i].lstrip()
            i += 1
    i += 1

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("Done!")