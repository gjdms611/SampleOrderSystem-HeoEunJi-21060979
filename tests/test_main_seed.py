from main import seed_default_samples
from repository.inventory_repository import InventoryRepository
from repository.sample_repository import SampleRepository


def test_seed_default_samples_registers_five_samples_when_empty(tmp_path):
    sample_repo = SampleRepository(str(tmp_path / "samples.json"))
    inventory_repo = InventoryRepository(str(tmp_path / "inventories.json"))

    seed_default_samples(sample_repo, inventory_repo)

    samples = sample_repo.find_all()
    assert len(samples) == 5
    assert sample_repo.find_by_id("S-001") is not None
    assert inventory_repo.find_by_sample_id("S-001").quantity == 480


def test_seed_default_samples_does_nothing_when_samples_already_exist(tmp_path):
    from model.sample import Sample

    sample_repo = SampleRepository(str(tmp_path / "samples.json"))
    inventory_repo = InventoryRepository(str(tmp_path / "inventories.json"))
    sample_repo.save(Sample("CUSTOM", "이미등록된시료", 1.0, 1.0))

    seed_default_samples(sample_repo, inventory_repo)

    samples = sample_repo.find_all()
    assert len(samples) == 1
    assert samples[0].sample_id == "CUSTOM"
