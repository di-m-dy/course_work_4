"""
ru: Модуль для работы с API для парсинга данных различных сайтов.
    Основа сделана на базе OpenAPI от hh.ru
en: Module for working with API for parsing data from various sites.
    The basis is made on the basis of OpenAPI from hh.ru

    MAIN URL: https://api.hh.ru
"""

from abc import ABC, abstractmethod
import requests
import json

from api_schemes import FindVacancySchema, FindEmployerSchema, InfoSchema


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

    def _query(self):
        """
        ru: Метод запроса к API.
        en: Method for requesting to the API.
        :return:
        """
        api_response = requests.get(self.scope)
        if self.check_response(api_response):
            return api_response.json()
        return

    @staticmethod
    def check_response(response: requests.Response):
        """
        ru: Метод проверки ответа от сервера.
        en: Method for checking the server response.
        :param response: server response object
        :return:
        """
        status = response.status_code
        if status == 200:
            return True
        elif status == 402:
            raise ValueError("Invalid response 402")
        elif status == 404:
            raise ValueError("Invalid response 404")
        elif status == 403:
            raise ValueError("Invalid response 403")
        else:
            raise ValueError("Invalid response")


class ApiFindBase(ApiBase):
    """
    ru: Базовый класс для работы с API поиска.
        Определяет методы для поиска.
    en: Base class for working with search API.
        Defines methods for searching.
    """
    def __init__(self, scope):
        super().__init__(scope)
        self._parameters = {}

    @property
    def parameters(self):
        if not self._parameters:
            return
        return {key: value for key, value in self._parameters.items() if value}

    def set_parameters(self, **params):
        self._parameters |= params

    def _query(self):
        get_requests = requests.get(self.scope, params=self._parameters)
        if self.check_response(get_requests):
            return get_requests.json()
        return

    def find(self):
        return self._query()


class ApiFindVacancy(ApiFindBase, FindVacancySchema):
    def __init__(self):
        super().__init__("https://api.hh.ru/vacancies")


class ApiFindEmployer(ApiFindBase, FindEmployerSchema):
    def __init__(self):
        super().__init__("https://api.hh.ru/employers")


class ApiInfoBase(ApiBase):
    def __init__(self, scope, id_):
        super().__init__(f"{scope}/{id_}")
        self._parameters = {}

    @property
    def parameters(self):
        if not self._parameters:
            return
        return {key: value for key, value in self._parameters.items() if value}

    def set_parameters(self, **params):
        self._parameters |= params

    def _query(self):
        get_requests = requests.get(self.scope, params=self._parameters)
        if self.check_response(get_requests):
            return get_requests.json()
        return

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
    vacancy = ApiInfoVacancy("6666666")
    try:
        print(vacancy.info["description"])
    except ValueError as e:
        print(e)
