from model.order import Order, OrderStatus
from storage.json_storage import load, save


class OrderRepository:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def save(self, order: Order):
        records = load(self.file_path)
        records = [r for r in records if r["order_id"] != order.order_id]
        records.append(
            {
                "order_id": order.order_id,
                "customer_name": order.customer_name,
                "sample_id": order.sample_id,
                "quantity": order.quantity,
                "status": order.status.value,
            }
        )
        save(records, self.file_path)

    def find_by_id(self, order_id):
        for order in self.find_all():
            if order.order_id == order_id:
                return order
        return None

    def find_all(self):
        records = load(self.file_path)
        orders = []
        for r in records:
            order = Order(r["order_id"], r["customer_name"], r["sample_id"], r["quantity"])
            order.status = OrderStatus(r["status"])
            orders.append(order)
        return orders
