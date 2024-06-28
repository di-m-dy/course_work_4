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

from api_schemes import FindVacancySchema


class Api(ABC):
    @abstractmethod
    def _query(self):
        pass


class ApiBase(Api):
    def __init__(self, scope):
        self.scope = scope

    def _query(self):
        api_response = requests.get(self.scope)
        if self.check_response(api_response):
            return api_response.json()
        return

    @staticmethod
    def check_response(response):
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


class ApiFind(ApiBase):
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
        get_requests = requests.get(self.scope, params=self.parameters)
        if self.check_response(get_requests):
            return get_requests.json()
        return

    def find(self):
        return self._query()


class ApiFindVacancy(ApiFind, FindVacancySchema):
    def __init__(self):
        super().__init__("https://api.hh.ru/vacancies")


class ApiFindEmployer(ApiFind):
    def __init__(self):
        super().__init__("https://api.hh.ru/employers")


class ApiInfoBase(ApiBase):
    pass
