"""
ru: Модуль для конфигурации проекта.
en: Module for project configuration.
"""

import os

# абсолютный путь к директории проекта / project root directory
ROOT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# директория базы данных / database directory
DB_DIR = os.path.join(ROOT_DIR, "data")

# название таблиц базы с описанием полей / database tables with fields description
VACANCY_FIELDS = {
    "name": "vacancy",
    "fields": {
        "id": "TEXT NOT NULL",
        "name": "TEXT NOT NULL",
        "employer_id": "TEXT NOT NULL",
        "area_id": "TEXT NOT NULL",
        "created_at": "TEXT NOT NULL",
        "published_at": "TEXT NOT NULL",
        "experience_id": "TEXT",
        "employment_id": "TEXT",
        "schedule_id": "TEXT",
        "alternate_url": "TEXT NOT NULL",
        "description": "TEXT"
    }
}


EMPLOYER_FIELDS = {
    "name": "employer",
    "fields": {
        "id": "TEXT NOT NULL",
        "name": "TEXT NOT NULL",
        "alternate_url": "TEXT NOT NULL",
        "accredited_it_employer": "BOOLEAN",
        "description": "TEXT",
        "site_url": "TEXT",
    }
}


SALARY_FIELDS = {
    "name": "salary",
    "fields": {
        "from": "INTEGER",
        "to": "INTEGER",
        "currency": "TEXT",
        "gross": "BOOLEAN",
        "vacancy_id": "TEXT NOT NULL"
    }
}

AREA_FIELDS = {
    "name": "area",
    "fields": {
        "id": "TEXT NOT NULL",
        "name": "TEXT NOT NULL",
        "url": "TEXT NOT NULL"
    }
}

EXPERIENCE_FIELDS = {
    "name": "experience",
    "fields": {
        "id": "TEXT NOT NULL",
        "name": "TEXT NOT NULL"
    }
}

EMPLOYMENT_FIELDS = {
    "name": "employment",
    "fields": {
        "id": "TEXT NOT NULL",
        "name": "TEXT NOT NULL"
    }
}

SCHEDULE_FIELDS = {
    "name": "schedule",
    "fields": {
        "id": "TEXT NOT NULL",
        "name": "TEXT NOT NULL"
    }
}

EMPLOYER_URL_LOGO_FIELDS = {
    "name": "employer_url_logo",
    "fields": {
        "90": "TEXT",
        "240": "TEXT",
        "original": "TEXT",
        "employer_id": "TEXT NOT NULL"
    }
}
