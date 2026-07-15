from enum import Enum


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
