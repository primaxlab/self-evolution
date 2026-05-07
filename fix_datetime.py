#!/usr/bin/env python3
"""Fix datetime serialization in evolution_system.py"""
with open(r'D:\OpenClaw_Main\workspace\self-evolution-system\src\core\evolution_system.py', 'r', encoding='utf-8') as f:
    content = f.read()

# The exact pattern from find_pattern.py output
old = '''tags=["system", "state", event],
        metadata={
            "state": self.get_system_state().__dict__,
            "event": event,
            "timestamp": datetime.now().isoformat()
        }'''

new = '''tags=["system", "state", event],
        metadata={
            "event": event,
            "timestamp": datetime.now().isoformat()
        }'''

if old in content:
    content = content.replace(old, new)
    with open(r'D:\OpenClaw_Main\workspace\self-evolution-system\src\core\evolution_system.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed!")
else:
    print("Pattern not found, trying alternative...")
    # Try without extra spaces
    old2 = 'metadata={\n            "state": self.get_system_state().__dict__,\n'
    content = content.replace(old2, 'metadata={\n')
    with open(r'D:\OpenClaw_Main\workspace\self-evolution-system\src\core\evolution_system.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Applied alternative fix")