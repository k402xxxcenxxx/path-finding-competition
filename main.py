import json
from pprint import pformat
import time

def main():
    from plaza.task import Task
    from plaza.plaza_algorithm import PlazaAlgorithm
    print('Init environment')
    task = Task(map_filepath="assets/plaza.yaml", db_filepath="assets/plaza_data.json")

    print('Starting')
    start = time.time()
    task.init_algorithm(PlazaAlgorithm(task.db, task.target_list))

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

    with open("result.json", "w") as f:
        json.dump(result, f)
    print()

    print('Ingestion Program finished.')

if __name__ == '__main__':
    main()
