import os
from datetime import datetime
import json
# from constants import FILE_NAME#, TEST_DATA_FILE_NAME
from enum import Enum
from utils import load_environ
FILE_NAME = 'data.json'
load_environ()
def set_filename():
    return FILE_NAME

class Transaction:
    @classmethod
    def get_transaction_type(cls, transaction_type: str) -> 'Transaction.TransactionType':
        if transaction_type.title() == 'Доход':
            return cls.TransactionType.INCOME
        elif transaction_type.title() == 'Расход':
            return cls.TransactionType.EXPENSES
        else:
            raise ValueError(
                'Неправильная категория, можно выбрать Доход или Расход'
            )

    class TransactionType(Enum):
        INCOME = 'Доход'
        EXPENSES = 'Расход'

    def __init__(self, date: str, category: str, amount: str, description: str):
        self.date: str = date
        self.category: Transaction.TransactionType = self.get_transaction_type(category)
        self.amount: int = int(amount)
        self.description: str = description

    def to_dict(self) -> dict[str, str]:
        return {
            'Дата': self.date,
            'Категория': self.category.value,
            'Сумма': str(self.amount),
            'Описание': self.description,
        }


class BudgetService:

    @staticmethod
    def load(filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
            with open(filename, 'w') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        return data

    @staticmethod
    def write(data, filename):
        try:
            with open(filename, 'w') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except FileNotFoundError:
            return


class BudgetManager:
    def __init__(self, data: list[Transaction]):
        self.data: list[Transaction] = data

    def _get_index(self, date, category, amount, description) -> int | None:
        obj: Transaction = None
        category_type = Transaction.get_transaction_type(category)
        for index, obj in enumerate(self.data):
            if obj.date == date and obj.category == category_type and obj.amount == amount and obj.description == description:
                return index
        print('Не удалось найти запись для обновления')

    def _save_data(self) -> None:
        data_to_save: list[dict[str, str]] = [transaction.to_dict() for transaction in self.data]
        Budget.save(data=data_to_save)

    def create(self, date, category, amount, description) -> str:
        new_entry = Transaction(date, category, amount, description)
        self.data.append(new_entry)
        self._save_data()
        return print(f'Создана новая запись: {new_entry.to_dict()}')

    def filter(self, *args) -> str:
        if not self.data:
            raise FileNotFoundError('Файл не найден или в нём отсутствуют записи!')
        result: list[dict[str, str]] = []
        for item in self.data:
            flag = True
            for arg in args:
                if arg not in item.to_dict().values():
                    flag = False
                    break
            if flag:
                result.append(item.to_dict())
        return (
            print(f'Вот, что удалось найти: {result}') if result != [] else
            print('По вашему запросу ничего не найдено')
        )

    def get_balance(self) -> str:
        if self.data == []:
            raise FileNotFoundError(
                'Файл не найден или в нём отсутствуют записи!'
            )
        income: int = 0
        expenses: int = 0
        for item in self.data:
            if item.category.value == 'Доход':
                income += item.amount
            elif item.category.value == 'Расход':
                expenses += item.amount
        balance = income - expenses
        return print(f'Ваш баланс составляет {balance}')

    def get_income(self) -> str:
        if self.data == []:
            raise FileNotFoundError(
                'Файл не найден или в нём отсутствуют записи!'
            )
        income = 0
        for item in self.data:
            if item.category.value == 'Доход':
                income += item.amount
        return print(f'Ваши доходы составляют {income}')

    def get_expenses(self) -> str:
        if self.data == []:
            raise FileNotFoundError(
                'Файл не найден или в нём отсутствуют записи!'
            )
        expenses: int = 0
        for item in self.data:
            if item.category.value == 'Расход':
                expenses += item.amount
        return print(f'Ваши расходы составляют {expenses}')

    def update(
        self, date: str, category: str, amount: str, description: str,
        new_date: str, new_category: str, new_amount: str, new_description: str
    ) -> str:
        index: int | None = self._get_index(date, category, int(amount), description)
        if index is not None:
            self.data[index].date = new_date
            self.data[index].category = Transaction.get_transaction_type(new_category)
            self.data[index].amount = new_amount
            self.data[index].description = new_description
            self._save_data()
            return print('Запись успешно обновлена!')


class Budget:
    filename: str = set_filename()
    list_of_transactions: list[dict[str, str]] = BudgetService.load(filename)
    data: list[Transaction] = []
    for item in list_of_transactions:
        transaction = Transaction(
            date=item['Дата'],
            category=item['Категория'],
            amount=item['Сумма'],
            description=item['Описание']
        )
        data.append(transaction)
    objects = BudgetManager(data)
    @classmethod
    def save(cls, data) -> None:
        BudgetService.write(data, filename=set_filename())

# if __name__ == '__main__':
