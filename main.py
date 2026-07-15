from controller.main_controller import MainController
from controller.monitoring_controller import MonitoringController
from controller.order_controller import OrderController
from controller.production_line_controller import ProductionLineController
from controller.sample_controller import SampleController
from model.production_queue import ProductionQueue
from repository.inventory_repository import InventoryRepository
from repository.order_repository import OrderRepository
from repository.sample_repository import SampleRepository


def main():
    sample_repo = SampleRepository("data/samples.json")
    inventory_repo = InventoryRepository("data/inventories.json")
    order_repo = OrderRepository("data/orders.json")
    production_queue = ProductionQueue(line_count=1)

    sample_controller = SampleController(sample_repo)
    order_controller = OrderController(order_repo, inventory_repo, sample_repo, production_queue)
    monitoring_controller = MonitoringController(order_repo, inventory_repo)
    line_controller = ProductionLineController(production_queue)

    main_controller = MainController(sample_controller, order_controller, monitoring_controller, line_controller)
    main_controller.run()


if __name__ == "__main__":
    main()
