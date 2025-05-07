from django.contrib import admin
from apps.orders.models import OrderModel, OrderItemModel, ProcessedFile

class OrderItemInline(admin.TabularInline):
    model = OrderItemModel
    extra = 0

@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_id', 'total')
    inlines = [OrderItemInline]

@admin.register(OrderItemModel)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product_id', 'price', 'quantity')

@admin.register(ProcessedFile)
class ProcessedFileAdmin(admin.ModelAdmin):
    list_display = ('filename', 'status', 'registered_at', 'processed_at')
