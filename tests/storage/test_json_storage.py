from storage.json_storage import load, save


def test_load_returns_empty_list_when_file_does_not_exist(tmp_path):
    path = tmp_path / "nonexistent.json"

    result = load(str(path))

    assert result == []


def test_save_then_load_round_trip_with_auto_created_directory(tmp_path):
    path = tmp_path / "nested" / "dir" / "data.json"
    data = [{"id": 1, "name": "sample"}]

    save(data, str(path))
    result = load(str(path))

    assert result == data
