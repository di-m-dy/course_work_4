"""
ru: Модуль для работы с пользовательским интерфейсом в CLI.
Классы и методы:
    UserInterface:
        start - запуск пользовательского интерфейса
        stop - остановка пользовательского интерфейса
        get_user_input - получение ввода пользователя
        show_message - вывод сообщения пользователю
        show_menu - вывод меню пользователю
        show_table - вывод таблицы пользователю
    en: Module for working with the user interface in CLI.
Classes and methods:
    UserInterface:
        start - start user interface
        stop - stop user interface
        get_user_input - get user input
        show_message - show message to user
        show_menu - show menu to user
        show_table - show table to user
"""

import os
import sys

import html2text

from abc import ABC, abstractmethod
from src.hh_parser import (
    HHFindVacancy,
    HHFindEmployer,
    HHInfoVacancy,
    HHInfoEmployer,
    HHVacancy,
    HHSalary,
    HHEmployer,
    HHGenerateVacanciesList,
    HHGenerateEmployersList
)
from src.data_base import JsonDB
from src.utils import create_areas_for_db, save_vacancies_to_db, check_areas


class WidgetCLIBase(ABC):
    @abstractmethod
    def show(self):
        pass

    @abstractmethod
    def get_callback(self, key: str):
        pass


class WidgetCLI(WidgetCLIBase):
    """
    ru: Виджет для работы с CLI.
        items - список словарей для отображения массива элементов:
        [{"text": str, "action": function, "args": dict}]
        footer - список словарей для дополнительных функций:
        [{"key": str, "text": str, "action": function, "args": dict}]
    en: Widget for working with CLI.
        items - list of dictionaries for displaying an array of elements:
        [{"text": str, "action": function, "args": dict}]
        footer - list of dictionaries for additional functions:
        [{"key": str, "text": str, "action": function, "args": dict}]
    :param header: заголовок
    :param description: описание
    :param items: элементы массива для отображения
    :param footer: дополнительные функции в низу страницы
    """
    def __init__(self, header: str, description: str, items: list[dict] = None, footer: list[dict] = None):
        self.header = header
        self.description = description
        self.items = items.copy() if items else []
        self.footer = footer.copy() if footer else []
        self.callbacks = {}

    @staticmethod
    def clear():
        os.system("clear")

    @staticmethod
    def stop():
        os.system("clear")
        sys.exit()

    @staticmethod
    def draw_line_header():
        print("+" * 70)

    @staticmethod
    def draw_line_items():
        print("-" * 70)

    def print_header(self):
        self.draw_line_header()
        print(self.header)
        self.draw_line_header()
        print('\n')

    def print_description(self):
        print(self.description)

    def print_items(self):
        print('\n')
        self.draw_line_items()
        print('\n')
        for i, item in enumerate(self.items):
            print(f"[{i + 1}] {item['text']}\n")
        self.draw_line_items()
        print('\n')

    def print_footer(self):
        for item in self.footer:
            print(f"[{item['key']}] {item['text']}")

    def show(self):
        self.clear()
        self.print_header()
        self.print_description()
        if self.items:
            self.print_items()
            self.callbacks = {str(i + 1): item for i, item in enumerate(self.items)}
        if self.footer:
            self.print_footer()
            self.callbacks.update({item["key"]: item for item in self.footer})
        if self.callbacks:
            self.get_callback(input())

    def invalid_input(self):
        self.clear()
        print("Неверный ввод! Попробуйте еще раз.")
        input("Нажмите любую клавишу.")

    def get_callback(self, key: str):
        if key == "exit":
            self.clear()
            self.stop()
        elif key in self.callbacks:
            arguments = self.callbacks[key].get("args")
            if arguments:
                self.callbacks[key]["action"](**arguments)
            else:
                self.callbacks[key]["action"]()
        else:
            self.invalid_input()
            self.show()


class WidgetCLIField(WidgetCLI):
    def __init__(self, header: str, description: str, callback: callable):
        super().__init__(header, description)
        self.header = header
        self.description = description
        self.callback = callback

    def show(self):
        self.clear()
        self.print_header()
        self.print_description()
        self.get_callback(input())

    def get_callback(self, key: str):
        if key == "exit":
            self.clear()
            self.stop()
        else:
            self.callback(key)


