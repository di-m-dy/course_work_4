"""
ru: Модуль для работы с API для выгрузки данных различных сайтов.
    Основа сделана на базе OpenAPI от hh.ru
en: Module for working with API for parsing data from various sites.
    The basis is made on the basis of OpenAPI from hh.ru

    MAIN URL: https://api.hh.ru
"""
from abc import ABC, abstractmethod
import requests

from src.api_schemes import FindVacancySchema, FindEmployerSchema, InfoSchema
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
    def __init__(self, scope: str):
        """
        ru: Инициализация класса.
        en: Class initialization.
        :param scope: request scope
        """
        self.scope = scope
        self._parameters = {}

    @property
    def parameters(self) -> dict:
        """
        ru: Свойства параметров
        en: Property of parameters
        :return: dict
        """
        return self._parameters

    def _query(self) -> dict:
        """
        ru: Метод запроса.
        en: Request method.
        :return: dict
        """
        response = requests.get(self.scope, params=self.parameters)
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
    def __init__(self, scope: str):
        super().__init__(scope)

    def find(self) -> dict:
        """
        ru: Метод поиска.
        en: Search method.
        :return: dict
        """
        return self._query()


class ApiFindVacancy(ApiFindBase, FindVacancySchema):
    """
    ru: Пользовательский ласс для поиска вакансий.
        Использует в качестве миксин схему FindVacancySchema поиска вакансий из модуля api_schemes.
    en: User class for searching for vacancies.
        Uses the search scheme for vacancies from the api_schemes module as a mixin.
    """

    def __init__(self):
        scope = "https://api.hh.ru/vacancies"
        super().__init__(scope)


class ApiFindEmployer(ApiFindBase, FindEmployerSchema):
    """
    ru: Пользовательский класс для поиска работодателей.
         Использует в качестве миксин схему FindEmployerSchema поиска работодателей из модуля api_schemes.
    en: User class for searching for employers.
        Uses the search scheme for employers from the api_schemes module as a mixin.
    """

    def __init__(self):
        scope = "https://api.hh.ru/employers"
        super().__init__(scope)


class ApiInfoBase(ApiBase):
    def __init__(self, scope, id_):
        super().__init__(f"{scope}/{id_}")

    @property
    def info(self) -> dict:
        return self._query()


class ApiInfoVacancy(ApiInfoBase, InfoSchema):
    def __init__(self, id_):
        super().__init__("https://api.hh.ru/vacancies", id_)


class ApiInfoEmployer(ApiInfoBase, InfoSchema):
    def __init__(self, id_):
        super().__init__("https://api.hh.ru/employers", id_)


class ApiDictionaryBase(ApiBase):
    pass
