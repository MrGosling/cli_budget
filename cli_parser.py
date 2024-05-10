import argparse
from utils_parser import (
    get_my_balance, get_my_income, get_my_expenses, find_transactions,
    create_transaction, update_transaction
)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Вежливый скрипт')
    parser.add_argument(
        '--balance',
        help=('Показать баланс'
              'Пример запроса: python3 cli_parser --balance'
              'Пример ответа: Ваш баланс составляет 5000'),
        action='store_true',
    )
    parser.add_argument(
        '--income',
        help=('Показать сумму доходов'
              'Пример запроса: python3 cli_parser --income'
              'Пример ответа: Ваши доходы составляют 5000'),
        action='store_true',
    )
    parser.add_argument(
        '--expenses',
        help=('Показать сумму расходов'
              'Пример запроса: python3 cli_parser --expenses'
              'Пример ответа: Ваши расходы составляют 5000'),
        action='store_true',
    )
    parser.add_argument(
        '--find',
        help='Находит операции, подходящие условию поиска',
        nargs='+',
    )
    parser.add_argument(
        '--create',
        help=('Создать новую запись'

              'Пример запроса:'
              'python3 cli_parser.py --create'
              'date=2024-05-03,category=Доход,amount=2000,description=newsss'

              'Пример ответа: Создана новая запись: {"Дата": "2024-05-03",'
              '"Категория": "Доход", "Сумма": "2000", "Описание": "newsss"}'),
        nargs='+',
    )
    parser.add_argument(
        '--update',
        help=('Изменить существующую запись'

              'Пример запроса:'
              'python3 cli_parser.py --update'
              'date=2024-05-03,category=Доход,amount=2000,description=newsss,'
              'new_date=2020-06-03,new_category=Доход,new_amount=5000,'
              'new_description=not_new'

              'Пример ответа: Запись успешно обновлена!'),
        nargs='+',
    )
    args = parser.parse_args()
    if args.balance:
        get_my_balance()
    if args.income:
        get_my_income()
    if args.expenses:
        get_my_expenses()
    if args.find:
        find_transactions(args.find)
    if args.create:
        create_transaction(args.create)
    if args.update:
        update_transaction(args.update)
