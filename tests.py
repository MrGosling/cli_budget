import os
from pathlib import Path
import unittest
from unittest.mock import patch, MagicMock, Mock
import json
import script
# from script import Transaction, Budget, BudgetManager, BudgetService#, set_filename
from constants import TEST_DATA_FILE_NAME#, FILE_NAME
from time import sleep
# from utils import load_environ

# load_environ()

class TestCLIParser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_file = TEST_DATA_FILE_NAME
        cls.db = cls.create_test_data()
        sleep(1)

    @classmethod
    def tearDownClass(cls):
        sleep(5)
        if os.path.exists(cls.test_file):
            os.remove(cls.test_file)

    @classmethod
    def create_test_data(cls):
        test_data = [
            {
                "date": "2024-05-01",
                "category": "Доход",
                "amount": "1000",
                "description": "Зарплата"
            },
            {
                "date": "2024-05-02",
                "category": "Расход",
                "amount": "500",
                "description": "Покупки"
            },
            {
                "date": "2024-05-03",
                "category": "Доход",
                "amount": "1500",
                "description": "Зарплата"
            },
            {
                "date": "2024-05-04",
                "category": "Расход",
                "amount": "100",
                "description": "Покупки"
            }
        ]

        with open(cls.test_file, 'w') as file:
            json.dump(test_data, file, ensure_ascii=False, indent=4)


    def setUp(self) -> None:
        pass

if __name__ == '__main__':
    unittest.main()