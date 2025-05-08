from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from apps.core.views import home  # ajuste conforme sua estrutura

from dtest import settings

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('api/', include('apps.orders.api.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)