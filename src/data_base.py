"""
ru: Модуль для работы с базой данных.
Классы и методы:
    BaseDB: абстрактный класс для работы с базой данных.
        Добавляя реальные базы данных, нужно наследовать этот класс и реализовать все методы.
        Разработчик может добавить свои методы. Работать можно с любой базой в едином интерфейсе.
    JsonDB: класс для работы с базой данных в формате JSON (тестовая база).
Classes:
    BaseDB: an abstract class for working with a database.
        By adding real databases, you need to inherit this class and implement all methods.
        The developer can add their own methods. You can work with any database in a single interface.
    JsonDB: class for working with a database in JSON format (test database).
"""

from abc import ABC, abstractmethod
import os
import json


class BaseDB(ABC):
    """
    ru: Абстрактный класс для работы с базой данных.
    en: Abstract class for working with the database.
    """
    @abstractmethod
    def create_area(self, area_name: str, fields: dict):
        pass

    @abstractmethod
    def check_area_name(self, area_name: str):
        pass

    @staticmethod
    @abstractmethod
    def check_key_fields(fields_ref: dict, fields: dict):
        pass

    @abstractmethod
    def delete_area(self, area_name: str):
        pass

    @abstractmethod
    def add_value(self, area_name: str, data_dict: dict):
        pass

    @abstractmethod
    def update_value(self, area_name: str, key_name: str, value: any, where_key: str, where_value: any):
        pass

    @abstractmethod
    def delete_value(self, area_name: str, key_name: str, value: any):
        pass

    @abstractmethod
    def select_value(self, area_name, key_value: dict = None):
        pass


class JsonDB(BaseDB):
    """
    ru: Класс для работы с базой данных в формате JSON.
    en: Class for working with a database in JSON format.
    """
    def __init__(self, path: str):
        """
        :param path: Путь к директории
        """
        if os.path.exists(path):
            self.path = path
        else:
            os.makedirs(path)
            self.path = path
        self.fields_types = {
            "INTEGER": int | None,
            "TEXT": str | None,
            "REAL": float | None,
            "BOOLEAN": bool,
            "BOOLEAN NOT NULL": bool | None,
            "BLOB": bytes | None,
            "INTEGER NOT NULL": int,
            "TEXT NOT NULL": str,
            "REAL NOT NULL": float,
            "BLOB NOT NULL": bytes,
        }

    @staticmethod
    def check_key_fields(fields_ref: dict, fields: dict):
        """
        ru: Проверка полей на соответствие названием ключей
        en: Checking fields for compliance with key names
        :param fields_ref: Референс названий ключей каждого поля
        :param fields: Названия ключей поля которое нужно проверить
        """
        if fields_ref.keys() != fields.keys():
            return False
        return True

    def check_type_fields(self, fields_ref: dict, fields: dict):
        """
        ru: Проверка полей на соответствие типам.
        en: Checking fields for compliance with types.
        :param fields_ref: Референс типов полей
        :param fields: Поля которые нужно проверить
        """
        for field in fields:
            if not isinstance(fields[field], self.fields_types[fields_ref[field]]):
                print(fields[field], self.fields_types[fields_ref[field]])
                return False
        return True

    def check_area_name(self, area_name: str) -> bool | str:
        """
        ru: Проверка на наличие таблицы в базе данных (в данном случае наличие файла).
        en: Check for the presence of a table in the database (in this case, the presence of a file).
        :param area_name: Название таблицы
        """
        file_name = os.path.join(self.path, f"{area_name}.json")
        if not os.path.exists(file_name):
            return False
        return file_name

    def create_area(self, area_name: str, fields: dict):
        """
        ru: Создать  таблицу для данных.
        en: Create an table for data.
        :param area_name: Название области
        :param fields: en: Поля
        """
        file_path = os.path.join(self.path, f"{area_name}.json")
        if os.path.exists(file_path):
            raise FileExistsError("File already exists")
        with open(file_path, 'w') as file:
            json.dump([fields], file, ensure_ascii=False, indent=4)

    def delete_area(self, area_name: str):
        """
        ru: Удалить область для данных.
        en: Delete the table for data.
        :param area_name: Название таблицы
        """
        file_path = self.check_area_name(area_name)
        if not file_path:
            raise FileNotFoundError("File not found")
        os.remove(file_path)

    def add_value(self, area_name: str, data_dict: dict):
        """
        ru: Добавить данные в таблицу.
        en: Add data to the table.
        :param area_name: Название таблицы
        :param data_dict: Словарь с данными
        """
        file_path = self.check_area_name(area_name)
        if not file_path:
            raise FileNotFoundError("File not found")
        with open(file_path, 'r') as file:
            data = json.load(file)
        if not self.check_key_fields(data[0], data_dict):
            raise TypeError("Fields do not match")
        if not self.check_type_fields(data[0], data_dict):
            raise TypeError("Types do not match")
        if data_dict not in data:
            data.append(data_dict)
            with open(file_path, 'w') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

    def update_value(self, area_name: str, key_name: str, value: any, where_key: str, where_value: any):
        """
        ru: Обновить данные в таблице.
        en: Update data in the table.
        :param area_name: Название таблицы
        :param key_name: Название ключа
        :param value: Значение
        :param where_key: Где ключ
        :param where_value: Где значение
        """
        file_path = self.check_area_name(area_name)
        if not file_path:
            raise FileNotFoundError("File not found")
        with open(file_path, 'r') as file:
            data = json.load(file)
        for record in data:
            if record[where_key] == where_value:
                record[key_name] = value
        with open(file_path, 'w') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def delete_value(self, area_name: str, key_name: str, value: any):
        """
        ru: Удалить данные из таблицы.
        en: Delete data from the table.
        :params: area_name: Название таблицы
        :params: key_name: Название ключа
        :params: value: Значение
        """
        file_path = self.check_area_name(area_name)
        if not file_path:
            raise FileNotFoundError("File not found")
        with open(file_path, 'r') as file:
            data = json.load(file)
        for record in data:
            if record[key_name] == value:
                data.remove(record)
        with open(file_path, 'w') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def select_value(self, area_name, key_value: dict = None) -> list[dict]:
        """
        ru: Выбрать данные из таблицы.
        en: Select data from the table.
        :param area_name: Название таблицы
        :param key_value: словарь с ключом и значением (необязательно) {"key": <key>, "value": <value>}

        """
        file_path = self.check_area_name(area_name)
        with open(file_path, 'r') as file:
            data = json.load(file)
        if key_value:
            return [record for record in data[1:] if record[key_value["key"]] == key_value["value"]]
        else:
            return data[1:]
