"""
ru: Модуль для работы с API для выгрузки данных различных сайтов.
    Основа сделана на базе OpenAPI от hh.ru
en: Module for working with API for parsing data from various sites.
    The basis is made on the basis of OpenAPI from hh.ru

    MAIN URL: https://api.hh.ru
"""
from abc import ABC, abstractmethod
import requests

from src.api_errors import (
    ApiQueryError
)


class Api(ABC):
    """
    ru: Абстрактный класс для работы с API.
        Определяет общий для всех дочерних классов метод запроса.
    en: Abstract class for working with API.
        Defines a common method for all child classes to request.
    """
    @abstractmethod
    def _query(self):
        pass


class ApiBase(Api):
    """
    ru: Базовый класс для работы с API.
        Определяет метод запроса и проверки ответа.
        Рекомендуется использовать для наследования, но можно использовать и самостоятельно.
        Базовый класс работает без параметров запроса.
    en: Base class for working with API.
        Defines the request method and response check.
        It is recommended to use for inheritance, but you can use it independently.
        The base class works without request parameters.
    """
    def __init__(self, scope: str, headers: dict = None):
        """
        ru: Инициализация класса.
        en: Class initialization.
        :param scope: request scope
        """
        self.scope = scope
        self.headers = headers or {}
        self.__parameters = {}

    @property
    def parameters(self) -> dict:
        """
        ru: Свойства параметров
        en: Property of parameters
        :return: dict
        """
        return self.__parameters

    @parameters.setter
    def parameters(self, value: dict):
        """
        ru: Свойства параметров
        en: Property of parameters
        :param value: dict
        """
        self.__parameters = value

    def _query(self) -> dict:
        """
        ru: Метод запроса.
        en: Request method.
        :return: dict
        """
        response = requests.get(
            self.scope,
            headers=self.headers,
            params=self.parameters
        )
        status = response.status_code
        if status == 200:
            return response.json()
        else:
            type_ = response.reason
            url = response.url
            raise ApiQueryError(f"«{url}»: [{status}] {type_}")


class ApiFindBase(ApiBase):
    """
    ru: Базовый класс для работы с API поиска.
        Определяет методы для поиска.
    en: Base class for working with search API.
        Defines methods for searching.
    """
    def __init__(self, scope: str, headers: dict = None):
        self.headers = headers or {}
        super().__init__(scope, self.headers)

    def find(self, **kwargs) -> dict:
        """
        ru: Метод поиска.
        en: Search method.
        :return: dict
        """
        self.parameters = kwargs
        return self._query()


class ApiInfoBase(ApiBase):
    def __init__(self, scope, id_, headers=None):
        self.headers = headers or {}
        super().__init__(f"{scope}/{id_}", headers)

    def info(self, id_: int | str, **kwargs) -> dict:
        self.parameters = kwargs
        return self._query()


class JobObjectBase(ABC):
    @classmethod
    @abstractmethod
    def create(cls, **kwargs):
        pass


class JobObject(JobObjectBase):  # todo: add method for return object as dict
    def __init__(self, **kwargs):
        self.__dict__ = self.rename_built_keys(**kwargs)

    @staticmethod
    def rename_built_keys(**kwargs):
        """
        ru: Переименование ключей, если они совпадают с ключевыми словами Python.
        en: Renaming keys if they match Python keywords.
        """
        arguments = {}
        builtins_names = ["id", "type", "from"]
        for key in kwargs.keys():
            if key in builtins_names:
                arguments[f"{key}_"] = kwargs[key]
            else:
                arguments[key] = kwargs[key]
        return arguments

    @classmethod
    def create(cls, **kwargs):
        return cls(**cls.rename_built_keys(**kwargs))

    def get_dict(self):
        built_keys = ["id_", "type_", "from_"]
        result = {}
        for key in self.__dict__.keys():
            if key.startswith("_"):
                continue
            if key in built_keys:
                result[key[:-1]] = self.__dict__[key]
            else:
                result[key] = self.__dict__[key]
        return result


class GenerateObjectsListBase(ABC):
    @abstractmethod
    def get_object(self):
        pass

    @abstractmethod
    def generate(self):
        pass


class GenerateObjectsList(GenerateObjectsListBase):
    def __init__(self, items: list[dict]):
        self.items = items

    def get_object(self):
        return JobObjectBase

    def generate(self):
        return [self.get_object().create(**obj) for obj in self.items]
