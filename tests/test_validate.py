""" """
import unittest
from unittest.mock import patch, mock_open
from src.validate import Priority, Size
from src.constants import CURRENT_DATE


class TestPriority(unittest.TestCase):

    @patch('src.validate.JsonFile.read')
    def test_is_valid_option(self, mock_read):
        """ Test that the is_valid_option returns True if the option is valid """
        mock_read.return_value = {
            "priority": {
                "colors": {
                    "low": "green",
                    "medium": "yellow",
                    "high": "red",
                    "critical": "red"
                }
            }
        }
        self.assertTrue(Priority.is_valid_option('low'))
        self.assertTrue(Priority.is_valid_option('medium'))
        self.assertTrue(Priority.is_valid_option('high'))
        self.assertTrue(Priority.is_valid_option('critical'))


class TestSize(unittest.TestCase):

    @patch('src.validate.JsonFile.read')
    def test_is_valid_option(self, mock_read):
        """ Test that the is_valid_option returns True if the option is valid """
        with patch('src.validate.JsonFile.read') as mock_read:
            mock_read.return_value = {
                "size": {
                    "colors": {
                        "small": "green",
                        "medium": "yellow",
                        "large": "red"
                    }
                }
            }
            self.assertTrue(Size.is_valid_option('small'))
            self.assertTrue(Size.is_valid_option('medium'))
            self.assertTrue(Size.is_valid_option('large'))