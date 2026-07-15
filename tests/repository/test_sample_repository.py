from model.sample import Sample
from repository.sample_repository import SampleRepository


def test_save_then_find_by_id_round_trip(tmp_path):
    path = tmp_path / "samples.json"
    repo = SampleRepository(str(path))
    sample = Sample("S001", "Wafer-A", 2.5, 0.9)

    repo.save(sample)
    result = repo.find_by_id("S001")

    assert result is not None
    assert result.sample_id == "S001"
    assert result.name == "Wafer-A"
    assert result.avg_production_time == 2.5
    assert result.yield_rate == 0.9


def test_find_by_id_returns_none_when_not_found(tmp_path):
    path = tmp_path / "samples.json"
    repo = SampleRepository(str(path))

    result = repo.find_by_id("UNKNOWN")

    assert result is None


def test_search_by_keyword_matches_name_substring(tmp_path):
    path = tmp_path / "samples.json"
    repo = SampleRepository(str(path))
    repo.save(Sample("S001", "Wafer-A", 2.5, 0.9))
    repo.save(Sample("S002", "Wafer-B", 3.0, 0.8))
    repo.save(Sample("S003", "Chip-C", 1.5, 0.95))

    result = repo.search("Wafer")

    assert {s.sample_id for s in result} == {"S001", "S002"}


def test_save_with_same_id_overwrites_existing_entry(tmp_path):
    path = tmp_path / "samples.json"
    repo = SampleRepository(str(path))
    repo.save(Sample("S001", "Wafer-A", 2.5, 0.9))

    repo.save(Sample("S001", "Wafer-A-Updated", 3.5, 0.7))
    result = repo.find_by_id("S001")

    assert result.name == "Wafer-A-Updated"
    assert result.avg_production_time == 3.5
    assert result.yield_rate == 0.7
