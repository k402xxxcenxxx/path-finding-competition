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
    task = Task(config_filepath=os.path.join(input_dir, "plaza.yaml"), num_item=2)

    print('Starting')
    start = time.time()
    task.init_algorithm(PlazaAlgorithm(task.env.map_data, task.target_list, task.start, task.end))

    print('-' * 10)

    print('Start simulation')
    task.run()
    duration = time.time() - start

    print("Completed simulation.")
    print(f"Total duration: {duration}")

    task.judge()
    
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
