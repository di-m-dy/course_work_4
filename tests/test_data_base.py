import pytest
import json
import os
from src.data_base import JsonDB


class TestJsonDB:
    @pytest.fixture
    def setup_jsondb(self, tmp_path):
        db_path = tmp_path / "testdb"
        db = JsonDB(str(db_path))
        return db, db_path

    def test_path_exists(self, setup_jsondb):
        path = os.path.dirname(__file__)
        db = JsonDB(path)
        assert os.path.exists(path) and db.path == path

    def test_create_area_creates_new_file(self, setup_jsondb):
        db, db_path = setup_jsondb
        area_name = "test_area"
        fields = {"id": "INTEGER", "name": "TEXT"}
        db.create_area(area_name, fields)
        assert (db_path / f"{area_name}.json").exists()

    def test_delete_area_removes_file(self, setup_jsondb):
        db, db_path = setup_jsondb
        area_name = "test_area"
        fields = {"id": "INTEGER", "name": "TEXT"}
        db.create_area(area_name, fields)
        db.delete_area(area_name)
        assert not (db_path / f"{area_name}.json").exists()

    def test_add_value_to_area(self, setup_jsondb):
        db, db_path = setup_jsondb
        area_name = "test_area"
        fields = {"id": "INTEGER", "name": "TEXT"}
        db.create_area(area_name, fields)
        db.add_value(area_name, {"id": 1, "name": "Test"})
        with open(db_path / f"{area_name}.json", 'r') as file:
            data = json.load(file)
        assert {"id": 1, "name": "Test"} in data
        with pytest.raises(FileNotFoundError):
            db.add_value("nonexistent_area", {"id": 1, "name": "Test"})

    def test_update_value_in_area(self, setup_jsondb):
        db, db_path = setup_jsondb
        area_name = "test_area"
        fields = {"id": "INTEGER", "name": "TEXT"}
        db.create_area(area_name, fields)
        db.add_value(area_name, {"id": 1, "name": "Test"})
        db.update_value(area_name, "name", "Updated Test", "id", 1)
        with open(db_path / f"{area_name}.json", 'r') as file:
            data = json.load(file)
        assert any(record["name"] == "Updated Test" for record in data)
        with pytest.raises(FileNotFoundError):
            db.update_value(
                "nonexistent_area",
                "name",
                "Updated Test",
                "id",
                1
            )

    def test_delete_value_from_area(self, setup_jsondb):
        db, db_path = setup_jsondb
        area_name = "test_area"
        fields = {"id": "INTEGER", "name": "TEXT"}
        db.create_area(area_name, fields)
        db.add_value(area_name, {"id": 1, "name": "Test"})
        db.delete_value(area_name, "id", 1)
        with open(db_path / f"{area_name}.json", 'r') as file:
            data = json.load(file)
        check = any([record["id"] == 1 for record in data])
        assert check is False
        with pytest.raises(FileNotFoundError):
            db.delete_value("nonexistent_area", "id", 1)

    def test_select_value_from_area_returns_correct_data(self, setup_jsondb):
        db, db_path = setup_jsondb
        area_name = "test_area"
        fields = {"id": "INTEGER", "name": "TEXT"}
        db.create_area(area_name, fields)
        db.add_value(area_name, {"id": 1, "name": "Test"})
        db.add_value(area_name, {"id": 2, "name": "Test2"})
        result = db.select_value(area_name, {"key": "id", "value": 1})
        assert result[0] == {"id": 1, "name": "Test"} and len(result) == 1
        all_data = db.select_value(area_name)
        assert all_data == [{"id": 1, "name": "Test"}, {"id": 2, "name": "Test2"}] and len(all_data) == 2

    def test_create_area_with_existing_name_raises_error(self, setup_jsondb):
        db, db_path = setup_jsondb
        area_name = "test_area"
        fields = {"id": "INTEGER", "name": "TEXT"}
        db.create_area(area_name, fields)
        with pytest.raises(FileExistsError):
            db.create_area(area_name, fields)

    def test_delete_nonexistent_area_raises_error(self, setup_jsondb):
        db, _ = setup_jsondb
        with pytest.raises(FileNotFoundError):
            db.delete_area("nonexistent_area")

    def test_add_value_with_mismatched_fields_raises_error(self, setup_jsondb):
        db, db_path = setup_jsondb
        area_name = "test_area"
        fields = {"id": "INTEGER", "name": "TEXT"}
        db.create_area(area_name, fields)
        with pytest.raises(TypeError):
            db.add_value(area_name, {"id": 1})

    def test_add_value_with_incorrect_types_raises_error(self, setup_jsondb):
        db, db_path = setup_jsondb
        area_name = "test_area"
        fields = {"id": "INTEGER", "name": "TEXT"}
        db.create_area(area_name, fields)
        with pytest.raises(TypeError):
            db.add_value(area_name, {"id": "one", "name": "Test"})
