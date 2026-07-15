import time
from datetime import datetime

from controller.order_controller import OrderController
from controller.production_line_controller import ProductionLineController
from model.inventory import Inventory
from model.production_queue import ProductionQueue
from model.sample import Sample
from repository.inventory_repository import InventoryRepository
from repository.order_repository import OrderRepository
from repository.sample_repository import SampleRepository


def make_all(tmp_path, line_count=1):
    sample_repo = SampleRepository(str(tmp_path / "samples.json"))
    inventory_repo = InventoryRepository(str(tmp_path / "inventories.json"))
    order_repo = OrderRepository(str(tmp_path / "orders.json"))
    queue = ProductionQueue(line_count=line_count)

    order_controller = OrderController(order_repo, inventory_repo, sample_repo, queue)
    line_controller = ProductionLineController(queue)

    return order_controller, line_controller, sample_repo, inventory_repo, order_repo, queue


def test_describe_current_includes_required_fields_for_running_line(tmp_path):
    order_controller, line_controller, sample_repo, inventory_repo, order_repo, queue = make_all(tmp_path)
    sample_repo.save(Sample("S1", "Wafer-A", avg_production_time=1.0, yield_rate=1.0))
    inventory_repo.save(Inventory("S1", 0))
    order = order_controller.submit(customer_name="Acme", sample_id="S1", quantity=3)
    order_controller.approve(order.order_id)
    job = queue.lines[0]
    job.produced_qty = 1

    result = line_controller.describe_current(order_repo, sample_repo, inventory_repo)

    assert len(result) == 1
    row = result[0]
    assert row["order_id"] == order.order_id
    assert row["sample_name"] == "Wafer-A"
    assert row["quantity"] == 3
    assert row["inventory"] == 0
    assert row["shortage"] == job.shortage
    assert row["actual_qty"] == job.actual_qty
    assert row["produced_qty"] == 1
    assert row["yield_rate"] == 1.0
    assert row["progress_ratio"] == 1 / job.actual_qty
    assert row["expected_completion_at"] == datetime.fromtimestamp(job.started_at + job.total_production_time)


def test_describe_current_excludes_idle_lines(tmp_path):
    order_controller, line_controller, sample_repo, inventory_repo, order_repo, queue = make_all(tmp_path, line_count=2)

    result = line_controller.describe_current(order_repo, sample_repo, inventory_repo)

    assert result == []


def test_describe_waiting_includes_required_fields_without_expected_completion(tmp_path):
    order_controller, line_controller, sample_repo, inventory_repo, order_repo, queue = make_all(tmp_path, line_count=1)
    sample_repo.save(Sample("S1", "Wafer-A", avg_production_time=1.0, yield_rate=1.0))
    inventory_repo.save(Inventory("S1", 0))

    order1 = order_controller.submit(customer_name="Acme", sample_id="S1", quantity=3)
    order_controller.approve(order1.order_id)
    order2 = order_controller.submit(customer_name="Beta", sample_id="S1", quantity=5)
    order_controller.approve(order2.order_id)

    result = line_controller.describe_waiting(order_repo, sample_repo)

    assert len(result) == 1
    row = result[0]
    waiting_job = queue.waiting[0]
    assert row["position"] == 1
    assert row["order_id"] == order2.order_id
    assert row["sample_name"] == "Wafer-A"
    assert row["quantity"] == 5
    assert row["shortage"] == waiting_job.shortage
    assert row["actual_qty"] == waiting_job.actual_qty
    assert row["expected_completion_at"] is None
