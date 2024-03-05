from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_admin_panel.settings')

app = Celery('tasks', broker='redis://localhost:6379')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_connection_retry_on_startup = True
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.beat_schedule = {
    'check_and_send_telegram_message': {
        'task': 'django_admin_panel.bot.tasks.check_and_send_telegram_message',
        'schedule': crontab(minute='*/1'),
    },
}
app.conf.update(
    task_track_started=True,
    worker_log_format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
