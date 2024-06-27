import json
from pprint import pformat
from plaza.task import Task

def main():
    task = Task(map_filepath="assets/simple.yaml", db_filepath="assets/plaza_data.json")

    task.run()

    result = task.get_result()

    print("Result:")
    print(pformat(result))
    
    with open("result.json", "w") as f:
        json.dump(result, f)

if __name__ == '__main__':
    main()
