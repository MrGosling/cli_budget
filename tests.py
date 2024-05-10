import json
import os
import time
import unittest
from subprocess import PIPE, Popen

from constants import FILE_NAME


class TestCLIParser(unittest.TestCase):
    """
    Класс для тестирования функционала парсера командной строки.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Метод для настройки классового окружения перед запуском тестов.
        """
        cls.backup_file_name: str = FILE_NAME + '.bak'

        if os.path.exists(FILE_NAME):
            os.rename(FILE_NAME, cls.backup_file_name)

        cls.transaction1: dict[str, str] = {
            'Дата': '2024-05-01',
            'Категория': 'Доход',
            'Сумма': '1000',
            'Описание': 'Зарплата'
        }

        cls.transaction2: dict[str, str] = {
            'Дата': '2024-05-02',
            'Категория': 'Расход',
            'Сумма': '500',
            'Описание': 'Покупки'
        }

        cls.to_find: dict[str, str] = {
            'Дата': '2024-05-03',
            'Категория': 'Доход',
            'Сумма': '1500',
            'Описание': 'Запись для поиска'
        }

        cls.to_update: dict[str, str] = {
            'Дата': '2024-05-04',
            'Категория': 'Расход',
            'Сумма': '100',
            'Описание': 'Запись для апдейта'
        }

        cls.to_create: dict[str, str] = {
            'Дата': '2024-05-03',
            'Категория': 'Доход',
            'Сумма': '2000',
            'Описание': 'Созданная запись'
        }

        cls.test_data: list[dict[str, str]] = [
            cls.transaction1,
            cls.transaction2,
            cls.to_find,
            cls.to_update
        ]

        with open(FILE_NAME, 'w') as file:
            json.dump(cls.test_data, file, ensure_ascii=False, indent=4)

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Метод для очистки классового окружения после выполнения всех тестов.
        """
        # введите в функцию sleep() значение в секундах больше ноля, если
        # хотите посмотреть файл с тестовыми данными.
        time.sleep(0)
        if os.path.exists(FILE_NAME):
            os.remove(FILE_NAME)

        if os.path.exists(cls.backup_file_name):
            os.rename(cls.backup_file_name, FILE_NAME)

    def setUp(self) -> None:
        """
        Метод для настройки окружения перед выполнением каждого теста.
        """
        with open(FILE_NAME, 'r') as file:
            data: list[dict[str, str]] = json.load(file)
        self.income: int = 0
        self.expenses: int = 0
        for item in data:
            if item['Категория'] == 'Доход':
                self.income += int(item['Сумма'])
            if item['Категория'] == 'Расход':
                self.expenses += int(item['Сумма'])
        self.balance: int = self.income - self.expenses

        base_command: list[str] = ['python3', 'cli_parser.py']
        self.balance_input: list[str] = base_command + ['--balance']
        self.income_input: list[str] = base_command + ['--income']
        self.expenses_input: list[str] = base_command + ['--expenses']
        self.create_input: list[str] = base_command + [
            '--create',
            'date=' + self.to_create['Дата'],
            'category=' + self.to_create['Категория'],
            'amount=' + self.to_create['Сумма'],
            'description=' + self.to_create['Описание']
        ]
        self.find_input: list[str] = base_command + [
            '--find',
            self.to_find['Описание']
        ]
        self.update_input: list[str] = base_command + [
            '--update',
            'date=' + self.to_update['Дата'],
            'category=' + self.to_update['Категория'],
            'amount=' + self.to_update['Сумма'],
            'description=' + self.to_update['Описание'],
            'new_date=2020-06-03',
            'new_category=Доход',
            'new_amount=5000',
            'new_description=not_new'
        ]

    def test_create_transaction(self) -> None:
        """
        Тест для функционала создания транзакции.
        """
        p = Popen(self.create_input, stdout=PIPE)
        stdout: bytes = None
        stderr: bytes = None
        stdout, stderr = p.communicate()
        output: str = stdout.decode('utf-8').strip()
        self.assertEqual(
            output,
            f"Создана новая запись: "
            f"{{'Дата': '{self.to_create['Дата']}', "
            f"'Категория': '{self.to_create['Категория']}', "
            f"'Сумма': '{self.to_create['Сумма']}', "
            f"'Описание': '{self.to_create['Описание']}'}}"
        )

    def test_find_transaction(self) -> None:
        """
        Тест для функционала поиска транзакции.
        """
        p = Popen(self.find_input, stdout=PIPE)
        stdout: bytes = None
        stderr: bytes = None
        stdout, stderr = p.communicate()
        output: str = stdout.decode('utf-8').strip()
        self.assertEqual(
            output,
            f"Вот, что удалось найти: "
            f"[{{'Дата': '{self.to_find['Дата']}', "
            f"'Категория': '{self.to_find['Категория']}', "
            f"'Сумма': '{self.to_find['Сумма']}', "
            f"'Описание': '{self.to_find['Описание']}'}}]"
        )

    def test_get_my_balance(self) -> None:
        """
        Тест для функционала получения баланса.
        """
        p = Popen(self.balance_input, stdout=PIPE)
        stdout: bytes = None
        stderr: bytes = None
        stdout, stderr = p.communicate()
        output: str = stdout.decode('utf-8').strip()
        self.assertEqual(output, f'Ваш баланс составляет {self.balance}')

    def test_get_my_expenses(self) -> None:
        """
        Тест для функционала получения расходов.
        """
        p = Popen(self.expenses_input, stdout=PIPE)
        stdout: bytes = None
        stderr: bytes = None
        stdout, stderr = p.communicate()
        output: str = stdout.decode('utf-8').strip()
        self.assertEqual(output, f'Ваши расходы составляют {self.expenses}')

    def test_get_my_income(self) -> None:
        """
        Тест для функционала получения доходов.
        """
        p = Popen(self.income_input, stdout=PIPE)
        stdout: bytes = None
        stderr: bytes = None
        stdout, stderr = p.communicate()
        output: str = stdout.decode('utf-8').strip()
        self.assertEqual(output, f'Ваши доходы составляют {self.income}')

    def test_update_transaction(self) -> None:
        """
        Тест для функционала обновления транзакции.
        """
        p = Popen(self.update_input, stdout=PIPE)
        stdout: bytes = None
        stderr: bytes = None
        stdout, stderr = p.communicate()
        output: str = stdout.decode('utf-8').strip()
        self.assertEqual(output, 'Запись успешно обновлена!')


if __name__ == '__main__':
    unittest.main()
