import pytest

from model.inventory import Inventory


def test_creates_inventory_with_valid_values():
    inventory = Inventory(sample_id="S1", quantity=10)

    assert inventory.sample_id == "S1"
    assert inventory.quantity == 10


def test_allows_zero_quantity():
    inventory = Inventory(sample_id="S1", quantity=0)

    assert inventory.quantity == 0


def test_rejects_negative_quantity():
    with pytest.raises(ValueError):
        Inventory(sample_id="S1", quantity=-1)
