from rest_framework import serializers

class OrderItemSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    price = serializers.IntegerField()
    quantity = serializers.IntegerField()

class CreateOrderSerializer(serializers.Serializer):
    customer_id = serializers.UUIDField()
    items = OrderItemSerializer(many=True)

class OrderSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    customer_id = serializers.UUIDField()
    total = serializers.IntegerField()
    items = OrderItemSerializer(many=True)