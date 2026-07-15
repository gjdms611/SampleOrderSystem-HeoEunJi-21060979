import pytest

from model.order import InvalidOrderTransitionError, Order, OrderStatus


def make_order_with_status(status):
    order = Order(order_id="O1", customer_name="Acme", sample_id="S1", quantity=10)
    order.status = status
    return order


def test_release_transitions_confirmed_to_release():
    order = make_order_with_status(OrderStatus.CONFIRMED)

    order.release()

    assert order.status == OrderStatus.RELEASE


@pytest.mark.parametrize(
    "status",
    [OrderStatus.RESERVED, OrderStatus.REJECTED, OrderStatus.PRODUCING, OrderStatus.RELEASE],
)
def test_release_rejects_when_status_not_confirmed(status):
    order = make_order_with_status(status)

    with pytest.raises(InvalidOrderTransitionError):
        order.release()
