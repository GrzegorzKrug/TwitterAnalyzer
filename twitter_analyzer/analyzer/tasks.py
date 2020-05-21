from __future__ import absolute_import, unicode_literals
from celery import shared_task

import time


@shared_task
def show(*args, **kwargs):
    duration = 10
    print(f"Start, args: {args}, kwargs: {kwargs}")
    for x in range(duration):
        # print(duration - x)
        time.sleep(0.3)
