""" Module with all the constants """
import os
import datetime
from pathlib import Path


APP_VERSION = '0.1.3'

# PATHS
if os.name == 'nt':  # Windows
    APPDATA = Path(os.getenv('LOCALAPPDATA')) 
else:
    APPDATA = os.path.expanduser('~/.local/share')
APPDATA_DIR = Path(APPDATA) / 'check' / 'data'
SETTINGS_PATH = Path(APPDATA_DIR) / 'todo_settings.json'
TODO_PATH = Path(APPDATA_DIR) / 'todo_list.json'

# DATES
CURRENT_DATE = str(datetime.date.today())
