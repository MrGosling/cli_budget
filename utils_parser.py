from budget import Budget


def get_my_balance() -> None:
    """
    Функция для вывода баланса из объекта Budget.
    """
    print(Budget.objects.get_balance())


def get_my_income() -> None:
    """
    Функция для вывода дохода из объекта Budget.
    """
    print(Budget.objects.get_income())


def get_my_expenses() -> None:
    """
    Функция для вывода расходов из объекта Budget.
    """
    print(Budget.objects.get_expenses())


def find_transactions(data: list[str]) -> None:
    """
    Функция для фильтрации и вывода транзакций на основе предоставленных
    фильтров.

    args:
        data (list): Список строк, представляющих фильтры.
    """
    filters: list[str] = (
        [value.strip() for value in ','.join(data).split(',')]
    )
    print(Budget.objects.filter(*filters))


def create_transaction(data: list[str]) -> None:
    """
    Функция для создания новой транзакции на основе предоставленных данных.

    args:
        data (list): Список строк, представляющих пары ключ-значение
        для новой транзакции.
    """
    new_transaction: dict = {}
    for entry in data:
        lines = entry.split(',')
        for line in lines:
            key, value = line.split('=')
            new_transaction[key] = value
    print(Budget.objects.create(**new_transaction))


def update_transaction(data: list[str]) -> None:
    """
    Функция для обновления транзакции новыми данными.

    args:
        data (list): Список строк, представляющих пары ключ-значение для
        обновления транзакции.
    """
    transaction_to_update = {}
    for entry in data:
        lines = entry.split(',')
        for line in lines:
            key, value = line.split('=')
            transaction_to_update[key] = value
    print(Budget.objects.update(**transaction_to_update))
