from datetime import datetime
import json
from constants import FILE_NAME


class BudgetService:
    @staticmethod
    def load(filename=FILE_NAME):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        return data
    
    @staticmethod
    def write(data, filename=FILE_NAME):
        try:
            with open(filename, 'w') as file:
                data = json.dump(data, file, ensure_ascii=False, indent=4)
        except FileNotFoundError:
            return


class BudgetManager:
    def __init__(self, data):
        self.data: list[dict] = data

    def _get_index(self, date, category, amount, description):
        index = self.data.index(
            {
                'Дата': date,
                'Категория': category,
                'Сумма': amount,
                'Описание': description,
            }
        )
        return index

    def _save_data(self):
        BudgetService.write(self.data,)

    def create(self, date, category, amount, description):
        new_entry = {
            'Дата': date,
            'Категория': category,
            'Сумма': amount,
            'Описание': description,
        }
        self.data.append(new_entry)
        self._save_data()

    def find(self, *args):
        if self.data == []:
            raise FileNotFoundError(
                'Файл не найден или в нём отсутствуют записи!'
            )
        result = []
        for item in self.data:
            if all(_ in item.values() for _ in args):
                result.append(item)
        return print(result)

    def get_balance(self):
        if self.data == []:
            raise FileNotFoundError(
                'Файл не найден или в нём отсутствуют записи!'
            )
        income = 0
        expenses = 0
        for item in self.data:
            if item['Категория'] == 'Доход':
                income += item['Сумма']
            elif item['Категория'] == 'Расход':
                expenses += item['Сумма']
        balance = income - expenses
        return print(f'Ваш баланс составляет {balance}')

    def get_income(self):
        if self.data == []:
            raise FileNotFoundError(
                'Файл не найден или в нём отсутствуют записи!'
            )
        income = 0
        for item in self.data:
            if item['Категория'] == 'Доход':
                income += item['Сумма']
        return print(f'Ваши доходы составляют {income}')

    def get_expenses(self):
        if self.data == []:
            raise FileNotFoundError(
                'Файл не найден или в нём отсутствуют записи!'
            )
        expenses = 0
        for item in self.data:
            if item['Категория'] == 'Расход':
                expenses += item['Сумма']
        return print(f'Ваши расходы составляют {expenses}')

    def patch(
        self, date, category, amount, description,
        new_date, new_category, new_amount, new_description
    ):
        index = self._get_index(date, category, amount, description)
        self.data[index]['Дата'] = new_date
        self.data[index]['Категория'] = new_category
        self.data[index]['Сумма'] = new_amount
        self.data[index]['Описание'] = new_description
        self._save_data()
        return print('Запись успешно обновлена!')


class Budget:
    data = BudgetService.load()
    objects = BudgetManager(data)


if __name__ == '__main__':
    # print(Budget)
    # print(Budget.objects.all())
    Budget.objects.find('Расход', 20)
    Budget.objects.get_balance()
    Budget.objects.get_expenses()
    Budget.objects.get_income()
    # Budget.objects.patch(date='2024-05-03', category='Расход', amount=20, description='new', new_date='2020-05-03', new_category='Доход', new_amount=2000, new_description='not_new',)
    # Budget.objects.create(date='2024-05-03', category='Расход', amount=20, description='new')