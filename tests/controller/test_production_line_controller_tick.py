import time

from controller.order_controller import OrderController
from controller.production_line_controller import ProductionLineController
from model.inventory import Inventory
from model.order import OrderStatus
from model.production_queue import ProductionQueue
from repository.inventory_repository import InventoryRepository
from repository.order_repository import OrderRepository
from repository.sample_repository import SampleRepository


def make_all(tmp_path):
    sample_repo = SampleRepository(str(tmp_path / "samples.json"))
    inventory_repo = InventoryRepository(str(tmp_path / "inventories.json"))
    order_repo = OrderRepository(str(tmp_path / "orders.json"))
    queue = ProductionQueue(line_count=1)

    order_controller = OrderController(order_repo, inventory_repo, sample_repo, queue)
    line_controller = ProductionLineController(queue)

    return order_controller, line_controller, inventory_repo, order_repo, queue


def start_producing_order(order_controller, sample_repo, inventory_repo, total_production_time):
    from model.sample import Sample

    sample_repo.save(Sample("S1", "Wafer-A", avg_production_time=total_production_time / 3, yield_rate=1.0))
    inventory_repo.save(Inventory("S1", 0))

    order = order_controller.submit(customer_name="Acme", sample_id="S1", quantity=3)
    approved = order_controller.approve(order.order_id)
    assert approved.status == OrderStatus.PRODUCING
    return order


def test_tick_advances_produced_qty_without_completing(tmp_path):
    order_controller, line_controller, inventory_repo, order_repo, queue = make_all(tmp_path)
    sample_repo = order_controller.sample_repo
    order = start_producing_order(order_controller, sample_repo, inventory_repo, total_production_time=3.0)

    job = queue.lines[0]
    job.started_at = time.time() - 2.5

    confirmed_orders = line_controller.tick(inventory_repo, order_controller)

    assert job.produced_qty == 2
    assert confirmed_orders == []
    assert order_repo.find_by_id(order.order_id).status == OrderStatus.PRODUCING


def test_tick_completes_job_and_confirms_order_when_elapsed_covers_full_duration(tmp_path):
    order_controller, line_controller, inventory_repo, order_repo, queue = make_all(tmp_path)
    sample_repo = order_controller.sample_repo
    order = start_producing_order(order_controller, sample_repo, inventory_repo, total_production_time=3.0)

    job = queue.lines[0]
    job.started_at = time.time() - 10

    confirmed_orders = line_controller.tick(inventory_repo, order_controller)

    assert queue.lines[0] is None
    assert len(confirmed_orders) == 1
    assert confirmed_orders[0].order_id == order.order_id
    assert confirmed_orders[0].status == OrderStatus.CONFIRMED
    assert order_repo.find_by_id(order.order_id).status == OrderStatus.CONFIRMED
