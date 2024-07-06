"""
en: Main file of the project for running the application.
ru: Главный файл проекта для запуска приложения.
"""

import json

from src.hh_parser import HHFindVacancy, HHVacancy, HHSalary, HHEmployer
from src.api_parser import JobObject
from src.user_interface import WidgetCLI, UserInterface


def run():
    ui = UserInterface()
    ui.start()


if __name__ == "__main__":
    run()
