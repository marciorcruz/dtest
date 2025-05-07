from datetime import timezone
import os
from apps.orders.models import ProcessedFile
from celery import shared_task
from apps.orders.repositories.django_impl import DjangoOrderRepository
from apps.orders.application.services import CreateOrderService, CSVBulkImportService

@shared_task
def import_orders_from_csv(csv_content):
    repo = DjangoOrderRepository()
    create_service = CreateOrderService(repo)
    bulk_service = CSVBulkImportService(create_service)
    return [str(oid) for oid in bulk_service.execute(csv_content)]


@shared_task
def scan_and_import_csv():
    base_dir = '/app/data/csv'
    for fname in os.listdir(base_dir):
        if not fname.lower().endswith('.csv'):
            continue
        if ProcessedFile.objects.filter(filename=fname).exists():
            continue
        path = os.path.join(base_dir, fname)
        content = open(path, 'r').read()
        # Registra como identified
        record = ProcessedFile.objects.create(filename=fname, status='REGISTERED')
        result = import_orders_from_csv.delay(content)
        # Quando a task finalizar, marque como processed
        from celery.result import AsyncResult # type: ignore
        task_result = AsyncResult(result.id)
        task_result.get()  # bloqueia até conclusão (ou adapte para callback)
        record.status = 'PROCESSED'
        record.processed_at = timezone.now()
        record.save()