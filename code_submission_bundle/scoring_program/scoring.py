import json
import os

reference_dir = os.path.join('/app/input/', 'ref')
prediction_dir = os.path.join('/app/input/', 'res')
score_dir = '/app/output/'

print('Reading result')
with open(os.path.join(prediction_dir, "result.json")) as f:
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
