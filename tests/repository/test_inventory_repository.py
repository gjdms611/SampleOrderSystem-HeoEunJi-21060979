from model.inventory import Inventory
from repository.inventory_repository import InventoryRepository


def test_save_then_find_by_sample_id_round_trip(tmp_path):
    path = tmp_path / "inventories.json"
    repo = InventoryRepository(str(path))
    inventory = Inventory("S001", 100)

    repo.save(inventory)
    result = repo.find_by_sample_id("S001")

    assert result is not None
    assert result.sample_id == "S001"
    assert result.quantity == 100


def test_find_by_sample_id_returns_none_when_not_found(tmp_path):
    path = tmp_path / "inventories.json"
    repo = InventoryRepository(str(path))

    result = repo.find_by_sample_id("UNKNOWN")

    assert result is None
