from uuid import UUID, uuid4
from .value_objects import Money

class Order:
    def __init__(self, customer_id: UUID):
        self.id = uuid4()
        self.customer_id = customer_id
        self.items = []
        self._total = Money(0)

    def add_item(self, product_id: UUID, price: Money, quantity: int):
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        item = OrderItem(product_id, price, quantity)
        self.items.append(item)
        self._recalculate_total()

    def _recalculate_total(self):
        total = sum(item.subtotal for item in self.items)
        self._total = Money(total)

    @property
    def total(self) -> Money:
        return self._total

class OrderItem:
    def __init__(self, product_id: UUID, price: Money, quantity: int):
        self.product_id = product_id
        self.price = price
        self.quantity = quantity

    @property
    def subtotal(self):
        return self.price.amount * self.quantity