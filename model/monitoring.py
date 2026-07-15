from enum import Enum


class StockStatus(Enum):
    SUFFICIENT = "SUFFICIENT"
    SHORTAGE = "SHORTAGE"
    DEPLETED = "DEPLETED"


def judge_stock_status(inventory_qty: int, demand_total: int) -> StockStatus:
    if inventory_qty == 0:
        return StockStatus.DEPLETED
    if inventory_qty < demand_total:
        return StockStatus.SHORTAGE
    return StockStatus.SUFFICIENT
