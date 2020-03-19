# analyzer.py
# Grzegorz Krug

import time
import os
import pandas as pd
import datetime
import glob
import threading
import calendar
import re
import ast

from .custom_logger import define_logger
from pandas.errors import ParserError
from twitter_analyzer.analyzer.api import TwitterApi
from twitter_analyzer.analyzer.api import Unauthorized, ApiNotFound, TooManyRequests


class Analyzer(TwitterApi):
    def __init__(self, auto_login=False):
        TwitterApi.__init__(self, auto_login=False)  # Do not login via api!

        self._data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tweets')
        os.makedirs(self._data_dir, exist_ok=True)  # Create folder for files

        # self.logger_ref = log_ui
        self.DF = None
        self.threads = []  # Thread reference list
        self.th_num = 0  # Thread counter
        self.loaded_to_DF = []
        self.logger = define_logger("Analyzer")

        if auto_login:
            valid = self.login_procedure()
            self.logger.debug(f"Auto_login status: '{valid}'")

    @staticmethod
    def add_timestamp_attr(tweet):
        """Adding time stamp to tweet dict"""
        tweet['timestamp'] = round(time.time())

    def auto_collect_home_tab(self, n=10, chunk_size=200, interval=60, file_name=None):
        """Loop that runs N times, and collect Tweet x chunk_size
        Twitter rate limit is 15 times in 15 mins"""
        if file_name is None:
            now = datetime.datetime.now()
            file_name = "Home_{y}{mon}{d}_{h}-{m}-{sec}_{interval}sec_{count}". \
                format(y=str(now.year).rjust(4, '0'), mon=str(now.month).rjust(2, '0'),
                       d=str(now.day).rjust(2, '0'), h=str(now.hour).rjust(2, '0'),
                       m=str(now.minute).rjust(2, '0'), sec=str(now.second).rjust(2, '0'),
                       interval=str(interval).rjust(3, '0'), count=str(chunk_size).rjust(3, '0'))
            file_with_ext = file_name + '.csv'
        ch = 1
        while ch < n + 1:
            try:
                if ch == 1:
                    self.logger.debug(f"Created file for tweets: {file_with_ext}")
                valid = self.collect_tweets_on_home_tab(chunk_size=chunk_size, file_name=file_name)
                if valid:
                    self.logger.debug(f"Dropping duplicates from home timeline: {file_name}")
                    app = Analyzer()
                    valid = app.load_df([file_with_ext])
                    if valid:
                        resp = app.drop_duplicates_from_df()
                    if valid and resp is not False:  # In case drop duplicates fails process further
                        app.save_current_df(full_name=file_name)
                    else:
                        self.logger.error("Duplicate drop not succeed in auto_home_line")

            except TooManyRequests as e:
                self.logger.warning(f"Too many requests: {e}")
                self.logger.debug('Repeating chunk {} / {} after 21s.'.format(ch, n))
                time.sleep(21)
                continue

            except Unauthorized as e:
                self.logger.critical(str(e))
                return False

            self.logger.debug(f"Tweets chunk saved: {ch} / {n}")
            if ch >= n:
                break
            if interval > 0:
                self.logger.debug('Sleeping {}s'.format(interval))
                time.sleep(interval)
            ch += 1

    @staticmethod
    def check_series_time_condition(time_series, timestamp_min, timestamp_max):
        """Times series are defined by tweeter,
        time_min is minimum input in format 'YMDhhmmss'
        time_max is maxmimum input in format 'YMDhhmmss'"""
        minimum = int(timestamp_min)
        maximum = int(timestamp_max)
        if minimum > maximum:
            minimum, maximum = maximum, minimum

        out_bool = []

        for time_text in time_series:
            dt = datetime.datetime.strptime(time_text, '%a %b %d %H:%M:%S %z %Y')
            timestamp = int(dt.timestamp())
            if minimum <= timestamp <= maximum:
                cond = True
            else:
                cond = False
            out_bool.append(cond)

        return out_bool

    @staticmethod
    def check_series_words_anywhere(series, words, inverted=False):
        words = re.split('[|+,\n\r]', words)  # split phrases but ignore spaces
        words = [w.lstrip(" ").rstrip(" ") for w in words if len(w.lstrip(" ").rstrip(" ")) > 0]
        out = []  # Empty out list

        for ind, row in series.iterrows():  # Find phrases in key or value
            tweet_row_checked = False
            for key, value in row.items():
                value = str(value)
                for word in words:
                    if word.lower() in value.lower() or word.lower() in key.lower():
                        out.append(False if inverted else True)
                        tweet_row_checked = True
                        break
                if tweet_row_checked:
                    break
            if tweet_row_checked is False:
                out.append(True if inverted else False)
        return out

    @staticmethod
    def check_series_words_in_text(series, words, inverted=False):
        words = re.split('[|+,\n\r]', words)  # split phrases but ignore spaces
        # Remove start-end spaces
        words = [w.lstrip(" ").rstrip(" ") for w in words if len(w.lstrip(" ").rstrip(" ")) > 0]
        out = []  # Empty out list

        data = series['full_text']
        for df in data:
            word_checked = False
            for word in words:
                if word.lower() in df.lower():
                    out.append(False if inverted else True)

                    word_checked = True
                    break
            if not word_checked:
                out.append(True if inverted else False)

        data = series['quoted_status']
        for i, df in enumerate(data):
            if out[i]:
                continue
            resp = Analyzer.check_series_quoted_status_recurrent(df, words)
            if resp:
                out[i] = False if inverted else True
        return out

    @staticmethod
    def check_series_user_text(series, user_text, inverted=False):
        user_text = user_text.lower()
        words = re.split('[|+,\n\r]', user_text)  # split phrases but ignore spaces
        Analyzer().logger.debug(f"filter words: '{words}'")
        # Remove start-end spaces
        words = [w.lstrip(" ").rstrip(" ") for w in words if len(w.lstrip(" ").rstrip(" ")) > 0]
        out = []  # Empty out list
        data = series['user']
        for row in data:
            word_checked = False
            if str(row).lower() == 'nan':
                out.append(False)
                continue

            user_dict = ast.literal_eval(row)

            if user_dict:
                user_id = str(user_dict['id'])
                name = user_dict['name'].lower()
                alias = user_dict['screen_name'].lower()
                # Analyzer().logger.debug(f"User: '{name}','{alias}', '{user_id}'")
                for word in words:
                    if word in name or word in alias or word in user_id:
                        out.append(False if inverted else True)
                        word_checked = True
                        break
            if not word_checked:
                out.append(True if inverted else False)
        return out

    @staticmethod
    def check_series_quoted_status_recurrent(tweet, words):
        tweet_str = str(tweet)
        if tweet_str.lower() == 'none' \
                or tweet_str.lower() == 'nan' \
                or tweet_str == "":
            return False
        tweet_dict = ast.literal_eval(tweet)
        if tweet_dict:
            data = tweet_dict['full_text']
            for word in words:  # If word is in text, return True
                if word.lower() in data.lower():
                    return True
            try:
                quoted_tweet = tweet_dict['quoted_status']
            except KeyError:
                return False

            if quoted_tweet:  # If quoted tweet exists go deeper
                resp = Analyzer.check_series_quoted_status_recurrent(quoted_tweet, words)
                return resp
            return False

    def collect_status_list(self, status_list, file_name=None):
        """Requests all status from List"""
        if type(status_list) is not list:
            self.logger.error(f"This is not list: '{status_list}'")
            return False

        if file_name is None:
            now = self.now_as_text()
            file_name = f"Tweets_{now}" + '.csv'
        st = 0
        status_list = list(set(status_list))  # Drop duplicated numbers
        n = len(status_list)
        threads = []
        for st, status_num in enumerate(status_list):
            if st % 25 == 0:
                for th in threads:
                    th.join()
                threads = []
            if st == 0:
                self.logger.debug(f"New tweets file: '{file_name}'")
            th = self.fork_method(
                method_to_fork=self.collect_status_list_thread,
                file_name=file_name, status_num=status_num, this_tweet_num=st, all_tweets=n)
            threads.append(th)

        for th in threads:
            th.join()

        self.logger.debug(f"All threads finished")
        return True

    @staticmethod
    def collect_status_list_thread(file_name, status_num, this_tweet_num, all_tweets):
        app = Analyzer()
        while True:
            try:
                this_st = app.request_status(status_num)

                if this_st:
                    app.add_timestamp_attr(this_st)
                    app.export_tweet_to_database(app._data_dir, this_st, file_name)
                    break
                else:
                    app.logger.error("No tweets, None object received.")
                    return None

            except TooManyRequests as tmr:
                app.logger.warning(f"Too many requests: {tmr}")
                time.sleep(10)

            except ApiNotFound as e:
                app.logger.error(f'{e} Not Found this tweet: {status_num}')
                return None

            except Unauthorized as un:
                app.logger.error(f"{un}: {status_num}")
                return None

        app.logger.debug(f"Status saved: {this_tweet_num} / {all_tweets}")

    def collect_tweets_on_home_tab(self, chunk_size, file_name):
        """Request home line, catch exceptions"""
        home_tweets = self.request_home_timeline(chunk_size=chunk_size)

        if len(home_tweets) != chunk_size:
            self.logger.warning(
                'Missing Tweets! Got {}, expected {}'.format(len(home_tweets), str(chunk_size))
            )
        if home_tweets:
            for i, tweet in enumerate(home_tweets):
                self.add_timestamp_attr(tweet)
                self.export_tweet_to_database(self._data_dir, tweet, file_name)
        else:
            self.logger.error("No tweets, None object received.")
            return False

        return True

    def delete_csv(self, file_list):
        """Removes tweets_ only !"""
        if type(file_list) is not list:
            file_list = [file_list]

        for file_path in file_list:
            file_name = os.path.basename(file_path)

            if not os.path.isabs(file_path):
                file_path = os.path.abspath(os.path.join(self._data_dir, file_path))

            if file_name[-4:] == '.csv':
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                        self.logger.debug(f'Removed: {file_path}')
                    except PermissionError:
                        self.logger.error(f'PermissionError: Close this file {file_name}')
                else:
                    self.logger.error(f'File does not exists {file_path}')
            else:
                self.logger.error(f"File {file_name} is not .csv")

    def delete_less(self, n=200):
        """Procedure, Finds Tweets .csv, Removes them."""
        file_list = self.find_local_tweets()
        for f in file_list:
            df = pd.read_csv(f, sep=';', encoding='utf8')
            if df.shape[0] < n:
                self.delete_csv(f)
            else:
                pass
        self.logger.debug(f'Done removing')

    def drop_tweet_in_df(self, index):
        if self.DF is not None:
            df = self.DF
            if 0 > index > len(df):
                self.logger.error("Invalid index, can not drop tweet")
                return None

            df = df.drop(df.index[index])
            if self.filter_conditions(df):
                self.logger.debug(f"Successfully dropped this tweet, index: {index}")
                self.DF = df
        else:
            self.logger.warning('DF is empty. Load some tweets first.')

    def drop_duplicates_from_df(self, keep_new=True):
        if keep_new:
            keep = 'last'
        else:
            keep = 'first'

        if self.DF is not None:
            df = self.DF
            df = df.sort_values('timestamp').drop_duplicates(subset=['id'], keep=keep)
            if self.filter_conditions(df):
                self.logger.debug("Successfully dropped duplicates")
                self.DF = df
                return True
            else:
                self.logger.warning("Could not drop duplicates")
        else:
            self.logger.warning('DF is empty. Load some tweets first.')

    # @staticmethod
    def export_tweet_to_database(self, _data_dir, tweet, filename='default', delay=0):
        if delay > 0:
            time.sleep(delay)
        if type(filename) != str:
            raise TypeError('File name is not string!')
        if not os.path.isabs(_data_dir):
            # Parent AbsPath + _data_dir
            _data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), _data_dir)

        file_path = os.path.join(_data_dir, filename + '.csv')
        header = ['id', 'timestamp', 'contributors', 'coordinates', 'created_at',
                  'current_user_retweet', 'favorite_count', 'favorited', 'full_text', 'geo',
                  'hashtags', 'id_str', 'in_reply_to_screen_name', 'in_reply_to_status_id',
                  'in_reply_to_user_id', 'lang', 'location', 'media', 'place', 'possibly_sensitive',
                  'quoted_status', 'quoted_status_id', 'quoted_status_id_str', 'retweet_count',
                  'retweeted', 'retweeted_status', 'scopes', 'source', 'truncated', 'urls',
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
                        text = str(tweet.get(key, None))
                        if text is None:
                            file.write('None')
                        elif text.lower() in ['nan', 'none', 'n\\a']:
                            file.write('None')
                        else:
                            for char in ['\n', ';', '\r']:
                                text = text.replace(char, ' ')
                            file.write(text)

                    except UnicodeEncodeError:
                        self.logger.error(f"UnicodeError while saving:")
                        self.logger.error(f"'{tweet}'")
                        file.write('UnicodeEncodeError')

                    if i < len(header)-1:
                        file.write(';')
                file.write('\n')
            return True
        except PermissionError:
            th = threading.Thread(
                target=lambda: Analyzer.export_tweet_to_database(Analyzer(), _data_dir, tweet, filename, 15)
            )
            th.start()
            self.logger.error(f"Permission error: {filename}, created background thread to save data")
            return None

    def filter_by_existing_key(self, key, inverted=False):  # Fix exceptions, bool type
        if not key or key == '' or key not in self.DF.keys():
            self.logger.warning('Invalid key to filter.')
            return False
        df = self.DF
        if df is None:
            return False

        if inverted:
            df = df.loc[(df[key] is None) | (df[key] == 0) | (df[key] == 'None')]
        else:
            df = df.loc[(df[key] is not None) & (df[key] != 0) & (df[key] != 'None')]

        if self.filter_conditions(df):
            self.logger.debug(f"Successfully filtered by existing key: {key}")
            self.DF = df
            return True
        else:
            return False

    def filter_conditions(self, df):
        if df.shape[0] > 0 and df.shape != self.DF.shape:
            return True
        elif df.shape[0] > 0:
            self.logger.debug('DF size is the same.')
            return False
        else:
            self.logger.debug('DF is empty.')
            return False

    def filter_df_by_lang(self, lang, inverted=False):
        lang = str(lang)
        if self.DF is not None:
            if inverted:
                df = self.DF.loc[lambda _df: _df['lang'] != lang]
            else:
                df = self.DF.loc[lambda _df: _df['lang'] == lang]

            if self.filter_conditions(df):
                self.DF = df
                self.logger.debug(f"Successfully filtered by language: {lang}")
                return True
        else:
            self.logger.warning('DF is empty. Load some tweets first.')

    def filter_df_search_phrases(self, words, only_in_text=True, inverted=False):
        if self.DF is None:
            self.logger.warning('DF is empty. Load some tweets first.')
            return False

        if only_in_text:
            method = Analyzer.check_series_words_in_text
        else:
            method = Analyzer.check_series_words_anywhere
        stages = re.split(';', words)  # Separating stages
        df = self.DF

        for filtration_stage in stages:
            self.logger.debug(f"Filtering df with phrases: {filtration_stage}, method: {method}")
            df = df.loc[lambda _df: method(_df, filtration_stage, inverted=inverted)]

        if self.filter_conditions(df):
            self.DF = df
            self.logger.debug(f"Successfully filtered tweets by phrases")
            return True

    def filter_df_by_timestamp(self, time_stamp_min, time_stamp_max):
        if self.DF is not None:
            df = self.DF.loc[lambda _df: self.check_series_time_condition(
                _df['created_at'],
                time_stamp_min,
                time_stamp_max)]
            if self.filter_conditions(df):
                self.DF = df
                self.logger.debug(f"Successfully filtered tweets in time range")
                return True
        else:
            self.logger.warning('DF is empty. Load some tweets first.')

    def filter_df_by_tweet_id(self, tweet_id, inverted=False):
        try:
            tweet_id = int(tweet_id)
        except ValueError as ve:
            self.logger.warning(f"Invalid Tweet id. {ve}")
            return None

        if self.DF is not None:
            if inverted:
                df = self.DF.loc[lambda _df: _df['id'] != tweet_id]
            else:
                df = self.DF.loc[lambda _df: _df['id'] == tweet_id]

            if self.filter_conditions(df):
                self.DF = df
                self.logger.debug(f"Successfully filtered tweets by tweet_id: {tweet_id}")
                return True
        else:
            self.logger.warning('DF is empty. Load some tweets first.')

    def filter_df_by_user(self, user_text, inverted=False):
        if self.DF is not None:
            df = self.DF.loc[lambda _df: self.check_series_user_text(_df, user_text, inverted=inverted)]
            if self.filter_conditions(df):
                self.DF = df
                self.logger.debug(f"Successfully filtered tweets by user data: {user_text}")
                return True
        else:
            self.logger.warning('DF is empty. Load some tweets first.')

    def find_local_tweets(self, path=None):
        """Find local tweets files"""
        if path:
            path = os.path.abspath(path)
        else:
            path = self._data_dir
        files = glob.glob(os.path.join(path, 'Tweets*.csv'))
        return files

    def find_parent_tweets(self, retweets=True, quoted=True):
        """Method will search quoted status ids and retweets id in current DF"""
        if self.DF is None:
            self.logger.warning("Load DF first")
            return False
        parent_ids = []

        if quoted:  # Search parents in quoted tweets
            for tweet in self.DF['quoted_status_id']:
                if tweet != "None":
                    parent_ids.append(tweet)

        if retweets:  # Search parents in retweets
            for tweet in self.DF['retweeted_status']:
                if tweet != 'None':
                    tweet_dict = ast.literal_eval(tweet)
                    parent_ids.append(tweet_dict['id'])

        return parent_ids

    def get_distinct_values_from_df(self, key):
        """Retrieve unique values from currently loaded DF"""
        if self.DF is None:
            return None
        if key not in self.DF:
            return None

        unique = self.DF[key].unique()
        return unique

    def fork_method(self, method_to_fork, *args, **kwargs):
        self.logger.debug(f"Forking '{method_to_fork}'")
        subprocess = threading.Thread(target=lambda: method_to_fork(*args, **kwargs))
        subprocess.__name__ = f'Thread #{self.th_num} ' + method_to_fork.__name__
        subprocess.start()
        self.threads += [subprocess]
        self.th_num += 1
        return subprocess

    def load_df(self, file_list):
        if type(file_list) is str:
            file_list = [file_list]
        valid_load = True
        self.DF = None
        self.loaded_to_DF = []
        for file in file_list:
            if os.path.isabs(file):
                file_path = file
            else:
                file_path = os.path.abspath(os.path.join(self._data_dir, file))
            try:
                self.logger.info(f"Loading: {file}")
                df = pd.read_csv(str(file_path), sep=';', encoding='utf8')
            except ParserError as pe:
                self.logger.error(f"Pandas Error: Can not load this file {file}.{pe}")
                valid_load = False
                continue

            except UnicodeDecodeError as ue:
                self.logger.error(f"Decode Error in file: {file}. {ue}")
                valid_load = False
                continue

            self.loaded_to_DF += [file]
            if self.DF is None:
                self.DF = df
            else:
                self.DF = pd.concat([self.DF, df], ignore_index=True)
        return valid_load

    def merge_without_duplicates(self, files, output_filename=None):
        if not output_filename:
            default_name = 'Auto_Merge' + '_' + self.now_as_text()
            file_with_ext = default_name + '.csv'
        else:
            file_with_ext = output_filename + '.csv'

        app = Analyzer()
        valid = app.load_df(files)
        if valid:
            resp = app.drop_duplicates_from_df()
        if valid and resp is not False:  # If drop duplicates fails, process further anyway
            if output_filename:
                valid = app.save_current_df(full_name=output_filename)
            else:
                valid = app.save_current_df(full_name=default_name)
        if valid:  # Delete only if chain is valid
            for curr_file in files:
                if file_with_ext == curr_file:
                    self.logger.warning(f"File names are the same! Not deleting: {curr_file}")
                    continue
                curr_file_path = os.path.join(self._data_dir, curr_file)
                try:
                    os.remove(curr_file_path)
                    self.logger.debug(f"Removed this file: {curr_file_path}")
                except PermissionError:
                    self.logger.error(f"Can not remove: {curr_file_path}")

    @staticmethod
    def now_as_text():
        now = datetime.datetime.now()
        text = f'{now.year}'.rjust(4, '0') \
               + f'{now.month}'.rjust(2, '0') \
               + f'{now.day}'.rjust(2, '0') \
               + '_' + f'{now.hour}'.rjust(2, '0') \
               + '-' + f'{now.minute}'.rjust(2, '0') \
               + '-' + f'{now.second}'.rjust(2, '0')
        return text

    def reload_df(self):
        self.DF = None
        text = 'Reloading Tweets:'
        if not self.loaded_to_DF:
            self.logger.warning('Never loaded anything!')
            return False

        for file in self.loaded_to_DF:
            file_path = os.path.join(self._data_dir, file)
            try:
                df = pd.read_csv(file_path, sep=';', encoding='utf8')
                text += f'\n{file}'
                if self.DF is None:
                    self.DF = df
                else:
                    self.DF = pd.concat([self.DF, df], ignore_index=True)
            except FileNotFoundError:
                self.logger.error(f'Can not reload missing file: {file}')
                continue
        self.logger.info(text)

    def save_current_df(self, full_name=None, extra_text=None):
        if extra_text:
            text = extra_text
        else:
            text = 'DataFrame'
        text = text + '_' + self.now_as_text()

        if full_name:
            text = full_name

        file_path = os.path.join(self._data_dir, text + '.csv')
        valid = self.save_df(self.DF, file_path)
        return valid

    def save_df(self, df, file_path):
        if df is None:
            self.logger.warning('DF is empty!')
            return None
        else:
            saved = False
            with open(file_path, 'wt', encoding='utf8') as f:
                df.to_csv(f, sep=';', encoding='utf8', index=False)
                saved = True
            if saved:
                self.logger.info(f'Saved DF to file: {os.path.abspath(file_path)}')
                return True
            else:
                self.logger.error(f'Failed to save DF to file: {os.path.abspath(file_path)}')
                return False

    @staticmethod
    def timestamp_from_date(year=1990, month=1, day=1, hour=0, minute=0):
        # Get timestamp within days
        new_date = datetime.date(year=year, month=month, day=day)
        new_timestamp = calendar.timegm(new_date.timetuple())

        # Add minutes, hours, day offset and rest from timestamp
        return new_timestamp + minute * 60 + hour * 3600

    @staticmethod
    def timestamp_offset(timestamp=None, year=0, month=0, day=0, hour=0, minute=0):
        if not timestamp:
            timestamp = int(datetime.datetime.now().timestamp())

        date = datetime.date.fromtimestamp(timestamp)
        date_rest = timestamp % (3600*24)  # Capture rest from day 3600 second * 24 hours

        year = year + date.year
        month = month + date.month

        # Keep month in <1,12> range
        while month < 1:
            month += 12
            year -= 1
        # Keep month in <1,12> range
        while month > 12:
            month -= 12
            year += 1

        # Get timestamp within days
        new_date = datetime.date(year=year, month=month, day=date.day)
        new_timestamp = calendar.timegm(new_date.timetuple())

        # Add minutes, hours, day offset and rest from timestamp
        return new_timestamp + minute*60 + hour*3600 + day*24*3600 + date_rest

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
    app = Analyzer(auto_login=False)
    app.load_df(['unittest_auto.csv'])
    app.filter_df_search_phrases(["tweet1"], only_in_text=True)
    # app.load_df(['Auto_Merge_20200308_21-31-23.csv'])
    # app.filter_df_search_phrases(["tweet1"], only_in_text=False)
    print('End...')
