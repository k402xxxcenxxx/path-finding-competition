import json
import os

result_dir = "/app/input/res"
score_dir = '/app/output/'

print('Reading result')
with open(os.path.join(result_dir, "result.json"), "r") as f:
    json_data = json.load(f)
    total_step = json_data.get("total_step", -1)
    duration = json_data.get("duration", -1)
    is_valid = json_data.get("is_valid", False)
    is_finish = json_data.get("is_finish", False)
    item_list = json_data.get("item_list", False)

print('Scores:')
scores = {
    "item_list": item_list,
    "duration": duration,
    "is_valid": is_valid,
    "is_finish": is_finish,
    "total_step": total_step,
}
print(scores)

with open(os.path.join(score_dir, "scores.json"), "w") as score_file:
    score_file.write(json.dumps(scores))
