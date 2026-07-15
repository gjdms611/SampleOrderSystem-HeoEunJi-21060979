class Sample:
    def __init__(self, sample_id: str, name: str, avg_production_time: float, yield_rate: float):
        if avg_production_time <= 0:
            raise ValueError("avg_production_time must be positive")
        if not (0 < yield_rate <= 1):
            raise ValueError("yield_rate must be in (0, 1]")

        self.sample_id = sample_id
        self.name = name
        self.avg_production_time = avg_production_time
        self.yield_rate = yield_rate
