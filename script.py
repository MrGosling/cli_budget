import json
from constants import FILE_NAME
from enum import Enum


def set_filename() -> str:
    return FILE_NAME


class Transaction:
    """
    Класс для представления транзакций.
    """
    @classmethod
    def set_transaction_type(
        cls, transaction_type: str
    ) -> 'Transaction.TransactionType':
        """
        Определяет тип транзакции на основе переданной строки.

        Args:
            transaction_type (str): Строка, представляющая тип транзакции.

        Returns:
            Transaction.TransactionType: Тип транзакции.

        Raises:
            ValueError: Если указана неправильная категория.
        """
        if transaction_type.title() == 'Доход':
            return cls.TransactionType.INCOME
        elif transaction_type.title() == 'Расход':
            return cls.TransactionType.EXPENSES
        else:
            raise ValueError(
                'Неправильная категория, можно выбрать Доход или Расход'
            )

    class TransactionType(Enum):
        """
        Перечисление для типов транзакций.
        """
        INCOME = 'Доход'
        EXPENSES = 'Расход'

    def __init__(
        self, date: str, category: str, amount: str, description: str
    ) -> None:
        """
        Инициализирует объект класса Transaction.

        Args:
            date (str): Дата транзакции.
            category (str): Категория транзакции.
            amount (str): Сумма транзакции.
            description (str): Описание транзакции.
        """
        self.date: str = date
        self.category: Transaction.TransactionType = (
            self.set_transaction_type(category)
        )
        self.amount: int = int(amount)
        self.description: str = description

    def to_dict(self) -> dict[str, str]:
        """
        Представляет транзакцию в виде словаря.

        Returns:
            dict[str, str]: Словарь с данными транзакции.
        """
        return {
            'Дата': self.date,
            'Категория': self.category.value,
            'Сумма': str(self.amount),
            'Описание': self.description,
        }


class BudgetService:
    """
    Сервис для работы с файлом бюджета.
    """

    @staticmethod
    def load(filename) -> list | list[dict[str, str]]:
        """
        Загружает данные из файла бюджета.

        Args:
            filename: Имя файла для загрузки данных.

        Returns:
            Загруженные данные.
        """
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
            with open(filename, 'w') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        return data

    @staticmethod
    def write(data, filename) -> None:
        """
        Записывает данные в файл бюджета.

        Args:
            data: Данные для записи.
            filename: Имя файла для записи.
        """
        try:
            with open(filename, 'w') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except FileNotFoundError:
            return


class BudgetManager:
    """
    Управление бюджетом.
    """
    def __init__(self, data: list[Transaction]) -> None:
        """
        Инициализирует объект класса BudgetManager.

        Args:
            data (list[Transaction]): Список транзакций.
        """
        self.data: list[Transaction] = data

    def _get_index(self, date, category, amount, description) -> int | None:
        """
        Возвращает индекс записи для обновления.

        Returns:
            int | None: Индекс записи.
        """
        category_type: Transaction.TransactionType = (
            Transaction.set_transaction_type(category)
        )
        for index, obj in enumerate(self.data):
            if (
                obj.date == date and
                obj.category == category_type and
                obj.amount == amount and
                obj.description == description
            ):
                return index
        print('Не удалось найти запись для обновления')

    def _save_data(self) -> None:
        """
        Сохраняет данные.
        """
        data_to_save: list[dict[str, str]] = (
            [transaction.to_dict() for transaction in self.data]
        )
        Budget.save(data=data_to_save)

    def create(self, date, category, amount, description) -> str:
        """
        Создает новую запись.

        Returns:
            str: Сообщение о созданной записи.
        """
        new_entry = Transaction(date, category, amount, description)
        self.data.append(new_entry)
        self._save_data()
        return f'Создана новая запись: {new_entry.to_dict()}'

    def filter(self, *args) -> str:
        """
        Фильтрует записи по заданным параметрам.

        Returns:
            str: Результат фильтрации.
        """
        if not self.data:
            raise FileNotFoundError(
                'Файл не найден или в нём отсутствуют записи!'
            )
        result: list[dict[str, str]] = []
        for item in self.data:
            flag = True
            for arg in args:
                if arg not in item.to_dict().values():
                    flag = False
                    break
            if flag:
                result.append(item.to_dict())
        return (
            f'Вот, что удалось найти: {result}' if result != [] else
            'По вашему запросу ничего не найдено'
        )

    def get_balance(self) -> str:
        """
        Считает и показывает баланс.

        Returns:
            str: Сообщение о балансе.
        """
        if self.data == []:
            raise FileNotFoundError(
                'Файл не найден или в нём отсутствуют записи!'
            )
        income: int = 0
        expenses: int = 0
        for item in self.data:
            if item.category.value == 'Доход':
                income += item.amount
            elif item.category.value == 'Расход':
                expenses += item.amount
        balance = income - expenses
        return f'Ваш баланс составляет {balance}'

    def get_income(self) -> str:
        """
        Считает и показывает доходы.

        Returns:
            str: Сообщение о доходах.
        """
        if self.data == []:
            raise FileNotFoundError(
                'Файл не найден или в нём отсутствуют записи!'
            )
        income = 0
        for item in self.data:
            if item.category.value == 'Доход':
                income += item.amount
        return f'Ваши доходы составляют {income}'

    def get_expenses(self) -> str:
        """
        Считает и показывает расходы.

        Returns:
            str: Сообщение о расходах.
        """
        if self.data == []:
            raise FileNotFoundError(
                'Файл не найден или в нём отсутствуют записи!'
            )
        expenses: int = 0
        for item in self.data:
            if item.category.value == 'Расход':
                expenses += item.amount
        return f'Ваши расходы составляют {expenses}'

    def update(
        self, date: str, category: str, amount: str, description: str,
        new_date: str, new_category: str, new_amount: str, new_description: str
    ) -> str:
        """
        Обновляет запись.

        Returns:
            str: Сообщение об успешном обновлении.
        """
        index: int | None = self._get_index(
            date, category, int(amount), description
        )
        if index is not None:
            self.data[index].date = new_date
            self.data[index].category = (
                Transaction.set_transaction_type(new_category)
            )
            self.data[index].amount = new_amount
            self.data[index].description = new_description
            self._save_data()
            return 'Запись успешно обновлена!'


class Budget:
    """
    Класс для управления бюджетом.
    """
    filename: str = set_filename()
    list_of_transactions: list[dict[str, str]] = BudgetService.load(filename)
    data: list[Transaction] = []
    for item in list_of_transactions:
        transaction = Transaction(
            date=item['Дата'],
            category=item['Категория'],
            amount=item['Сумма'],
            description=item['Описание']
        )
        data.append(transaction)
    objects = BudgetManager(data)

    @classmethod
    def save(cls, data) -> None:
        """
        Сохраняет данные.

        Args:
            data: Данные для сохранения.
        """
        BudgetService.write(data, filename=set_filename())
