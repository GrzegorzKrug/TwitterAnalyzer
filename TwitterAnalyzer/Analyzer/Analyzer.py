# TwitterAnalyzer.py
# Grzegorz Krug
# import twitter
import json
import time
import os
import pandas as pd
import datetime
import glob
import threading

from TwitterAnalyzer.Analyzer.TwitterApi import TwitterApi
from TwitterAnalyzer.Analyzer.TwitterApi import Unauthorized, ApiNotFound, TooManyRequests


class Analyzer(TwitterApi):
    def __init__(self, autologin=True, log_ui=None):
        TwitterApi.__init__(self, autologin=False)

        self._data_dir = os.path.dirname(os.path.dirname(__file__)) + '\\' + 'tweets'
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
        tweet['timestamp'] = round(time.time())

    def collect_new_tweets(self, n=10, chunk_size=200, interval=60, filename=None):
        '''Loop that runs N times, and collect Tweet x chunk_size
        Twitter rate limit is 15 times in 15 mins'''
        # chunk_size += 1
        try:
            if filename is None:
                now = datetime.datetime.now()
                filename = "Home_{y}{mon}{d}_{h}-{m}-{sec}_{interval}sec_{count}".\
                    format(y=str(now.year).rjust(4, '0'), mon=str(now.month).rjust(2, '0'),
                           d=str(now.day).rjust(2, '0'), h=str(now.hour).rjust(2, '0'),
                           m=str(now.minute).rjust(2, '0'), sec=str(now.second).rjust(2, '0'),
                           interval=str(interval).rjust(3, '0'), count=str(chunk_size).rjust(3, '0'))
            ch = 1
            while ch < n + 1:
                try:
                    home_twetts = self.collectHomeLine(chunk_size=chunk_size)
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
                except TooManyRequests as e:
                    self.log_ui(e)
                    print('Repeating chunk {} / {} after 21s.'.format(ch, n))
                    time.sleep(21)
                    continue

                except Unauthorized as e:
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

    def collect_status(self, statusList, filename=None):
        '''Requests all status from List'''
        if type(statusList) is not list:
            raise TypeError
        try:
            if filename is None:
                now = self.nowAsText()
                filename = f"Tweets_{now}"
            st = 0
            n = len(statusList)
            while st < n:
                try:
                    this_st = self.request_status(statusList[st])
                    if st == 0:
                        self.log_ui('Tweets -> {}'.format(filename + '.csv'))                    
                    if this_st:
                        self.add_timestamp_attr(this_st)
                        self.export_tweet_to_database(self._data_dir, this_st, filename)
                        
                    else:
                        self.log_ui("No tweets, None object received.")
                except TooManyRequests as e:
                    self.log_ui(e)
                    print('Repeating {} / {} after 10s.'.format(st+1, n))
                    time.sleep(10)
                    continue

                except ApiNotFound as e:
                    self.log_ui(f'{e} Not Found this tweet')
                                    
                except Unauthorized as e:
                    self.log_ui(str(e))
                    return False

                text = ('\tStatus saved: {} / {}'.format(st+1, n))                
                self.log_ui(text)                
                st += 1
            return True
        
        finally:
            pass
            
    def delete_csv(self, filelist):
        'Removes tweets_ only !'
        if type(filelist) is not list:
            filelist = [filelist]

        for file_path in filelist:
            file = os.path.basename(file_path)
            
            if not os.path.isabs(file_path):
                file_path = self._data_dir + '\\' + file_path            
            if file[-4:] == '.csv':
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                        self.log_ui(f'Removed: {file_path}')
                    except PermissionError:
                        self.log_ui(f' PermissionError: Close this file {file}')
                else:
                    self.log_ui(f'File does not exists {file_path}')
                    
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
        if not os.path.isabs(_data_dir):
            # Parent AbsPath + _data_dir
            _data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), _data_dir)
            
        file_path = _data_dir + '\\' + filename + '.csv'
        header = ['id', 'timestamp', 'contributors', 'coordinates', 'created_at',
                  'current_user_retweet', 'favorite_count', 'favorited', 'full_text', 'geo',
                  'hashtags', 'id_str', 'in_reply_to_screen_name', 'in_reply_to_status_id',
                  'in_reply_to_user_id', 'lang', 'location', 'media', 'place', 'possibly_sensitive',
                  'quoted_status', 'quoted_status_id', 'quoted_status_id_str', 'retweet_count',
                  'retweeted', 'retweeted_status', 'scopes', 'source', 'full_text', 'truncated', 'urls',
                  'user', 'user_mentions', 'withheld_copyright', 'withheld_in_countries',
                  'withheld_scope', 'tweet_mode']

        if not os.path.isfile(file_path):
            with open(file_path, 'wt') as file:
                for i, h in enumerate(header):
                    file.write(h)
                    if i < len(header)-1:
                        file.write(';')
                file.write('\n')
        if not tweet:
            return True
        try:
            with open(file_path, 'at', encoding='utf8') as file:
                for i, key in enumerate(header):
                    try:
                        text = str(tweet.get(key, None))  # fix here, dont replace?
                        for char in ['\n', ';', '\r']:
                            text = text.replace(char, '')
                        # if key == 'text':
                        #     text = text.lower()
                        file.write(text)
                    except UnicodeEncodeError:
                        input("UnicodeEncodeError...")
                        file.write('UnicodeEncodeError')

                    if i < len(header)-1:
                        file.write(';')
                file.write('\n')
            return True
        except PermissionError:
            th = threading.Thread(target=lambda:
                TwitterAnalyzer.export_tweet_to_database(_data_dir, tweet, filename, 15))

            th.start()
            self.log_ui('PermissionError, created background thread to save data')
            return None

    def filtrerDF_ByExistingKey(self, key):  # Fix exceptions, bool type
        if not key or key == '' or key not in self.DF.keys():
            self.log_ui('Wrong key to filter.')
            return False
        DF = self.DF
        df = DF.loc[(DF[key] != None) & (DF[key] != 'nan') & (DF[key] != r'n/a')
                    & (DF[key] != 'None')]
        
        if max(df.shape) > 0 and df.shape != DF.shape:
            self.DF = df
            return True
        else:
            return False
    
    def filterDF_byLang(self, lang):
        lang = str(lang)
        if self.DF is not None:
            self.DF = self.DF.loc[lambda df: df['lang'] == lang]
            self.log_ui(f'DF filtered by Language: {lang}')
        else:
            self.log_ui('DF is empty.')
        
    def find_local_tweets(self, path=None):
        if path:
            path = os.path.abspath(path)
        else:
            path = self._data_dir
        files = glob.glob(path + '\\tweets*.csv')
        return files

    def load_DF(self, file_list):
        if type(file_list) is str:
            file_list = [file_list]
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

    @staticmethod
    def nowAsText():
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
        text = 'Reloading Tweets:'
        if not self.loaded_to_DF:
            self.log_ui('Never loaded anything!')
            return False
        
        for file in self.loaded_to_DF:
            file_path = self._data_dir + '\\' + file
            try:
                df = pd.read_csv(file_path, sep=';', encoding='utf8')
                text += f'\n\t {file}'
                if self.DF is None:
                    self.DF = df
                else:
                    self.DF = pd.concat([self.DF, df])
            except FileNotFoundError:
                text += f'Missing file: {file}'
                continue

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
    app = Analyzer(autologin=False)
    app.load_DF('Home_20191104_23-36-09_060sec_200.csv')
    print(f'Shape {app.DF.shape}')
    valid = app.filtrerDF_ByExistingKey('in_reply_to_screen_name')
    print(f'Valid {valid}, Shape {app.DF.shape}')
    input('Press key....')
