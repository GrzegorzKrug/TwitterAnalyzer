from __future__ import absolute_import, unicode_literals
from celery import Celery

import os

# os.environ.setdefault('worker_pool', '10')

user = os.getenv('LOGIN', 'admin')
password = os.getenv('PASSWORD', 'mypass')
hostname = os.getenv('HOSTNAME', 'localhost')

broker_url = f'amqp://{user}:{password}@{hostname}:5672/'
app = Celery('celery_app', broker=broker_url, namespace="celery", include=['celery_app.tasks'])

# if __name__ == '__main__':
#     app.start()
