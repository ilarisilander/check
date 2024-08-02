""" """
import unittest
from unittest.mock import patch, mock_open
from src.validate import Deadline
from src.constants import CURRENT_DATE


class TestDeadline(unittest.TestCase):

    def test_is_correct_format_return_true(self):
        deadline = '2124-08-03'
        expected = True
        actual = Deadline.is_corret_format(deadline)
        self.assertEqual(expected, actual)

    def test_is_correct_format_return_false(self):
        deadline = '2020'
        expected = False
        actual = Deadline.is_corret_format(deadline)
        self.assertEqual(expected, actual)

    def test_is_newer_than_old_date_return_true(self):
        deadline = '2124-08-02'
        expected = True
        actual = Deadline.is_newer_than_old_date(deadline)
        self.assertEqual(expected, actual)

    def test_is_newer_than_old_date_return_false(self):
        deadline = '2020-01-01'
        expected = False
        actual = Deadline.is_newer_than_old_date(deadline)
        self.assertEqual(expected, actual)
