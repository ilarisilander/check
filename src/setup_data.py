""" Module to handle the setup of all the data files"""
import os
import json

from src.constants import APPDATA_DIR, SETTINGS_PATH, TODO_PATH
from pathlib import Path


class Files:
    def __init__(self) -> None:
        self.todo_dict = {
            "id_count": 0,
            "todo": {},
            "in_progress": {},
            "done": {}
        }
        self.settings_dict = {
            "priority": {
                "colors": {
                    "low": "green",
                    "medium": "yellow",
                    "high": "red",
                    "critical": "red"
                }
            },
            "size": {
                "colors": {
                    "small": "green",
                    "medium": "yellow",
                    "large": "red"
                }
            },
            "deadline": {
                "colors": {
                    "critical": "red",
                    "urgent": "yellow",
                    "healthy": "green",
                    "None": "white"
                },
                "warning": {
                    "critical": 0.2,
                    "urgent": 0.4
                }
            },
            "is_done": {
                "colors": {
                    "yes": "green",
                    "no": "red"
                }
            }
        }

    def ensure_appdata_dir(self):
        if not APPDATA_DIR.exists():
            APPDATA_DIR.mkdir(parents=True, exist_ok=True)
            print(f'Created an AppData directory in {APPDATA_DIR}')

    def ensure_settings_file(self):
        if not SETTINGS_PATH.exists():
            SETTINGS_PATH.write_text(json.dumps(self.settings_dict))
            print(f'Created a new settings file in {SETTINGS_PATH}')

    def ensure_todo_file(self):
        if not TODO_PATH.exists():
            TODO_PATH.write_text(json.dumps(self.todo_dict))
            print(f'Created a new todo list file in {TODO_PATH}')


if __name__ == '__main__':
    files = Files()
    files.ensure_appdata_dir()
    files.ensure_settings_file()
    files.ensure_todo_file()