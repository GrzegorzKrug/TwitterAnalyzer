# TwitterAnalyzer.py
# Grzegorz Krug
import twitter
import json
import time
import os
import pandas as pd
from TwitterApi import TwitterApi
import datetime

class TwitterAnalyzer(TwitterApi):
    def __init__(self, autologin=True):
        TwitterApi.__init__(self, autologin=autologin)

        self._data_dir = 'tweets'
        os.makedirs(self._data_dir, exist_ok=True)  # Create folder for files

    def export_tweet_to_database(self, tweet, filename='default'):
        if type(filename) != str:
            raise TypeError('File name is not string!')
        file_path = self._data_dir + '\\' + filename + '.csv'
        head = ['id', 'timestamp', 'contributors', 'coordinates', 'created_at',
                'current_user_retweet', 'favorite_count', 'favorited', 'full_text', 'geo',
                'hashtags', 'id_str', 'in_reply_to_screen_name', 'in_reply_to_status_id',
                'in_reply_to_user_id', 'lang', 'location', 'media', 'place', 'possibly_sensitive',
                'quoted_status', 'quoted_status_id', 'quoted_status_id_str', 'retweet_count',
                'retweeted', 'retweeted_status', 'scopes', 'source', 'text', 'truncated', 'urls',
                'user', 'user_mentions', 'withheld_copyright', 'withheld_in_countries',
                'withheld_scope', 'tweet_mode']

        # df = pd.DataFrame.from_dict(tweet)
        if not os.path.isfile(file_path):
            with open(file_path, 'wt') as file:
                for h in head:
                    file.write(h)
                    file.write(';')
                file.write('\n')

        with open(file_path, 'at') as file:
            for key in head:
                try:
                    text = str(tweet.get(key, 'n/a'))
                    for char in ['\n', ';', '\r']:
                        text = text.replace(char, '')
                    file.write(text)
                except UnicodeEncodeError:
                    file.write('UnicodeEncodeError')

                file.write(';')
            file.write('\n')

    def add_timestamp(self, tweet):
        try:
            setattr(tweet, 'timestamp', round(time.time()))

        except AttributeError:
            tweet['timestamp'] = round(time.time())

    @staticmethod
    def tweet_strip(tweet):
        def add_data(query, new_query=None):
            if new_query == None:
                new_query = query

            out[new_query] = tweet[query]
        out = {}
        add_data('text')
        add_data('lang')
        add_data('created_at')

        add_data('id')
        add_data('user')
        add_data('urls')

        add_data('user_mentions')
        add_data('hashtags')
        add_data('media')

        add_data('retweet_count')
        add_data('favorite_count')
        # add_data comments  # <-- ??

        add_data('in_reply_to_screen_name')
        add_data('in_reply_to_status_id')
        add_data('in_reply_to_user_id')
        add_data('quoted_status')
        add_data('quoted_status_id', 'quoted_status_id')

        return out

    def collect_new_tweets(self, N=20, chunk_count=50, interval=60, filename=None):
        try:
            if filename == None:
                now = datetime.datetime.now()
                filename = "tweets_{y}{mon}{d}_{h}-{m}_{interval}sec_{count}".format(y=now.year, mon=now.month, d=now.day,
                                                                                    h=now.hour, m=now.minute,
                                                                                    interval=interval, count=chunk_count)
            print('Collecting tweets -> {}'.format(filename + '.csv'))
            for x in range(1, N + 1):
                print('Current tweet chunk: {} / {}'.format(x, N))
                try:
                    home_twetts = app.CollectHome(chunk_count)
                    for i, tweet in enumerate(home_twetts):
                        app.add_timestamp(tweet)
                        app.export_tweet_to_database(tweet, filename)

                except twitter.error.TwitterError:
                    print('Twitter rate limit exceeded!')
                time.sleep(interval)
        finally:
            print('Collecting is finished -> {}'.format(filename+'.csv'))


if __name__ == "__main__":
    app = TwitterAnalyzer()
    for i in range(10):
        app.collect_new_tweets(N=100, chunk_count=100, interval=60)
    input('End....')










