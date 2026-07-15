from controller.monitoring_controller import MonitoringController
from controller.order_controller import OrderController
from controller.production_line_controller import ProductionLineController
from controller.sample_controller import SampleController
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

    sample_controller = SampleController(sample_repo, inventory_repo)
    order_controller = OrderController(order_repo, inventory_repo, sample_repo, queue)
    monitoring_controller = MonitoringController(order_repo, inventory_repo)
    line_controller = ProductionLineController(queue)

    return sample_controller, order_controller, monitoring_controller, line_controller, inventory_repo, order_repo, queue


def test_full_flow_submit_approve_shortage_produce_complete_release(tmp_path):
    (
        sample_controller,
        order_controller,
        monitoring_controller,
        line_controller,
        inventory_repo,
        order_repo,
        queue,
    ) = make_all(tmp_path)

    sample_controller.register("S1", "Wafer-A", avg_production_time=1.0, yield_rate=1.0)
    inventory_repo.save(Inventory("S1", 3))

    order = order_controller.submit(customer_name="Acme", sample_id="S1", quantity=10)
    assert order.status == OrderStatus.RESERVED

    approved = order_controller.approve(order.order_id)
    assert approved.status == OrderStatus.PRODUCING
    job = queue.lines[0]
    assert line_controller.current_jobs() == [job]
    assert job.shortage == 7
    assert job.actual_qty == 7

    counts = monitoring_controller.count_orders_by_status()
    assert counts[OrderStatus.PRODUCING] == 1

    inventory = inventory_repo.find_by_sample_id("S1")
    confirmed_jobs = []
    for _ in range(job.actual_qty):
        confirmed_jobs += queue.produce_unit(0, inventory)
    inventory_repo.save(inventory)

    assert confirmed_jobs == [job]
    assert line_controller.current_jobs() == []

    confirmed_orders = order_controller.complete_production(confirmed_jobs)

    assert len(confirmed_orders) == 1
    assert confirmed_orders[0].order_id == order.order_id
    assert confirmed_orders[0].status == OrderStatus.CONFIRMED
    assert order_repo.find_by_id(order.order_id).status == OrderStatus.CONFIRMED

    released = order_controller.release_order(order.order_id)
    assert released.status == OrderStatus.RELEASE
    assert order_repo.find_by_id(order.order_id).status == OrderStatus.RELEASE
