"""
ru: Модуль для работы с API hh.ru.
    Также модуль содержит необходимые классы для объектов работы с данными:
        Vacancy: описание вакансии
        Employer: описание работодателя
        Salary: описание зарплаты
        Area: описание локации
        Experience: описание опыта работы
        Employment: описание типа занятости
        Schedule: описание графика работы

en: Module for working with the hh.ru API.
    The module also contains the necessary classes for data objects:
        Vacancy: vacancy description
        Employer: employer description
        Salary: salary description
        Area: location description
        Experience: work experience description
        Employment: employment type description
        Schedule: work schedule description
"""

import datetime

from src.api_errors import AttrValueRestrictionError
from src.api_parser import ApiFindBase, ApiInfoBase
from src.api_parser import JobObject
from src.api_parser import GenerateObjectsList

# API URL
SCOPES = {
    "find_vacancies": "https://api.hh.ru/vacancies",
    "find_employers": "https://api.hh.ru/employers",
    "info_vacancy": "https://api.hh.ru/vacancies",
    "info_employer": "https://api.hh.ru/employers"
}

# API HEADERS
HEADERS = {"User-Agent": "HH-User-Agent"}


class HHFindVacancy(ApiFindBase):
    """
    ru: Класс для поиска вакансий.
    en: Class for searching for vacancies.
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
        ru: Метод поиска с параметрами запроса
        en: Search method with request parameters

        :param per_page: integer <= 100, Количество элементов на странице
        :param page: integer, Количество страниц
        :param text: string, Текст поиска
        :param search_field: string, Поиск по полям (если не указано, то по всем полям)
        :param experience: string, Опыт работы (по id - https://api.hh.ru/dictionaries)
        :param employment: string, Тип занятости (по id - https://api.hh.ru/dictionaries)
        :param schedule: string, График работы (по id - https://api.hh.ru/dictionaries)
        :param area: string, Локация (по id - https://api.hh.ru/areas)
        :param industry: string, Отрасль (по id - https://api.hh.ru/dictionaries)
        :param employer_id: string, Id работодателя
        :param currency: string, Валюта (по id - https://api.hh.ru/dictionaries)
        :param salary: string, Зарплата
        :param label: string, Метка (по id - https://api.hh.ru/dictionaries)
        :param only_with_salary: boolean, Только с зарплатой
        :param period: integer, Период публикации вакансии
        :param date_from: string, Дата, ограничивающая диапазон дат публикации вакансий снизу
        :param date_to: string, Дата, ограничивающая диапазон дат публикации вакансий сверху
        :param top_lat: float, Верхняя широта границы. В адресе вакансии используется.
        :param bottom_lat: float, Нижняя широта границы. В адресе вакансии используется.
        :param left_lng: float, Левая долгота границы. В адресе вакансии используется.
        :param right_lng: float, Правая долгота границы. В адресе вакансии используется.
        :param order_by: string, Сортировка (по id - https://api.hh.ru/dictionaries)
        :param sort_point_lat: float, Для сортировки по удаленности - широта
        :param sort_point_lng: float, Для сортировки по удаленности - долгота
        :param clusters: boolean, Кластеры
        :param describe_arguments: boolean, Описать аргументы  # TODO: Использовать в клиентском коде для коллбеков
        :param no_magic: boolean,
        :param premium: boolean, Премиум вакансии
        :param responses_count_enabled: boolean, Количество откликов
        :param part_time: string, Частичная занятость
        :param accept_temporary: boolean, Принимаются временные вакансии
        :param locale: string, Локализация
        :param host: string, Хост
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
    ru: Класс для поиска работодателей.
    en: Class for searching for employers.
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
            per_page: int = 10,
            locale: str = "RU",
            host: str = "hh.ru"
    ):
        """
        ru: Метод поиска с параметрами запроса.
        en: Search method with request parameters.

        :param text: string, Текст поиска
        :param area: string, Локация (по id - https://api.hh.ru/areas)
        :param type_: string, Тип работодателя (по id - https://api.hh.ru/dictionaries)
        :param only_with_vacancies: boolean, Только с вакансиями
        :param sort_by: string, Сортировка по имени или по открытым вакансиям
        :param page: integer, Номер страницы
        :param per_page: integer, Количество элементов на странице
        :param locale: string, Локализация
        :param host: string, Хост
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
    ru: Класс для запроса информации о вакансии.
    en: Class for requesting information about a vacancy.
    """
    def __init__(self, id_: int):
        """
        :param id_: integer, Id вакансии
        """
        self.id_ = id_
        self.scope = SCOPES["info_vacancy"]
        self.headers = HEADERS
        super().__init__(self.scope, id_, self.headers)

    def info(
            self,
            locale: str = "RU",
            host: str = "hh.ru"
    ) -> dict:
        """
        ru: Метод для возврата информации о вакансии с параметрами
        en: Method for setting request parameters.

        :param locale: string, Locale
        :param host: string, Host
        """
        return super().info(self.id_, locale=locale, host=host)


class HHInfoEmployer(ApiInfoBase):
    """
    ru: Класс для запроса информации о работодателе.
    en: Class for requesting information about an employer.
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
    ) -> dict:
        """
        ru: Метод для возврата информации о работодателе с параметрами
        en: Method for setting request parameters.

        :param locale: string, Locale
        :param host: string, Host
        """
        return super().info(self.id_, locale=locale, host=host)


class HHSchedule(JobObject):
    """
    ru: Класс для создания объекта графика работы.
    en: Class for creating a work schedule object.
    """
    def __init__(
            self,
            id_: str,
            name: str
    ):
        """
        :param id_: string, Id графика работы
        :param name: string, Название графика работы
        """
        self.id_ = id_
        self.name = name
        super().__init__(id_=id_, name=name)

    def __str__(self):
        return f"График работы: {self.name}"


class HHExperience(JobObject):
    """
    ru: Класс для создания объекта опыта работы.
    en: Class for creating a work experience object.
    """
    def __init__(
            self,
            id_: str,
            name: str
    ):
        """
        :param id_: string, Id опыта работы
        :param name: string, Название опыта работы
        """
        self.id_ = id_
        self.name = name
        super().__init__(id_=id_, name=name)

    def __str__(self):
        return f"Опыт работы: {self.name}"


class HHEmployment(JobObject):
    """
    ru: Класс для создания объекта типа занятости.
    en: Class for creating an employment type object.
    """
    def __init__(
            self,
            id_: str,
            name: str
    ):
        """
        :param id_: string, Id типа занятости
        :param name: string, Название типа занятости
        """
        self.id_ = id_
        self.name = name
        super().__init__(id_=id_, name=name)

    def __str__(self):
        return f"Тип занятости: {self.name}"


class HHArea(JobObject):
    """
    ru: Класс для создания объекта локации.
    en: Class for creating a location object.
    """
    def __init__(
            self,
            id_: str,
            name: str,
            url: str,
    ):
        """
        :param id_: string, Id локации
        :param name: string, Название локации
        """
        self.id_ = id_
        self.name = name
        self.url = url
        super().__init__(id_=id_, name=name, url=self.url)

    def __str__(self):
        return f"Локация: {self.name}"


class HHSalary(JobObject):
    """
    ru: Класс для создания объекта зарплаты.
    en: Class for creating a salary object.
    """
    def __init__(
            self,
            from_: int,
            to: int,
            currency: str,
            gross: bool = False,
    ):
        """
        :param from_: integer, Зарплата от
        :param to: integer, Зарплата до
        :param currency: string, Валюта
        :param gross: boolean, Налог
        """
        self.from_ = from_
        self.to = to
        self.currency = currency
        self.gross = gross
        super().__init__(from_=from_, to=to, currency=currency, gross=gross)

    def __lt__(self, other):
        if not other:
            return False
        self_list = [self.from_, self.to]
        other_list = [other.from_, other.to]
        if all(self_list) and all(other_list):
            return sum(self_list) / 2 < sum(other_list) / 2
        elif all(self_list) and any(other_list):
            return sum(self_list) / 2 < (other.from_ or other.to)
        elif any(self_list) and all(other_list):
            return (self.from_ or self.to) < sum(other_list) / 2
        return (self.from_ or self.to) < (other.from_ or other.to)

    def __gt__(self, other):
        if not other:
            return True
        self_list = [self.from_, self.to]
        other_list = [other.from_, other.to]
        if all(self_list) and all(other_list):
            return sum(self_list) / 2 > sum(other_list) / 2
        elif all(self_list) and any(other_list):
            return sum(self_list) / 2 > (other.from_ or other.to)
        elif any(self_list) and all(other_list):
            return (self.from_ or self.to) > sum(other_list) / 2
        return (self.from_ or self.to) > (other.from_ or other.to)

    def __str__(self):
        if self.from_ and self.to:
            return f"Зарплата: от {self.from_} до {self.to} {self.currency}"
        elif self.from_:
            return f"Зарплата: от {self.from_} {self.currency}"
        elif self.to:
            return f"Зарплата: до {self.to} {self.currency}"
        else:
            return "Уровень дохода не указан"


class HHEmployerUrlLogo(JobObject):
    """
    ru: Класс для создания объекта логотипа работодателя.
    en: Class for creating an employer logo object.
    """
    def __init__(
            self,
            **kwargs
    ):
        """
        :param original: string, Оригинальный размер логотипа
        :param 90: string, Размер 90x90
        :param 240: string, Размер 240x240
        """
        self.original = kwargs.get("original")
        self.size90 = kwargs.get("90")
        self.size240 = kwargs.get("240")
        super().__init__(
            original=self.original,
            size90=self.size90,
            size240=self.size240
        )

    def get_dict(self) -> dict:
        return {
            "original": self.original,
            "90": self.size90,
            "240": self.size240
        }


class HHEmployer(JobObject):
    """
    ru: Класс для coздания объекта работодателя.
    en: Class for creating an employer object.
    """
    def __init__(
            self,
            id_: str,
            name: str,
            alternate_url: str,
            logo_urls: dict | HHEmployerUrlLogo = None,
            accredited_it_employer: bool = False,
            description: str | None = None,
            site_url: str | None = None,
            **kwargs

    ):
        """
        :param id_: string, Id работодателя
        :param name: string, Название работодателя
        :param alternate_url: string, Ссылка на работодателя
        :param logo_urls: dict, Логотип работодателя
        :param accredited_it_employer: boolean, Аккредитованный it-работодатель
        :param description: string, Описание работодателя
        :param site_url: string, Сайт работодателя
        """
        self.additional = kwargs
        self.id_ = id_
        self.name = name
        self.site_url = site_url
        self.alternate_url = alternate_url
        self.logo_urls = logo_urls if isinstance(logo_urls, HHEmployerUrlLogo) else HHEmployerUrlLogo(**logo_urls) if logo_urls else None
        self.accredited_it_employer = accredited_it_employer
        self.description = description
        super().__init__(
            id_=self.id_,
            name=self.name,
            alternate_url=self.alternate_url,
            logo_urls=self.logo_urls,
            accredited_it_employer=self.accredited_it_employer,
            description=self.description,
            site_url=self.site_url,
            additional=self.additional
        )

    def __str__(self):
        url = f"\nСсылка работодателя: {self.alternate_url}" if self.alternate_url else ""
        return f"Работодатель: {self.name}{url}"


class HHVacancy(JobObject):
    """
    ru: Класс для создания объекта вакансии.
    en: Class for creating a vacancy object.
    """
    def __init__(
            self,
            id_: str,
            name: str,
            created_at: str,
            published_at: str,
            alternate_url: str,
            employer: dict | HHEmployer,
            salary: dict | HHSalary,
            area: dict | None,
            experience: dict | None,
            employment: dict | None,
            schedule: dict | None,
            description: str | None = None,
            **kwargs
    ):
        """
        :param id_: string, Id вакансии
        :param name: string, Название вакансии
        :param created_at: string, Дата создания вакансии
        :param published_at: string, Дата публикации вакансии
        :param alternate_url: string, Ссылка на вакансию
        :param employer: dict, Работодатель
        :param salary: dict, Зарплата
        :param area: dict, Локация
        :param experience: dict, Опыт работы
        :param employment: dict, Тип занятости
        :param schedule: dict, График работы
        :param description: string, Описание вакансии
        :param kwargs: dict, Дополнительные параметры
        """
        self.employer = employer if isinstance(employer, HHEmployer) else HHEmployer.create(**employer)
        self.salary = salary if isinstance(salary, HHSalary) else HHSalary.create(**salary) if salary else None
        self.name = name
        self.created_at = created_at
        self.published_at = published_at
        self.id_ = id_
        self.alternate_url = alternate_url
        self.area = area if isinstance(area, HHArea) else HHArea.create(**area) if area else None
        self.experience = experience if isinstance(experience, HHExperience) \
            else HHExperience.create(**experience) if experience else None
        self.employment = employment if isinstance(employment, HHEmployment) \
            else HHEmployment.create(**employment) if employment else None
        self.schedule = schedule if isinstance(schedule, HHSchedule)\
            else HHSchedule.create(**schedule) if schedule else None
        self.description = description
        self.additional = kwargs
        super().__init__(
            id_=id_,
            description=self.description,
            name=self.name,
            area=self.area,
            salary=self.salary,
            published_at=self.published_at,
            created_at=self.created_at,
            alternate_url=self.alternate_url,
            employer=self.employer,
            schedule=self.schedule,
            experience=self.experience,
            employment=self.employment,
            additional=self.additional
        )

    def __str__(self):
        name = f"Вакансия: {self.name}" if self.name else ""
        date_to_other_view = datetime.datetime.fromisoformat(self.published_at).strftime("%d-%m-%Y")
        date = f"\nОпубликовано: {date_to_other_view}" if self.published_at else ""
        url = f"\nСсылка вакансии: {self.alternate_url}" if self.alternate_url else ""
        return f"{name}{date}{url}"


class HHGenerateVacanciesList(GenerateObjectsList):
    """
    ru: Класс для генерации списка объектов вакансий.
    en: Class for generating a list of vacancy objects.
    """
    def __init__(self, items: list[dict]):
        """
        :param items: list, Список словарей с параметрами вакансий
        """
        # валидация словарей / validation of dictionaries
        valid_items = []
        for item in items:
            new_dict = {
                "id_": item["id"],
                "name": item["name"],
                "created_at": item["created_at"],
                "published_at": item["published_at"],
                "alternate_url": item["alternate_url"],
                "employer": item["employer"],
                "salary": item["salary"],
                "area": item["area"],
                "experience": item["experience"],
                "employment": item["employment"],
                "schedule": item["schedule"],
                "description": item.get("description")
            }
            valid_items.append(new_dict)
        super().__init__(valid_items)

    def get_object(self):
        """
        ru: Фабричный метод для создания объекта вакансии.
        en: Factory method for creating a vacancy object.
        """
        return HHVacancy


class HHGenerateEmployersList(GenerateObjectsList):
    """
    ru: Класс для генерации списка объектов работодателей.
    en: Class for generating a list of employer objects.
    """
    def __init__(self, items: list[dict]):
        """
        :param items: list, Список словарей с параметрами работодателей
        """
        # валидация словарей / validation of dictionaries
        valid_items = []
        for item in items:
            new_dict = {
                "id_": item["id"],
                "name": item["name"],
                "alternate_url": item["alternate_url"],
                "logo_urls": item.get("logo_urls"),
                "accredited_it_employer": item.get("accredited_it_employer"),
                "description": item.get("description"),
                "site_url": item.get("site_url")
            }
            valid_items.append(new_dict)
        super().__init__(items)

    def get_object(self):
        """
        ru: Фабричный метод для создания объекта работодателя.
        en: Factory method for creating an employer object.
        """
        return HHEmployer
