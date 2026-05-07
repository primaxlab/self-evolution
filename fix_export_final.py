#!/usr/bin/env python3
"""Fix export_memories indentation properly"""
with open(r'D:\OpenClaw_Main\workspace\self-evolution-system\src\memory\storage.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Fix lines 550-573
for i in range(549, 573):
    line = lines[i]
    stripped = line.rstrip()
    if not stripped or stripped.startswith('#'):
        continue
    
    if i == 549:  # with open...
        lines[i] = '            with open(export_path, \'w\', encoding=\'utf-8\') as f:\n'
    elif i == 550:  # f.write -- Memory
        lines[i] = '                f.write(\'-- Memory Storage Export\\n\')\n'
    elif i == 551:  # f.write BEGIN
        lines[i] = '                f.write(\'BEGIN TRANSACTION;\\n\\n\')\n'
    elif i == 552:  # empty line
        lines[i] = '\n'
    elif i == 553:  # for mem in memories:
        lines[i] = '                for mem in memories:\n'
    elif i == 554:  # f.write INSERT
        lines[i] = '                    f.write(f"INSERT OR REPLACE INTO memories VALUES (\\n")\n'
    elif i == 555:  # f.write mem.id
        lines[i] = '                    f.write(f" \'{mem.id}\',\\n")\n'
    elif i == 556:  # f.write mem.type
        lines[i] = '                    f.write(f" \'{mem.type.value}\',\\n")\n'
    elif i == 557:  # escaped = 
        lines[i] = '                    escaped = mem.content.replace("\'", "\'\'")\n'
    elif i == 558:  # f.write escaped
        lines[i] = '                    f.write(f" \'{escaped}\',\\n")\n'
    elif i == 559:  # f.write NULL
        lines[i] = '                    f.write(f" NULL,\\n")\n'
    elif i == 560:  # comment
        lines[i] = '                    # \\u538b\\u7f29\\u5185\\u5bb9\\u4e0d\\u5bfc\\u51fa\n'
    elif i == 561:  # f.write timestamp
        lines[i] = '                    f.write(f" \'{mem.timestamp.isoformat()}\',\\n")\n'
    elif i == 562:  # f.write session_id
        lines[i] = '                    f.write(f" \'{mem.session_id}\',\\n")\n'
    elif i == 563:  # f.write importance
        lines[i] = '                    f.write(f" {mem.importance.value},\\n")\n'
    elif i == 564:  # f.write associations
        lines[i] = '                    f.write(f" \'{json.dumps(mem.associations)}\',\\n")\n'
    elif i == 565:  # f.write tags
        lines[i] = '                    f.write(f" \'{json.dumps(mem.tags)}\',\\n")\n'
    elif i == 566:  # f.write metadata
        lines[i] = '                    f.write(f" \'{json.dumps(mem.metadata)}\',\\n")\n'
    elif i == 567:  # f.write access_count
        lines[i] = '                    f.write(f" {mem.access_count},\\n")\n'
    elif i == 568:  # f.write last_accessed
        lines[i] = '                    f.write(f" \'{mem.last_accessed.isoformat()}\',\\n")\n'
    elif i == 569:  # f.write relevance_score
        lines[i] = '                    f.write(f" {mem.relevance_score}\\n")\n'
    elif i == 570:  # f.write );
        lines[i] = '                    f.write(\');\\n\\n\')\n'
    elif i == 571:  # empty line
        lines[i] = '\n'
    elif i == 572:  # f.write COMMIT
        lines[i] = '                f.write(\'COMMIT;\\n\')\n'

with open(r'D:\OpenClaw_Main\workspace\self-evolution-system\src\memory\storage.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("Fixed!")