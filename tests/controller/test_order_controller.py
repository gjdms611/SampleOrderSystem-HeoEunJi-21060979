from controller.order_controller import OrderController
from model.order import OrderStatus
from repository.inventory_repository import InventoryRepository
from repository.order_repository import OrderRepository
from repository.sample_repository import SampleRepository


def make_controller(tmp_path):
    order_repo = OrderRepository(str(tmp_path / "orders.json"))
    inventory_repo = InventoryRepository(str(tmp_path / "inventories.json"))
    sample_repo = SampleRepository(str(tmp_path / "samples.json"))
    return OrderController(order_repo, inventory_repo, sample_repo), order_repo


def test_submit_creates_reserved_order_with_sequential_id_and_saves_it(tmp_path):
    controller, order_repo = make_controller(tmp_path)

    order1 = controller.submit(customer_name="Acme", sample_id="S1", quantity=10)
    order2 = controller.submit(customer_name="Globex", sample_id="S2", quantity=5)

    assert order1.order_id == "O1"
    assert order1.status == OrderStatus.RESERVED
    assert order2.order_id == "O2"

    saved1 = order_repo.find_by_id("O1")
    assert saved1 is not None
    assert saved1.customer_name == "Acme"
    assert saved1.quantity == 10


def test_reject_transitions_order_to_rejected_and_persists(tmp_path):
    controller, order_repo = make_controller(tmp_path)
    order = controller.submit(customer_name="Acme", sample_id="S1", quantity=10)

    result = controller.reject(order.order_id)

    assert result.status == OrderStatus.REJECTED
    assert order_repo.find_by_id(order.order_id).status == OrderStatus.REJECTED


def test_cancel_transitions_reserved_order_to_rejected_and_persists(tmp_path):
    controller, order_repo = make_controller(tmp_path)
    order = controller.submit(customer_name="Acme", sample_id="S1", quantity=10)

    result = controller.cancel(order.order_id)

    assert result.status == OrderStatus.REJECTED
    assert order_repo.find_by_id(order.order_id).status == OrderStatus.REJECTED


def test_cancel_on_already_rejected_order_returns_none_without_raising(tmp_path):
    controller, order_repo = make_controller(tmp_path)
    order = controller.submit(customer_name="Acme", sample_id="S1", quantity=10)
    controller.reject(order.order_id)

    result = controller.cancel(order.order_id)

    assert result is None
    assert order_repo.find_by_id(order.order_id).status == OrderStatus.REJECTED
