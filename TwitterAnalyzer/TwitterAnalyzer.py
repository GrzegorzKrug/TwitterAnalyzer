# TwitterAnalyzer.py
# Grzegorz Krug
import twitter
import json
import time
import os
import pandas as pd
from TwitterApi import TwitterApi


class TwitterAnalyzer(TwitterApi):
    def __init__(self, autologin=True):
        TwitterApi.__init__(self, autologin=autologin)

        self._data_dir = 'tweets'
        self.tweet_file_name = 'last_file'
        os.makedirs(self._data_dir, exist_ok=True)  # Create folder for files

        if self.logged_in:
            user_data = self.api.VerifyCredentials()
            print('Logged in as {}.'.format(user_data['screen_name']))



    def export_tweet_to_database(self, tweet, filename='default_name'):
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

    def collect_new_tweets(self, count=20):
        home_twetts = app.CollectHome(count)
        for i, tweet in enumerate(home_twetts):
            app.add_timestamp(tweet)
            app.export_tweet_to_database(tweet)

if __name__ == "__main__":
    app = TwitterAnalyzer()
    for x in range(100):
        app.collect_new_tweets(100)
        time.sleep(30)









