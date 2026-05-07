import os
print("=== self-evolution-system/src ===")
ses = "D:/OpenClaw_Main/workspace/self-evolution-system"
for root, dirs, files in os.walk(ses):
    for f in files:
        if not f.endswith('.pyc'):
            print(os.path.relpath(os.path.join(root, f), ses))
print()
print("=== complete-self-evolution/src ===")
ce = "D:/OpenClaw_Main/workspace/complete-self-evolution"
if os.path.exists(ce):
    for root, dirs, files in os.walk(ce):
        for f in files:
            if not f.endswith('.pyc'):
                print(os.path.relpath(os.path.join(root, f), ce))
else:
    print("Directory does not exist")