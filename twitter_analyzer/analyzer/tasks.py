from __future__ import absolute_import, unicode_literals
from .celery import app
from .tweet_operator import TwitterOperator
from .database_operator import drop_existing_tweets

import time


@app.task
def get_tweets_from_home_board(n=1, chunk_size=200, interval=60):
    _app = TwitterOperator()
    _app.auto_collect_home_tab(n=n, chunk_size=chunk_size, interval=interval)


@app.task
def download_parent_tweets(tweet_list=None):
    if tweet_list is None:
        TwitterOperator().logger.error(f"Missing input, tweet_list: {tweet_list}")
        return None
    _app = TwitterOperator(auto_login=False)
    _app.tweet_list = tweet_list.copy()
    status_list = _app.find_parent_tweets()
    if status_list and len(status_list) > 0:
        status_list = drop_existing_tweets(_app.Session, status_list)
        _app.logger.debug(f"Starting download of {len(status_list)} parent tweets")
        _app.collect_status_list(status_list=status_list)


@app.task
def collect_status_list(tweet_list=None, overwrite=False):
    if tweet_list is None:
        TwitterOperator().logger.error(f"Missing input, tweet_list: {tweet_list}")
        return None
    _app = TwitterOperator(auto_login=False)
    _app.collect_status_list(tweet_list, overwrite=overwrite)
