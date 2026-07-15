from model.order import Order, OrderStatus
from model.sample import Sample


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


def test_approve_transitions_reserved_to_producing_and_creates_production_job_when_inventory_insufficient():
    from model.production_job import ProductionJob

    sample = Sample(sample_id="S1", name="Sample1", avg_production_time=2.5, yield_rate=0.9)
    order = Order(order_id="O1", customer_name="Acme", sample_id="S1", quantity=100)

    result = order.approve(inventory_qty_at_approval=30, sample=sample)

    assert isinstance(result, ProductionJob)
    assert result.shortage == 70
    assert result.actual_qty == 78
    assert result.total_production_time == 195.0
    assert result.produced_qty == 0
    assert order.status == OrderStatus.PRODUCING
