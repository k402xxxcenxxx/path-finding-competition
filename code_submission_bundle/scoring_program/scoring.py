import json
import os

result_dir = os.path.join("/app/input/")
score_dir = '/app/output/'


import os

def list_files(start_path):
    for root, dirs, files in os.walk(start_path):
        level = root.replace(start_path, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print(f"{indent}{os.path.basename(root)}/")
        sub_indent = ' ' * 4 * (level + 1)
        for file in files:
            print(f"{sub_indent}{file}")
        for dir in dirs:
            list_files(os.path.join(root, dir))

# Replace 'your/path' with the path you want to list
list_files('/app')

print('Reading result')
with open(os.path.join(result_dir, "result.json")) as f:
    efficiency = json.load(f).get("efficiency", -1)
    duration = json.load(f).get("duration", -1)

print('Scores:')
scores = {
    "efficiency": efficiency,
    "duration": duration
}
print(scores)

with open(os.path.join(score_dir, "scores.json"), "w") as score_file:
    score_file.write(json.dumps(scores))
