import os
from pathlib import Path


def set_filename(filename) -> str:
    """
    Устанавливает имя файла и возвращает его.

    Args:
        filename (str): Имя файла.

    Returns:
        str: Установленное имя файла.
    """
    return filename


def load_environ() -> None:
    """
    Загружает переменные окружения из файла '.env' в окружение программы.

    Raises:
        FileNotFoundError: Если файл '.env' не найден.
    """
    try:
        env_path = Path('.') / '.env'
        with open(env_path) as file:
            for line in file:
                key, value = line.strip().split('=')
                os.environ[key] = value
    except FileNotFoundError:
        pass
