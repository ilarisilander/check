""" """
import unittest
from unittest.mock import patch, mock_open
from src.task import Create, Read, Update, Delete


class TestCreate(unittest.TestCase):
    def setUp(self) -> None:
        create = Create()

    