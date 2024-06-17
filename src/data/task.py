import os
import sys
import json
import datetime

#from enums import Priority, Size
from ..helpers.file_handler import JsonFile

TODO_PATH = os.path.join('data', 'todo_list.json')
CURRENT_DATE = str(datetime.date.today())


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
            'is_done': False,
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
    def __init__(self) -> None:
        pass


class Update:
    def __init__(self) -> None:
        pass


class Delete:
    def __init__(self) -> None:
        pass



if __name__ == '__main__':
    create = Create('title', 'description', 'high', 'small', None)
    create.new_task()