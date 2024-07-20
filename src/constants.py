""" Module with all the constants """
import os
import datetime
import json

from pathlib import Path


APP_VERSION = '0.1.4'


# PATHS
if os.name == 'nt':  # Windows
    APPDATA = Path(os.getenv('LOCALAPPDATA')) 
else:
    APPDATA = os.path.expanduser('~/.local/share')
APPDATA_DIR = Path(APPDATA) / 'check' / 'data'
TODO_PATH = Path(APPDATA_DIR) / 'lists'
SETTINGS_PATH = Path(APPDATA_DIR) / 'todo_settings.json'

# DATES
CURRENT_DATE = str(datetime.date.today())
