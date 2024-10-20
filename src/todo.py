""" Handle the todo lists """
from pathlib import Path
from src.settings_handler import Todo
from src.file_handler import JsonFile
from src.constants import TODO_PATH


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
        for category, value in list_content.items():
            if category == 'id_count':
                continue
            if task_id in value:
                task = list_content[category][task_id]
                if 'issue' not in task:
                    return None
                return list_content[category][task_id]['issue']
        return None
