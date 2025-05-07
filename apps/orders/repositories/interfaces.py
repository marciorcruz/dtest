from abc import ABC, abstractmethod
from uuid import UUID
from apps.orders.domain.entities import Order

class OrderRepository(ABC):
    @abstractmethod
    def add(self, order: Order) -> None:
        ...

    @abstractmethod
    def get_by_id(self, order_id: UUID) -> Order | None:
        ...

    @abstractmethod
    def list_by_customer(self, customer_id: UUID) -> list[Order]:
        ...