from controller.main_controller import MainController
from controller.monitoring_controller import MonitoringController
from controller.order_controller import OrderController
from controller.production_line_controller import ProductionLineController
from controller.sample_controller import SampleController
from model.inventory import Inventory
from model.production_queue import ProductionQueue
from model.sample import Sample
from repository.inventory_repository import InventoryRepository
from repository.order_repository import OrderRepository
from repository.sample_repository import SampleRepository

DEFAULT_SAMPLES = [
    ("S-001", "실리콘 웨이퍼-8인치", 0.5, 0.92, 480),
    ("S-002", "GaN 에피택셜-4인치", 0.3, 0.78, 220),
    ("S-003", "SiC 파워기판-6인치", 0.8, 0.92, 30),
    ("S-004", "포토레지스트-PR7", 0.2, 0.95, 910),
    ("S-005", "산화막 웨이퍼-SiO2", 0.6, 0.88, 0),
]


def seed_default_samples(sample_repo, inventory_repo):
    if sample_repo.find_all():
        return
    for sample_id, name, avg_production_time, yield_rate, initial_quantity in DEFAULT_SAMPLES:
        sample_repo.save(Sample(sample_id, name, avg_production_time, yield_rate))
        inventory_repo.save(Inventory(sample_id, initial_quantity))


def main():
    sample_repo = SampleRepository("data/samples.json")
    inventory_repo = InventoryRepository("data/inventories.json")
    order_repo = OrderRepository("data/orders.json")
    production_queue = ProductionQueue(line_count=1)

    seed_default_samples(sample_repo, inventory_repo)

    sample_controller = SampleController(sample_repo)
    order_controller = OrderController(order_repo, inventory_repo, sample_repo, production_queue)
    monitoring_controller = MonitoringController(order_repo, inventory_repo)
    line_controller = ProductionLineController(production_queue)

    main_controller = MainController(sample_controller, order_controller, monitoring_controller, line_controller)
    main_controller.run()


if __name__ == "__main__":
    main()
