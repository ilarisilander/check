""" Module to handle the setup of all the data files"""
import os
import json

from pathlib import Path
from src.file_handler import JsonFile
from src.constants import APPDATA_DIR, SETTINGS_PATH, TODO_PATH, DELETED_DIR, JIRA_CONFIG_PATH


class Files:
    def __init__(self) -> None:
        self.todo_dict = {
            "id_count": 0,
            "todo": {},
            "active": {},
            "done": {}
        }
        self.settings_dict = {
            "lists": {
                "active": "",
                "inactive": []
            },
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
            "is_done": {
                "colors": {
                    "yes": "green",
                    "no": "red"
                }
            }
        }
        self.jira_config_dict = {
            "credentials": {
                "base_url": None,
                "api_token": None,
                "user_token": None
            },
            "project": {
                "id": None,
                "name": None
            },
            "assignee": {
                "name": None
            },
            "issuetype": {
                "story": {
                    "id": None,
                    "name": None,
                }
            },
            "leading_work_group": {
                "value": None,
                "id": None,
            },
            "transitions": {
                "todo": None,
                "in_progress": None,
                "done": None
            },
            "feature_link": None,
            "components": None
        }

    def ensure_appdata_dir(self):
        if not APPDATA_DIR.exists():
            APPDATA_DIR.mkdir(parents=True, exist_ok=True)
            print(f'Created an AppData directory in {APPDATA_DIR}')

    def ensure_deleted_dir(self):
        if not DELETED_DIR.exists():
            DELETED_DIR.mkdir(parents=True, exist_ok=True)
            print(f'Created delete directory in {DELETED_DIR}')

    def ensure_settings_file(self):
        if not SETTINGS_PATH.exists():
            SETTINGS_PATH.write_text(json.dumps(self.settings_dict))
            print(f'Created a new settings file in {SETTINGS_PATH}')
        else:  # If upgrading from old version, it might not have lists implemented
            settings_data = JsonFile.read(SETTINGS_PATH)
            if not "lists" in settings_data.keys():
                settings_data["lists"] = {
                    "active": "",
                    "inactive": []
                }
                JsonFile.write(SETTINGS_PATH, settings_data)
                print('Added lists section to settings')

    def ensure_todo_file(self) -> bool:
        if not os.path.exists(TODO_PATH):
            os.makedirs(TODO_PATH)
        has_files = any(TODO_PATH.iterdir())
        if not has_files:
            return False
        return True

    def ensure_jira_config_file(self):
        if not JIRA_CONFIG_PATH.exists():
            JIRA_CONFIG_PATH.write_text(json.dumps(self.jira_config_dict))
            print(f'Created a new Jira configuration file in {JIRA_CONFIG_PATH}')


if __name__ == '__main__':
    files = Files()
    files.ensure_appdata_dir()
    files.ensure_settings_file()
    files.ensure_todo_file()
