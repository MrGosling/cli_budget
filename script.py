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
    
    class TransactionType(Enum):
        INCOME = 'income'
        EXPENSE = 'expense'
    
    def __init__(self, date, category, amount: str, description):
        self.date = date
        self.category = category
        self.amount = int(amount)
        self.description = description
        
    def to_dict(self):
        return {
            'Дата': self.date,
            'Категория': self.category,
            'Сумма': str(self.amount),
            'Описание': self.description,
        }


class BudgetService:
    # @staticmethod
    # def set_filename(filename):
    #     return filename

    @staticmethod
    def load(filename):
        # if filename is None:
            # filename = FILE_NAME
            # filename = set_filename()
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
        # if filename is None:
        #     filename = set_filename()
        try:
            with open(filename, 'w') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except FileNotFoundError:
            return


class BudgetManager:
    def __init__(self, data):
        self.data: list[Transaction] = data

    def _get_index(self, date, category, amount, description):
        for index, obj in enumerate(self.data):
            if obj.date == date and obj.category == category and obj.amount == amount and obj.description == description:
                return index
        print('Не удалось найти запись для обновления')
        # raise ValueError('Не удалось найти объект для обновления')

    def _save_data(self):
        data_to_save = [transaction.to_dict() for transaction in self.data]
        Budget.save(data=data_to_save)

    def create(self, date, category, amount, description):
        new_entry = Transaction(date, category, amount, description)
        self.data.append(new_entry)
        self._save_data()
        return print(f'Создана новая запись: {new_entry.to_dict()}')

    def filter(self, *args):
        if not self.data:
            raise FileNotFoundError('Файл не найден или в нём отсутствуют записи!')
        result = []
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

    def get_balance(self):
        if self.data == []:
            raise FileNotFoundError(
                'Файл не найден или в нём отсутствуют записи!'
            )
        income = 0
        expenses = 0
        for item in self.data:
            if item.category == 'Доход':
                income += item.amount
            elif item.category == 'Расход':
                expenses += item.amount
        balance = income - expenses
        return print(f'Ваш баланс составляет {balance}')

    def get_income(self):
        if self.data == []:
            raise FileNotFoundError(
                'Файл не найден или в нём отсутствуют записи!'
            )
        income = 0
        for item in self.data:
            if item.category == 'Доход':
                income += item.amount
        return print(f'Ваши доходы составляют {income}')

    def get_expenses(self):
        if self.data == []:
            raise FileNotFoundError(
                'Файл не найден или в нём отсутствуют записи!'
            )
        expenses = 0
        for item in self.data:
            if item.category == 'Расход':
                expenses += item.amount
        return print(f'Ваши расходы составляют {expenses}')

    def update(
        self, date, category, amount, description,
        new_date, new_category, new_amount, new_description
    ):
        index = self._get_index(date, category, int(amount), description)
        if index is not None:
            self.data[index].date = new_date
            self.data[index].category = new_category
            self.data[index].amount = new_amount
            self.data[index].description = new_description
            self._save_data()
            return print('Запись успешно обновлена!')


class Budget:
    filename = set_filename()#'test_data.json'
    list_of_transactions = BudgetService.load(filename)
    data = []
    for item in list_of_transactions:
        transaction = Transaction(date = item['Дата'], category=item['Категория'], amount=item['Сумма'], description=item['Описание'])
        data.append(transaction)
    objects = BudgetManager(data)
    @classmethod
    def save(cls, data):
        BudgetService.write(data)

if __name__ == '__main__':
    # print(Budget)
    # print(Budget.objects.all())
    # Budget.objects.filter('2024-05-03','Расход', '20')
    Budget.objects.get_balance()
    # Budget.objects().get_balance()
    # Budget.objects.get_expenses()
    # Budget.objects.get_income()
    # Budget.objects.update(date='2024-05-03', category='Доход', amount=2000, description='new', new_date='2020-06-03', new_category='Доход', new_amount=5000, new_description='not_new',)
    # Budget.objects.create(date='2024-05-03', category='Доход', amount=2000, description='new')
    # Budget.all()
    # print(Budget.objects.all())