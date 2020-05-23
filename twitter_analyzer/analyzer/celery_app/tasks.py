from __future__ import absolute_import, unicode_literals
from .celery import app

import time


@app.task
def show(*args, **kwargs):
    print(f"Start, args: {args}, kwargs: {kwargs}")
    for x in range(10):
        time.sleep(0.1)


@app.task
def printer(duration):
    duration = duration // 1
    if duration < 0:
        duration = 0

    for x in range(duration):
        print(x)
        time.sleep(0.1)


__all__ = ('show',)
