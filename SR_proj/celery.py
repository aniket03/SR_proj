from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
##set the default settings module for the 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE','SR_proj.settings')

app=Celery('SR_proj')
app.config_from_object('django.conf:settings')
##app.setup_security()

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
	print('Request: {0!r}'.format(self.request))	
