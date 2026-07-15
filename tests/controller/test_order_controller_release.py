from controller.order_controller import OrderController
from model.order import Order, OrderStatus
from model.production_queue import ProductionQueue
from repository.inventory_repository import InventoryRepository
from repository.order_repository import OrderRepository
from repository.sample_repository import SampleRepository


def make_controller(tmp_path):
    order_repo = OrderRepository(str(tmp_path / "orders.json"))
    inventory_repo = InventoryRepository(str(tmp_path / "inventories.json"))
    sample_repo = SampleRepository(str(tmp_path / "samples.json"))
    production_queue = ProductionQueue(line_count=1)
    return OrderController(order_repo, inventory_repo, sample_repo, production_queue), order_repo


def test_release_order_transitions_confirmed_to_release_and_persists(tmp_path):
    controller, order_repo = make_controller(tmp_path)
    order = Order("O1", "Acme", "S1", 10)
    order.status = OrderStatus.CONFIRMED
    order_repo.save(order)

    result = controller.release_order("O1")

    assert result.status == OrderStatus.RELEASE
    assert order_repo.find_by_id("O1").status == OrderStatus.RELEASE


def test_release_order_on_non_confirmed_order_returns_none_without_raising(tmp_path):
    controller, order_repo = make_controller(tmp_path)
    order = Order("O1", "Acme", "S1", 10)
    order_repo.save(order)

    result = controller.release_order("O1")

    assert result is None
    assert order_repo.find_by_id("O1").status == OrderStatus.RESERVED


def test_release_order_on_nonexistent_order_id_returns_none_without_raising(tmp_path):
    controller, _order_repo = make_controller(tmp_path)

    result = controller.release_order("NOPE")

    assert result is None
