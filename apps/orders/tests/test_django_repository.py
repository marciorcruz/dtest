from uuid import uuid4
from django.test import TestCase
from apps.orders.repositories.django_impl import DjangoOrderRepository
from apps.orders.domain.value_objects import Money
from apps.orders.domain.entities import Order

class DjangoRepoTest(TestCase):
    def setUp(self):
        self.repo = DjangoOrderRepository()
        self.customer_id = uuid4()

    def test_add_and_get_by_id(self):
        order = Order(customer_id=self.customer_id)
        order.add_item(uuid4(), Money(100), 1)
        order.add_item(uuid4(), Money(200), 2)
        self.repo.add(order)

        fetched = self.repo.get_by_id(order.id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.id, order.id)
        self.assertEqual(fetched.customer_id, self.customer_id)
        self.assertEqual(fetched.total, order.total)
        self.assertEqual(len(fetched.items), 2)