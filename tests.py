import os
import unittest
from unittest.mock import patch
import json
from script import Transaction, Budget, BudgetManager, BudgetService
from constants import TEST_DATA_FILE_NAME
from time import sleep
# from utils_parser import load_environ

# load_environ()

class TestCLIParser(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        cls.test_file = TEST_DATA_FILE_NAME
        cls.create_test_data()

    @classmethod
    def tearDownClass(cls):
        sleep(10)
        if os.path.exists(cls.test_file):
            os.remove(cls.test_file)

    @classmethod
    def create_test_data(cls):
        test_data = [
            {
                "date": "2024-05-01",
                "category": "Доход",
                "amount": "1000",
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

    @patch('script.FILE_NAME', TEST_DATA_FILE_NAME)
    def setUp(self) -> None:
        self.budget = Budget()
        
    @patch('script.FILE_NAME', TEST_DATA_FILE_NAME)
    def test_create_transaction(self):
        self.budget.objects.create(date='2024-05-03', category='Доход', amount=22000, description='test')
    
    @patch('script.FILE_NAME', TEST_DATA_FILE_NAME)
    def test_get_balance(self):
        self.budget.objects.get_balance()
        
    @patch('script.FILE_NAME', TEST_DATA_FILE_NAME)
    def test_get_income(self):
        self.budget.objects.get_income()
    
    @patch('script.FILE_NAME', TEST_DATA_FILE_NAME)
    def test_get_expenses(self):
        self.budget.objects.get_expenses()
    
    @patch('script.FILE_NAME', TEST_DATA_FILE_NAME)
    def test_filter(self):
        self.budget.objects.filter('Доход')
    
    @patch('script.FILE_NAME', TEST_DATA_FILE_NAME)
    def test_update(self):
        pass
    

if __name__ == '__main__':
    unittest.main()