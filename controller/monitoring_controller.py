from model.order import OrderStatus
from model.monitoring import judge_stock_status


class MonitoringController:
    def __init__(self, order_repo, inventory_repo):
        self.order_repo = order_repo
        self.inventory_repo = inventory_repo

    def count_orders_by_status(self):
        counts = {status: 0 for status in OrderStatus}
        for order in self.order_repo.find_all():
            counts[order.status] += 1
        return counts

    def judge_all_stock(self):
        demand_by_sample = {}
        for order in self.order_repo.find_all():
            if order.status in (OrderStatus.RESERVED, OrderStatus.PRODUCING):
                demand_by_sample[order.sample_id] = demand_by_sample.get(order.sample_id, 0) + order.quantity

        result = {}
        for inventory in self.inventory_repo.find_all():
            demand_total = demand_by_sample.get(inventory.sample_id, 0)
            result[inventory.sample_id] = judge_stock_status(inventory.quantity, demand_total)
        return result
