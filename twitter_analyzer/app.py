# app.py
# Grzegorz Krug

from PyQt5 import QtCore, QtWidgets  # QtGui
from twitter_analyzer.analyzer.analyzer import Analyzer
# from twitter_analyzer.analyzer.twitter_api import TwitterApi
from twitter_analyzer.gui.gui import Ui_MainWindow

import webbrowser
import datetime
import traceback
import sys
import os
import ast
import pandas as pd
import time


class TwitterAnalyzerGUI(Analyzer, Ui_MainWindow):
    def __init__(self, main_window, auto_login=False):
        Ui_MainWindow.__init__(self)
        self.setupUi(main_window)
        Analyzer.__init__(self, auto_login=auto_login)

        self._init_wrappers()
        self._init_triggers()
        self._init_settings()
        self.refresh_gui()

        self._loaded_files = []  # Last loaded files, for reloading
        self.currTweetDF_ind = -1  # Current tweet index from DF

    def _init_triggers(self):
        self.actionLogin.triggered.connect(self.login_to_twitter_ui)
        self.actionWho_am_I.triggered.connect(self.pop_window)
        self.actionRefresh_GUI.triggered.connect(self.refresh_gui)
        self.actionTweet_Description.triggered.connect(self.show_tweet_keys)

        # self.label_login_status.mousePressEvent = self.update_status

        'Requesting methods'
        self.pushButton_collect1.clicked.connect(lambda: self.fork_method(self.download_full_chunk))
        self.pushButton_collect10.clicked.connect(lambda f: self.fork_method(self.download10_chunks))
        self.pushButton_Request_Status.clicked.connect(self.request_status_from_box)
        self.pushButton_request_parent_tweets_from_files.clicked.connect(lambda: self.fork_method(
            method_to_fork=self.download_parent_tweets,
            file_list=self.current_tree_selection()
        ))
        self.pushButton_request_parent_tweets_from_df.clicked.connect(lambda: self.fork_method(
            method_to_fork=self.download_parent_tweets,
            df=self.DF
        ))

        'Settings'
        self.checkBox_wrap_console.clicked.connect(self.change_info_settings)
        self.checkBox_filtration_keep_drop.clicked.connect(self.change_box_text)

        'Buttons'
        self.pushButton_load_selected_csv.clicked.connect(self.load_selected)
        self.pushButton_load_selected_csv_2.clicked.connect(self.load_selected)
        self.pushButton_clear_log.clicked.connect(self.clear_log)
        self.pushButton_delete100.clicked.connect(lambda: self.delete_less(100))
        self.pushButton_delete500.clicked.connect(lambda: self.delete_less(500))
        self.pushButton_deleteSelected.clicked.connect(self.delete_selected)
        self.pushButton_merge_selected.clicked.connect(self.merge_selected)
        self.pushButton_export_DF.clicked.connect(lambda: self.save_current_df(self.lineEdit_DF_comment.text()))
        self.pushButton_Info_screenLog.clicked.connect(self.copy_info_to_logs)
        self.pushButton_showTweets.clicked.connect(self.show_df_info)
        self.pushButton_reload_DF.clicked.connect(self.reset_df)
        self.pushButton_check_threads.clicked.connect(self.check_threads)
        self.pushButton_open_in_browser.clicked.connect(self.open_in_browser)
        self.pushButton_merge_without_duplicates.clicked.connect(self.merge_without_duplicates_trigger)

        'Displaying Tweets'
        self.pushButton_ShowTweet.clicked.connect(self.show_current_tweet_from_df)
        self.pushButton_NextTweet.clicked.connect(self.show_next_tweet_from_df)
        self.pushButton_PreviousTweet.clicked.connect(self.show_prev_tweet_from_df)
        self.pushButton_JumpToTweet.clicked.connect(self.show_tweet_jump_to)
        self.pushButton_drop_current_tweet.clicked.connect(self.trigger_drop_current_tweet)

        'Filtration Buttons'
        self.pushButton_FilterDF_Lang_Polish.clicked.connect(lambda: self.trigger_filter_by_lang('pl'))
        self.pushButton_FilterDF_Lang_English.clicked.connect(lambda: self.trigger_filter_by_lang('en'))
        self.pushButton_FilterDF_Lang_Other.clicked.connect(self.trigger_filter_by_lang)
        self.pushButton_FilterDF_by_NonEmptyKey.clicked.connect(self.trigger_filter_by_non_empty_key)
        self.pushButton_FilterDF_TweetID.clicked.connect(self.trigger_filter_by_tweet_id)
        self.pushButton_filter_by_Age.clicked.connect(self.trigger_filter_by_age)
        self.pushButton_filter_by_Date.clicked.connect(self.trigger_filter_by_date)
        self.pushButton_filter_search_words.clicked.connect(
            lambda: self.trigger_filter_by_search_words(only_in_text=True))
        self.pushButton_filter_search_words_anywhere.clicked.connect(
            lambda: self.trigger_filter_by_search_words(only_in_text=False))
        self.pushButton_drop_new_duplicates.clicked.connect(self.trigger_drop_new_duplicates)
        self.pushButton_drop_old_duplicates.clicked.connect(self.trigger_drop_old_duplicates)
        self.pushButton_FilterDF_user.clicked.connect(self.trigger_filter_by_user)

        'Analyze Buttons'
        self.pushButton_analyze_unique_vals.clicked.connect(self.trigger_analyze_unique)

        'DEBUG'
        self.pushButton_Magic_Debug.clicked.connect(self.go_debug)

    def _init_wrappers(self):
        self.login_procedure = self.post_action(self.login_procedure, self.update_login_box)

    def _init_settings(self):
        self.change_info_settings()

    def go_debug(self):
        print(self.find_parent_tweets())

    def add_log(self, text_line):
        text_line = str(text_line)
        text = str(text_line) + '\n' + self.textEdit_log.toPlainText()
        text = self.add_timestamp_to_text(text)
        self.textEdit_log.setPlainText(text)

    @staticmethod
    def add_timestamp_to_text(text):
        text = str(text)
        now = datetime.datetime.now()
        h = now.hour
        m = now.minute
        s = now.second
        timestamp = str(h).rjust(2, '0') + '-' + str(m).rjust(2, '0') + '-' + str(s).rjust(2, '0') + ': '
        return timestamp + text

    @staticmethod
    def download_full_chunk():
        app = Analyzer(auto_login=True)
        app.collect_new_tweets(n=1, chunk_size=200, interval=0)

    def check_settings_inverted(self):
        return False if self.checkBox_filtration_keep_drop.checkState() == 2 else True

    def check_threads(self):
        threads = self.threads
        self.threads = []
        for th in threads:
            if th.isAlive():
                self.add_log(f'{th.__name__} is still alive')
                self.threads += [th]
            else:
                pass
                # self.add_log(f'{th.__name__} is finished, removing from list')

        if not self.threads:
            self.add_log(f'All tasks are complete')
            return False

    def change_box_text(self):
        checked = True if self.checkBox_filtration_keep_drop.checkState() == 2 else False
        if checked:
            self.checkBox_filtration_keep_drop.setText("Filtration: keep")
        else:
            self.checkBox_filtration_keep_drop.setText("Filtration: drop")

    def change_info_settings(self):
        checked = True if self.checkBox_wrap_console.checkState() == 2 else False
        if checked:
            self.plainTextEdit_info.setLineWrapMode(QtWidgets.QPlainTextEdit.WidgetWidth)
        else:
            self.plainTextEdit_info.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)

    def copy_info_to_logs(self):
        text = '=== Info:'
        for line in self.plainTextEdit_info.toPlainText().split('\n'):
            text += '\n\t' + line
        self.add_log(text)
        time.sleep(0.8)

    def clear_log(self):
        self.textEdit_log.setPlainText('')

    def current_tree_selection(self, ignore_name=False, ignore_extension=False):
        """Loads currently selected csv file from tree"""
        files_list = []
        selected_list = self.treeView.selectedIndexes()
        for i, item in enumerate(selected_list):
            if item.column() == 0:
                files_list += [item.data()]
        good_files = []
        for file in files_list:
            if file[-4:] == '.csv' or ignore_extension:
                good_files += [file]
            else:
                self.add_log("Invalid extension, not CSV: {}".format(file))
        return good_files

    def display_add(self, text):
        old_text = self.plainTextEdit_info.toPlainText()
        text = old_text + '\n' + text
        self.plainTextEdit_info.setPlainText(text)

    def display(self, text):
        while len(text) > 1 and\
                (text[-1] == '\n'
                 or text[-1] == '\r'
                 or text[-1] == ' '):
            text = text[:-1]
        self.plainTextEdit_info.setPlainText(text)

    def delete_selected(self):
        file_list = self.current_tree_selection(ignore_name=True, ignore_extension=True)
        if file_list is []:
            self.add_log('Make selection!')
            return None

        for f in file_list:
            try:
                os.remove(os.path.join(self._data_dir, f))
                self.add_log(f'Removed {f}')

            except PermissionError:
                self.add_log(f'PermissionError!!!: Close Files {f}')

    @staticmethod
    def download10_chunks():
        app = Analyzer(auto_login=True)
        app.collect_new_tweets(n=10, chunk_size=200, interval=60)

    @staticmethod
    def download_parent_tweets(file_list=None, df=None):
        if (file_list is None or file_list == []) and df is None:
            Analyzer().logger.error(f"Missing input, file_list: {file_list}, df: {df}")
            return None
        app = Analyzer(auto_login=False)
        if file_list:
            app.load_df(file_list)
        else:
            app.DF = df.copy()
        status_list = app.find_parent_tweets()
        app.collect_status(status_list=status_list, filename=f'Parent_{Analyzer.now_as_text()}')

    def load_selected(self):
        self.currTweetDF_ind = -1
        files = self.current_tree_selection()
        self.load_df(files)
        if self.DF is not None:
            self.currTweetDF_ind = 0
            self.show_current_tweet_from_df()

    def login_to_twitter_ui(self):
        valid = self.login_procedure()
        if valid:
            self.add_log(f"Credentials are valid")
        else:
            self.add_log(f"Credentials are invalid")

    def merge_selected(self):
        file_list = self.current_tree_selection()
        if not file_list:
            self.add_log('Error. Select files!')
            return None
        if len(file_list) <= 1:
            self.add_log('You can not merge this.')
            return None

        now = datetime.datetime.now()
        merged_file = 'merged_' \
                      + f'{now.year}'.rjust(4, '0') \
                      + f'{now.month}'.rjust(2, '0') \
                      + f'{now.day}'.rjust(2, '0') \
                      + '_' + f'{now.hour}'.rjust(2, '0') \
                      + '-' + f'{now.minute}'.rjust(2, '0') \
                      + '-' + f'{now.second}'.rjust(2, '0') \
                      + '.csv'

        file_path = os.path.join(self._data_dir, merged_file)
        with open(file_path, 'wt', encoding='utf8') as f:
            for i, file in enumerate(file_list):
                curr_file_path = os.path.join(self._data_dir, file)
                df = pd.read_csv(curr_file_path, sep=';', encoding='utf8')
                if i == 0:
                    df.to_csv(f, header=True, sep=';', encoding='utf8', index=False)
                else:
                    df.to_csv(f, header=False, sep=';', encoding='utf8', index=False)
                try:
                    os.remove(curr_file_path)
                except PermissionError:
                    self.add_log(f'Merged, but can not remove {file}')

        self.add_log(f'Merged to file: {merged_file}')

    def merge_without_duplicates_trigger(self):
        files = self.current_tree_selection()
        self.fork_method(self.merge_without_duplicates, files)

    def merge_without_duplicates(self, files):
        app = Analyzer()
        valid = app.load_df(files)
        if valid:
            resp = app.drop_duplicates_from_df()
        if valid and resp is not False:  # In case drop duplicates fails process further
            valid = app.save_current_df('Auto_Merge')
        if valid:  # Delete only if chain is valid
            for curr_file in files:
                curr_file_path = os.path.join(self._data_dir, curr_file)
                try:
                    os.remove(curr_file_path)
                except PermissionError:
                    self.add_log(f'Merged, but can not remove {curr_file_path}')

    def open_in_browser(self):
        if self.DF is not None:
            if 0 <= self.currTweetDF_ind < len(self.DF):
                tweet = self.DF.iloc[self.currTweetDF_ind]
                # author = tweet['user']
                author = ast.literal_eval(tweet['user'])['screen_name']
                status_id = tweet['id']
                url = f'https://twitter.com/{author}/status/{status_id}'
                self.fork_method(self._open_browser, url)

    @staticmethod
    def _open_browser(url):
        webbrowser.open(url)
        return True

    @staticmethod
    def post_action(method, next_method=None):
        def wrapper(*args, **kwargs):
            out = None
            if method:
                out = method(*args, **kwargs)
            if next_method:
                next_method()
            return out
        return wrapper

    def pop_window(self):
        msg = QtWidgets.QMessageBox()
        if self.me:
            msg.setText('Currently logged in as {} ({}).'
                        .format(self.me['screen_name'], self.me['name']))
        else:
            msg.setText('Currently not logged in.')
        msg.exec()

    def print_tweet_to_info(self, ind):
        try:
            ind = int(ind)
        except ValueError:
            self.add_log('This is not a number')
            return None
        flag_hide_empty = True if self.checkBox_HideEmptyValues.checkState() == 2 else False
        flag_short_user = True if self.checkBox_DisplayShortUserinfo.checkState() == 2 else False
        flag_short_quote = True if self.checkBox_DisplayShortQuoteStatus.checkState() == 2 else False
        if ind < 0 or ind >= len(self.DF):
            self.add_log(f'Index is not correct!')
            return None
        self.currTweetDF_ind = ind

        text = f'Tweet index: {self.currTweetDF_ind} / {len(self.DF) - 1}\n'
        for key, value in self.DF.iloc[self.currTweetDF_ind].items():
            if "str" in key:
                continue
            value_is_none = value == 0 or value == "0" or value == "none" or value == "None"
            if flag_hide_empty and value_is_none:
                continue
            if value_is_none:
                text += f'{key}:'.ljust(25) + f'{value}\n'
                continue

            if key == "user" and flag_short_user:
                user_dict = ast.literal_eval(value)
                text += f'{key}:'.ljust(25) + ''.join([f"{deep_key}: {deep_val}, ".replace('\n', '') if deep_key in [
                    "id",
                    "name",
                    "screen_name",
                    "location",
                    "favourites_count"]
                                                       else "" for deep_key, deep_val in user_dict.items()])
            elif (key == "quoted_status" or key == "retweeted_status") and flag_short_quote:
                user_dict = ast.literal_eval(value)
                text += f'{key}:'.ljust(25) + ''.join(
                    [f"{deep_key}: {deep_val}, ".replace('\n', '') if deep_key in [
                        "id",
                        "full_text"]
                     else "" for deep_key, deep_val in user_dict.items()])
            else:
                text += f'{key}:'.ljust(25) + f'{value}\n'
        self.display(text)

    def refresh_gui(self):
        self.show_tree()

    def reset_df(self):
        """Loads last used files"""
        self.reload_df()
        self.currTweetDF_ind = 0
        self.show_current_tweet_from_df()

    def request_status_from_box(self):
        text = self.lineEdit_request_statusId.text()
        try:
            num = int(text)
        except ValueError:
            self.add_log('This is not a number')
            return None
        self.collect_status([num])

    def show_tree(self):
        path = self._data_dir
        model = QtWidgets.QFileSystemModel()
        model.setRootPath(path)
        self.treeView.setModel(model)
        self.treeView.setRootIndex(model.index(path))
        self.treeView.setColumnWidth(0, 40*8)
        self.treeView.setColumnWidth(1, 10*8)
        self.treeView.setColumnWidth(2, 10*8)
        self.treeView.setColumnWidth(3, 15*8)
        # self.treeView.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)  # its defined in GUI.py

    def show_df_info(self):
        if self.DF is None:
            self.add_log('DF is None!')
            return None
        else:
            self.display(f'DF size: {self.DF.shape}')
            self.display_add(str(self.DF.head()))

    def show_tweet_jump_to(self):
        if self.DF is None:
            self.add_log('DF not loaded!')
            return None
        ind_str = self.lineEdit_JumpToTweet.text()
        self.print_tweet_to_info(ind_str)

    def show_current_tweet_from_df(self):
        if self.DF is None:
            self.add_log('DF not loaded!')
            return None
        if self.currTweetDF_ind < 0:
            self.currTweetDF_ind = 0
        elif self.currTweetDF_ind >= len(self.DF):
            self.currTweetDF_ind = len(self.DF) - 1

        self.print_tweet_to_info(self.currTweetDF_ind)

    def show_next_tweet_from_df(self):
        if self.DF is None:
            self.add_log('DF not loaded!')
            return None
        self.currTweetDF_ind += 1
        if self.currTweetDF_ind < 0 or self.currTweetDF_ind >= len(self.DF):
            self.currTweetDF_ind = 0  # First Tweet index

        self.print_tweet_to_info(self.currTweetDF_ind)

    def show_prev_tweet_from_df(self):
        if self.DF is None:
            self.add_log('DF not loaded!')
            return None
        self.currTweetDF_ind -= 1
        if self.currTweetDF_ind < 0:
            self.currTweetDF_ind = len(self.DF)-1  # Last Tweet index
        elif self.currTweetDF_ind >= len(self.DF):
            self.currTweetDF_ind = 0

        self.print_tweet_to_info(self.currTweetDF_ind)

    def show_user_info(self, user_data):
        text = ''
        for key in ['screen_name', 'name', 'id', 'friends_count', 'followers_count', 'following', 'location',
                    'verified', 'lang']:
            text += str(key + ':').ljust(25) + str(user_data[key]) + '\n'
        self.display(text)

    def trigger_analyze_unique(self):
        key = self.lineEdit_analyze_unique_key.text()
        unique = self.get_distinct_values_from_df(key)
        text = f"Unique values [{key}]:\n"
        if unique is None:
            return False
        else:
            for val in unique:
                text += f"'{val}'\n"
        print(f"'{text}'")
        self.display(text)

    def trigger_drop_current_tweet(self):
        self.drop_tweet_in_df(self.currTweetDF_ind)
        self.show_current_tweet_from_df()

    def trigger_drop_new_duplicates(self):
        valid = self.drop_duplicates_from_df(keep_new=False)
        if valid:
            self.currTweetDF_ind = 0
            self.show_current_tweet_from_df()

    def trigger_drop_old_duplicates(self):
        valid = self.drop_duplicates_from_df(keep_new=True)
        if valid:
            self.currTweetDF_ind = 0
            self.show_current_tweet_from_df()

    def trigger_filter_by_age(self):
        """Function is reading input from gui spinboxes and translates it to timestamp, later calls filtration"""
        year = self.spinBox_timefilter_from_year.value()
        month = self.spinBox_timefilter_from_month.value()
        day = self.spinBox_timefilter_from_day.value()
        hour = self.spinBox_timefilter_from_hour.value()
        minute = self.spinBox_timefilter_from_min.value()
        timestamp_min = self.timestamp_offset(year=-year, month=-month, day=-day, hour=-hour, minute=-minute)

        year = self.spinBox_timefilter_to_year.value()
        month = self.spinBox_timefilter_to_month.value()
        day = self.spinBox_timefilter_to_day.value()
        hour = self.spinBox_timefilter_to_hour.value()
        minute = self.spinBox_timefilter_to_min.value()
        timestamp_max = self.timestamp_offset(year=-year, month=-month, day=-day, hour=-hour, minute=-minute)

        valid = self.filter_df_by_timestamp(timestamp_min, timestamp_max)
        if valid:
            self.currTweetDF_ind = 0
            self.show_current_tweet_from_df()

    def trigger_filter_by_date(self):
        try:
            year = self.spinBox_timefilter_from_year.value()
            month = self.spinBox_timefilter_from_month.value()
            day = self.spinBox_timefilter_from_day.value()
            hour = self.spinBox_timefilter_from_hour.value()
            minute = self.spinBox_timefilter_from_min.value()
            timestamp_min = self.timestamp_from_date(year=year, month=month, day=day, hour=hour, minute=minute)

            year = self.spinBox_timefilter_to_year.value()
            month = self.spinBox_timefilter_to_month.value()
            day = self.spinBox_timefilter_to_day.value()
            hour = self.spinBox_timefilter_to_hour.value()
            minute = self.spinBox_timefilter_to_min.value()
            timestamp_max = self.timestamp_from_date(year=year, month=month, day=day, hour=hour, minute=minute)

            valid = self.filter_df_by_timestamp(timestamp_min, timestamp_max)
            if valid:
                self.currTweetDF_ind = 0
                self.show_current_tweet_from_df()

        except ValueError as ve:
            self.add_log(f"Value Error: {ve}")

    def trigger_filter_by_non_empty_key(self):
        text = self.lineEdit_filterKeyinput.text()
        inverted = self.check_settings_inverted()
        valid = self.filter_by_existing_key(text, inverted=inverted)
        if valid:
            self.currTweetDF_ind = 0
            self.show_current_tweet_from_df()

    def trigger_filter_by_lang(self, lang=None):
        if not lang:
            lang = self.lineEdit_FilterLangOther.text()
            lang = str(lang)
        if lang == '':
            self.add_log('Box is empty!')
            return None
        inverted = self.check_settings_inverted()
        valid = self.filter_df_by_lang(lang, inverted=inverted)
        if valid:
            self.currTweetDF_ind = 0
            self.show_current_tweet_from_df()

    def trigger_filter_by_search_words(self, only_in_text=True):
        words = self.lineEdit_filter_words.text()
        inverted = self.check_settings_inverted()
        valid = self.filter_df_search_phrases(words, only_in_text=only_in_text, inverted=inverted)
        if valid:
            self.currTweetDF_ind = 0
            self.show_current_tweet_from_df()

    def trigger_filter_by_tweet_id(self):
        text = self.lineEdit_tweet_id.text()
        if len(text) < 0:
            self.add_log("This is not valid ID")
        inverted = self.check_settings_inverted()
        valid = self.filter_df_by_tweet_id(text, inverted=inverted)
        if valid:
            self.currTweetDF_ind = 0
            self.show_current_tweet_from_df()

    def trigger_filter_by_user(self):
        user_text = self.lineEdit_user_input.text()
        inverted = self.check_settings_inverted()
        valid = self.filter_df_by_user(user_text, inverted)
        if valid:
            self.currTweetDF_ind = 0
            self.show_current_tweet_from_df()

    def update_login_box(self):
        if self.logged_in:
            self.label_login_status.setText('True')
            self.label_login_status.setStyleSheet("background-color: rgb(30, 255, 180);")
            self.show_user_info(self.me)
        else:
            self.label_login_status.setText('False')
            self.label_login_status.setStyleSheet("background-color: rgb(255, 149, 151);\n"
                                                  "color: rgb(255, 255, 255);")

    def show_tweet_keys(self):
        text = 'Tweet index:             index / last tweet' \
               '\nid:                      tweet id' \
               '\ntimestamp:               time when tweet was collected' \
               '\ncontributors:            <help>' \
               '\ncoordinates:             <help>' \
               '\ncreated_at:              Tweet creation time' \
               '\ncurrent_user_retweet:    <help>' \
               '\nfavorite_count:          <help>' \
               '\nfavorited:               <help>' \
               '\nfull_text:               Tweet text' \
               '\ngeo:                     geolocation' \
               '\nhashtags:                hashtags used in tweet' \
               '\nid_str:                  tweetid string' \
               '\nin_reply_to_screen_name: <help>' \
               '\nin_reply_to_status_id:   <help>' \
               '\nin_reply_to_user_id:     <help>' \
               '\nlang:                    <help>' \
               '\nlocation:                <help>' \
               '\nmedia:                   <help>' \
               '\nplace:                   <help>' \
               '\npossibly_sensitive:      <help>' \
               '\nquoted_status:           <help>' \
               '\nquoted_status_id:        <help>' \
               '\nquoted_status_id_str:    <help>' \
               '\nretweet_count:           <help>' \
               '\nretweeted:               <help>' \
               '\nretweeted_status:        <help>' \
               '\nscopes:                  <help>' \
               '\nsource:                  <help>' \
               '\ntruncated:               <help>' \
               '\nurls:                    <help>' \
               '\nuser:                    <help>' \
               '\nuser_mentions:           <help>' \
               '\nwithheld_copyright:      <help>' \
               '\nwithheld_in_countries:   <help>' \
               '\nwithheld_scope:          <help>' \
               '\ntweet_mode:              <help>'
        self.display(text)
        
# ------ Sorted methods are above --------------------------------------------------------------------------------------


if QtCore.QT_VERSION >= 0x50501:  # Showing traceback from crashes
    def except_hook(type_, value, traceback_):
        traceback.print_exception(type_, value, traceback_)
        QtCore.qFatal('')
    sys.excepthook = except_hook


def run_gui():
    ui = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    app = TwitterAnalyzerGUI(main_window, auto_login=False)
    # ui.setupUi(MainWindow)  # moved to class init
    error_dialog = QtWidgets.QErrorMessage()
    main_window.show()
    sys.exit(ui.exec_())


if __name__ == "__main__":
    run_gui()