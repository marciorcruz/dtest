from django.urls import path
from .views import CustomerOrdersView, OrderView

urlpatterns = [
    path('orders/', OrderView.as_view()),
    path('orders/<uuid:pk>/', OrderView.as_view()),
    path('orders/customer/<uuid:customer_id>/', CustomerOrdersView.as_view()),
]