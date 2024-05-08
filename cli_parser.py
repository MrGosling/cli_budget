import argparse
from script import Budget

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
              'python3 cli_parser.py --create date=2024-05-03,category=Доход,amount=2000,description=newsss' #noqa
              'Пример ответа: Создана новая запись: {"Дата": "2024-05-03", "Категория": "Доход", "Сумма": "2000", "Описание": "newsss"}'), #noqa
        nargs='+',
    )
    parser.add_argument(
        '--update',
        help=('Изменить существующую запись'
              'Пример запроса:'
              'python3 cli_parser.py --update date=2024-05-03,category=Доход,amount=2000,description=newsss,new_date=2020-06-03,new_category=Доход,new_amount=5000,new_description=not_new' #noqa
              'Пример ответа: Запись успешно обновлена!'), #noqa
        nargs='+',
    )
    args = parser.parse_args()
    if args.balance:
        Budget.objects.get_balance()
    if args.income:
        Budget.objects.get_income()
    if args.expenses:
        Budget.objects.get_expenses()
    if args.find:
        filters = [value.strip() for value in ','.join(args.find).split(',')]
        Budget.objects.filter(*filters)
    if args.create:
        new_transaction = {}
        data = args.create
        for entry in data:
            lines = entry.split(',')
            for line in lines:
                key, value = line.split('=')
                new_transaction[key] = value
        Budget.objects.create(**new_transaction)
    if args.update:
        transaction_to_update = {}
        data = args.update
        for entry in data:
            lines = entry.split(',')
            for line in lines:
                key, value = line.split('=')
                transaction_to_update[key] = value
        Budget.objects.update(**transaction_to_update)
