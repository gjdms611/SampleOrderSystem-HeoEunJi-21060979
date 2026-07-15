import math


def calc_shortage(order_qty: int, inventory_qty: int) -> int:
    return order_qty - inventory_qty


def calc_actual_production_qty(shortage: int, yield_rate: float) -> int:
    return math.ceil(shortage / yield_rate)


def calc_total_production_time(avg_production_time: float, actual_qty: int) -> float:
    return avg_production_time * actual_qty


def calc_surplus(actual_qty: int, shortage: int) -> int:
    return actual_qty - shortage
