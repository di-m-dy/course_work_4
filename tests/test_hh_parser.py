import pytest
from unittest.mock import patch
from src.hh_parser import (
    HHFindVacancy,
    HHFindEmployer,
    HHInfoVacancy,
    HHInfoEmployer,
    HHGenerateVacanciesList,
    HHGenerateEmployersList,
    HHSchedule,
    HHExperience,
    HHEmployment,
    HHArea,
    HHSalary,
    HHEmployerUrlLogo,
    HHEmployer,
    HHVacancy
)
from src.api_errors import AttrValueRestrictionError


@pytest.fixture
def vacancy_data():
    return {
        "id": "1",
        "name": "Software Engineer",
        "created_at": "2021-01-01T00:00:00",
        "published_at": "2021-01-01T00:00:00",
        "alternate_url": "http://example.com/vacancy/1",
        "employer": {"id": "1", "name": "ExampleCorp", "alternate_url": "http://example.com/employer/1"},
        "salary": {"from": 1000, "to": 2000, "currency": "USD"},
        "area": {"id": "1", "name": "Remote", "url": "http://example.com/area/1"},
        "experience": {"id": "1", "name": "No experience"},
        "employment": {"id": "1", "name": "Full time"},
        "schedule": {"id": "1", "name": "Flexible"},
        "description": "Job description here"
    }


@pytest.fixture
def employer_data():
    return {
        "id": "1",
        "name": "ExampleCorp",
        "alternate_url": "http://example.com/employer/1",
        "logo_urls": {"original": "http://example.com/logo.png"},
        "accredited_it_employer": True,
        "description": "Employer description here",
        "site_url": "http://example.com"
    }


class TestHHFindVacancy:
    def test_find_vacancy_with_valid_parameters_returns_vacancies(self):
        hh_find_vacancy = HHFindVacancy()
        assert hh_find_vacancy.scope == "https://api.hh.ru/vacancies"
        assert hh_find_vacancy.headers == {"User-Agent": "HH-User-Agent"}
        with patch('src.api_parser.ApiFindBase.find') as mock_find:
            mock_find.return_value = {"items": [], "found": 0}
            result = hh_find_vacancy.find(text="Python Developer")
            assert "items" in result
            assert result["found"] == 0

    def test_find_vacancy_with_invalid_per_page_raises_error(self):
        hh_find_vacancy = HHFindVacancy()
        with pytest.raises(AttrValueRestrictionError):
            hh_find_vacancy.find(per_page=101)


class TestHHFindEmployer:
    def test_find_employer_with_valid_parameters_returns_employers(self):
        hh_find_employer = HHFindEmployer()
        with patch('src.api_parser.ApiFindBase.find') as mock_find:
            mock_find.return_value = {"items": [], "found": 0}
            result = hh_find_employer.find(text="ExampleCorp")
            assert "items" in result
            assert result["found"] == 0


class TestHHInfoVacancy:
    def test_info_vacancy_returns_correct_vacancy_info(self, vacancy_data):
        hh_info_vacancy = HHInfoVacancy(id_=vacancy_data["id"])
        with patch('src.api_parser.ApiInfoBase.info') as mock_info:
            mock_info.return_value = vacancy_data
            result = hh_info_vacancy.info()
            assert result["id"] == vacancy_data["id"]
            assert result["name"] == vacancy_data["name"]


class TestHHInfoEmployer:
    def test_info_employer_returns_correct_employer_info(self, employer_data):
        hh_info_employer = HHInfoEmployer(id_=employer_data["id"])
        with patch('src.api_parser.ApiInfoBase.info') as mock_info:
            mock_info.return_value = employer_data
            result = hh_info_employer.info()
            assert result["id"] == employer_data["id"]
            assert result["name"] == employer_data["name"]


class TestHHGenerateVacanciesList:
    def test_generate_vacancies_list_creates_vacancy_objects(self, vacancy_data):
        hh_generate_vacancies_list = HHGenerateVacanciesList(items=[vacancy_data])
        vacancies_list = hh_generate_vacancies_list.generate()
        assert len(vacancies_list) == 1
        assert vacancies_list[0].id_ == vacancy_data["id"]
        assert vacancies_list[0].name == vacancy_data["name"]


