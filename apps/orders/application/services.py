import csv
from uuid import UUID
from apps.orders.domain.entities import Order
from apps.orders.repositories.interfaces import OrderRepository
from apps.orders.domain.value_objects import Money
from io import StringIO
from uuid import UUID

class CreateOrderService:
    def __init__(self, repo: OrderRepository):
        self.repo = repo

    def execute(self, customer_id: UUID, items: list[dict]) -> UUID:
        order = Order(customer_id=customer_id)
        for itm in items:
            order.add_item(itm['product_id'], Money(itm['price']), itm['quantity'])
        self.repo.add(order)
        return order.id

class ListOrdersByCustomerService:
    def __init__(self, repo: OrderRepository):
        self.repo = repo

    def execute(self, customer_id: UUID) -> list[Order]:
        return self.repo.list_by_customer(customer_id)
    

class CSVBulkImportService:
    def __init__(self, create_service: CreateOrderService):
        self.create_service = create_service

    def execute(self, csv_content: str):
        reader = csv.DictReader(StringIO(csv_content))
        results = []

        for row_number, row in enumerate(reader, start=1):
            # Verificação básica de linha válida
            if not row or not row.get('customer_id'):
                print(f"Pulando linha {row_number}: linha vazia ou sem customer_id")
                continue

            try:
                customer_id = UUID(row['customer_id'])
            except Exception as e:
                print(f"Erro ao converter customer_id na linha {row_number}: {e}")
                continue

            items = []
            for i in range(1, 6):
                pid = row.get(f'item{i}_id')
                if not pid:
                    break  # Sem mais itens

                try:
                    item = {
                        'product_id': UUID(pid),
                        'price': int(row[f'item{i}_price']),
                        'quantity': int(row[f'item{i}_qty']),
                    }
                except Exception as e:
                    print(f"Erro ao processar item{i} na linha {row_number}: {e}")
                    break  # Pula linha com item inválido
                items.append(item)

            if not items:
                print(f"Pulando linha {row_number}: sem itens válidos")
                continue

            try:
                order_id = self.create_service.execute(customer_id, items)
                results.append(order_id)
            except Exception as e:
                print(f"Erro ao criar pedido na linha {row_number}: {e}")
                continue

        return results