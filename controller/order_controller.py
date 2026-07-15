from model.order import InvalidOrderTransitionError, Order


class OrderController:
    def __init__(self, order_repo, inventory_repo, sample_repo, production_queue):
        self.order_repo = order_repo
        self.inventory_repo = inventory_repo
        self.sample_repo = sample_repo
        self.production_queue = production_queue

    def submit(self, customer_name, sample_id, quantity):
        if self.sample_repo.find_by_id(sample_id) is None:
            return None
        order_id = f"O{len(self.order_repo.find_all()) + 1}"
        order = Order(order_id, customer_name, sample_id, quantity)
        self.order_repo.save(order)
        return order

    def reject(self, order_id):
        order = self.order_repo.find_by_id(order_id)
        if order is None:
            return None
        try:
            order.reject()
        except InvalidOrderTransitionError:
            return None
        self.order_repo.save(order)
        return order

    def cancel(self, order_id):
        order = self.order_repo.find_by_id(order_id)
        if order is None:
            return None
        try:
            order.cancel()
        except InvalidOrderTransitionError:
            return None
        self.order_repo.save(order)
        return order

    def release_order(self, order_id):
        order = self.order_repo.find_by_id(order_id)
        if order is None:
            return None
        try:
            order.release()
        except InvalidOrderTransitionError:
            return None
        self.order_repo.save(order)
        return order

    def complete_production(self, confirmed_jobs):
        confirmed_orders = []
        for job in confirmed_jobs:
            order = self.order_repo.find_by_id(job.order_id)
            order.complete_production()
            self.order_repo.save(order)
            confirmed_orders.append(order)
        return confirmed_orders

    def approve(self, order_id):
        order = self.order_repo.find_by_id(order_id)
        if order is None:
            return None

        sample = self.sample_repo.find_by_id(order.sample_id)
        if sample is None:
            return None

        inventory = self.inventory_repo.find_by_sample_id(order.sample_id)
        inventory_qty_at_approval = inventory.quantity if inventory is not None else 0

        try:
            job = order.approve(inventory_qty_at_approval=inventory_qty_at_approval, sample=sample)
        except InvalidOrderTransitionError:
            return None

        if job is not None:
            if inventory is not None:
                inventory.quantity = 0
                self.inventory_repo.save(inventory)
            self.production_queue.enqueue(job)
            self.production_queue.assign_idle_lines()
        else:
            if inventory is not None:
                inventory.quantity -= order.quantity
                self.inventory_repo.save(inventory)

        self.order_repo.save(order)
        return order
