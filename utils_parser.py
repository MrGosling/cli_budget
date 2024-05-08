from pathlib import Path
import os
from script import Budget


def get_my_balance() -> None:
    Budget.objects.get_balance()
    
def get_my_income() -> None:
    Budget.objects.get_income()

def get_my_expenses() -> None:
    Budget.objects.get_expenses()

def find_transactions(data) -> None:
    filters = [value.strip() for value in ','.join(data).split(',')]
    Budget.objects.filter(*filters)

def create_transaction(data) -> None:
    new_transaction = {}
    for entry in data:
        lines = entry.split(',')
        for line in lines:
            key, value = line.split('=')
            new_transaction[key] = value
    Budget.objects.create(**new_transaction)

def update_transaction(data) -> None:
    transaction_to_update = {}
    for entry in data:
        lines = entry.split(',')
        for line in lines:
            key, value = line.split('=')
            transaction_to_update[key] = value
    Budget.objects.update(**transaction_to_update)

# def load_environ():
#     env_path = Path('.') / '.env'
#     with open(env_path) as file:
#         for line in file:
#             key, value = line.strip().split('=')
#             os.environ[key] = value