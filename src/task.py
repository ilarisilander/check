""" Module to handle all the tasks (create, read, update, delete) """

import os
import json

from constants import TODO_PATH, CURRENT_DATE
from rich.console import Console
from file_handler import JsonFile
from view import Display


class Create:
    def __init__(self, title:str, description: str, priority, size, deadline):
        self.title = title
        self.description = description
        self.priority = priority
        self.size = size
        self.deadline = deadline

    def new_task(self):
        """ Create a new task and add it to the todo_list.json file
        
        The task will contain a unique ID, a DESCRIPTION, PRIORITY,
        SIZE and DEADLINE.
        """
        if not os.path.exists(TODO_PATH):
            # TODO: Log creation of the todo file
            os.makedirs(os.path.dirname(TODO_PATH), exist_ok=True)
            # TODO: Log successful
            self._setup_todo_list()
        todo_dict = JsonFile.read(TODO_PATH)
        new_todo_dict = self._add_task_to_todo(todo_dict)
        JsonFile.write(TODO_PATH, new_todo_dict)

    def _add_task_to_todo(self, todo: dict) -> dict:
        """ Add a new task to the old todo dict and return a new dict """
        task_id = todo['id_count'] + 1
        task_data = {
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'size': self.size,
            'create_date': CURRENT_DATE,
            'done_date': None,
            'is_done': "no",
            'deadline': self.deadline
        }
        todo['id_count'] = task_id
        todo['todo'][task_id] = task_data
        return todo

    def _setup_todo_list(self) -> None:
        """ Setup the todo list with default keys and values """
        print(f'Setting up {TODO_PATH} with default keys and values')
        default_dict = {
            'id_count': 0,
            'todo': {},
            'in_progress': {},
            'done': {}
        }
        with open(TODO_PATH, 'w', encoding='utf-8') as file:
            json.dump(default_dict, file, indent=4)


class Read:
    """ Class to handle the reading of the tasks """
    def __init__(self) -> None:
        self.console = Console()
        self.display = Display()

    def tasks(self, flag: str) -> None:
        if flag == 'all':
            self._all_tasks()
        elif flag == 'in_progress':
            self._in_progress_tasks()
        elif flag == 'todo':
            self._todo_tasks()
        elif flag == 'done':
            self._done_tasks()

    def _all_tasks(self):
        self.display.tasks('todo')
        self.display.tasks('in_progress')
        self.display.tasks('done')

    def _in_progress_tasks(self):
        self.display.tasks('in_progress')

    def _todo_tasks(self):
        self.display.tasks('todo')

    def _done_tasks(self):
        self.display.tasks('done')

class Update:
    def __init__(self) -> None:
        pass


class Delete:

    def task(self, id: str) -> None:
        """ Delete a specific task from the todo list
        
        Task is based on the task ID
        """
        todo_dict = JsonFile.read(TODO_PATH)
        new_todo_dict = self._delete_task_from_todo(id, todo_dict)
        JsonFile.write(TODO_PATH, new_todo_dict)

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
    create = Create('title', 'description', 'high', 'small', None)
    create.new_task()