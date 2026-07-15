import math
import time
from datetime import datetime


class ProductionLineController:
    def __init__(self, queue):
        self.queue = queue

    def current_jobs(self):
        return [job for job in self.queue.lines if job is not None]

    def waiting_jobs(self):
        return list(self.queue.waiting)

    def tick(self, inventory_repo, order_controller):
        confirmed_jobs = []
        for line_index, job in enumerate(self.queue.lines):
            if job is None:
                continue
            per_unit_time = job.total_production_time / job.actual_qty
            elapsed = time.time() - job.started_at
            target_qty = min(job.actual_qty, math.floor(elapsed / per_unit_time))
            while job.produced_qty < target_qty:
                inventory = inventory_repo.find_by_sample_id(job.sample_id)
                confirmed_jobs.extend(self.queue.produce_unit(line_index, inventory))
                inventory_repo.save(inventory)

        return order_controller.complete_production(confirmed_jobs)

    def describe_current(self, order_repo, sample_repo, inventory_repo):
        rows = []
        for job in self.current_jobs():
            order = order_repo.find_by_id(job.order_id)
            sample = sample_repo.find_by_id(job.sample_id)
            inventory = inventory_repo.find_by_sample_id(job.sample_id)
            rows.append({
                "order_id": job.order_id,
                "sample_name": sample.name,
                "quantity": order.quantity,
                "inventory": inventory.quantity if inventory is not None else 0,
                "shortage": job.shortage,
                "actual_qty": job.actual_qty,
                "produced_qty": job.produced_qty,
                "yield_rate": sample.yield_rate,
                "progress_ratio": job.produced_qty / job.actual_qty,
                "expected_completion_at": datetime.fromtimestamp(job.started_at + job.total_production_time),
            })
        return rows

    def describe_waiting(self, order_repo, sample_repo):
        rows = []
        for position, job in enumerate(self.waiting_jobs(), start=1):
            order = order_repo.find_by_id(job.order_id)
            sample = sample_repo.find_by_id(job.sample_id)
            rows.append({
                "position": position,
                "order_id": job.order_id,
                "sample_name": sample.name,
                "quantity": order.quantity,
                "shortage": job.shortage,
                "actual_qty": job.actual_qty,
                "expected_completion_at": None,
            })
        return rows
