from datetime import datetime
import json

class BudgetService:

    # @staticmethod
    # def get_list(filename='file.json'):
    #     try:
    #         with open(filename, 'r') as file:
    #             data = json.load(file)
    #     except FileNotFoundError:
    #         raise ('Файл не найден!')
    #     return data

    @staticmethod
    def load(filename='file.json'):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        return data

class Budget:
    
    def __init__(self, category, amount, description, date = datetime.now()):
        self.date: datetime = date
        self.category: str = category
        self.amount: int = amount
        self.description: str = description

    def __str__(self):
        data = {
            'Дата': self.date.strftime('%Y-%m-%d'),
            'Категория': self.category,
            'Сумма': self.amount,
            'Описание': self.description,
        }
        return data

    @staticmethod
    def find(filename='file.json', *args):
        data: list[dict] = BudgetService.load(filename)
        if data == []:
            raise FileNotFoundError(
                'Файл не найден или в нём отсутствуют записи!'
            )
        list_to_find = [x for x in args if x != None]
        result = []
        for item in data:            
            if all(key in item.values() for key in list_to_find):
                result.append(item)
        print(result)
        return result

    def patch(self, category, amount, description):
        # изменение существующего объекта
        pass

    def save(self, filename='file.json'):
        data = self.__str__()
        budget_list = BudgetService.load(filename)
        budget_list.append(data)
        with open(filename, 'w') as file:
            json.dump(budget_list, file, ensure_ascii=False, indent=1)

    @staticmethod
    def get_balance(filename='file.json'):
        list_of_transactions = BudgetService.load(filename)
        if list_of_transactions == []:
            raise FileNotFoundError(
                'Файл не найден или в нём отсутствуют записи!'
            )
        income = 0
        expenses = 0
        for item in list_of_transactions:
            if item['Категория'] == 'Доход':
                income += item['Сумма']
            elif item['Категория'] == 'Расход':
                expenses += item['Сумма']
        balance = income - expenses
        return print(f'Ваш баланс составляет {balance}')

    @staticmethod
    def get_income(filename='file.json'):
        list_of_transactions = BudgetService.load(filename)
        if list_of_transactions == []:
            raise FileNotFoundError(
                'Файл не найден или в нём отсутствуют записи!'
            )
        income = 0
        for item in list_of_transactions:
            if item['Категория'] == 'Доход':
                income += item['Сумма']
        return print(f'Ваши доходы составляют {income}')

    @staticmethod
    def get_expenses(filename='file.json'):
        list_of_transactions = BudgetService.load(filename)
        if list_of_transactions == []:
            raise FileNotFoundError(
                'Файл не найден или в нём отсутствуют записи!'
            )
        expenses = 0
        for item in list_of_transactions:
            if item['Категория'] == 'Расход':
                expenses += item['Сумма']
        return print(f'Ваши расходы составляют {expenses}')


if __name__ == '__main__':
    b = Budget(category='1', amount=20, description='new')
    c = Budget(category='2', amount=30, description='1new')
    # c.save()
    # b.save()
    Budget.find('file.json', 'Расход')
    Budget.get_balance()
    Budget.get_income()
    Budget.get_expenses()
