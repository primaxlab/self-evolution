#!/usr/bin/env python3
"""Fix export_memories function indentation"""
file_path = r'D:\OpenClaw_Main\workspace\self-evolution-system\src\memory\storage.py'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the export_memories function and fix indentation
in_export = False
fix_start = None
fix_end = None

for i, line in enumerate(lines):
    if 'def export_memories' in line:
        in_export = True
        fix_start = i
    elif in_export and 'def ' in line and 'export_memories' not in line:
        # Next function found
        fix_end = i
        break

if fix_start and fix_end:
    print(f"Found export_memories at lines {fix_start+1}-{fix_end+1}")
    # The f.write lines inside for mem in memories: need to be indented
    for i in range(fix_start, fix_end):
        line = lines[i]
        # Lines that should be inside for loop (after for mem in memories:)
        if 'for mem in memories:' in line:
            lines[i] = '    for mem in memories:\n'
        elif 'f.write(f"INSERT OR REPLACE' in line:
            lines[i] = '        f.write(f"INSERT OR REPLACE INTO memories VALUES (\\n")\n'
        elif 'f.write(f" \'{mem.id}\'' in line:
            lines[i] = '        f.write(f" \'{mem.id}\',\\n")\n'
        elif 'f.write(f" \'{mem.type.value}\'' in line:
            lines[i] = '        f.write(f" \'{mem.type.value}\',\\n")\n'
        elif 'escaped = mem.content' in line:
            lines[i] = '        escaped = mem.content.replace("\'", "\'\'")\n'
        elif 'f.write(f" \'{escaped}\'' in line:
            lines[i] = '        f.write(f" \'{escaped}\',\\n")\n'
        elif 'f.write(f" NULL' in line and '压缩' in lines[i-1] if i > 0 else False:
            lines[i] = '        f.write(f" NULL,\\n")\n'
        elif 'f.write(f" \'{mem.timestamp' in line:
            lines[i] = '        f.write(f" \'{mem.timestamp.isoformat()}\',\\n")\n'
        elif 'f.write(f" \'{mem.session_id' in line:
            lines[i] = '        f.write(f" \'{mem.session_id}\',\\n")\n'
        elif 'f.write(f" {mem.importance.value}"' in line:
            lines[i] = '        f.write(f" {mem.importance.value},\\n")\n'
        elif 'f.write(f" \'{json.dumps(mem.associations)' in line:
            lines[i] = '        f.write(f" \'{json.dumps(mem.associations)}\',\\n")\n'
        elif 'f.write(f" \'{json.dumps(mem.tags)' in line:
            lines[i] = '        f.write(f" \'{json.dumps(mem.tags)}\',\\n")\n'
        elif 'f.write(f" \'{json.dumps(mem.metadata)' in line:
            lines[i] = '        f.write(f" \'{json.dumps(mem.metadata)}\',\\n")\n'
        elif 'f.write(f" {mem.access_count}' in line:
            lines[i] = '        f.write(f" {mem.access_count},\\n")\n'
        elif 'f.write(f" \'{mem.last_accessed' in line:
            lines[i] = '        f.write(f" \'{mem.last_accessed.isoformat()}\',\\n")\n'
        elif 'f.write(f" {mem.relevance_score}"' in line:
            lines[i] = '        f.write(f" {mem.relevance_score}\\n")\n'
        elif "f.write(');" in line:
            lines[i] = "        f.write(');\\n\\n')\n"
        elif "f.write('COMMIT" in line:
            lines[i] = "    f.write('COMMIT;\\n')\n"

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("Done!")