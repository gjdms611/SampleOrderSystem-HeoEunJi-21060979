from model.order import Order, OrderStatus


def test_order_creation_sets_status_reserved():
    order = Order(order_id="O1", customer_name="Acme", sample_id="S1", quantity=10)

    assert order.status == OrderStatus.RESERVED
    assert order.order_id == "O1"
    assert order.customer_name == "Acme"
    assert order.sample_id == "S1"
    assert order.quantity == 10
