#!/usr/bin/env python3
"""Fix datetime in metadata"""
with open(r'D:\OpenClaw_Main\workspace\self-evolution-system\src\core\evolution_system.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find and fix the metadata section around line 586-591
for i, line in enumerate(lines):
    if 'metadata={' in line and i > 580 and i < 595:
        print(f"Found metadata at line {i+1}")
        # Check next few lines
        for j in range(i, min(i+10, len(lines))):
            print(f"  {j+1}: {repr(lines[j])}")
        # Remove the "state" line
        if '"state": self.get_system_state().__dict__,' in lines[i+1]:
            lines[i+1] = lines[i+1].replace('"state": self.get_system_state().__dict__,\n', '')
            print(f"Removed state line at {i+2}")
        break

with open(r'D:\OpenClaw_Main\workspace\self-evolution-system\src\core\evolution_system.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("Done!")