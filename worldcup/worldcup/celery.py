from __future__ import absolute_import, unicode_literals
import os

import json
from django.utils import timezone
from django.conf import settings
from celery import Celery
from celery.schedules import crontab



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'worldcup.settings')

app = Celery('worldcup')


app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.enable_utc = False

app.conf.update(timezone ='Asia/Kathmandu')


# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'get_EPLfixtures_at_3am': {
        'task': 'league.task.Epl_today_fixtures',
        'schedule': crontab(hour=4, minute=00, day_of_month="6-14", month_of_year=11),
        'args': (str(timezone.localtime(timezone.now()).date()),'PL')
    },
    'get_WCfixturesnov_at_4am': {
        'task': 'league.task.Epl_today_fixtures',
        'schedule': crontab(hour=4, minute=00, day_of_month="18-30", month_of_year=11),
        'args': (str(timezone.localtime(timezone.now()).date()),'WC')
    },
    'get_WCfixturesdec_at_4am': {
        'task': 'league.task.Epl_today_fixtures',
        'schedule': crontab(hour=4, minute=00, day_of_month="1-18", month_of_year=12),
        'args': (str(timezone.localtime(timezone.now()).date()),'WC')
    },
    'pointreset_at_18nov': {
        'task': 'league.task.point_reset',
        'schedule': crontab(hour=4, minute=00, day_of_month="18", month_of_year=11),
        'args': ()
    },
    'winner_of_worldcup': {
        'task': 'league.task.winnerpoint',
        'schedule': crontab(hour=00, minute=1, day_of_month="19", month_of_year=12),
        'args': ()
    }
    
}
# str(timezone.localtime(timezone.now()).date())

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')