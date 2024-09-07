"""
Celery configuration.
"""
import os
import logging

from celery import Celery
from celery.schedules import crontab

from decouple import config

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'llm.settings')


app = Celery('llm_job', broker=config('REDIS_URL'))


# Load the celery settings from the Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(['application.llm_service'])

# Read schedule from environment variable
schedule_interval_minute = config('RANDOM_GENERATOR_SCHEDULE_INTERVAL_MINUTE', '*')
schedule_interval_hour = config('RANDOM_GENERATOR_SCHEDULE_INTERVAL_HOUR', '*')

LOG = logging.getLogger(__name__)

app.conf.beat_schedule = {
    'generate-performance-metrics-dynamically': {
        'task': 'application.llm_service.generate_performance_metrics',
        'schedule': crontab(minute=schedule_interval_minute, hour=schedule_interval_hour),
    },
}