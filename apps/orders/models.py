from django.db import models
import uuid

class ProcessedFile(models.Model):
    STATUS_CHOICES = [
        ('REGISTERED', 'Registered'),
        ('PROCESSED', 'Processed'),
    ]
    filename = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='REGISTERED')
    registered_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
class OrderModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_id = models.UUIDField()
    total = models.PositiveIntegerField()

class OrderItemModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(OrderModel, related_name="items", on_delete=models.CASCADE)
    product_id = models.UUIDField()
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()