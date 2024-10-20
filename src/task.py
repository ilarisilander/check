""" Module to handle all the tasks (create, read, update, delete) """

import os
import json

from pathlib import Path
from src.constants import TODO_PATH, CURRENT_DATE
from rich.console import Console
from src.file_handler import JsonFile
from src.view import Display
from src.settings_handler import Todo


# ACTIVE_LIST_PATH = Path(TODO_PATH) / (Todo.get_active_todo_list() + '.json')


class Create:
    """ Creation of tasks """
    def __init__(self, title: str, description: str, priority, size, issue):
        self.title = title
        self.description = description
        self.priority = priority
        self.size = size
        self.issue = issue
        self.active_list_path = Path(TODO_PATH) / (Todo.get_active_todo_list() + '.json')

    def new_task(self):
        """ Create a new task and add it to the todo_list.json file

        The task will contain a unique ID, a DESCRIPTION, PRIORITY and SIZE
        """
        todo_dict = JsonFile.read(self.active_list_path)
        new_todo_dict = self._add_task_to_todo(todo_dict)
        JsonFile.write(self.active_list_path, new_todo_dict)

    def _add_task_to_todo(self, todo: dict) -> dict:
        """ Add a new task to the old todo dict and return a new dict """
        task_id = todo['id_count'] + 1
        task_data = {
            'issue': self.issue,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'size': self.size,
            'create_date': CURRENT_DATE,
            'done_date': None,
            'is_done': "no",
        }
        todo['id_count'] = task_id
        todo['todo'][task_id] = task_data
        return todo

    def _setup_todo_list(self) -> None:
        """ Setup the todo list with default keys and values """
        print(f'Setting up {self.active_list_path} with default keys and values')
        default_dict = {
            'id_count': 0,
            'todo': {},
            'active': {},
            'done': {}
        }
        with open(self.active_list_path, 'w', encoding='utf-8') as file:
            json.dump(default_dict, file, indent=4)


class Read:
    """ Class to handle the reading of the tasks """
    def __init__(self) -> None:
        self.console = Console()
        self.display = Display()
        self.active_list_path = Path(TODO_PATH) / (Todo.get_active_todo_list() + '.json')

    def tasks(self, flag: str) -> None:
        if flag == 'all':
            self._all_tasks()
        elif flag == 'active':
            self._active_tasks()
        elif flag == 'todo':
            self._todo_tasks()
        elif flag == 'done':
            self._done_tasks()

    def _all_tasks(self):
        self.display.tasks('todo')
        self.display.tasks('active')
        self.display.tasks('done')

    def _active_tasks(self):
        self.display.tasks('active')

    def _todo_tasks(self):
        self.display.tasks('todo')

    def _done_tasks(self):
        self.display.tasks('done')

    def search_task(self, **search_criteria):
        # TODO: This differs from the private functions above, refactor to look the same
        todo_dict = JsonFile.read(self.active_list_path)
        filtered_todo_dict = {}
        for category, tasks in todo_dict.items():
            if category != 'id_count':
                for task_id, task_values in tasks.items():
                    if self._filter_by_criteria(task_values, **search_criteria):
                        filtered_todo_dict[task_id] = task_values
        self.display.filtered_tasks(filtered_todo_dict)

    def _filter_by_criteria(self, task: dict, **search_criteria) -> bool:
        for option, criteria in search_criteria.items():
            if not str(criteria).lower() in str(task[option]).lower():
                return False
        return True

class Update:
    """ Handle all the changes made to an already existing task """
    def __init__(self) -> None:
        self.active_list_path = Path(TODO_PATH) / (Todo.get_active_todo_list() + '.json')

    def start_task(self, task_id: str) -> None:
        """ The task is moved from 'todo' to 'active' """
        todo_dict = JsonFile.read(self.active_list_path)
        if task_id in todo_dict['todo']:
            todo_dict['active'][task_id] = todo_dict['todo'][task_id]
            todo_dict['todo'].pop(task_id)
            JsonFile.write(self.active_list_path, todo_dict)
            print(f'Task with ID: {task_id} was moved to "active"')
        else:
            print(f'There is no task with ID: {task_id} in "todo"')

    def end_task(self, task_id: str):
        todo_dict = JsonFile.read(self.active_list_path)
        for category, task in todo_dict.items():
            if category != 'id_count' and task_id in task.keys():
                if category != 'done':
                    todo_dict['done'][task_id] = todo_dict[category][task_id]
                    todo_dict['done'][task_id]['done_date'] = CURRENT_DATE
                    todo_dict['done'][task_id]['is_done'] = "yes"
                    todo_dict[category].pop(task_id)
                    JsonFile.write(self.active_list_path, todo_dict)
                    print(f'Task with ID: {task_id} was moved to "done"')
                    return
                else:
                    print(f'Task with ID: {task_id} is already done')

    def change_task(self, id, **kwargs):
        todo_dict = JsonFile.read(self.active_list_path)
        for category, task in todo_dict.items():
            if category != 'id_count' and id in task.keys():
                for key_to_change, value in kwargs.items():
                    todo_dict[category][id][key_to_change] = value
                    print(f'Changed {key_to_change} to {value}')
        JsonFile.write(self.active_list_path, todo_dict)

    def move_task(self, id, destination):
        todo_dict = JsonFile.read(self.active_list_path)
        for category, tasks in todo_dict.items():
            if category != 'id_count' and id in tasks.keys():
                todo_dict[destination][id] = tasks[id]
                if not id in todo_dict[destination]:
                    print(f'Task with ID: {id} was not moved to {destination}')
                    return
                if category == 'done':
                    todo_dict[destination][id]['is_done'] = 'no'
                    todo_dict[destination][id]['done_date'] = None
                todo_dict[category].pop(id)
                JsonFile.write(self.active_list_path, todo_dict)
                print(f'Task with ID: {id} was moved to {destination}')
                return
        print(f'Task with ID: {id} was not found in the list')


class Delete:
    def __init__(self) -> None:
        self.active_list_path = Path(TODO_PATH) / (Todo.get_active_todo_list() + '.json')

    def task(self, id: str) -> None:
        """ Delete a specific task from the todo list

        Task is based on the task ID
        """
        todo_dict = JsonFile.read(self.active_list_path)
        for category, tasks in todo_dict.items():
            if category != 'id_count' and id in tasks.keys():
                todo_dict[category].pop(id, None)
        JsonFile.write(self.active_list_path, todo_dict)
        print(f'Task with ID: {id} was removed from the list')

    @staticmethod
    def _delete_task_from_todo(id: str, todo: dict) -> dict:
        if id in todo['todo']:
            todo['todo'].pop(id, None)
            print(f'Task with ID: {id} was removed from the list')
        else:
            print(f'{id} not in todo list')
        # TODO: Iterate through all levels to look for the ID
        return todo


if __name__ == '__main__':
    pass
