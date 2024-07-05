"""
ru: Модуль для работы с базой данных.
Классы и методы:
    DataBase:
        create table - создание области для данных
        delete table - удаление области для данных
        add record - добавление данных в область
        update record - обновление данных в области
        delete record - удаление данных из области
        select record - выбор данных из области
    en: Module for working with the database.
Classes:
    DataBase:
        connect db - connect to db
        create table - create area for data
        delete table - delete area for data
        add record - add data to area
        update record - update data in area
        delete record - delete data from area
        select record - select data from area
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
    params: path: en: Path to the directory / ru: Путь к директории
    """
    def __init__(self, path: str):
        """
        ru: Инициализация класса.
        en: Class initialization.
        :param path: directory path
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
        ru: Проверка полей на соответствие типам.
        en: Checking fields for compliance with types.
        :param fields_ref: en: Reference fields / ru: Справочные поля
        :param fields: en: Fields / ru: Поля
        """
        if fields_ref.keys() != fields.keys():
            return False
        return True

    def check_type_fields(self, fields_ref: dict, fields: dict):
        """
        ru: Проверка полей на соответствие типам.
        en: Checking fields for compliance with types.
        :param fields_ref: en: Reference fields / ru: Справочные поля
        :param fields: en: Fields / ru: Поля
        """
        for field in fields:
            if not isinstance(fields[field], self.fields_types[fields_ref[field]]):
                print(fields[field], self.fields_types[fields_ref[field]])
                return False
        return True

    def check_area_name(self, area_name: str):
        """
        ru: Проверка пути к файлу.
        en: Check the file path.
        :param area_name: en: Area name / ru: Название области
        """
        file_name = os.path.join(self.path, f"{area_name}.json")
        if not os.path.exists(file_name):
            return False
        return file_name

    def create_area(self, area_name: str, fields: dict):
        """
        ru: Создать область для данных.
        en: Create an area for data.
        :param area_name: en: Area name / ru: Название области
        :param fields: en: Fields / ru: Поля
        """
        file_path = os.path.join(self.path, f"{area_name}.json")
        if os.path.exists(file_path):
            raise FileExistsError("File already exists")
        with open(file_path, 'w') as file:
            json.dump([fields], file, ensure_ascii=False, indent=4)

    def delete_area(self, area_name: str):
        """
        ru: Удалить область для данных.
        en: Delete the area for data.
        :param area_name: en: Area name / ru: Название области
        """
        file_path = self.check_area_name(area_name)
        if not file_path:
            raise FileNotFoundError("File not found")
        os.remove(file_path)

    def add_value(self, area_name: str, data_dict: dict):
        """
        ru: Добавить данные в область.
        en: Add data to the area.
        :param area_name: en: Area name / ru: Название области
        :param data_dict: en: Data dictionary / ru: Словарь данных
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
        ru: Обновить данные в области.
        en: Update data in the area.
        :param area_name: en: Area name / ru: Название области
        :param key_name: en: Key name / ru: Название ключа
        :param value: en: Value / ru: Значение
        :param where_key: en: Where key / ru: Где ключ
        :param where_value: en: Where value / ru: Где значение
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
        ru: Удалить данные из области.
        en: Delete data from the area.
        :params: area_name: en: Area name / ru: Название области
        :params: key_name: en: Key name / ru: Название ключа
        :params: value: en: Value / ru: Значение
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

    def select_value(self, area_name, key_value: dict = None):
        """
        ru: Выбрать данные из области.
        en: Select data from the area.
        :param area_name: en: Area name / ru: Название области
        :param key_value:
            en: dict with key and value
            ru: словарь с ключом и значением (необязательно)
            {"key": <key>, "value": <value>}

        """
        file_path = self.check_area_name(area_name)
        with open(file_path, 'r') as file:
            data = json.load(file)
        if key_value:
            return [record for record in data[1:] if record[key_value["key"]] == key_value["value"]]
        else:
            return data[1:]
