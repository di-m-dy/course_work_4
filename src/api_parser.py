"""
ru: Модуль для работы с API для парсинга данных различных сайтов.
    Основа сделана на базе OpenAPI от hh.ru
en: Module for working with API for parsing data from various sites.
    The basis is made on the basis of OpenAPI from hh.ru

    MAIN URL: https://api.hh.ru
"""
from abc import ABC, abstractmethod
import requests

from .api_schemes import FindVacancySchema, FindEmployerSchema, InfoSchema
from .api_errors import (
    ObjectNotFoundError,
    BadArgumentError,
    AdditionalActionError,
    UnknownError
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
    def __init__(self, scope):
        """
        ru: Инициализация класса.
        en: Class initialization.
        :param scope: request scope
        """
        self.scope = scope
        self._parameters = {}

    @property
    def parameters(self):
        return self._parameters

    def _query(self):
        response = requests.get(self.scope, params=self.parameters)
        status = response.status_code
        if status == 200:
            return response.json()
        else:
            type_ = response
            if status == 400:
                print(type_)
                #raise BadArgumentError(type_)
            elif status == 404:
                print(type_)
                #raise ObjectNotFoundError(type_)
            elif status == 403:
                print(type_)
                #raise AdditionalActionError(type_)
            else:
                print(type_)
                #raise UnknownError


class ApiFindBase(ApiBase):
    """
    ru: Базовый класс для работы с API поиска.
        Определяет методы для поиска.
    en: Base class for working with search API.
        Defines methods for searching.
    """
    def __init__(self, scope):
        super().__init__(scope)

    def find(self):
        return self._query()


class ApiFindVacancy(ApiFindBase, FindVacancySchema):

    def __init__(self):
        scope = "https://api.hh.ru/vacancies"
        super().__init__(scope)


class ApiFindEmployer(ApiFindBase, FindEmployerSchema):

    def __init__(self):
        scope = "https://api.hh.ru/employers"
        super().__init__(scope)


class ApiInfoBase(ApiBase):
    def __init__(self, scope, id_):
        super().__init__(f"{scope}/{id_}")

    @property
    def info(self):
        return self._query()


class ApiInfoVacancy(ApiInfoBase, InfoSchema):
    def __init__(self, id_):
        super().__init__("https://api.hh.ru/vacancies", id_)


class ApiInfoEmployer(ApiInfoBase, InfoSchema):
    def __init__(self, id_):
        super().__init__("https://api.hh.ru/employers", id_)


class ApiDictionaryBase(ApiBase):
    pass


if __name__ == "__main__":
    # "https://api.hh.ru/" - 403
    # "https://api.ru/" - requests.exceptions.ConnectionError
    # "" - requests.exceptions.MissingSchema: Invalid URL
    api = ApiBase("")
    print(api._query())
