from datetime import datetime
import json
from constants import FILE_NAME

class BudgetEntry:
    def __init__(self, date, category, amount, description):
        self.date = date
        self.category = category
        self.amount = amount
        self.description = description

    def to_dict(self):
        return {
            'Дата': self.date,
            'Категория': self.category,
            'Сумма': self.amount,
            'Описание': self.description,
        }

class BudgetManager:
    def __init__(self, data):
        self.entries = [BudgetEntry(**entry) for entry in data]

    def all(self):
        return [entry.to_dict() for entry in self.entries]

    def create(self, date, category, amount, description):
        new_entry = BudgetEntry(date, category, amount, description)
        self.entries.append(new_entry)
        self._save_data()

    def _save_data(self):
        data_to_save = [entry.to_dict() for entry in self.entries]
        with open(FILE_NAME, 'w') as file:
            json.dump(data_to_save, file, ensure_ascii=False, indent=4)

    # Остальные методы класса BudgetManager оставляем без изменений

class BudgetService:
    @staticmethod
    def load(filename='file.json'):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        return data

class Budget:
    data = BudgetService.load('file.json')
    objects = BudgetManager(data)

if __name__ == '__main__':
    Budget.objects.create(date='2024-05-03', category='Расход', amount=20, description='new')
    Budget.objects.create(date='2024-05-04', category='Доход', amount=30, description='old')
    print(Budget.objects.all())
