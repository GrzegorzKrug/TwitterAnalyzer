from __future__ import absolute_import, unicode_literals
from .celery import app
from celery import shared_task
from .tweet_operator import TwitterOperator
from .database_operator import drop_existing_tweets
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
def get_tweets_from_home_board(n=1, chunk_size=200, interval=60):
    _app = TwitterOperator()
    _app.auto_collect_home_tab(n=n, chunk_size=chunk_size, interval=interval)


@shared_task
def download_parent_tweets(tweet_list=None):
    if tweet_list is None:
        TwitterOperator().logger.error(f"Missing input, tweet_list: {tweet_list}")
        return None
    _app = TwitterOperator(auto_login=False)
    _app.tweet_list = tweet_list.copy()
    status_list = _app.find_parent_tweets()
    status_list = drop_existing_tweets(_app.Session, status_list)
    _app.logger.debug(f"Starting download of {len(status_list)} parent tweets")
    _app.collect_status_list(status_list=status_list)
