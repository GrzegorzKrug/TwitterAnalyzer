# TwitterAnalyzer.py
# Grzegorz Krug
import twitter
import json
import time
import os
import pandas as pd
from TwitterApi import TwitterApi, TwitterLoginFailed
import datetime
import glob
import json
import threading

class TwitterAnalyzer(TwitterApi):
    def __init__(self, autologin=True):
        TwitterApi.__init__(self, autologin=autologin)

        self._data_dir = 'tweets'
        os.makedirs(self._data_dir, exist_ok=True)  # Create folder for files

    def add_timestamp_attr(self, tweet):
        try:
            setattr(tweet, 'timestamp', round(time.time()))

        except AttributeError:
            print('Attribute error')
            tweet['timestamp'] = round(time.time())

    def collect_new_tweets(self, N=20, chunk_size=50, interval=60, filename=None, logUI=None):
        chunk_size += 1
        try:
            if filename == None:
                now = datetime.datetime.now()
                filename = "tweets_{y}{mon}{d}_{h}-{m}-{sec}_{interval}sec_{count}".\
                    format(y=str(now.year).rjust(4, '0'), mon=str(now.month).rjust(2, '0'),
                           d=str(now.day).rjust(2, '0'), h=str(now.hour).rjust(2, '0'),
                           m=str(now.minute).rjust(2, '0'), sec=str(now.second).rjust(2, '0'),
                           interval=str(interval).rjust(3, '0'), count=str(chunk_size).rjust(3, '0'))

            text = 'New tweets -> {}'.format(filename + '.csv')
            self.print_log(text, logUI)
            x = 1
            while x <  N + 1:
                try:
                    home_twetts = self.CollectHome(chunk_size)
                    if len(home_twetts) != chunk_size - 1:
                        self.print_log('\tMissing Tweets! Got {}, expected {}'.
                                       format(len(home_twetts), str(chunk_size-1)),
                                       logUI)


                    if home_twetts != None:
                        for i, tweet in enumerate(home_twetts):
                            self.add_timestamp_attr(tweet)
                            self.export_tweet_to_database(self._data_dir, tweet, filename)
                    else:
                        pass  # print("No tweets, None object received.")
                except twitter.error.TwitterError as e:
                    self.print_log(e, logUI)
                    time.sleep(25)
                    print('Repeating chunk {} / {}'.format(x, N))
                    continue

                except TwitterLoginFailed as e:
                    self.print_log(str(e), logUI)
                    return False

                text = ('\tTweets chunk saved: {} / {}'.format(x, N))
                self.print_log(text, logUI)

                if x >= N:
                    break

                if interval > 0:
                    self.print_log('\tSleeping {}s'.format(interval), logUI)
                    time.sleep(interval)
                x += 1
            text = '\tFinished -> {}'.format(filename + '.csv')
            self.print_log(text, logUI)

            return True
        finally:
            pass
            # text = 'Finished -> {}'.format(filename + '.csv')
            # print(text)

    @staticmethod
    def export_tweet_to_database(_data_dir, tweet, filename='default', delay=0):
        if delay > 0:
            time.sleep(delay)

        if type(filename) != str:
            raise TypeError('File name is not string!')
        file_path = _data_dir + '\\' + filename + '.csv'
        header = ['id', 'timestamp', 'contributors', 'coordinates', 'created_at',
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
                for i,h in enumerate(header):
                    file.write(h)
                    if i < len(header)-1:
                        file.write(';')
                file.write('\n')

        try:
            with open(file_path, 'a', encoding='utf8') as file:
                for i, key in enumerate(header):
                    try:
                        text = str(tweet.get(key, 'n/a'))
                        for char in ['\n', ';', '\r']:
                            text = text.replace(char, '')
                        file.write(text)
                    except UnicodeEncodeError:
                        file.write('UnicodeEncodeError')
                    if i < len(header)-1:
                        file.write(';')
                file.write('\n')
        except PermissionError:
            th = threading.Thread(target=lambda: TwitterAnalyzer.export_tweet_to_database(_data_dir, tweet, filename, 15))
            th.start()
            print('PermissionError, created background thread to save data')
            return None

    @staticmethod
    def export_tweet_to_jsonbase(_data_dir, tweet, filename='default', delay=0):
        if delay > 0:
            time.sleep(delay)

        if type(filename) != str:
            raise TypeError('File name is not string!')
        file_path = _data_dir + '\\' + filename + '.json'
        header = ['id', 'timestamp', 'contributors', 'coordinates', 'created_at',
                  'current_user_retweet', 'favorite_count', 'favorited', 'full_text', 'geo',
                  'hashtags', 'id_str', 'in_reply_to_screen_name', 'in_reply_to_status_id',
                  'in_reply_to_user_id', 'lang', 'location', 'media', 'place', 'possibly_sensitive',
                  'quoted_status', 'quoted_status_id', 'quoted_status_id_str', 'retweet_count',
                  'retweeted', 'retweeted_status', 'scopes', 'source', 'text', 'truncated', 'urls',
                  'user', 'user_mentions', 'withheld_copyright', 'withheld_in_countries',
                  'withheld_scope', 'tweet_mode']

        try:
            with open(file_path, 'a', encoding='utf8') as file:
                json.dump(tweet, file, indent=4)

        except PermissionError:
            th = threading.Thread(
                target=lambda: TwitterAnalyzer.export_tweet_to_jsonbase(_data_dir, tweet, filename, 15))
            th.start()
            print('PermissionError, created background thread to save data')

    def find_local_tweets(self, path=None):
        if path == None:
            path = self._data_dir
        else:
            path = os.path.abspath(path)

        files = glob.glob(path + '\\tweets*.csv')
        print(files)
        return files

    def load_csv(self, file_path):
        df = None
        with open(file_path) as f:
            df = pd.read_csv()

        return df

    @staticmethod
    def print_log(text, logUI):
        print(text)
        if logUI:
            logUI(text)

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


if __name__ == "__main__":
    app = TwitterAnalyzer()
    app.collect_new_tweets(N=3, chunk_size=5, interval=10)
    print('End....')










