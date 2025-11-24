from dataclasses import dataclass
import datetime
import json
import os
import pprint
from sqlite3.dbapi2 import Timestamp
import sys
from typing import Optional


@dataclass
class Task:
    id: int
    description: str
    status: str
    createdAt: datetime.datetime
    modifiedAt: Optional[datetime.datetime]


def task_to_json(task):
    return {
        "id": task.id,
        "description": task.description,
        "status": task.status,
        "createdAt": task.createdAt.isoformat(),
        "modifiedAt": task.modifiedAt.isoformat() if task.modifiedAt else None,
    }


def json_to_task(data):
    return Task(
        data["id"],
        data["description"],
        data["status"],
        datetime.datetime.fromisoformat(data["createdAt"]),
        datetime.datetime.fromisoformat(data["modifiedAt"])
        if data["modifiedAt"]
        else None,
    )


def task_add(cli_input):
    if len(cli_input) < 3:
        print("Wrogn input!")
        exit(1)

    tasks = get_data_from_file()
    last_id = max((task.id for task in tasks), default=0)
    new_task = Task(last_id + 1, cli_input[2], "to-do", Timestamp.now(), None)
    tasks.append(new_task)
    save_data_to_file(tasks)
    exit()


def task_update(cli_input):
    if len(cli_input) < 4:
        print("Wrogn input!")
        exit(1)

    task_id = int(cli_input[2])
    tasks = get_data_from_file()
    for index, task in enumerate(tasks):
        if task.id == task_id:
            new_task = Task(
                task.id,
                cli_input[3],
                task.status,
                task.createdAt,
                datetime.datetime.now()
            )
            tasks[index] = new_task
            save_data_to_file(tasks)
            print("Task succesfully updated")
            exit()
    print("Task not found")
    exit()


def task_delete(cli_input):
    if len(cli_input) < 3:
        print("Wrogn input!")
        exit(1)

    task_id = int(cli_input[2])
    tasks = get_data_from_file()
    for index, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(index)
            save_data_to_file(tasks)
            print("Task succesfully deleted")
            exit()
    print("Task not found")
    exit()


def task_change_status(cli_input):
    if len(cli_input) < 3:
        print("Wrogn input!")
        exit(1)

    status_split_list = cli_input[1].split("-")
    status = "-".join(status_split_list[1:])
    if status not in ['to-do', 'in-progress', 'done']:
        print("Wrogn status")
        exit(1)

    task_id = int(cli_input[2])
    tasks = get_data_from_file()
    for index, task in enumerate(tasks):
        if task.id == task_id:
            new_task = Task(
                task.id,
                task.description,
                status,
                task.createdAt,
                datetime.datetime.now()
            )
            tasks[index] = new_task
            save_data_to_file(tasks)
            print("Task status succesfully updated")
            exit()
    print("Task not found")
    exit()


def task_list(cli_input):
    
    if len(cli_input) < 2:
        print("Wrong input!")
        exit(1)
    
    tasks = get_data_from_file()
    if cli_input[2] not in ['to-do', 'in-progress', 'done']:
        print("Wrong status")
    if len(cli_input) == 3:        
        filtered_tasks = [task for task in tasks if task.status == cli_input[2]]
        pprint.pp(filtered_tasks)
        exit()
    pprint.pp(tasks)


def get_data_from_file() -> list[Task]:
    try:
        r = open("tasks.json", "r", encoding="utf-8")
        data = r.read()
        if len(data) == 0:
            return []
        json_data = json.loads(data)
        return [json_to_task(task_data) for task_data in json_data]
    except FileNotFoundError:
        with open("tasks.json", "w", encoding="utf-8") as w:
            w.write(json.dumps([]))
        return []


def save_data_to_file(tasks):
    json_data = [task_to_json(task_data) for task_data in tasks]
    with open("tasks.json", "w", encoding="utf-8") as w:
        w.write(json.dumps(json_data))


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    cli_input = sys.argv
    if len(cli_input) < 1:
        print("Invalid empty command!!")
        exit(1)

    command = cli_input[1]

    if command == "add":
        task_add(cli_input)
    elif command == "update":
        task_update(cli_input)
    elif command == "delete":
        task_delete(cli_input)
    elif command == "list":
        task_list(cli_input)
    elif "mark" in command:
        task_change_status(cli_input)
    print("Unknown command")