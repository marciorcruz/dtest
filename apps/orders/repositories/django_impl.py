from uuid import UUID
from apps.orders.repositories.interfaces import OrderRepository
from apps.orders.domain.entities import Order
from apps.orders.models import OrderModel, OrderItemModel
from apps.orders.domain.value_objects import Money

class DjangoOrderRepository(OrderRepository):
    def add(self, order: Order) -> None:
        model = OrderModel(id=order.id, customer_id=order.customer_id, total=order.total.amount)
        model.save()
        for item in order.items:
            OrderItemModel.objects.create(
                order=model,
                product_id=item.product_id,
                price=item.price.amount,
                quantity=item.quantity,
            )

    def get_by_id(self, order_id: UUID) -> Order | None:
        try:
            m = OrderModel.objects.get(id=order_id)
        except OrderModel.DoesNotExist:
            return None
        order = Order(customer_id=m.customer_id)
        order.id = m.id
        for itm in m.items.all():
            order.add_item(itm.product_id, Money(itm.price), itm.quantity)
        return order
    
    def list_by_customer(self, customer_id: UUID) -> list[Order]:
        models = OrderModel.objects.filter(customer_id=customer_id)
        orders = []
        for m in models:
            order = Order(customer_id=m.customer_id)
            order.id = m.id
            for itm in m.items.all():
                order.add_item(itm.product_id, Money(itm.price), itm.quantity)
            orders.append(order)
        return orders