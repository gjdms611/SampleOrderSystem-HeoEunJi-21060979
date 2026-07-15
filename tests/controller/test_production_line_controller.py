from controller.production_line_controller import ProductionLineController
from model.production_job import ProductionJob
from model.production_queue import ProductionQueue


def make_job(order_id):
    return ProductionJob(
        order_id=order_id,
        sample_id="S1",
        shortage=10,
        actual_qty=12,
        total_production_time=30.0,
    )


def test_current_jobs_returns_jobs_assigned_to_lines():
    queue = ProductionQueue(line_count=2)
    job1 = make_job("O1")
    queue.lines[0] = job1
    controller = ProductionLineController(queue)

    result = controller.current_jobs()

    assert result == [job1]


def test_waiting_jobs_returns_queue_waiting_list():
    queue = ProductionQueue(line_count=1)
    job1 = make_job("O1")
    queue.lines[0] = job1
    job2 = make_job("O2")
    queue.enqueue(job2)
    controller = ProductionLineController(queue)

    result = controller.waiting_jobs()

    assert result == [job2]
