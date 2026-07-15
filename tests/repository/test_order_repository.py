from model.order import Order, OrderStatus
from repository.order_repository import OrderRepository


def test_save_then_find_by_id_round_trips_status_enum(tmp_path):
    path = tmp_path / "orders.json"
    repo = OrderRepository(str(path))
    order = Order(order_id="O1", customer_name="Acme", sample_id="S1", quantity=10)
    order.status = OrderStatus.CONFIRMED

    repo.save(order)
    result = repo.find_by_id("O1")

    assert result is not None
    assert result.order_id == "O1"
    assert result.customer_name == "Acme"
    assert result.sample_id == "S1"
    assert result.quantity == 10
    assert result.status == OrderStatus.CONFIRMED
    assert isinstance(result.status, OrderStatus)


def test_find_by_id_returns_none_when_not_found(tmp_path):
    path = tmp_path / "orders.json"
    repo = OrderRepository(str(path))

    result = repo.find_by_id("NOPE")

    assert result is None


def test_save_overwrites_existing_order_with_same_id(tmp_path):
    path = tmp_path / "orders.json"
    repo = OrderRepository(str(path))
    order = Order(order_id="O1", customer_name="Acme", sample_id="S1", quantity=10)
    repo.save(order)

    order.quantity = 20
    order.status = OrderStatus.PRODUCING
    repo.save(order)

    result = repo.find_by_id("O1")
    assert result.quantity == 20
    assert result.status == OrderStatus.PRODUCING
    assert len(repo.find_all()) == 1


def test_find_all_returns_all_saved_orders(tmp_path):
    path = tmp_path / "orders.json"
    repo = OrderRepository(str(path))
    order1 = Order(order_id="O1", customer_name="Acme", sample_id="S1", quantity=10)
    order2 = Order(order_id="O2", customer_name="Globex", sample_id="S2", quantity=5)
    order2.status = OrderStatus.REJECTED

    repo.save(order1)
    repo.save(order2)

    result = repo.find_all()

    assert len(result) == 2
    ids = {o.order_id: o for o in result}
    assert ids["O1"].status == OrderStatus.RESERVED
    assert ids["O2"].status == OrderStatus.REJECTED
