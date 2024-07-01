"""
ru: Модуль для описания схемы разных запросов к API.
    Каждый класс описывает аттрибуты параметров, которые могут быть использованы для запроса.
en: Module for describing the scheme of different requests to the API.
    Each class describes the attributes of parameters that can be used for the request.
"""

from src.api_errors import AttrValueRestrictionError
from src.api_parser import ApiFindBase, ApiInfoBase
from src.api_parser import JobObject
from src.api_parser import GenerateObjectsList


SCOPES = {
    "find_vacancies": "https://api.hh.ru/vacancies",
    "find_employers:": "https://api.hh.ru/employers",
    "info_vacancy": "https://api.hh.ru/vacancies",
    "info_employer": "https://api.hh.ru/employers"
}

HEADERS = {"User-Agent": "HH-User-Agent"}


class HHFindVacancy(ApiFindBase):
    """
    ru: Класс для описания схемы запроса вакансий.
    en: Class for describing the vacancy request scheme.
    """
    def __init__(self):
        self.scope = SCOPES["find_vacancies"]
        self.headers = HEADERS
        super().__init__(self.scope, self.headers)

    def find(
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
        return super().find(
            per_page=per_page,
            page=page,
            text=text,
            search_field=search_field,
            experience=experience,
            employment=employment,
            schedule=schedule,
            area=area,
            industry=industry,
            employer_id=employer_id,
            currency=currency,
            salary=salary,
            label=label,
            only_with_salary=only_with_salary,
            period=period,
            date_from=date_from,
            date_to=date_to,
            top_lat=top_lat,
            bottom_lat=bottom_lat,
            left_lng=left_lng,
            right_lng=right_lng,
            order_by=order_by,
            sort_point_lat=sort_point_lat,
            sort_point_lng=sort_point_lng,
            clusters=clusters,
            describe_arguments=describe_arguments,
            no_magic=no_magic,
            premium=premium,
            responses_count_enabled=responses_count_enabled,
            part_time=part_time,
            accept_temporary=accept_temporary,
            locale=locale,
            host=host
        )


class HHFindEmployer(ApiFindBase):
    """
    ru: Класс для описания схемы запроса работодателей.
    en: Class for describing the employer request scheme.
    """
    def __init__(self):
        self.scope = SCOPES["find_employers"]
        self.headers = HEADERS
        super().__init__(self.scope)

    def find(
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
        return super().find(
            text=text,
            area=area,
            type_=type_,
            only_with_vacancies=only_with_vacancies,
            sort_by=sort_by,
            page=page,
            per_page=per_page,
            locale=locale,
            host=host
        )


class HHInfoVacancy(ApiInfoBase):
    """
    ru: Класс для описания схемы запроса информации о вакансии.
    en: Class for describing the information request scheme about the vacancy.
    """
    def __init__(self, id_: int):
        self.id_ = id_
        self.scope = SCOPES["info_vacancy"]
        self.headers = HEADERS
        super().__init__(self.scope, id_, self.headers)

    def info(
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
        return super().info(self.id_, locale=locale, host=host)


class HHInfoEmployer(ApiInfoBase):
    """
    ru: Класс для описания схемы запроса информации о работодателе.
    en: Class for describing the information request scheme about the employer.
    """
    def __init__(self, id_: int):
        self.id_ = id_
        self.scope = SCOPES["info_employer"]
        self.headers = HEADERS
        super().__init__(self.scope, id_, self.headers)

    def info(
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
        return super().info(self.id_, locale=locale, host=host)


class HHSalary(JobObject):  # todo: add validation for all fields
    """
    ru: Класс для описания схемы зарплаты.
    en: Class for describing the salary scheme.
    """
    def __init__(
            self,
            from_: int,
            to: int,
            currency: str,
            **kwargs
    ):
        self.from_ = from_
        self.to = to
        self.currency = currency
        super().__init__(from_=from_, to=to, currency=currency)

    def __lt__(self, other):
        return self.from_ < other.from_  # todo: add algorithm for comparing salaries

    def __gt__(self, other):
        return self.from_ > other.from_  # todo: add algorithm for comparing salaries

    def __str__(self):
        if self.from_ and self.to:
            return f"Зарплата: от {self.from_} до {self.to} {self.currency}"
        elif self.from_:
            return f"Зарплата: от {self.from_} {self.currency}"
        elif self.to:
            return f"Зарплата: до {self.to} {self.currency}"
        else:
            return "Уровень дохода не указан"


class HHEmployer(JobObject):  # todo: add validation for all fields
    """
    ru: Класс для описания схемы работодателя.
    en: Class for describing the employer scheme.
    """
    def __init__(
            self,
            id_: int,
            name: str,
            alternate_url: str,
            logo_urls: dict,
            accredited_it_employer: bool | None = None,
            type_: str | None = None,
            description: str | None = None,
            site_url: str | None = None,
            area: dict | None = None,
            industries: list | None = None,
            insider_interview: list | None = None,
            **kwargs

    ):

        super().__init__(
            id_=id_,
            name=name,
            alternate_url=alternate_url,
            logo_urls=logo_urls,
            accredited_it_employer=accredited_it_employer,
            type_=type_,
            description=description,
            site_url=site_url,
            area=area,
            industries=industries,
            insider_interview=insider_interview
        )


class HHVacancy(JobObject):  # todo: add validation for all fields
    """
    ru: Класс для описания схемы вакансии.
    en: Class for describing the vacancy scheme.
    """
    def __init__(
            self,
            id_: int,
            premium: bool,
            name: str,
            department: dict,
            has_test: bool,
            response_letter_required: bool,
            area: dict,
            salary: dict | HHSalary,
            type_: dict,
            address: dict,
            response_url: str,
            published_at: str,
            created_at: str,
            archived: bool,
            apply_alternate_url: str,
            insider_interview: list,
            alternate_url: str,
            employer: dict | HHEmployer,
            contacts: dict,
            schedule: dict,
            working_days: list,
            working_time_intervals: list,
            working_time_modes: list,
            accept_temporary: bool,
            professional_roles: list,
            accept_incomplete_resumes: bool,
            experience: dict,
            employment: dict,
            description: str | None = None,
            **kwargs

    ):
        employer = employer if isinstance(employer, HHEmployer) else HHEmployer.create(**employer)
        salary = salary if isinstance(salary, HHSalary) else HHSalary.create(**salary) if salary else None
        super().__init__(
            id_=id_,
            description=description,
            premium=premium,
            name=name,
            department=department,
            has_test=has_test,
            response_letter_required=response_letter_required,
            area=area,
            salary=salary,
            type_=type_,
            address=address,
            response_url=response_url,
            published_at=published_at,
            created_at=created_at,
            archived=archived,
            apply_alternate_url=apply_alternate_url,
            insider_interview=insider_interview,
            alternate_url=alternate_url,
            employer=employer,
            contacts=contacts,
            schedule=schedule,
            working_days=working_days,
            working_time_intervals=working_time_intervals,
            working_time_modes=working_time_modes,
            accept_temporary=accept_temporary,
            professional_roles=professional_roles,
            accept_incomplete_resumes=accept_incomplete_resumes,
            experience=experience,
            employment=employment
        )


class HHGenerateVacanciesList(GenerateObjectsList):
    """
    ru: Класс для генерации списка объектов вакансий.
    en: Class for generating a list of vacancy objects.
    """
    def __init__(self, items: list):
        super().__init__(items)

    def get_object(self):
        return HHVacancy


class HHGenerateEmployersList(GenerateObjectsList):
    """
    ru: Класс для генерации списка объектов работодателей.
    en: Class for generating a list of employer objects.
    """
    def __init__(self, items: list):
        super().__init__(items)

    def get_object(self):
        return HHEmployer


if __name__ == "__main__":
    search = HHFindVacancy()
    data = search.find(text="Режиссер театр", only_with_salary=True, per_page=10, page=0)
    vacancies = HHGenerateVacanciesList(data["items"])
    for i in vacancies.generate():
        print("Работодатель: ", i.employer.name)
        print("Ссылка: ", i.alternate_url)
        print("Вакансия: ", i.name)
        print("Зарплата: ", str(i.salary))
        print(i.salary.__dict__)
        print('='*50)
