import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dtest.settings')
app = Celery('dtest', broker=os.getenv('BROKER_URL'))
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()