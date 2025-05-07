from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.orders.api.serializers import CreateOrderSerializer, OrderSerializer
from apps.orders.repositories.django_impl import DjangoOrderRepository
from apps.orders.application.services import CreateOrderService, ListOrdersByCustomerService

class OrderView(APIView):
    repo = DjangoOrderRepository()
    service = CreateOrderService(repo)

    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        order_id = self.service.execute(data['customer_id'], data['items'])
        return Response({'id': order_id}, status=status.HTTP_201_CREATED)

    def get(self, request, pk=None):
        order = self.repo.get_by_id(pk)
        if not order:
            return Response(status=status.HTTP_404_NOT_FOUND)
        data = {
            'id': order.id,
            'customer_id': order.customer_id,
            'total': order.total.amount,
            'items': [
                {'product_id': itm.product_id, 'price': itm.price.amount, 'quantity': itm.quantity}
                for itm in order.items
            ]
        }
        serializer = OrderSerializer(data)
        return Response(serializer.data)
    
class CustomerOrdersView(APIView):
    repo = DjangoOrderRepository()
    service = ListOrdersByCustomerService(repo)

    def get(self, request, customer_id):
        orders = self.service.execute(customer_id)
        response_data = [
            {
                'id': order.id,
                'customer_id': order.customer_id,
                'total': order.total.amount,
                'items': [
                    {'product_id': itm.product_id, 'price': itm.price.amount, 'quantity': itm.quantity}
                    for itm in order.items
                ]
            }
            for order in orders
        ]
        return Response(response_data)