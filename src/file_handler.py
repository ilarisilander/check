""" Thif module handles file operations """
import json
from pathlib import Path


class JsonFile:

    @staticmethod
    def read(file_path: str) -> dict:
        """ Read a json file and return the data as a dict

        :param file_path: str
            Path to the json file
        :return: dict
            The json data in dict format
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    @staticmethod
    def write(file_path: str, new_data: dict) -> None:
        assert isinstance(new_data, dict), 'new_data must be a dictionary'
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(new_data, file, indent=4)

    @staticmethod
    def get_all_tasks(todo: dict) -> dict:
        todo.pop('id_count')
        return todo

    @staticmethod
    def create_todo_file(file_path, name):
        placeholder_data = {
            "id_count": 0,
            "todo": {},
            "active": {},
            "done": {}
        }
        json_path = Path(file_path) / (name + '.json')
        json_path.parent.mkdir(parents=True, exist_ok=True)  # Create if it does not exist
        with open(json_path, 'w', encoding='utf-8') as file:
            json.dump(placeholder_data, file, ensure_ascii=False, indent=4)
