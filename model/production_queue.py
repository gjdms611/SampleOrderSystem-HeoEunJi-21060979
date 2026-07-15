class ProductionQueue:
    def __init__(self, line_count: int = 1):
        self.lines = [None] * line_count
        self.waiting = []

    def enqueue(self, job) -> None:
        self.waiting.append(job)

    def assign_idle_lines(self) -> None:
        for i, line in enumerate(self.lines):
            if line is None and self.waiting:
                self.lines[i] = self.waiting.pop(0)

    def produce_unit(self, line_index: int, inventory) -> list:
        job = self.lines[line_index]
        job.produced_qty += 1

        confirmed = []

        if job.produced_qty > job.shortage:
            inventory.quantity += 1

            remaining = []
            for waiting_job in self.waiting:
                if waiting_job.sample_id == inventory.sample_id and inventory.quantity >= waiting_job.shortage:
                    inventory.quantity -= waiting_job.shortage
                    confirmed.append(waiting_job)
                else:
                    remaining.append(waiting_job)
            self.waiting = remaining

        if job.produced_qty == job.actual_qty:
            confirmed.append(job)
            self.lines[line_index] = None
            self.assign_idle_lines()

        return confirmed
