from model.order import Order, OrderStatus


def test_order_creation_sets_status_reserved():
    order = Order(order_id="O1", customer_name="Acme", sample_id="S1", quantity=10)

    assert order.status == OrderStatus.RESERVED
    assert order.order_id == "O1"
    assert order.customer_name == "Acme"
    assert order.sample_id == "S1"
    assert order.quantity == 10


def test_reject_transitions_reserved_to_rejected():
    order = Order(order_id="O1", customer_name="Acme", sample_id="S1", quantity=10)

    order.reject()

    assert order.status == OrderStatus.REJECTED


def test_approve_transitions_reserved_to_confirmed_when_inventory_sufficient():
    order = Order(order_id="O1", customer_name="Acme", sample_id="S1", quantity=10)

    result = order.approve(inventory_qty_at_approval=10)

    assert result is None
    assert order.status == OrderStatus.CONFIRMED
