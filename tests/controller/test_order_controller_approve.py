from controller.order_controller import OrderController
from model.inventory import Inventory
from model.order import Order, OrderStatus
from model.production_queue import ProductionQueue
from model.sample import Sample
from repository.inventory_repository import InventoryRepository
from repository.order_repository import OrderRepository
from repository.sample_repository import SampleRepository


def make_controller(tmp_path, line_count=1):
    order_repo = OrderRepository(str(tmp_path / "orders.json"))
    inventory_repo = InventoryRepository(str(tmp_path / "inventories.json"))
    sample_repo = SampleRepository(str(tmp_path / "samples.json"))
    production_queue = ProductionQueue(line_count=line_count)
    controller = OrderController(order_repo, inventory_repo, sample_repo, production_queue)
    return controller, order_repo, inventory_repo, sample_repo, production_queue


def test_approve_with_sufficient_inventory_confirms_and_saves_order(tmp_path):
    controller, order_repo, inventory_repo, sample_repo, queue = make_controller(tmp_path)
    sample_repo.save(Sample("S1", "Wafer-A", 2.5, 0.9))
    inventory_repo.save(Inventory("S1", 20))
    order = controller.submit(customer_name="Acme", sample_id="S1", quantity=10)

    result = controller.approve(order.order_id)

    assert result.status == OrderStatus.CONFIRMED
    assert order_repo.find_by_id(order.order_id).status == OrderStatus.CONFIRMED


def test_approve_with_insufficient_inventory_producing_and_enqueues_job(tmp_path):
    controller, order_repo, inventory_repo, sample_repo, queue = make_controller(tmp_path)
    sample_repo.save(Sample("S1", "Wafer-A", 2.5, 0.9))
    inventory_repo.save(Inventory("S1", 3))
    order = controller.submit(customer_name="Acme", sample_id="S1", quantity=10)

    result = controller.approve(order.order_id)

    assert result.status == OrderStatus.PRODUCING
    assert order_repo.find_by_id(order.order_id).status == OrderStatus.PRODUCING
    assert queue.lines[0] is not None
    assert queue.lines[0].order_id == order.order_id
    assert queue.lines[0].shortage == 7


def test_approve_when_inventory_not_registered_treats_it_as_zero_and_producing(tmp_path):
    controller, order_repo, inventory_repo, sample_repo, queue = make_controller(tmp_path)
    sample_repo.save(Sample("S1", "Wafer-A", 2.5, 0.9))
    order = controller.submit(customer_name="Acme", sample_id="S1", quantity=10)

    result = controller.approve(order.order_id)

    assert result.status == OrderStatus.PRODUCING
    assert queue.lines[0].shortage == 10


def test_approve_on_non_reserved_order_returns_none_without_raising(tmp_path):
    controller, order_repo, inventory_repo, sample_repo, queue = make_controller(tmp_path)
    sample_repo.save(Sample("S1", "Wafer-A", 2.5, 0.9))
    inventory_repo.save(Inventory("S1", 20))
    order = controller.submit(customer_name="Acme", sample_id="S1", quantity=10)
    controller.reject(order.order_id)

    result = controller.approve(order.order_id)

    assert result is None


def test_approve_on_nonexistent_order_id_returns_none_without_raising(tmp_path):
    controller, order_repo, inventory_repo, sample_repo, queue = make_controller(tmp_path)

    result = controller.approve("NOPE")

    assert result is None


def test_approve_on_order_with_unregistered_sample_returns_none_without_raising(tmp_path):
    controller, order_repo, inventory_repo, sample_repo, queue = make_controller(tmp_path)
    order = Order("O1", "Acme", "NOPE", 10)
    order_repo.save(order)

    result = controller.approve("O1")

    assert result is None
