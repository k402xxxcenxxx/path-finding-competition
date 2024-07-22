import json
from pprint import pformat
import time

def main():
    from plaza.task import Task
    from plaza.plaza_algorithm import PlazaAlgorithm
    print('Init environment')
    task = Task(config_filepath="assets/plaza.yaml", num_item=20)

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
    task.dump_path_image("path_image.png")

    result = task.get_result()
    result["duration"] = duration

    print("Result: ")
    print(pformat(result))

    with open("result.json", "w") as f:
        json.dump(result, f)
    print()

    print('Ingestion Program finished.')

    task.draw()

if __name__ == '__main__':
    main()
