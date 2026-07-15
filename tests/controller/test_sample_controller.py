from controller.sample_controller import SampleController
from repository.sample_repository import SampleRepository


def test_register_creates_and_saves_sample(tmp_path):
    path = tmp_path / "samples.json"
    repo = SampleRepository(str(path))
    controller = SampleController(repo)

    result = controller.register("S001", "Wafer-A", 2.5, 0.9)

    assert result.sample_id == "S001"
    assert result.name == "Wafer-A"
    assert result.avg_production_time == 2.5
    assert result.yield_rate == 0.9

    saved = repo.find_by_id("S001")
    assert saved is not None
    assert saved.sample_id == "S001"
    assert saved.name == "Wafer-A"
    assert saved.avg_production_time == 2.5
    assert saved.yield_rate == 0.9


def test_get_returns_registered_sample(tmp_path):
    path = tmp_path / "samples.json"
    repo = SampleRepository(str(path))
    controller = SampleController(repo)
    controller.register("S001", "Wafer-A", 2.5, 0.9)

    result = controller.get("S001")

    assert result is not None
    assert result.sample_id == "S001"
    assert result.name == "Wafer-A"
    assert result.avg_production_time == 2.5
    assert result.yield_rate == 0.9


def test_get_returns_none_when_not_found(tmp_path):
    path = tmp_path / "samples.json"
    repo = SampleRepository(str(path))
    controller = SampleController(repo)

    result = controller.get("UNKNOWN")

    assert result is None


def test_search_returns_matching_samples_by_keyword(tmp_path):
    path = tmp_path / "samples.json"
    repo = SampleRepository(str(path))
    controller = SampleController(repo)
    controller.register("S001", "Wafer-A", 2.5, 0.9)
    controller.register("S002", "Wafer-B", 3.0, 0.8)
    controller.register("S003", "Chip-C", 1.5, 0.95)

    result = controller.search("Wafer")

    assert {s.sample_id for s in result} == {"S001", "S002"}


def test_list_all_returns_every_registered_sample(tmp_path):
    path = tmp_path / "samples.json"
    repo = SampleRepository(str(path))
    controller = SampleController(repo)
    controller.register("S001", "Wafer-A", 2.5, 0.9)
    controller.register("S002", "Wafer-B", 3.0, 0.8)

    result = controller.list_all()

    assert {s.sample_id for s in result} == {"S001", "S002"}
