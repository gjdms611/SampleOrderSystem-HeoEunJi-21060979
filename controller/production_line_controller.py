import math
import time


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