class TestHHGenerateEmployersList:
    def test_generate_employers_list_creates_employer_objects(self, employer_data):
        hh_generate_employers_list = HHGenerateEmployersList([employer_data])
        employers_list = hh_generate_employers_list.generate()
        assert len(employers_list) == 1
        assert employers_list[0].id_ == employer_data["id"]
        assert employers_list[0].name == employer_data["name"]


class TestHHScheduleStr:
    def test_str_returns_correct_schedule(self):
        schedule = HHSchedule(id_="1", name="Full time")
        assert str(schedule) == "График работы: Full time"


class TestHHExperienceStr:
    def test_str_returns_correct_experience(self):
        experience = HHExperience(id_="1", name="No experience")
        assert str(experience) == "Опыт работы: No experience"


class TestHHEmploymentStr:
    def test_str_returns_correct_employment(self):
        employment = HHEmployment(id_="1", name="Full time")
        assert str(employment) == "Тип занятости: Full time"


class TestHHAreaStr:
    def test_str_returns_correct_area(self):
        area = HHArea(id_="1", name="Remote", url="http://example.com/area/1")
        assert str(area) == "Регион: Remote"


class TestHHSalary:
    def test_str_returns_correct_salary(self):
        salary_1 = HHSalary(from_=1000, to=2000, currency="USD", gross=False)
        salary_2 = HHSalary(from_=1000, to=None, currency="USD", gross=False)
        salary_3 = HHSalary(from_=None, to=2000, currency="USD", gross=False)
        salary_4 = HHSalary(from_=10, to=50, currency="USD", gross=False)
        salary_5 = HHSalary(from_=None, to=None, currency="USD", gross=True)
        assert str(salary_1) == "Зарплата: от 1000 до 2000 USD"
        assert salary_2 < salary_3
        assert None < salary_3
        assert not salary_2 < None
        assert salary_4 < salary_1
        assert salary_4 < salary_3
        assert salary_4 < salary_2
        assert salary_2 < salary_1
        assert salary_3 > salary_2
        assert salary_3 > None
        assert salary_2 > None
        assert salary_1 > salary_4
        assert salary_3 > salary_4
        assert salary_2 > salary_4
        assert salary_1 > salary_2
        assert str(salary_1) == "Зарплата: от 1000 до 2000 USD"
        assert str(salary_2) == "Зарплата: от 1000 USD"
        assert str(salary_3) == "Зарплата: до 2000 USD"
        assert str(salary_5) == "Уровень дохода не указан"


class TestHHEmployerUrlLogo:
    def test_get_dict_returns_correct_dict(self, employer_data):
        employer_url_logo = HHEmployerUrlLogo(**{"original": "test", "90": "test", "240": "test"})
        assert employer_url_logo.get_dict() == {"original": "test", "90": "test", "240": "test"}


class TestHHEmployerStr:
    def test_str_returns_correct_employer(self, employer_data):
        employer = HHEmployer(
            id_=employer_data["id"],
            name=employer_data["name"],
            alternate_url=employer_data["alternate_url"],
            logo_urls=employer_data["logo_urls"],
            accredited_it_employer=employer_data["accredited_it_employer"],
            description=employer_data["description"],
            site_url=employer_data["site_url"]
        )
        assert str(employer) == "Работодатель: ExampleCorp\nСсылка работодателя: http://example.com/employer/1"

class TestHHVacancy:
    def test_str(self):
        vacancy = HHVacancy(
            id_="1",
            name="Software Engineer",
            created_at="2021-01-01T00:00:00",
            published_at="2021-01-01T00:00:00",
            alternate_url="http://example.com/vacancy/1",
            employer={"id": "1", "name": "ExampleCorp", "alternate_url": "http://example.com/employer/1"},
            salary={"from": 1000, "to": 2000, "currency": "USD"},
            area={"id": "1", "name": "Remote", "url": "http://example.com/area/1"},
            experience={"id": "1", "name": "No experience"},
            employment={"id": "1", "name": "Full time"},
            schedule={"id": "1", "name": "Flexible"},
            description="Job description here"
        )
        assert str(vacancy) == ("Вакансия: Software Engineer\n"
                                "Опубликовано: 01-01-2021\n"
                                "Ссылка вакансии: http://example.com/vacancy/1")






