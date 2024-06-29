import json
import os

result_dir = "/app/input/res"
score_dir = '/app/output/'

print('Reading result')
with open(os.path.join(result_dir, "result.json"), "r") as f:
    json_data = json.load(f)
    accomplishment_rate = json_data.get("accomplishment_rate", -1)
    total_step = json_data.get("total_step", -1)
    duration = json_data.get("duration", -1)

print('Scores:')
scores = {
    "accomplishment_rate": accomplishment_rate,
    "total_step": total_step,
    "duration": duration
}
print(scores)

with open(os.path.join(score_dir, "scores.json"), "w") as score_file:
    score_file.write(json.dumps(scores))
