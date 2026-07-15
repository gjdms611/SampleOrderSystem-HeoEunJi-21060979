import pytest

from model.order import InvalidOrderTransitionError, Order, OrderStatus


def make_reserved_order():
    return Order(order_id="O1", customer_name="Acme", sample_id="S1", quantity=10)


def test_cancel_transitions_reserved_to_rejected():
    order = make_reserved_order()

    order.cancel()

    assert order.status == OrderStatus.REJECTED


@pytest.mark.parametrize(
    "status",
    [OrderStatus.REJECTED, OrderStatus.CONFIRMED, OrderStatus.PRODUCING, OrderStatus.RELEASE],
)
def test_cancel_rejects_when_status_not_reserved(status):
    order = make_reserved_order()
    order.status = status

    with pytest.raises(InvalidOrderTransitionError):
        order.cancel()


def test_reject_rejects_when_status_not_reserved():
    order = make_reserved_order()
    order.status = OrderStatus.REJECTED

    with pytest.raises(InvalidOrderTransitionError):
        order.reject()


def test_approve_rejects_when_status_not_reserved():
    order = make_reserved_order()
    order.status = OrderStatus.REJECTED

    with pytest.raises(InvalidOrderTransitionError):
        order.approve(inventory_qty_at_approval=10)
