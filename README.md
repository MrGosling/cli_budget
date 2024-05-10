# CLI_budget
CLI_budget - небольшая программа, позволяющая вести учёт доходов и расходов
посредством работы с терминалом.

## Установка
Дальнейшие шаги предполагают, что на компьютере пользователя установлен Python.

* Скопировать проект к себе в директорию проектов и перейти в проект.
Команда выполняется в директории проектов.
```
git clone git@github.com:MrGosling/cli_budget.git && cd cli_budget
```

* Создать и активировать виртульное окружение. Программа реализована с помощью
встроенных возможностей и библиотек Python, поэтому этот шаг необязателен,
всё будет работать и так.
```
python3 -m venv venv && source venv/bin/activate
```

Всё готово, можно приступать к использованию.

## Использование
* Программа хранит записи в виде файла .json. Если вы хотите назначить какое-то
конкретное имя для файла, то необходимо в директории проекта создать файл .env.
Но программа предусматривает имя по умолчанию, так что это не является
обязательным. Файл с данными создаётся при добавлении первой записи.
```
touch .env
```
В файле .env необходим написать строку
```
FILE_NAME=<custom_file_name>.json
```
Образец есть в файле example.env.

Работа с программой осуществляется из директории проекта.
date(Дата) предусматривает ввод строкового значения, формат - любой, удобный
пользователю. Автор предпочёл формат YYYY-mm-dd.
category(Категория) предусматривает только варианты Доход или Расход,
в случае присвоения иного значения программа сообщит о невозможности создания
записи с такой категорией.
amount(Сумма) - сумма средств дохода или расхода. Ожидает значение без копеек.
description(Описание) - строка с описание транзакции.

* Создать запись, все аргументы обязательны
```
python3 cli_parser.py --create date=2024-05-03,category=Доход,amount=2000,description=Зарплата
```

* Показать баланс
```
python3 cli_parser.py  --balance
```

* Показать сумму доходов
```
python3 cli_parser.py  --income
```

* Показать сумму расходов
```
python3 cli_parser.py  --expenses
```

* Найти записи по полному совпадение с переданными аргументами, аргументы не
именованы, перечисляются через запятую. Можно передавать любое количество
аргументов.
```
python3 cli_parser.py --find Зарплата,2000
```

* Редактировать запись. Аргументы именованы, все обязательны.
date, category, amount, description - аргументы для поиска записи, которую
нужно изменить. Если запись не найдена, программа об этом сообщит.
new_date, new_category, new_amount, new_description - аргументы, передающие
новые значения в запись.
```
python3 cli_parser.py --update date=2024-05-03,\n
                               category=Доход,\n
                               amount=2000,\n
                               description=Зарплата,\n
                               new_date=2020-06-03,\n
                               new_category=Доход,\n
                               new_amount=5000,\n
                               new_description=new_description
```

## Тестирование
Для программы написаны автотесты с использованием библиотеки unittest. Тесты
изолированы, не работают с основным файлом, в котором хранятся данные.

* Запустить тесты
```
python3 tests.py
```

Желаю приятного использования.

### Автор
Григорий Шевчук (Github - [MrGosling](https://github.com/MrGosling/))