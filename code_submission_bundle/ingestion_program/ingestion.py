import json
from pprint import pformat
import time
import sys
import os

module_path = '/app/'
input_dir = '/app/input_data/'
output_dir = '/app/output/'
submission_dir = '/app/ingested_program'

sys.path.append(module_path)
sys.path.append(submission_dir)

def main():
    from plaza.task import Task
    from plaza.plaza_algorithm import PlazaAlgorithm
    print('Init environment')
    task = Task(config_filepath=os.path.join(input_dir, "plaza.yaml"))

    print('Starting')
    start = time.time()
    task.init_algorithm(PlazaAlgorithm(task.env.maps, task.target_list, task.start, task.start_level, task.end, task.end_level))

    print('-' * 10)

    print('Start simulation')
    task.run()
    duration = time.time() - start

    print("Completed simulation.")
    print(f"Total duration: {duration}")

    task.judge()
    task.dump_path_image(os.path.join(output_dir, "path.png"))

    result = task.get_result()
    result["duration"] = duration

    print("Result: ")
    print(pformat(result))

    with open(os.path.join(output_dir, "result.json"), "w") as f:
        json.dump(result, f)
    print()

    print('Ingestion Program finished.')

if __name__ == '__main__':
    main()
