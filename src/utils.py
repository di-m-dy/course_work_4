"""
ru: Модуль с функциями для работы с базой данных и парсинга данных.
en: Module with functions for working with a database and parsing data.
"""

from src.data_base import BaseDB, JsonDB
from src.api_parser import JobObject
from src.hh_parser import HHVacancy, HHSalary, HHEmployer


VACANCIES_FIELDS = {
    "id": "INTEGER NOT NULL",
    "name": "TEXT NOT NULL",
    "employer": "TEXT NOT NULL",
    "area": "TEXT",
    "created_at": "TEXT NOT NULL",
    "published_at": "TEXT NOT NULL",
    "experience": "TEXT",
    "employment": "TEXT",
    "schedule": "TEXT",
    "alternate_url": "TEXT NOT NULL",
    "description": "TEXT"
}


EMPLOYERS_FIELDS = {
    "id": "INTEGER NOT NULL",
    "name": "TEXT NOT NULL",
    "alternate_url": "TEXT NOT NULL",
    "accredited_it_employer": "BOOLEAN",
    "description": "TEXT",
    "site_url": "TEXT",
    "area": "TEXT"
}


SALARY_FIELDS = {
    "vacancy_id": "INTEGER NOT NULL",
    "from": "INTEGER",
    "to": "INTEGER",
    "currency": "TEXT",
    "gross": "BOOLEAN"
}


def save_vacancies_to_db(db: BaseDB, items: list[HHVacancy]):
    """
    ru: Сохранение данных в формате JSON.
    en: Saving data in JSON format.
    :param db: database object
    :param items: list of objects
    """

    for item in items:
        vacancy = {"id": item.id_, "name": item.name, "area": item.area["id"], "created_at": item.created_at,
                   "published_at": item.published_at, "experience": item.experience, "employment": item.employment,
                   "schedule": item.schedule, "alternate_url": item.alternate_url, "description": item.description,
                   "salary": item.salary.get_dict() if item.salary else None, "employer": item.employer.id_}
        employer = item.employer.get_dict()
        db.add_value("employers", employer)
        db.add_value("vacancies", vacancy)


def create_areas_for_db(db: BaseDB):
    """
    ru: Создание областей для данных.
    en: Creating areas for data.
    :param db: database object
    """
    try:
        db.create_area("vacancies", VACANCIES_FIELDS)
        db.create_area("employers", EMPLOYERS_FIELDS)
    except FileExistsError:
        return


def check_areas(db: BaseDB):
    """
    ru: Проверка наличия областей для данных.
    en: Checking the presence of areas for data.
    :param db: database object
    """
    if not db.check_area_name("vacancies"):
        db.create_area("vacancies", VACANCIES_FIELDS)
    if not db.check_area_name("employers"):
        db.create_area("employers", EMPLOYERS_FIELDS)
    if not db.check_area_name("salaries"):
        db.create_area("salaries", SALARY_FIELDS)

