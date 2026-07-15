class ProductionJob:
    def __init__(self, order_id, sample_id, shortage, actual_qty, total_production_time):
        self.order_id = order_id
        self.sample_id = sample_id
        self.shortage = shortage
        self.actual_qty = actual_qty
        self.total_production_time = total_production_time
        self.produced_qty = 0
