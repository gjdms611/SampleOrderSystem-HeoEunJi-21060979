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
