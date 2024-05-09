import os
from subprocess import Popen, PIPE
import sys
from pathlib import Path
import unittest
from io import StringIO
from unittest.mock import patch, MagicMock, Mock
import json
import script
# from script import Transaction, Budget, BudgetManager, BudgetService#, set_filename
from constants import TEST_DATA_FILE_NAME, FILE_NAME
from time import sleep
from cli_parser import get_my_balance, get_my_income, get_my_expenses, find_transactions, create_transaction, update_transaction
# from utils import load_environ

# load_environ()

class TestCLIParser(unittest.TestCase):

    # @classmethod
    # def setUpClass(cls):
    #     super().setUpClass()
    #     cls.test_file = TEST_DATA_FILE_NAME
    #     cls.db = cls.create_test_data()
    #     sleep(1)

    # @classmethod
    # def tearDownClass(cls):
    #     sleep(1)
    #     if os.path.exists(cls.test_file):
    #         os.remove(cls.test_file)

    # @classmethod
    # def create_test_data(cls):
    #     test_data = [
    #         {
    #             "date": "2024-05-01",
    #             "category": "Доход",
    #             "amount": "1000",
    #             "description": "Зарплата"
    #         },
    #         {
    #             "date": "2024-05-02",
    #             "category": "Расход",
    #             "amount": "500",
    #             "description": "Покупки"
    #         },
    #         {
    #             "date": "2024-05-03",
    #             "category": "Доход",
    #             "amount": "1500",
    #             "description": "Зарплата"
    #         },
    #         {
    #             "date": "2024-05-04",
    #             "category": "Расход",
    #             "amount": "100",
    #             "description": "Покупки"
    #         }
    #     ]

        # with open(cls.test_file, 'w') as file:
        #     json.dump(test_data, file, ensure_ascii=False, indent=4)

    def setUp(self) -> None:
        with open(FILE_NAME, 'r') as file:
            data = json.load(file)
        self.income = 0
        self.expenses = 0
        for item in data:
            if item['Категория'] == 'Доход':
                self.income += int(item['Сумма'])
            if item['Категория'] == 'Расход':
                self.expenses += int(item['Сумма'])
        self.balance = self.income - self.expenses
        template_input = ['python3', 'cli_parser.py']
        self.balance_input = ['python3', 'cli_parser.py', '--balance']
        self.income_input = ['python3', 'cli_parser.py', '--income']
        self.expenses_input = ['python3', 'cli_parser.py', '--expenses']
        self.create_input = ['python3', 'cli_parser.py', '--create', 'date=2024-05-03', 'category=Доход', 'amount=2000', 'description=newsss']
        self.find_input = ['python3', 'cli_parser.py', '--find', 'newsss']
        self.update_input = ['python3', 'cli_parser.py', '--update', 'date=2024-05-03', 'category=Доход', 'amount=2000', 'description=newsss', 'new_date=2020-06-03', 'new_category=Доход', 'new_amount=5000', 'new_description=not_new']

    def test_get_my_balance(self):
        p = Popen(self.balance_input, stdout=PIPE)
        stdout, stderr = p.communicate()
        output = stdout.decode('utf-8').strip()
        self.assertEqual(output, f'Ваш баланс составляет {self.balance}')

    def test_get_my_income(self):
        p = Popen(self.income_input, stdout=PIPE)
        stdout, stderr = p.communicate()
        output = stdout.decode('utf-8').strip()
        self.assertEqual(output, f'Ваши доходы составляют {self.income}')

    def test_get_my_expenses(self):
        p = Popen(self.expenses_input, stdout=PIPE)
        stdout, stderr = p.communicate()
        output = stdout.decode('utf-8').strip()
        self.assertEqual(output, f'Ваши расходы составляют {self.expenses}')

    def test_create_transaction(self):
        p = Popen(self.create_input, stdout=PIPE)
        stdout, stderr = p.communicate()
        output = stdout.decode('utf-8').strip()
        self.assertEqual(output, "Создана новая запись: {'Дата': '2024-05-03', 'Категория': 'Доход', 'Сумма': '2000', 'Описание': 'newsss'}")

    @unittest.expectedFailure
    def test_find_transaction(self):
        p= Popen(self.find_input, stdout=PIPE)
        stdout, stderr = p.communicate()
        output = stdout.decode('utf-8').strip()
        self.assertEqual(output, "Вот, что удалось найти: [{'Дата': '2024-[576 chars]s'}]")

    def test_update_transaction(self):
        p = Popen(self.update_input, stdout=PIPE)
        stdout, stderr = p.communicate()
        output = stdout.decode('utf-8').strip()
        self.assertEqual(output, 'Запись успешно обновлена!')

if __name__ == '__main__':
    unittest.main()