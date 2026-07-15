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


def test_enqueue_maintains_fifo_order():
    queue = ProductionQueue(line_count=1)
    job1, job2, job3 = make_job("O1"), make_job("O2"), make_job("O3")

    queue.enqueue(job1)
    queue.enqueue(job2)
    queue.enqueue(job3)

    assert queue.waiting == [job1, job2, job3]


def test_assign_idle_lines_assigns_front_of_queue_to_idle_line():
    queue = ProductionQueue(line_count=1)
    job1 = make_job("O1")
    queue.enqueue(job1)

    queue.assign_idle_lines()

    assert queue.lines == [job1]
    assert queue.waiting == []


def test_assign_idle_lines_fills_multiple_idle_lines_at_once():
    queue = ProductionQueue(line_count=2)
    job1, job2, job3 = make_job("O1"), make_job("O2"), make_job("O3")
    queue.enqueue(job1)
    queue.enqueue(job2)
    queue.enqueue(job3)

    queue.assign_idle_lines()

    assert queue.lines == [job1, job2]
    assert queue.waiting == [job3]


def test_assign_idle_lines_keeps_extra_jobs_waiting_when_lines_full():
    queue = ProductionQueue(line_count=1)
    job1, job2 = make_job("O1"), make_job("O2")
    queue.enqueue(job1)
    queue.assign_idle_lines()

    queue.enqueue(job2)
    queue.assign_idle_lines()

    assert queue.lines == [job1]
    assert queue.waiting == [job2]
