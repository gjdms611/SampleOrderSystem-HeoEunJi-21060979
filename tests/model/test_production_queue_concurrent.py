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


def test_produce_unit_reflects_surplus_into_inventory_immediately():
    queue = ProductionQueue(line_count=1)
    job = make_job("O1", shortage=0, actual_qty=10)
    queue.lines[0] = job
    inventory = Inventory("S1", 0)

    queue.produce_unit(0, inventory)

    assert job.produced_qty == 1
    assert inventory.quantity == 1


def test_waiting_order_confirmed_immediately_once_surplus_covers_its_shortage():
    queue = ProductionQueue(line_count=1)
    producing_job = make_job("O1", shortage=0, actual_qty=10)
    queue.lines[0] = producing_job
    waiting_job = make_job("O2", shortage=3, actual_qty=5)
    queue.waiting.append(waiting_job)
    inventory = Inventory("S1", 0)

    result1 = queue.produce_unit(0, inventory)
    result2 = queue.produce_unit(0, inventory)
    result3 = queue.produce_unit(0, inventory)

    assert result1 == []
    assert result2 == []
    assert result3 == [waiting_job]
    assert waiting_job not in queue.waiting
    assert inventory.quantity == 0


def test_prd_6_2_scenario_20ea_confirmed_at_cumulative_120_100ea_stays_producing():
    queue = ProductionQueue(line_count=1)
    job_100 = make_job("O100", shortage=100, actual_qty=150)
    queue.lines[0] = job_100
    job_20 = make_job("O20", shortage=20, actual_qty=30)
    queue.waiting.append(job_20)
    inventory = Inventory("S1", 0)

    confirmed_so_far = []
    for _ in range(120):
        confirmed_so_far += queue.produce_unit(0, inventory)

    assert confirmed_so_far == [job_20]
    assert job_20 not in queue.waiting
    assert job_100.produced_qty == 120

    for _ in range(30):
        queue.produce_unit(0, inventory)

    assert job_100.produced_qty == 150
    assert queue.lines[0] is job_100
