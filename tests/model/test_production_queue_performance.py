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


class ShortageAccessProbe:
    """실제 job을 감싸 .shortage 접근 횟수를 센다 (조기 종료 검증용)."""

    def __init__(self, job):
        self._job = job
        self.access_count = 0

    @property
    def shortage(self):
        self.access_count += 1
        return self._job.shortage

    def __getattr__(self, name):
        return getattr(self._job, name)


def test_assign_idle_lines_still_fifo_after_optimization():
    queue = ProductionQueue(line_count=1)
    job_large_shortage = make_job("O1", shortage=100, actual_qty=100)
    job_small_shortage = make_job("O2", shortage=1, actual_qty=1)
    queue.enqueue(job_large_shortage)
    queue.enqueue(job_small_shortage)

    queue.assign_idle_lines()

    assert queue.lines[0] is job_large_shortage
    assert queue.waiting == [job_small_shortage]


def test_confirms_in_shortage_ascending_order_not_arrival_order():
    queue = ProductionQueue(line_count=1)
    producing_job = make_job("O1", shortage=0, actual_qty=100)
    queue.lines[0] = producing_job
    job_shortage_5 = make_job("O2", shortage=5, actual_qty=5)
    job_shortage_2 = make_job("O3", shortage=2, actual_qty=2)
    queue.waiting.append(job_shortage_5)
    queue.waiting.append(job_shortage_2)
    inventory = Inventory("S1", 0)

    confirmed_so_far = []
    for _ in range(5):
        confirmed_so_far += queue.produce_unit(0, inventory)

    assert confirmed_so_far == [job_shortage_2, job_shortage_5]


def test_confirmation_scan_stops_at_first_unmet_shortage():
    queue = ProductionQueue(line_count=1)
    producing_job = make_job("O1", shortage=0, actual_qty=1)
    queue.lines[0] = producing_job
    probe = ShortageAccessProbe(make_job("O2", shortage=1_000_000, actual_qty=1))
    other_probes = [
        ShortageAccessProbe(make_job(f"O{i}", shortage=2_000_000 + i, actual_qty=1)) for i in range(999)
    ]
    queue.waiting.append(probe)
    queue.waiting.extend(other_probes)
    inventory = Inventory("S1", 0)

    queue.produce_unit(0, inventory)

    assert probe.access_count == 1
    assert all(p.access_count == 0 for p in other_probes)
