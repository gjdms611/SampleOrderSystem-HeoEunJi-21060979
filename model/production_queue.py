import heapq
import itertools
import time


class ProductionQueue:
    def __init__(self, line_count: int = 1):
        self.lines = [None] * line_count
        self.waiting = []
        self._waiting_heaps = {}
        self._waiting_ids = set()
        self._seq_counter = itertools.count()

    def enqueue(self, job) -> None:
        self.waiting.append(job)
        self._waiting_ids.add(id(job))
        heap = self._waiting_heaps.setdefault(job.sample_id, [])
        heapq.heappush(heap, (job.shortage, next(self._seq_counter), job))

    def assign_idle_lines(self) -> None:
        for i, line in enumerate(self.lines):
            if line is None and self.waiting:
                job = self.waiting.pop(0)
                self._waiting_ids.discard(id(job))
                job.started_at = time.time()
                self.lines[i] = job

    def produce_unit(self, line_index: int, inventory) -> list:
        job = self.lines[line_index]
        job.produced_qty += 1

        confirmed = []

        if job.produced_qty > job.shortage:
            inventory.quantity += 1
            confirmed.extend(self._drain_confirmable(inventory))

        if job.produced_qty == job.actual_qty:
            confirmed.append(job)
            self.lines[line_index] = None
            self.assign_idle_lines()

        return confirmed

    def _drain_confirmable(self, inventory) -> list:
        confirmed = []
        heap = self._waiting_heaps.get(inventory.sample_id, [])
        while heap:
            _, _, candidate = heap[0]
            if id(candidate) not in self._waiting_ids:
                heapq.heappop(heap)
                continue
            shortage = candidate.shortage
            if inventory.quantity < shortage:
                break
            heapq.heappop(heap)
            self._waiting_ids.discard(id(candidate))
            self.waiting.remove(candidate)
            inventory.quantity -= shortage
            confirmed.append(candidate)
        return confirmed
