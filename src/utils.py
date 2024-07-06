"""
Модуль для создания упрощенной работы с базой данных
Конструкторы классов принимают объект базы данных, а методы принимают на вход объекты JobObject

CreateDB: класс для создания областей в базе данных:
    : проверить наличие базы данных и областей в ней
    : создать базу данных с необходимыми полями: vacancy, employer, salary, area, experience, employment, schedule

WriteData: класс на запись в базу данных c методами добавления разных объектов в базу данных

ReadData: класс на чтение из базы данных и методы вывода данных из базы данных в списки словарей:

FilterDataDB: класс для фильтрации вакансий из базы данных
"""

from src.config import (
    VACANCY_FIELDS,
    EMPLOYER_FIELDS,
    SALARY_FIELDS,
    AREA_FIELDS,
    EXPERIENCE_FIELDS,
    EMPLOYMENT_FIELDS,
    SCHEDULE_FIELDS,
    EMPLOYER_URL_LOGO_FIELDS
)
from src.data_base import BaseDB
from src.api_parser import JobObject


class CreateDB:
    """
    ru: Класс для создания областей в базе данных.
        Проверяет наличие базы данных и всех областей в ней.
    en: Class for creating areas in the database.
        Checks the presence of a database and all areas in it.
    """
    def __init__(self, db: BaseDB):
        """
        ru: Инициализация класса.
        en: Class initialization.
        :param db: database object
        """
        self.db = db
        self.fields = [
            VACANCY_FIELDS,
            EMPLOYER_FIELDS,
            SALARY_FIELDS,
            AREA_FIELDS,
            EXPERIENCE_FIELDS,
            EMPLOYMENT_FIELDS,
            SCHEDULE_FIELDS,
            EMPLOYER_URL_LOGO_FIELDS
        ]
        for field in self.fields:
            check = self.db.check_area_name(field["name"])
            if not check:
                self.db.create_area(field["name"], field["fields"])


class WriteData:
    """
    ru: Класс для записи данных в базу данных.
    en: Class for writing data to the database.
    """
    def __init__(self, db: BaseDB):
        """
        :param db: database object
        """
        self.db = db

    def add_area(self, area: JobObject):
        """
        ru: Добавить локацию в базу данных.
        en: Add location to the database.
        :param area: объект локации
        """
        self.db.add_value(AREA_FIELDS["name"], area.get_dict())

    def add_experience(self, experience: JobObject):
        """
        ru: Добавить опыт работы в базу данных.
        en: Add experience to the database.
        :param experience: объект опыта работы
        """
        self.db.add_value(EXPERIENCE_FIELDS["name"], experience.get_dict())

    def add_employment(self, employment: JobObject):
        """
        ru: Добавить тип занятости в базу данных.
        en: Add employment type to the database.
        :param employment: объект типа занятости
        """
        self.db.add_value(EMPLOYMENT_FIELDS["name"], employment.get_dict())

    def add_schedule(self, schedule: JobObject):
        """
        ru: Добавить график работы в базу данных.
        en: Add work schedule to the database.
        :param schedule: объект графика работы
        """
        self.db.add_value(SCHEDULE_FIELDS["name"], schedule.get_dict())

    def add_salary(self, salary: JobObject, vacancy_id: int):
        """
        ru: Добавить зарплату в базу данных.
        en: Add salary to the database.
        :param salary: объект зарплаты
        """
        to_add = salary.get_dict()
        to_add["vacancy_id"] = vacancy_id
        self.db.add_value(SALARY_FIELDS["name"], to_add)

    def add_employer_url_logo(self, employer_url_logo: JobObject, employer_id: int):
        """
        ru: Добавить логотип работодателя в базу данных.
        en: Add employer logo to the database.
        :param employer_url_logo: объект логотипа работодателя
        """
        to_add = employer_url_logo.get_dict()
        to_add["employer_id"] = employer_id
        self.db.add_value(EMPLOYER_URL_LOGO_FIELDS["name"], to_add)

    def add_employer(self, employer: JobObject):
        """
        ru: Добавить работодателя в базу данных.
        en: Add employer to the database.
        :param employer: объект работодателя
        """
        get_dict = employer.get_dict()
        to_add = {
            "id": get_dict["id"],
            "name": get_dict["name"],
            "alternate_url": get_dict["alternate_url"],
            "accredited_it_employer": get_dict["accredited_it_employer"],
            "description": get_dict["description"],
            "site_url": get_dict["site_url"]
        }
        logo_urls = get_dict.get("logo_urls")
        if logo_urls:
            self.add_employer_url_logo(logo_urls, to_add["id"])
        self.db.add_value(EMPLOYER_FIELDS["name"], to_add)

    def add_vacancy(self, vacancy: JobObject):
        """
        ru: Добавить вакансию в базу данных.
        en: Add vacancy to the database.
        :param vacancy: объект вакансии
        """
        get_dict = vacancy.get_dict()
        employer = get_dict["employer"]
        area = get_dict["area"]
        experience = get_dict["experience"]
        employment = get_dict["employment"]
        schedule = get_dict["schedule"]
        salary = get_dict["salary"]
        to_add = {
            "id": get_dict["id"],
            "name": get_dict["name"],
            "alternate_url": get_dict["alternate_url"],
            "published_at": get_dict["published_at"],
            "created_at": get_dict["created_at"],
            "employer_id": employer.id_,
            "area_id": area.id_,
            "experience_id": experience.id_,
            "employment_id": employment.id_,
            "schedule_id": schedule.id_,
            "description": get_dict["description"]
        }
        if salary:
            self.add_salary(salary, to_add["id"])
        if area:
            self.add_area(area)
        if experience:
            self.add_experience(experience)
        if employment:
            self.add_employment(employment)
        if schedule:
            self.add_schedule(schedule)
        self.add_employer(employer)
        self.db.add_value(VACANCY_FIELDS["name"], to_add)


