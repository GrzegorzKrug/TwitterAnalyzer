from __future__ import absolute_import, unicode_literals
from .celery import app
from celery import shared_task
from .tweet_operator import TwitterOperator

import time


@shared_task
def show(*args, **kwargs):
    print(f"Start, args: {args}, kwargs: {kwargs}")
    for x in range(10):
        time.sleep(0.1)


@shared_task
def printer(duration):
    duration = duration // 1
    if duration < 0:
        duration = 0

    for x in range(duration):
        print(x)
        time.sleep(0.1)


@shared_task
def download_home_page():
    _app = TwitterOperator()
    _app.auto_collect_home_tab(n=1, chunk_size=200, interval=0)

# __all__ = ('show', 'download_home_page',)
