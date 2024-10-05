""" Module to handle validations """
from src.file_handler import JsonFile
from src.constants import SETTINGS_PATH


class Priority:

    @staticmethod
    def is_valid_option(option: str) -> bool:
        """ Check that the option is a valid option

        The input should be in the check settings json file
        """
        settings = JsonFile.read(SETTINGS_PATH)
        valid_options = settings['priority']['colors']

        if option not in valid_options:
            return False
        return True


class Size:

    @staticmethod
    def is_valid_option(option: str) -> bool:
        """ Check that the option is a valid option """
        settings = JsonFile.read(SETTINGS_PATH)
        valid_options = settings['size']['colors']

        if option not in valid_options:
            return False
        return True