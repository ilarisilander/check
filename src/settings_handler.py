""" Logic to handle processes for the settings """
import shutil
import re

from src.file_handler import JsonFile
from src.constants import SETTINGS_PATH, APPDATA_DIR, TODO_PATH, DELETED_DIR
from pathlib import Path


class Todo:
    """ Class to handle the list section of the settings """
    @staticmethod
    def is_valid_list_name(list_name: str) -> bool:
        pattern = r'^[a-z0-9]+(_[a-z0-9]+)*$'
        return bool(re.match(pattern, list_name))

    @staticmethod
    def get_active_todo_list() -> str:
        settings_data = JsonFile.read(SETTINGS_PATH)
        return settings_data['lists']['active']

    @staticmethod
    def get_inactive_todo_list() -> list:
        settings_data = JsonFile.read(SETTINGS_PATH)
        return settings_data['lists']['inactive']

    def get_todo_list_path(self, list_name: str) -> str:
        full_path = Path(APPDATA_DIR) / list_name + '.json'
        return full_path

    @staticmethod
    def create_todo_list(name: str):
        settings = JsonFile.read(SETTINGS_PATH)
        settings['lists']['inactive'].append(name)
        JsonFile.write(SETTINGS_PATH, settings)
        print(f'Todo list with the name {name} has been created')

    @staticmethod
    def remove_todo_list(name: str):
        settings = JsonFile.read(SETTINGS_PATH)
        settings['lists']['inactive'].remove(name)
        JsonFile.write(SETTINGS_PATH, settings)

    @staticmethod
    def remove_todo_file(name: str):
        """ Move the 'deleted' directory to have a bit of a backup """
        file_path = Path(TODO_PATH) / (name + '.json')
        destination_path = Path(DELETED_DIR) / (name + '.json')
        shutil.move(str(file_path), str(destination_path))

    @staticmethod
    def is_active_list(name: str) -> bool:
        settings = JsonFile.read(SETTINGS_PATH)
        if settings['lists']['active'] == name:
            print(f'{name} is already the active list')
            return True
        return False

    @staticmethod
    def list_exists(list_name: str) -> bool:
        settings = JsonFile.read(SETTINGS_PATH)
        for _, value in settings['lists'].items():
            if isinstance(value, list):
                for each in value:
                    if each == list_name:
                        return True
            elif value == list_name:
                return True
        return False

    @staticmethod
    def change_active_todo_list(new_list):
        settings = JsonFile.read(SETTINGS_PATH)
        old_active = settings['lists']['active']
        if not old_active == "":
            settings['lists']['inactive'].append(old_active)  # Move old active to inactive
        settings['lists']['active'] = new_list  # Activate new list as active
        settings['lists']['inactive'].remove(new_list)  # Remove the new active from the inactive list
        JsonFile.write(SETTINGS_PATH, settings)
        print(f'{new_list} is now the active list')


if __name__ == '__main__':
    pass