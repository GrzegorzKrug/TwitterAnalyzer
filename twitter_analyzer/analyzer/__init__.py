from __future__ import absolute_import, unicode_literals

from .my_celery_app import app as celery_app

celery_app = celery_app()

__all__ = ('celery_app',)
