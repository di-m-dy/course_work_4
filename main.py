"""
en: Main file of the project for running the application.
ru: Главный файл проекта для запуска приложения.
"""

from src.api_parser import VacancyApiHH


def run():
    vacancies = VacancyApiHH()
    vacancies.set_parameters(period=2, text="Python Junior", search_field='name')
    data = vacancies.get_data()
    for i in data['items']:
        print(i['name'])


if __name__ == "__main__":
    run()
