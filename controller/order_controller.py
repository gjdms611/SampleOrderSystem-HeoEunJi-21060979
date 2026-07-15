from model.order import InvalidOrderTransitionError, Order


class OrderController:
    def __init__(self, order_repo, inventory_repo, sample_repo):
        self.order_repo = order_repo
        self.inventory_repo = inventory_repo
        self.sample_repo = sample_repo

    def submit(self, customer_name, sample_id, quantity):
        order_id = f"O{len(self.order_repo.find_all()) + 1}"
        order = Order(order_id, customer_name, sample_id, quantity)
        self.order_repo.save(order)
        return order

    def reject(self, order_id):
        order = self.order_repo.find_by_id(order_id)
        try:
            order.reject()
        except InvalidOrderTransitionError:
            return None
        self.order_repo.save(order)
        return order

    def cancel(self, order_id):
        order = self.order_repo.find_by_id(order_id)
        try:
            order.cancel()
        except InvalidOrderTransitionError:
            return None
        self.order_repo.save(order)
        return order
