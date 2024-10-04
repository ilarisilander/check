""" Module with all the constants """
import os
import datetime

from pathlib import Path


APP_VERSION = '0.1.12'


# PATHS
if os.name == 'nt':  # Windows
    APPDATA = Path(os.getenv('LOCALAPPDATA'))
else:
    APPDATA = os.path.expanduser('~/.local/share')
APPDATA_DIR = Path(APPDATA) / 'check' / 'data'
TODO_PATH = Path(APPDATA_DIR) / 'lists'
DELETED_DIR = Path(APPDATA_DIR) / 'deleted'
SETTINGS_PATH = Path(APPDATA_DIR) / 'todo_settings.json'
JIRA_SETTINGS_PATH = Path(APPDATA_DIR) / 'jira_configuration.json'

# DATES
CURRENT_DATE = str(datetime.date.today())
