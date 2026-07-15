from enum import Enum

from model.production_calc import calc_actual_production_qty, calc_shortage, calc_total_production_time
from model.production_job import ProductionJob


class OrderStatus(Enum):
    RESERVED = "RESERVED"
    REJECTED = "REJECTED"
    CONFIRMED = "CONFIRMED"
    PRODUCING = "PRODUCING"
    RELEASE = "RELEASE"


class Order:
    def __init__(self, order_id, customer_name, sample_id, quantity):
        self.order_id = order_id
        self.customer_name = customer_name
        self.sample_id = sample_id
        self.quantity = quantity
        self.status = OrderStatus.RESERVED

    def reject(self) -> None:
        self.status = OrderStatus.REJECTED

    def approve(self, inventory_qty_at_approval: int, sample=None):
        if inventory_qty_at_approval >= self.quantity:
            self.status = OrderStatus.CONFIRMED
            return None

        return self._start_production(inventory_qty_at_approval, sample)

    def _start_production(self, inventory_qty_at_approval: int, sample) -> ProductionJob:
        shortage = calc_shortage(self.quantity, inventory_qty_at_approval)
        actual_qty = calc_actual_production_qty(shortage, sample.yield_rate)
        total_production_time = calc_total_production_time(sample.avg_production_time, actual_qty)
        self.status = OrderStatus.PRODUCING
        return ProductionJob(
            order_id=self.order_id,
            sample_id=self.sample_id,
            shortage=shortage,
            actual_qty=actual_qty,
            total_production_time=total_production_time,
        )
