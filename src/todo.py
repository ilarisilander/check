""" Handle the todo lists """
from src.settings_handler import Todo
from src.file_handler import JsonFile
from src.constants import TODO_PATH
from pathlib import Path


class List:
    @staticmethod
    def get_issue_from_task(task_id: str) -> str:
        """ Get the issue from a task

        :param task_id: The ID of the task
        :return: The issue Jira issue of the task
        """
        active_list_name = Todo.get_active_todo_list()
        list_path = Path(TODO_PATH) / (active_list_name + '.json')
        list_content = JsonFile.read(list_path)
        task = list_content['todo'][task_id]
        if 'issue' not in task:
            return 'None'
        return list_content['todo'][task_id]['issue']