class ReadData:
    """
    ru: Класс для чтения данных из базы данных.
    en: Class for reading
    """
    def __init__(self, db: BaseDB):
        """
        :param db: database object
        """
        self.db = db

    def get_area(self, key_value: dict[str, any] = None) -> list:
        """
        ru: Получить локации из базы данных.
        en: Get locations from the database.
        :param key_value: ключ и значение для поиска
        """
        if key_value:
            data = self.db.select_value(AREA_FIELDS["name"], key_value)
        else:
            data = self.db.select_value(AREA_FIELDS["name"])
        return data

    def get_experience(self, key_value: dict[str, any] = None) -> list:
        """
        ru: Получить опыт работы из базы данных.
        en: Get experience from the database.
        :param key_value: ключ и значение для поиска
        """
        if key_value:
            data = self.db.select_value(EXPERIENCE_FIELDS["name"], key_value)
        else:
            data = self.db.select_value(EXPERIENCE_FIELDS["name"])
        return data

    def get_employment(self, key_value: dict[str, any] = None) -> list:
        """
        ru: Получить тип занятости из базы данных.
        en: Get employment type from the database.
        :param key_value: ключ и значение для поиска
        """
        if key_value:
            data = self.db.select_value(EMPLOYMENT_FIELDS["name"], key_value)
        else:
            data = self.db.select_value(EMPLOYMENT_FIELDS["name"])
        return data

    def get_schedule(self, key_value: dict[str, any] = None) -> list:
        """
        ru: Получить график работы из базы данных.
        en: Get work schedule from the database.
        :param key_value: ключ и значение для поиска
        """
        if key_value:
            data = self.db.select_value(SCHEDULE_FIELDS["name"], key_value)
        else:
            data = self.db.select_value(SCHEDULE_FIELDS["name"])
        return data

    def get_salary(self, key_value: dict[str, any] = None) -> list:
        """
        ru: Получить зарплаты из базы данных.
        en: Get salaries from the database.
        :param key_value: ключ и значение для поиска
        """
        if key_value:
            data = self.db.select_value(SALARY_FIELDS["name"], key_value)
        else:
            data = self.db.select_value(SALARY_FIELDS["name"])
        return data

    def get_employer_url_logo(self, key_value: dict[str, any] = None) -> list:
        """
        ru: Получить логотипы работодателей из базы данных.
        en: Get employer logos from the database.
        :param key_value: ключ и значение для поиска
        """
        if key_value:
            data = self.db.select_value(EMPLOYER_URL_LOGO_FIELDS["name"], key_value)
        else:
            data = self.db.select_value(EMPLOYER_URL_LOGO_FIELDS["name"])
        return data

    def get_employer(self, key_value: dict[str, any] = None) -> list:
        """
        ru: Получить работодателей из базы данных.
        en: Get employers from the database.
        :param key_value: ключ и значение для поиска
        """
        if key_value:
            data = self.db.select_value(EMPLOYER_FIELDS["name"], key_value)
        else:
            data = self.db.select_value(EMPLOYER_FIELDS["name"])
        for employer in data:
            logo = self.get_employer_url_logo({"key": "employer_id", "value": employer["id"]})
            logo = logo[0] if logo else None
            employer["logo_urls"] = logo
        return data

    def get_vacancy(self, key_value: dict[str, any] = None) -> list:
        """
        ru: Получить вакансии из базы данных.
        en: Get vacancies from the database.
        :param key_value: ключ и значение для поиска
        """
        if key_value:
            data = self.db.select_value(VACANCY_FIELDS["name"], key_value)
        else:
            data = self.db.select_value(VACANCY_FIELDS["name"])

        for vacancy in data:
            area = self.get_area({"key": "id", "value": vacancy.pop("area_id")})
            area = area[0] if area else None
            vacancy["area"] = area

            experience = self.get_experience({"key": "id", "value": vacancy.pop("experience_id")})
            experience = experience[0] if experience else None
            vacancy["experience"] = experience

            employment = self.get_employment({"key": "id", "value": vacancy.pop("employment_id")})
            employment = employment[0] if employment else None
            vacancy["employment"] = employment

            schedule = self.get_schedule({"key": "id", "value": vacancy.pop("schedule_id")})
            schedule = schedule[0] if schedule else None
            vacancy["schedule"] = schedule
            salary = self.get_salary({"key": "vacancy_id", "value": vacancy["id"]})
            if salary:
                salary = {
                    "from": salary[0]["from"],
                    "to": salary[0]["to"],
                    "currency": salary[0]["currency"],
                    "gross": salary[0]["gross"]
                }
            else:
                salary = None
            vacancy["salary"] = salary

            employer = self.get_employer({"key": "id", "value": vacancy.pop("employer_id")})
            employer = employer[0] if employer else None
            vacancy["employer"] = employer

        return data


class FilterDataDB:
    """
    ru: Класс для фильтрации вакансий из базы данных.
    en: Class for filtering vacancies from the database.
    """
    def __init__(self, items: list[dict[str, any]]):
        """
        :param items: list of vacancies
        """
        self.items = items

    def filter(self, text: str, key: str) -> list:
        """
        ru: Фильтрация вакансий по локации.
        en: Filtering vacancies by location.
        """
        return [item for item in self.items if text.lower() in item[key].lower()]
