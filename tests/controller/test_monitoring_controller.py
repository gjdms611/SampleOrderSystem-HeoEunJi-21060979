from controller.monitoring_controller import MonitoringController
from model.inventory import Inventory
from model.monitoring import StockStatus
from model.order import Order, OrderStatus
from repository.inventory_repository import InventoryRepository
from repository.order_repository import OrderRepository


def make_controller(tmp_path):
    order_repo = OrderRepository(str(tmp_path / "orders.json"))
    inventory_repo = InventoryRepository(str(tmp_path / "inventories.json"))
    return MonitoringController(order_repo, inventory_repo), order_repo, inventory_repo


def test_count_orders_by_status(tmp_path):
    controller, order_repo, inventory_repo = make_controller(tmp_path)
    order1 = Order("O1", "Acme", "S1", 10)
    order2 = Order("O2", "Acme", "S1", 5)
    order2.status = OrderStatus.CONFIRMED
    order3 = Order("O3", "Acme", "S1", 3)
    order3.status = OrderStatus.CONFIRMED
    order_repo.save(order1)
    order_repo.save(order2)
    order_repo.save(order3)

    result = controller.count_orders_by_status()

    assert result[OrderStatus.RESERVED] == 1
    assert result[OrderStatus.CONFIRMED] == 2


def test_judge_all_stock_uses_reserved_and_producing_demand(tmp_path):
    controller, order_repo, inventory_repo = make_controller(tmp_path)
    inventory_repo.save(Inventory("S1", 5))
    inventory_repo.save(Inventory("S2", 0))
    order1 = Order("O1", "Acme", "S1", 20)
    order1.status = OrderStatus.PRODUCING
    order_repo.save(order1)

    result = controller.judge_all_stock()

    assert result["S1"] == StockStatus.SHORTAGE
    assert result["S2"] == StockStatus.DEPLETED
