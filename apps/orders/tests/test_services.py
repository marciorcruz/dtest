from uuid import uuid4
import pytest
from apps.orders.application.services import CreateOrderService
from apps.orders.domain.value_objects import Money

class DummyRepo:
    def __init__(self):
        self.saved = None

    def add(self, order):
        self.saved = order

    def get_by_id(self, order_id):
        return None


def test_create_order_service_executes_and_returns_id():
    repo = DummyRepo()
    service = CreateOrderService(repo)
    customer_id = uuid4()
    items = [{"product_id": uuid4(), "price": 200, "quantity": 2}]
    order_id = service.execute(customer_id, items)

    assert isinstance(order_id, type(uuid4()))
    saved = repo.saved
    assert saved.customer_id == customer_id
    assert saved.total == Money(400)