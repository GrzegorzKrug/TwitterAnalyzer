# TwitterAnalyzer.py
# Grzegorz Krug
import twitter
import json
import time
import os
import pandas as pd
import datetime
import glob
import threading
from TwitterAnalyzer.Analyzer.TwitterApi import TwitterApi


class TwitterAnalyzer(TwitterApi):
    def __init__(self, autologin=True, log_ui=None):
        TwitterApi.__init__(self, autologin=False)

        if os.path.basename(os.getcwd()) == 'Analyzer':
            self._data_dir = os.path.dirname(os.getcwd()) + '\\' + 'tweets'
        else:
            self._data_dir = 'tweets'
        os.makedirs(self._data_dir, exist_ok=True)  # Create folder for files

        self.log_ui_ref = log_ui
        self.DF = None
        self.loaded_to_DF = []
        
        if autologin:
            valid, text = self._login_procedure()
            self.log_ui(text)

    @staticmethod
    def add_timestamp_attr(tweet):
        '''Adding time stamp to tweet dict'''
        try:
            setattr(tweet, 'timestamp', round(time.time()))

        except AttributeError:
            print('Attribute error')
            tweet['timestamp'] = round(time.time())

    def collect_new_tweets(self, n=10, chunk_size=200, interval=60, filename=None):
        '''Loop that runs N times, and collect Tweet x chunk_size
        Twitter rate limit is 15 times in 15 mins'''
        # chunk_size += 1
        try:
            if filename is None:
                now = datetime.datetime.now()
                filename = "tweets_{y}{mon}{d}_{h}-{m}-{sec}_{interval}sec_{count}".\
                    format(y=str(now.year).rjust(4, '0'), mon=str(now.month).rjust(2, '0'),
                           d=str(now.day).rjust(2, '0'), h=str(now.hour).rjust(2, '0'),
                           m=str(now.minute).rjust(2, '0'), sec=str(now.second).rjust(2, '0'),
                           interval=str(interval).rjust(3, '0'), count=str(chunk_size).rjust(3, '0'))

            ch = 1
            while ch < n + 1:
                try:
                    home_twetts = self.CollectHome(chunk_size)
                    if ch == 1:
                        self.log_ui('New tweets -> {}'.format(filename + '.csv'))
                    if len(home_twetts) != chunk_size:
                        self.log_ui('\tMissing Tweets! Got {}, expected {}'.format(len(home_twetts), str(chunk_size)))
                    if home_twetts:
                        for i, tweet in enumerate(home_twetts):
                            # if tweet['id_str'][-1] == '0':
                            #     print(tweet)
                            self.add_timestamp_attr(tweet)
                            self.export_tweet_to_database(self._data_dir, tweet, filename)
                    else:
                        self.log_ui("No tweets, None object received.")
                except twitter.error.TwitterError as e:
                    self.log_ui(e)
                    print('Repeating chunk {} / {} after 25s.'.format(ch, n))
                    time.sleep(25)
                    continue

                except TwitterLoginFailed as e:
                    self.log_ui(str(e))
                    return False

                text = ('\tTweets chunk saved: {} / {}'.format(ch, n))
                self.log_ui(text)
                if ch >= n:
                    break
                if interval > 0:
                    self.log_ui('\tSleeping {}s'.format(interval))
                    time.sleep(interval)
                ch += 1
            # text = '\tFinished -> {}'.format(filename + '.csv')
            # self.log_ui(text)

            return True
        finally:
            pass
            # text = 'Finished -> {}'.format(filename + '.csv')
            # print(text)

    def delete_csv(self, filelist):
        'Removes tweets_ only !'
        if type(filelist) is str:
            filelist = [filelist]

        for file_path in filelist:
            file = os.path.basename(file_path)
            if file[-4:] == '.csv' and file[:7] == 'tweets_':
                file_path = self._data_dir + '\\' + file
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                        self.log_ui(f'Removed {file}')
                    except PermissionError:
                        self.log_ui(f' PermissionError: Close this file {file}')

    def delete_less(self, n=200):
        'Procedure, Finds Tweets .csv, Removes them.'
        filelist = self.find_local_tweets()
        for f in filelist:
            df = pd.read_csv(f, sep=';', encoding='utf8')
            if df.shape[0] < n:
                # self.log_ui('Smaller file '+ f)
                self.delete_csv(f)
            else:
                pass
        self.log_ui(f'Done removing')

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

        if not os.path.isfile(file_path):
            with open(file_path, 'wt') as file:
                for i, h in enumerate(header):
                    file.write(h)
                    if i < len(header)-1:
                        file.write(';')
                file.write('\n')
        try:
            with open(file_path, 'at', encoding='utf8') as file:
                for i, key in enumerate(header):
                    try:
                        text = str(tweet.get(key, 'n/a'))
                        for char in ['\n', ';', '\r']:
                            text = text.replace(char, '')
                        # if key == 'text':
                        #     text = text.lower()
                        file.write(text)
                    except UnicodeEncodeError:
                        file.write('UnicodeEncodeError')

                    if i < len(header)-1:
                        file.write(';')
                file.write('\n')
        except PermissionError:
            th = threading.Thread(target=lambda:
                TwitterAnalyzer.export_tweet_to_database(_data_dir, tweet, filename, 15))

            th.start()
            print('PermissionError, created background thread to save data')
            return None

    # @staticmethod
    # def export_tweet_to_jsonbase(_data_dir, tweet, filename='default', delay=0):
    #     if delay > 0:
    #         time.sleep(delay)
    #
    #     if type(filename) != str:
    #         raise TypeError('File name is not string!')
    #     file_path = _data_dir + '\\' + filename + '.json'
    #     header = ['id', 'timestamp', 'contributors', 'coordinates', 'created_at',
    #               'current_user_retweet', 'favorite_count', 'favorited', 'full_text', 'geo',
    #               'hashtags', 'id_str', 'in_reply_to_screen_name', 'in_reply_to_status_id',
    #               'in_reply_to_user_id', 'lang', 'location', 'media', 'place', 'possibly_sensitive',
    #               'quoted_status', 'quoted_status_id', 'quoted_status_id_str', 'retweet_count',
    #               'retweeted', 'retweeted_status', 'scopes', 'source', 'text', 'truncated', 'urls',
    #               'user', 'user_mentions', 'withheld_copyright', 'withheld_in_countries',
    #               'withheld_scope', 'tweet_mode']
    #     try:
    #         with open(file_path, 'a', encoding='utf8') as file:
    #             json.dump(tweet, file, indent=4)
    #
    #     except PermissionError:
    #         th = threading.Thread(
    #             target=lambda: TwitterAnalyzer.export_tweet_to_jsonbase(_data_dir, tweet, filename, 15))
    #         th.start()
    #         print('PermissionError, created background thread to save data')

    def find_local_tweets(self, path=None):
        if path:
            path = os.path.abspath(path)
        else:
            path = self._data_dir
        files = glob.glob(path + '\\tweets*.csv')
        return files

    def load_DF(self, file_list):
        self.DF = None
        self.loaded_to_DF = []
        text = 'Loading Tweets:'
        for file in file_list:
            file_path = self._data_dir + '\\' + file
            df = pd.read_csv(file_path, sep=';', encoding='utf8')
            self.loaded_to_DF += [file]
            text += f'\n\t {file}'
            if self.DF is None:
                self.DF = df
            else:
                self.DF = pd.concat([self.DF, df])
        self.log_ui(text)

    def log_ui(self, text):
        print(text)
        if self.log_ui_ref:
            self.log_ui_ref(text)

    def nowAsText(self):
        now = datetime.datetime.now()
        text = f'{now.year}'.ljust(4, '0') \
              + f'{now.month}'.ljust(2, '0') \
              + f'{now.day}'.ljust(2, '0') \
              + f'_{now.hour}'.ljust(3, '0') \
              + f'-{now.minute}'.ljust(3, '0') \
              + f'-{now.second}'.ljust(3, '0')
        return text

    def reloadDF(self):
        self.DF = None
        text = 'Reloading Tweets'
        for file in self.loaded_to_DF:
            file_path = self._data_dir + '\\' + file
            df = pd.read_csv(file_path, sep=';', encoding='utf8')
            text += f'\n\t {file}'
            if self.DF is None:
                self.DF = df
            else:
                self.DF = pd.concat([self.DF, df])

        self.log_ui(text)


    def save_current_DF(self, extraText=None):
        if extraText:
            extraText = '_' + extraText
        filepath = self._data_dir + '\\' + 'dataframe_' + self.nowAsText() + extraText + '.csv'
        self.save_DF(self.DF, filepath)

    def save_DF(self, DF, filepath):
        if DF is None:
            self.log_ui('DF is empty!')
            return None
        else:
            with open(filepath, 'wt', encoding='utf8') as f:
                DF.to_csv(f, sep=';', encoding='utf8', index=False)
                self.log_ui(f'Saved DF to file: {os.path.abspath(filepath)}')

        #    return True
        #self.log_ui(f'Error when saving to file, {os.path.abspath(filepath)}')

    @staticmethod
    def tweet_strip(tweet):
        def add_data(query, new_query=None):
            if new_query is None:
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
    for x in range(10):
        app.collect_new_tweets(n=60, chunk_size=200, interval=60)
    input('Press key....')
