#!/usr/bin/env python3
"""Fix SQL OR syntax error in engine.py"""
with open(r'D:\OpenClaw_Main\workspace\self-evolution-system\src\learning\engine.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Fix line 700 - remove leading OR
if "conditions.append(f\"OR ({' OR '.join(content_conditions)})\")" in lines[699]:
    lines[699] = "                conditions.append(f\"({' OR '.join(content_conditions)})\")\n"
    print("Fixed line 700")
else:
    print("Line 700 not as expected")
    print(repr(lines[699]))

with open(r'D:\OpenClaw_Main\workspace\self-evolution-system\src\learning\engine.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("Done")