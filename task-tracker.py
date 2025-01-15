# Returns a list with the comand line arguments and the script name in the first index
import os
import json
from sys import argv
from datetime import datetime

# Creates a timezone class with the timezone code as argument.
from zoneinfo import ZoneInfo


LOCAL_TIMEZONE = ZoneInfo("America/Monterrey")


def is_json_created():
    files = os.listdir()

    if "tasks.json" in files:
        return

    else:
        with open("tasks.json", "w") as tasks_file:
            default = {"maxId": 0, "tasks": {}}
            tasks_file.write(json.dumps(default))


def create_task(description: str, status: str = "in_progress"):

    tasks_file = open("./tasks.json", "r")
    datetime_with_timezone = datetime.now(tz=LOCAL_TIMEZONE)

    file_content = json.loads(tasks_file.read())

    tasks_file.close()

    tasks_file = open("./tasks.json", "w")

    max_id = file_content["maxId"]

    tasks = file_content["tasks"]

    tasks[f"{max_id + 1}"] = (
        f'{{"description": "{description}", "status": "{status}", "createdAt": "{datetime_with_timezone.strftime("%d/%m/%Y %H:%M:%S")}", "updatedAt": "{datetime_with_timezone.strftime("%d/%m/%Y %H:%M:%S")}"}}'
    )

    file_content["maxId"] = max_id + 1

    tasks_file.write(json.dumps(file_content))

    tasks_file.close()


def get_tasks():
    with open("./tasks.json", "r") as tasks_file:
        file_content = json.loads(tasks_file.read())

        tasks = file_content["tasks"]

        for task in tasks.items():
            load_task = json.loads(task[1])
            print(f"{task[0]}: {load_task['description']} / created at: {load_task['createdAt']}")


def user_input(cli_arguments):
    input = cli_arguments

    command = input[1]

    if command == "add":
        task_description = input[2]
        create_task(task_description)

    elif command == "list":
        get_tasks()

    else:
        print("Unrecognized command.")


is_json_created()
user_input(argv)
