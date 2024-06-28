"""
ru: Модуль для описания схемы разных запросов к API.
    Каждый класс описывает аттрибуты параметров, которые могут быть использованы для запроса.
en: Module for describing the scheme of different requests to the API.
    Each class describes the attributes of parameters that can be used for the request.
"""

from abc import ABC, abstractmethod
from .api_errors import AttrValueRestrictionError


class SchemaBase(ABC):
    """
    ru: Абстрактный класс для описания схемы запроса.
    en: Abstract class for describing the request scheme.
    """
    @abstractmethod
    def set_parameters(self):
        pass


class FindVacancySchema(SchemaBase):
    """
    ru: Класс для описания схемы запроса вакансий.
    en: Class for describing the vacancy request scheme.
    """
    def __init__(self):
        self._parameters = {}

    def set_parameters(
            self,
            per_page: int = 10,
            page: int = 0,
            text: str = None,
            search_field: str = None,
            experience: str = None,
            employment: str = None,
            schedule: str = None,
            area: str = None,
            industry: str = None,
            employer_id: int = None,
            currency: int = None,
            salary: int = None,
            label: str = None,
            only_with_salary: bool = False,
            period: int = None,
            date_from: str = None,
            date_to: str = None,
            top_lat: float = None,
            bottom_lat: float = None,
            left_lng: float = None,
            right_lng: float = None,
            order_by: str = None,
            sort_point_lat: float = None,
            sort_point_lng: float = None,
            clusters: bool = False,
            describe_arguments: bool = False,
            no_magic: bool = False,
            premium: bool = False,
            responses_count_enabled: bool = False,
            part_time: str = None,
            accept_temporary: bool = False,
            locale: str = "RU",
            host: str = "hh.ru"
    ):
        """
        ru: Метод для установки параметров запроса.
        en: Method for setting request parameters.

        :param per_page: integer <= 100, Count of items on page
        :param page: integer, Number of page
        :param text: string, Search query at search_field
        :param search_field: string, Search field (for text area, if None = all fields)
        :param experience: string, Experience level (text id from ApiDictionary(VacancyExperience))
        :param employment: string, Employment type (text id from ApiDictionary(VacancyEmployment))
        :param schedule: string, Schedule type (text id from ApiDictionary(VacancySchedule))
        :param area: string, Area id from ApiDictionary(Area)
        :param industry: string, Industry id from ApiDictionary(Industry)
        :param employer_id: string, Employer id
        :param currency: string, Currency id from ApiDictionary(Currency)
        :param salary: string, Salary id from ApiDictionary(Salary)
        :param label: string, Label id from ApiDictionary(VacancyLabel)
        :param only_with_salary: boolean, Only with salary
        :param period: integer, Number of days within which the search is performed for vacancies
        :param date_from: string, Date that limits the range of publication dates for vacancies from below.
        :param date_to: string, Date that limits the range of publication dates for vacancies from above.
        :param top_lat: float, The upper latitude boundary. In the vacancy address is used.
        :param bottom_lat: float, The lower latitude boundary. In the vacancy address is used.
        :param left_lng: float, The left longitude boundary. In the vacancy address is used.
        :param right_lng: float, The right longitude boundary. In the vacancy address is used.
        :param order_by: string, Sort order (text id from ApiDictionary(VacancySearchOrder))
        :param sort_point_lat: float, Sort point latitude for order_by
        :param sort_point_lng: float, Sort point longitude for order_by
        :param clusters: boolean, Return clusters
        :param describe_arguments: boolean, Return describe arguments
        :param no_magic: boolean, No magic
        :param premium: boolean, Premium
        :param responses_count_enabled: boolean, Responses count enabled
        :param part_time: string, Part time
        :param accept_temporary: boolean, Accept temporary
        :param locale: string, Locale
        :param host: string, Host
        """
        if not 1 <= per_page <= 100:
            raise AttrValueRestrictionError()
        self._parameters["per_page"] = per_page
        self._parameters["page"] = page
        self._parameters["text"] = text
        self._parameters["search_field"] = search_field
        self._parameters["experience"] = experience
        self._parameters["employment"] = employment
        self._parameters["schedule"] = schedule
        self._parameters["area"] = area
        self._parameters["industry"] = industry
        self._parameters["employer_id"] = employer_id
        self._parameters["currency"] = currency
        self._parameters["salary"] = salary
        self._parameters["label"] = label
        self._parameters["only_with_salary"] = only_with_salary
        self._parameters["period"] = period
        self._parameters["date_from"] = date_from
        self._parameters["date_to"] = date_to
        self._parameters["top_lat"] = top_lat
        self._parameters["bottom_lat"] = bottom_lat
        self._parameters["left_lng"] = left_lng
        self._parameters["right_lng"] = right_lng
        self._parameters["order_by"] = order_by
        self._parameters["sort_point_lat"] = sort_point_lat
        self._parameters["sort_point_lng"] = sort_point_lng
        self._parameters["clusters"] = clusters
        self._parameters["describe_arguments"] = describe_arguments
        self._parameters["no_magic"] = no_magic
        self._parameters["premium"] = premium
        self._parameters["responses_count_enabled"] = responses_count_enabled
        self._parameters["part_time"] = part_time
        self._parameters["accept_temporary"] = accept_temporary
        self._parameters["locale"] = locale
        self._parameters["host"] = host


class FindEmployerSchema(SchemaBase):
    """
    ru: Класс для описания схемы запроса работодателей.
    en: Class for describing the employer request scheme.
    """
    def __init__(self):
        self._parameters = {}

    def set_parameters(
            self,
            text: str = None,
            area: str = None,
            type_: str = None,
            only_with_vacancies: bool = False,
            sort_by: str = None,
            page: int = 0,
            per_page: int = 20,
            locale: str = "RU",
            host: str = "hh.ru"
    ):
        """
        ru: Метод для установки параметров запроса.
        en: Method for setting request parameters.

        :param text: string, Search text
        :param area: string, Area id from ApiDictionary(Area)
        :param type_: string, Employer type id from ApiDictionary(EmployerType)
        :param only_with_vacancies: boolean, Only with vacancies
        :param sort_by: string, Sort by name or by vacancies open
        :param page: integer, Number of page
        :param per_page: integer, Count of items on page
        :param locale: string, Locale
        :param host: string, Host
        """

        self._parameters["text"] = text
        self._parameters["area"] = area
        self._parameters["type"] = type_
        self._parameters["only_with_vacancies"] = only_with_vacancies
        self._parameters["sort_by"] = sort_by
        self._parameters["page"] = page
        self._parameters["per_page"] = per_page
        self._parameters["locale"] = locale
        self._parameters["host"] = host


class InfoSchema(SchemaBase):
    """
    ru: Класс для описания схемы запроса информации о вакансии.
    en: Class for describing the information request scheme about the vacancy.
    """
    def __init__(self):
        self._parameters = {}

    def set_parameters(
            self,
            locale: str = "RU",
            host: str = "hh.ru"
    ):
        """
        ru: Метод для установки параметров запроса.
        en: Method for setting request parameters.

        :param locale: string, Locale
        :param host: string, Host
        """
        for param in locals():
            if param != 'self':
                self._parameters[param] = locals()[param]
