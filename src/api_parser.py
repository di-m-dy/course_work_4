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


class VacancyApiHH:
    """
    Description
    """
    def __init__(self):
        self.url = "https://api.hh.ru/vacancies/"
        self.parameters = {
            "per_page": None,
            "page": None,
            "text": None,
            "search_field": None,
            "experience": None,
            "employment": None,
            "schedule": None,
            "area": None,
            "industry": None,
            "employer_id": None,
            "currency": None,
            "salary": None,
            "label": None,
            "only_with_salary": None,
            "period": None,
            "date_from": None,
            "date_to": None,
        }

    def set_parameters(self, **params):
        for param in params:
            if param not in self.parameters:
                raise AttributeError(
                    f"Invalid Attribute: {param}\n"
                    f"It must be: {', '.join(self.parameters)}"
                )
            else:
                self.parameters[param] = params[param]

    def get_parameters(self):
        return {key: value for key, value in self.parameters.items() if value}

    def get_data(self):
        get_requests = requests.get(self.url, params=self.get_parameters())
        if get_requests.status_code == 200:
            return get_requests.json()
        else:
            error = get_requests.json()
            raise ValueError(f"{error['error']['type']}")


class EmployerApiHH:
    pass





