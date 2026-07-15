from model.inventory import Inventory
from model.production_job import ProductionJob
from model.production_queue import ProductionQueue


def make_job(order_id, shortage, actual_qty, sample_id="S1"):
    return ProductionJob(
        order_id=order_id,
        sample_id=sample_id,
        shortage=shortage,
        actual_qty=actual_qty,
        total_production_time=30.0,
    )


def test_completing_own_actual_qty_confirms_job_and_frees_line():
    queue = ProductionQueue(line_count=1)
    job = make_job("O1", shortage=5, actual_qty=5)
    queue.lines[0] = job
    inventory = Inventory("S1", 0)

    confirmed = []
    for _ in range(5):
        confirmed = queue.produce_unit(0, inventory)

    assert confirmed == [job]
    assert queue.lines[0] is None


def test_completed_line_is_backfilled_with_next_waiting_job():
    queue = ProductionQueue(line_count=1)
    job1 = make_job("O1", shortage=0, actual_qty=1)
    queue.lines[0] = job1
    job2 = make_job("O2", shortage=0, actual_qty=1)
    queue.waiting.append(job2)
    inventory = Inventory("S1", 0)

    confirmed = queue.produce_unit(0, inventory)

    assert job1 in confirmed
    assert queue.lines[0] is job2
    assert job2 not in queue.waiting


def test_surplus_remains_in_inventory_after_completion():
    queue = ProductionQueue(line_count=1)
    job = make_job("O1", shortage=3, actual_qty=5)
    queue.lines[0] = job
    inventory = Inventory("S1", 0)

    for _ in range(5):
        queue.produce_unit(0, inventory)

    assert inventory.quantity == 2
