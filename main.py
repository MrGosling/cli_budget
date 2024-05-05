from datetime import datetime
import json


class Budget:
    
    def __init__(self, category, amount, description):
        self.date: datetime = datetime.now()
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

    def save(self, filename='file.txt'):
        data = self.__str__()

        with open(filename, 'a+') as file:
            if file.tell() > 0:
                file.write('\n')
            json.dump(data, file, ensure_ascii=False, indent=4)
            
# from main import Budget
# b = Budget(category='1', amount=20, description='new')
# b.save('file.json')
