from uuid import uuid4
import pytest
from apps.orders.domain.entities import Order, OrderItem
from apps.orders.domain.value_objects import Money

@pytest.mark.parametrize("quantidade", [1, 5, 10])
def test_add_item_recalculates_total(quantidade):
    order = Order(customer_id=uuid4())
    order.add_item(product_id=uuid4(), price=Money(100), quantity=quantidade)
    assert order.items[0].quantity == quantidade
    assert order.total == Money(100 * quantidade)


def test_add_item_negative_quantity_raises():
    order = Order(customer_id=uuid4())
    with pytest.raises(ValueError):
        order.add_item(product_id=uuid4(), price=Money(50), quantity=0)


def test_orderitem_subtotal():
    item = OrderItem(product_id=uuid4(), price=Money(20), quantity=3)
    assert item.subtotal == 60