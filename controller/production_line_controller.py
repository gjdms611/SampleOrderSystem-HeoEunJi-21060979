class ProductionLineController:
    def __init__(self, queue):
        self.queue = queue

    def current_jobs(self):
        return [job for job in self.queue.lines if job is not None]

    def waiting_jobs(self):
        return list(self.queue.waiting)
