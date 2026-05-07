#!/usr/bin/env python3
"""Fix shutdown order in evolution_system.py properly"""
with open(r'D:\OpenClaw_Main\workspace\self-evolution-system\src\core\evolution_system.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# We need to:
# 1. Record shutdown memory FIRST
# 2. Then close memory_storage
# 3. Remove the second if self.memory_storage check

# Find lines 624-641 (0-indexed: 623-640)
# Line 624: # 记录关闭记忆
# Line 625: if self.memory_storage:
# Line 626-639: shutdown_memory creation
# Line 640: self.memory_storage.store_memory(shutdown_memory)

# Move this block BEFORE the close calls, then remove original
new_lines = []
i = 0
while i < len(lines):
    # When we hit the "记录关闭记忆" section, insert it before the close section
    if i == 614:  # Right after "try:"
        # First insert the shutdown memory recording
        new_lines.append(lines[i])  # try:
        new_lines.append('        # \u8bb0\u5f55\u5173\u95ed\u8bb0\u5fc6\n')
        new_lines.append('        shutdown_memory = MemoryRecord(\n')
        new_lines.append('            id=f"shutdown_{self.session_id}",\n')
        new_lines.append('            type=MemoryType.EXPERIENCE,\n')
        new_lines.append('            content="\u81ea\u6211\u8fdb\u5316\u7cfb\u7edf\u5173\u95ed",\n')
        new_lines.append('            timestamp=datetime.now(),\n')
        new_lines.append('            session_id=self.session_id,\n')
        new_lines.append('            importance=ImportanceLevel.MEDIUM,\n')
        new_lines.append('            tags=["system", "shutdown"],\n')
        new_lines.append('            metadata={\n')
        new_lines.append('                "evolution_count": self.state.evolution_count,\n')
        new_lines.append('                "total_memories": self.state.total_memories\n')
        new_lines.append('            }\n')
        new_lines.append('        )\n')
        new_lines.append('        self.memory_storage.store_memory(shutdown_memory)\n')
        new_lines.append('\n')
        i += 1
        continue
    
    # Skip lines 623-640 (the original shutdown memory block)
    if i >= 623 and i <= 640:
        i += 1
        continue
    
    new_lines.append(lines[i])
    i += 1

with open(r'D:\OpenClaw_Main\workspace\self-evolution-system\src\core\evolution_system.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print("Fixed! Shutdown memory now recorded before closing storage.")