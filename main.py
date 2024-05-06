from datetime import datetime
import json

class BudgetService:
    
    @staticmethod
    def get_list(filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            raise ('Файл не найден!')
        return data

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

    def _get_balance(self, budget_list):
        # сортировка по категории доходы/расходы, разница между доходами и расходами
        pass

    @staticmethod
    def find(filename='file.json', *args):
    # def find(self, filename='file.json', category=None, date=None, amount=None):
        data: list[dict] = BudgetService.get_list(filename)
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

if __name__ == '__main__':
    b = Budget(category='1', amount=20, description='new')
    c = Budget(category='2', amount=30, description='1new')
    c.save()
    b.save()
    Budget.find('file.json', '1', 20)
