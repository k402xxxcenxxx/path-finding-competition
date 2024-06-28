import json
from pprint import pformat
import time
import sys
import os

module_path = '/app/plaza/'
input_dir = '/app/input_data/'
output_dir = '/app/output/'

sys.path.append(module_path)

def main():
    from plaza.task import Task
    print('Init environment')
    task = Task(map_filepath=os.path.join(input_dir, "plaza.yaml"),
                db_filepath=os.path.join(input_dir, "plaza_data.json"))

    print('Starting')
    start = time.time()
    task.init_algorithm()

    print('-' * 10)

    print('Start simulation')
    task.run()
    duration = time.time() - start

    print("Completed simulation.")
    print(f"Total duration: {duration}")
    
    result = task.get_result()
    result["duration"] = duration

    print("Result: ")
    print(pformat(result))

    with open(os.path.join(output_dir, "result.json"), 'w+') as f:
        json.dump(result, f)
    print()

    print('Ingestion Program finished.')

if __name__ == '__main__':
    main()
