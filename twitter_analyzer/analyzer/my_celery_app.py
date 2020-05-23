from __future__ import absolute_import, unicode_literals
from celery import Celery

import os

# os.environ.setdefault('worker_pool', '10')

user = os.getenv('LOGIN', 'admin')
password = os.getenv('PASSWORD', 'mypass')
hostname = os.getenv('HOSTNAME', 'localhost')

broker_url = f'amqp://{user}:{password}@{hostname}:5672/'
app = Celery('tasks', broker=broker_url, namespace="celery", include=['tasks'])

if __name__ == "__main__":
    pass
    # app.worker_main(argv=["--autoscale", "10,3"])
