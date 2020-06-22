from __future__ import absolute_import, unicode_literals
from celery import Celery

import os

user = os.getenv('LOGIN', 'admin')
password = os.getenv('PASSWORD', 'mypass')
hostname = os.getenv('HOSTNAME', 'localhost')

broker_url = f'amqp://{user}:{password}@{hostname}:5672/'
app = Celery('tasks', broker=broker_url, namespace="analyzer_celery", include=['analyzer.tasks'])

app.conf.beat_schedule = {
        'Add-Home-Page': {
                'task': 'analyzer.tasks.get_tweets_from_home_board',
                'schedule': 90,
        },
}

__all__ = ("app",)