class UserInterface:
    def __init__(self):
        self.find_vacancy = HHFindVacancy()
        self.find_employer = HHFindEmployer()
        self.html2text = html2text.HTML2Text()
        self.db = JsonDB("data/json_db/")
        check_areas(self.db)

    def start(self):
        header = "[Г]лавное [М]еню"
        description = "HHParse - парсер вакансий и работодателей с сайта hh.ru\nВыберите действие:"
        items = [
            {"text": "ОНЛАЙН", "action": self.menu_online, "args": {}},
            {"text": "ЛОКАЛЬНО", "action": self.menu_local, "args": {}},
        ]
        footer = [
            {"key": "q", "text": "выход", "action": WidgetCLI.stop, "args": {}}
        ]
        widget = WidgetCLI(header, description, items, footer)
        widget.show()

    def menu_online(self):
        header = "[О]нлайн [М]еню"
        description = "Выберите действие:"
        items = [
            {"text": "Поиск вакансий", "action": self.find_vacancy_online, "args": {}},
            {"text": "Поиск работодателей", "action": self.find_employer_online, "args": {}},
        ]
        footer = [
            {"key": "<", "text": "назад", "action": self.start, "args": {}}
        ]
        widget = WidgetCLI(header, description, items, footer)
        widget.show()

    def menu_local(self):
        header = "[Л]окальное [М]еню"
        description = "Выберите действие:"
        items = [
            {"text": "Поиск вакансий", "action": self.find_vacancy_local, "args": {}},
            {"text": "Поиск работодателей", "action": self.find_employer_local, "args": {}},
        ]
        footer = [
            {"key": "<", "text": "назад", "action": self.start, "args": {}}
        ]
        widget = WidgetCLI(header, description, items, footer)
        widget.show()

    def find_vacancy_online(self):
        header = "[П]оиск [В]акансий [О]нлайн"
        description = "Быстрый поиск или расширенный поиск?"
        items = [
            {"text": "Быстрый поиск", "action": self.quick_search_menu, "args": {}},
            {"text": "Расширенный поиск", "action": self.advanced_search_vacancy, "args": {}},
        ]
        footer = [
            {"key": "<", "text": "назад", "action": self.menu_online, "args": {}}
        ]
        widget = WidgetCLI(header, description, items, footer)
        widget.show()

    def quick_search_menu(self):
        header = "[Б]ыстрый [П]оиск"
        description = "Введите название вакансии:"
        widget = WidgetCLIField(header, description, self.quick_search_vacancy)
        widget.show()

    def quick_search_vacancy(self, vacancy_name: str, page: int = 0, **kwargs):  #todo: передавать не название вакансии а словарь со всеми параметрами
        data = self.find_vacancy.find(text=vacancy_name, page=page, **kwargs)
        vacancies = data["items"]
        page = data["page"]
        pages = data["pages"]
        found = data["found"]
        obj_list = HHGenerateVacanciesList(vacancies).generate()
        header = f"Результаты поиска вакансий '{vacancy_name}':"
        description = f"Найдено {found} вакансий.\n{page + 1} страница из {pages}.\nВыберите вакансию для просмотра."
        items = [
            {
                "text": f"{str(obj)}\n{str(obj.salary)}\n{str(obj.employer)}",
                "action": self.show_info_vacancy,
                "args": {"vacancy": obj, "vacancy_name": vacancy_name, "page": page}
            } for obj in obj_list
        ]

        next_page = {
            "key": ">>",
            "text": "следующая страница",
            "action": self.quick_search_vacancy,
            "args": {"page": page + 1, "vacancy_name": vacancy_name}
        }
        prev_page = {
            "key": "<<",
            "text": "предыдущая страница",
            "action": self.quick_search_vacancy,
            "args": {"page": page - 1, "vacancy_name": vacancy_name}
        }
        footer = [
            {"key": "q", "text": "выйти", "action": self.find_vacancy_online, "args": {}},
            {"key": "s", "text": "сохранить страницу", "action": self.save_page_vacancies, "args": {"vacancies": vacancies, "page": page}}
        ]
        if page > 0:
            footer.append(prev_page)
        if page < pages:
            footer.append(next_page)
        widget = WidgetCLI(header, description, items, footer)
        widget.show()

    def show_info_vacancy(self, vacancy: HHVacancy, vacancy_name: str, page: int):
        vacancy_info = HHInfoVacancy(vacancy.id_).info()
        vacancy_description = self.html2text.handle(vacancy_info["description"])
        salary = f"Зарплата: {str(vacancy.salary) if vacancy.salary else 'не указана'}"
        employer = f"Работодатель: {str(vacancy.employer)}"
        header = f"Информация о вакансии '{vacancy.name}':"
        description = f"{salary}\n{employer}\n\n{vacancy_description}"
        footer = [
            {
                "key": "<",
                "text": "назад",
                "action": self.quick_search_vacancy,
                "args": {"vacancy_name": vacancy_name, "page": page}
            }
        ]
        widget = WidgetCLI(header=header, description=description, footer=footer)
        widget.show()

    def save_page_vacancies(self, vacancies: list[HHVacancy], page: int):
        save_vacancies_to_db(self.db, vacancies)
        header = "Сохранение данных"
        description = f"Страница {page} сохранена в базу данных."
        footer = [
            {"key": "<", "text": "назад", "action": self.quick_search_vacancy, "args": {}}
        ]
        widget = WidgetCLI(header=header, description=description, footer=footer)
        widget.show()

    def advanced_search_vacancy(self):
        pass

    def find_employer_online(self):
        pass

    def find_vacancy_local(self):
        pass

    def find_employer_local(self):
        pass

    def save_all_vacancies(self, vacancy_name: str):
        pass

    def save_vacancy_info(self):
        pass
