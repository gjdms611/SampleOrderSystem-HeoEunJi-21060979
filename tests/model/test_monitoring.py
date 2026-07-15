from model.monitoring import StockStatus, judge_stock_status


def test_judge_stock_status_depleted_when_inventory_zero():
    assert judge_stock_status(inventory_qty=0, demand_total=10) == StockStatus.DEPLETED


def test_judge_stock_status_shortage_when_inventory_below_demand():
    assert judge_stock_status(inventory_qty=5, demand_total=10) == StockStatus.SHORTAGE


def test_judge_stock_status_sufficient_when_inventory_meets_demand():
    assert judge_stock_status(inventory_qty=10, demand_total=10) == StockStatus.SUFFICIENT
