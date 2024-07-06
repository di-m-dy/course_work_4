import pytest
import requests_mock
from src.api_parser import ApiBase, ApiFindBase, ApiInfoBase, JobObject, GenerateObjectsList
from src.api_errors import ApiQueryError


@pytest.fixture
def api_base():
    return ApiBase("http://example.com/api")


@pytest.fixture
def api_find_base():
    return ApiFindBase("http://example.com/api/search")


@pytest.fixture
def api_info_base():
    return ApiInfoBase("http://example.com/api/info", "123")


@pytest.fixture
def job_object_data():
    return {
        "id": 1,
        "name": "Developer",
        "type": "Full Time",
        "from": "2021-01-01"
    }


@pytest.fixture
def generate_objects_list_data():
    return [
        {"id": 1, "name": "Developer", "type": "Full Time", "from": "2021-01-01"},
        {"id": 2, "name": "Tester", "type": "Part Time", "from": "2021-02-01"}
    ]


class TestApiBase:
    @staticmethod
    def test_successful_query_returns_json(api_base):
        with requests_mock.Mocker() as m:
            m.get("http://example.com/api", json={"success": True}, status_code=200)
            response = api_base._query()
            assert response == {"success": True}

    @staticmethod
    def test_unsuccessful_query_raises_api_query_error(api_base):
        with requests_mock.Mocker() as m:
            m.get("http://example.com/api", status_code=404)
            with pytest.raises(ApiQueryError):
                api_base._query()


def test_find_method_returns_correct_data(api_find_base):
    with requests_mock.Mocker() as m:
        m.get("http://example.com/api/search", json={"results": []}, status_code=200)
        response = api_find_base.find(query="python")
        assert "results" in response


class TestApiInfoBase:
    @staticmethod
    def test_info_method_returns_correct_data(api_info_base):
        with requests_mock.Mocker() as m:
            m.get("http://example.com/api/info/123", json={"data": "info"}, status_code=200)
            response = api_info_base.info(id_=123)
            assert "data" in response


class TestJobObject:
    @staticmethod
    def test_job_object_creation_with_keywords(job_object_data):
        job = JobObject(**job_object_data)
        assert job.get_dict() == {"id": 1, "name": "Developer", "type": "Full Time", "from": "2021-01-01"}

    @staticmethod
    def test_rename_built_keys_method_renames_correctly(job_object_data):
        renamed_keys = JobObject.rename_built_keys(**job_object_data)
        assert renamed_keys == {"id_": 1, "name": "Developer", "type_": "Full Time", "from_": "2021-01-01"}

    @staticmethod
    def test_get_dict_method_continue(job_object_data):
        job = JobObject(**job_object_data)
        job._test = "test"
        assert job.get_dict() == {"id": 1, "name": "Developer", "type": "Full Time", "from": "2021-01-01"}


class TestGenerateObjectsList:
    @staticmethod
    def test_generate_objects_list_creates_correct_instances(generate_objects_list_data):
        generator = GenerateObjectsList(generate_objects_list_data)
        objects_list = generator.generate()
        assert len(objects_list) == 2
        assert all(isinstance(obj, JobObject) for obj in objects_list)
