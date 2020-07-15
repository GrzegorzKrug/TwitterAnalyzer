# application.py
# Grzegorz Krug

from PyQt5 import QtCore, QtWidgets  # QtGui

from twitter_analyzer.analyzer.tweet_operator import TwitterOperator
from twitter_analyzer.gui.gui import Ui_MainWindow
from twitter_analyzer.analyzer.custom_logger import define_logger
from analyzer.tasks import (
    download_parent_tweets, collect_status_list, export_tweets_to_csv
)

import numpy as np
import webbrowser
import datetime
import traceback
import sys
import os


class TwitterAnalyzerGUI(TwitterOperator, Ui_MainWindow):
    def __init__(self, main_window, auto_login=False):
        self.args = main_window, auto_login

        Ui_MainWindow.__init__(self)
        self.setupUi(main_window)
        TwitterOperator.__init__(self, auto_login=auto_login)

        self._init_triggers()
        self._init_settings()
        self._init_table_widget()
        self._loaded_files = []  # Last loaded files, for reloading
        self.current_tweet_selected = -1  # Current tweet index from DF

    def _init_triggers(self):
        self.actionLogin.triggered.connect(self.validate_credentials)
        self.actionWho_am_I.triggered.connect(self.show_me)
        self.actionTweet_Description.triggered.connect(self.show_tweet_keys)
        self.actionRestart.triggered.connect(lambda: self.__init__(*self.args))

        "Debug Actions"
        self.actionDebugUsers.triggered.connect(lambda: self.request_followers())

        'Requesting methods'
        self.pushButton_Request_Status.clicked.connect(self.request_status_from_box)
        self.pushButton_request_parent_tweets_from_df.clicked.connect(lambda: download_parent_tweets.delay(
                tweet_list=self.tweet_list
        ))
        self.pushButton_request_tweet_update.clicked.connect(lambda: collect_status_list.delay(
                tweet_list=self.tweet_list,
                overwrite=True
        ))

        'Settings'
        self.checkBox_wrap_console.clicked.connect(self.text_box_update_settings)
        self.checkBox_filtration_continuous.clicked.connect(self.update_chk_box_filtration)
        self.checkBox_filtration_keep_drop.clicked.connect(self.change_box_text)
        self.checkBox_show_only_text.clicked.connect(self.show_current_tweet)

        'File Buttons'
        self.pushButton_export_DF.clicked.connect(
                lambda: export_tweets_to_csv.delay(self.tweet_list, name=self.lineEdit_DF_comment.text()))

        'Displaying Tweets'
        self.pushButton_ShowTweetAll.clicked.connect(self.show_all_tweets)
        self.pushButton_ShowTweet.clicked.connect(self.show_current_tweet)
        self.pushButton_NextTweet.clicked.connect(self.show_next_tweet)
        self.pushButton_PreviousTweet.clicked.connect(self.show_prev_tweet)
        self.pushButton_JumpToTweet.clicked.connect(self.jump_to_tweet)
        self.pushButton_open_in_browser.clicked.connect(self.open_in_browser)
        # self.pushButton_drop_current_tweet.clicked.connect(self.trigger_drop_current_tweet)

        'WorkListManage'
        self.pushButton_add_to_work_list.clicked.connect(self.trigger_add_one_to_work_list)
        self.pushButton_drop_current_tweet.clicked.connect(self.trigger_drop_one_from_work_list)

        self.pushButton_drop_selection_from_WL.clicked.connect(lambda: self.drop_from_work_list(self.tweet_list))
        self.pushButton_add_selection_to_worklist.clicked.connect(lambda: self.add_to_work_list(self.tweet_list))

        self.pushButton_save_work_list.clicked.connect(self.save_list_as_work_list)
        self.pushButton_load_work_list.clicked.connect(self.trigger_load_work_list)
        self.pushButton_clear_work_list.clicked.connect(self.clear_work_list)

        'Filtration Buttons'
        self.pushButton_FilterDF_Lang_Polish.clicked.connect(lambda: self.trigger_filter_by_lang('pl'))
        self.pushButton_FilterDF_Lang_English.clicked.connect(lambda: self.trigger_filter_by_lang('en'))
        self.pushButton_FilterDF_Lang_Other.clicked.connect(self.trigger_filter_by_lang)
        self.pushButton_FilterDF_TweetID.clicked.connect(self.trigger_filter_by_tweet_id)
        self.pushButton_filter_by_Age.clicked.connect(self.trigger_filter_by_age)
        self.pushButton_filter_by_Date.clicked.connect(self.trigger_filter_by_date)
        self.pushButton_filter_search_words.clicked.connect(
                lambda: self.trigger_filter_by_search_words())
        self.pushButton_filter_search_words_anywhere.clicked.connect(
                lambda: self.trigger_filter_by_search_phrases())
        self.pushButton_find_retweets.clicked.connect(self.trigger_filter_retweets)
        self.pushButton_filter_quoted_tweets.clicked.connect(self.trigger_filter_quotes)

        'Time spinboxes'
        self.pushButton_reset_time.clicked.connect(self.time_spinboxes_reset_time)
        self.pushButton_set_current_time.clicked.connect(self.time_spinboxes_set_current_time)

        'Analyze Buttons'
        # self.pushButton_analyze_unique_vals.clicked.connect(self.trigger_analyze_unique)

        'Labeling'
        self.button_save_labeled_data.clicked.connect(self.trigger_save_labeled_data)
        self.button_load_labeled_data.clicked.connect(self.trigger_load_labeled_data)
        self.button_clear_labels_table.clicked.connect(self.dataset_clear_data)
        self.button_clear_selected_labels.clicked.connect(self.trigger_remove_selection_labeled_data)
        self.pushButton_add_label1.clicked.connect(lambda: self.dataset_add_row())
        self.pushButton_add_label2.clicked.connect(lambda: self.dataset_read_row(5))

    def _init_settings(self):
        self.text_box_update_settings()
        self.update_chk_box_filtration()

    def _init_table_widget(self):
        self.tableWidget_labeled_data.horizontalHeaderItem(0).setText("tweet_id")
        self.tableWidget_labeled_data.horizontalHeaderItem(1).setText("label")

    @staticmethod
    def add_timestamp_to_text(text):
        text = str(text)
        now = datetime.datetime.now()
        h = now.hour
        m = now.minute
        s = now.second
        timestamp = str(h).rjust(2, '0') + '-' + str(m).rjust(2, '0') + '-' + str(s).rjust(2, '0') + ': '
        return timestamp + text

    def check_filtration_settings(self):
        cont_checked = True if self.checkBox_filtration_continuous.checkState() == 2 else False
        keep_checked = True if self.checkBox_filtration_keep_drop.checkState() == 2 else False
        return cont_checked, keep_checked

    def change_box_text(self):
        checked = True if self.checkBox_filtration_keep_drop.checkState() == 2 else False
        if checked:
            self.checkBox_filtration_keep_drop.setText("Keep found")
        else:
            self.checkBox_filtration_keep_drop.setText("Drop found")

    def update_chk_box_filtration(self):
        """Enables child checkbox if this is enabled"""
        checked = True if self.checkBox_filtration_continuous.checkState() == 2 else False
        self.change_check_box_settings(checked)

    def change_check_box_settings(self, enable=True):
        """Turns on and off checkbox"""
        self.checkBox_filtration_keep_drop.setEnabled(enable)

    def text_box_update_settings(self):
        """
        Wrap text box if checkbox has tick
        Returns:

        """
        checked = True if self.checkBox_wrap_console.checkState() == 2 else False
        if checked:
            self.plainTextEdit_info.setLineWrapMode(QtWidgets.QPlainTextEdit.WidgetWidth)
        else:
            self.plainTextEdit_info.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)

    def display_add(self, text):
        old_text = self.plainTextEdit_info.toPlainText()
        text = old_text + '\n' + text
        self.plainTextEdit_info.setPlainText(text)

    def display(self, text):
        while len(text) > 1 and \
                (text[-1] == '\n'
                 or text[-1] == '\r'
                 or text[-1] == ' '):
            text = text[:-1]
        self.plainTextEdit_info.setPlainText(text)

    @staticmethod
    def _open_browser(url):
        webbrowser.open(url)
        return True

    def open_in_browser(self):
        if self.tweet_list:
            if 0 <= self.current_tweet_index < len(self.tweet_list):
                tweet = self.get_full_tweet(self.tweet_list[self.current_tweet_index])
                author = tweet.User.screen_name
                status_id = tweet.Tweet.tweet_id
                url = f'https://twitter.com/{author}/status/{status_id}'
                self.logger.debug(f"Starting browser: '{url}'")
                self.fork_method(self._open_browser, url)
            else:
                self.logger.warning(f"Can not open url, index error")
        else:
            self.logger.warning(f"Can not open url, tweet list is empty.")

    @staticmethod
    def post_action(method, next_method=None):
        """Wrapper to run method after first one"""

        def wrapper(*args, **kwargs):
            out = None
            if method:
                out = method(*args, **kwargs)
            if next_method:
                next_method()
            return out

        return wrapper

    @staticmethod
    def pop_window(text):
        """Window popup with customizable text"""
        if len(text) > 0:
            msg = QtWidgets.QMessageBox()
            msg.setText(text)
            msg.exec()

    def show_me(self):
        if self.me:
            text = f"Currently logged in as {self.me['screen_name']}({self.me['name']})"
        else:
            text = "Not having any information about you."
        self.pop_window(text)

    def show_all_tweets(self):
        tweets = self.get_all_tweets()
        valid = self.set_tweet_list(tweets)
        if not valid:
            self.pop_window("New list is empty")
        self.show_current_tweet()

    def show_current_tweet(self):
        ind = self.current_tweet_index
        self.display_full_tweet(ind)

    def show_next_tweet(self):
        self.current_tweet_index += 1
        self.show_current_tweet()

    def jump_to_tweet(self):
        self.current_tweet_index = self.lineEdit_JumpToTweet.text()
        self.show_current_tweet()

    def show_prev_tweet(self):
        self.current_tweet_index -= 1
        self.show_current_tweet()

    def trigger_add_one_to_work_list(self):
        try:
            self.add_to_work_list(self.tweet_list[self.current_tweet_index])
            self.tweet_list.pop(self.current_tweet_index)
        except IndexError:
            pass
        self.show_current_tweet()

    def trigger_drop_one_from_work_list(self):
        try:
            self.drop_from_work_list(self.tweet_list[self.current_tweet_index])
            self.tweet_list.pop(self.current_tweet_index)
        except IndexError:
            pass
        self.show_current_tweet()

    def trigger_load_work_list(self):
        """
        Loads list from work list and displays tweet
        Returns:

        """
        self.load_list_from_work_list()
        self.current_tweet_index = 0
        self.show_current_tweet()

    def display_full_tweet(self, ind):
        try:
            ind = int(ind)
        except ValueError:
            self.logger.error(f"Can not show tweet, this is not number {ind}")
            return None
        if len(self.tweet_list) < 1:
            self.logger.warning(f"Tweet list is empty. Can not display tweet")
            return None

        flag_hide_empty = True if self.checkBox_HideEmptyValues.checkState() == 2 else False
        flag_short_user = True if self.checkBox_DisplayShortUserinfo.checkState() == 2 else False
        flag_short_quote = True if self.checkBox_DisplayShortQuoteStatus.checkState() == 2 else False
        flag_text_only = True if self.checkBox_show_only_text.checkState() == 2 else False

        if ind < 0:
            ind = 0
        elif ind >= len(self.tweet_list):
            ind = len(self.tweet_list) - 1

        self.current_tweet_index = ind
        tweet = self.get_full_tweet(self.tweet_list[ind])
        tweet_full_text = tweet.Tweet.full_text.replace('\n', '')

        text = f"Index: {ind} of {len(self.tweet_list) - 1}\n"
        if flag_text_only:
            text += "id:".ljust(8) + f"{tweet.Tweet.tweet_id}\n"
            text += f"{tweet_full_text}\n"
        else:
            text += "id".ljust(25) + f"{tweet.Tweet.tweet_id}\n"
            text += "timestamp".ljust(25) + f"{tweet.Tweet.timestamp}\n"
            text += "contributors".ljust(25) + f"{tweet.Tweet.contributors}\n"
            text += "coordinates".ljust(25) + f"{tweet.Tweet.coordinates}\n"
            text += "created_at".ljust(25) + f"{tweet.Tweet.created_at}\n"
            text += "current_user_retweet".ljust(25) + f"{tweet.Tweet.current_user_retweet}\n"
            text += "favorite_count".ljust(25) + f"{tweet.Tweet.favorite_count}\n"
            text += "favorited".ljust(25) + f"{tweet.Tweet.favorited}\n"
            text += "hashtags".ljust(25) + f"{tweet.Tweet.hashtags}\n"
            text += "in_reply_to_status_id".ljust(25) + f"{tweet.Tweet.in_reply_to_status_id}\n"
            text += "in_reply_to_user_id".ljust(25) + f"{tweet.Tweet.in_reply_to_user_id}\n"
            text += "location".ljust(25) + f"{tweet.Tweet.location}\n"
            text += "lang".ljust(25) + f"{tweet.Tweet.lang}\n"
            text += "quoted_status_id".ljust(25) + f"{tweet.Tweet.quoted_status_id}\n"
            text += "retweet_count".ljust(25) + f"{tweet.Tweet.retweet_count}\n"
            text += "retweeted_status_id".ljust(25) + f"{tweet.Tweet.retweeted_status_id}\n"
            text += "source_status_id".ljust(25) + f"{tweet.Tweet.source_status_id}\n"
            text += "user_id".ljust(25) + f"{tweet.Tweet.user_id}\n"
            text += "user_mentions".ljust(25) + f"{tweet.Tweet.user_mentions}\n"
            text += "screen_name".ljust(25) + f"{tweet.User.screen_name}\n"
            text += "full_text".ljust(25) + f"{tweet_full_text}\n"
        self.display(text)

    def dataset_add_row(self, tweet_id=0, label=0):
        row_id = self.tableWidget_labeled_data.rowCount()
        self.tableWidget_labeled_data.insertRow(row_id)
        self.dataset_set_row(row_id, tweet_id, label)

    def dataset_set_row(self, row_id, tweet_id, label):
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_labeled_data.setItem(row_id, 0, item)
        item.setText(f"{tweet_id}")

        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_labeled_data.setItem(row_id, 1, item)
        item.setText(f"{label}")

        self.tableWidget_labeled_data.selectRow(row_id)

    def trigger_remove_selection_labeled_data(self):
        sel = self.tableWidget_labeled_data.selectedIndexes()
        to_remove = list(set(ob.row() for ob in sel))
        to_remove.sort(reverse=True)
        self.logger.info(f"Deleting table indexes: {to_remove}")
        for num in to_remove:
            self.data_set_remove_row(num)

    def data_set_remove_row(self, row):
        self.tableWidget_labeled_data.removeRow(row)

    def trigger_save_labeled_data(self):
        f_name = "labels"
        data = [(tweet, label) for tweet, label in self.dataset_read_all_rows()]
        np.save(f_name, data)

    def trigger_load_labeled_data(self):
        f_name = "labels.npy"
        if os.path.isfile(f_name):
            data = np.load(f_name, allow_pickle=True)
            self.dataset_clear_data()

            for num, label in data:
                self.dataset_add_row(num, label)
        else:
            self.logger.warning(f"Can not load labels, file not found")

    def dataset_clear_data(self):
        self.tableWidget_labeled_data.clearContents()
        self.tableWidget_labeled_data.setRowCount(0)

    def dataset_read_all_rows(self):
        for row_id in range(self.tableWidget_labeled_data.rowCount()):
            yield self.dataset_read_row(row_id)

    def dataset_read_row(self, row_id):
        try:
            item1 = self.tableWidget_labeled_data.item(row_id, 0)
            item2 = self.tableWidget_labeled_data.item(row_id, 1)

            t1 = item1.text()
            t2 = item2.text()
            return t1, t2

        except AttributeError as ae:
            self.logger.error(f"{ae}")
            return None, None

    def request_status_from_box(self):
        """
        Collect one ore more tweets with specified ids
        Returns:

        """
        text = self.lineEdit_request_statusId.text()
        try:
            num = int(text)
        except ValueError:
            msg = f"Can not request tweet, this is not number '{text}'"
            self.pop_window(msg)
            self.logger.error(msg)
            return None
        collect_status_list.delay([num])

    # def trigger_analyze_unique(self):
    #     key = self.lineEdit_analyze_unique_key.text()
    #     unique = self.get_distinct_values_from_df(key)
    #     text = f"Unique values [{key}]:\n"
    #     if unique is None:
    #         return False
    #     else:
    #         for val in unique:
    #             text += f"'{val}'\n"
    #     print(f"'{text}'")
    #     self.display(text)

    #
    # def trigger_drop_new_duplicates(self):
    #     valid = self.drop_duplicates_from_df(keep_new=False)
    #     if valid:
    #         self.currTweetDF_ind = 0
    #         self.show_current_tweet_from_df()
    #
    # def trigger_drop_old_duplicates(self):
    #     valid = self.drop_duplicates_from_df(keep_new=True)
    #     if valid:
    #         self.currTweetDF_ind = 0
    #         self.show_current_tweet_from_df()

    def trigger_filter_by_age(self):
        """Function is reading input from gui spinboxes and translates it to timestamp, later calls filtration"""
        try:
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

            if timestamp_min > timestamp_max:
                timestamp_max, timestamp_min = timestamp_min, timestamp_max

            tweets = self.filter_tweets_by_timestamp(timestamp_min, timestamp_max)
            cont, keep = self.check_filtration_settings()
            valid = self.set_tweet_list(tweets, continuous=cont, keep_found=keep)
            if not valid:
                self.pop_window("New list is empty")
            self.show_current_tweet()

        except ValueError as ve:
            self.pop_window(str(ve))
            self.logger.error(str(ve))

    def trigger_filter_by_date(self):
        try:
            timezone = int(self.spinBox_timezone.value())

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

            timestamp_min -= (timezone + 1) * 3600  # offset to match twitter time
            timestamp_max -= (timezone + 1) * 3600  # offset to match twitter time

            if timestamp_min > timestamp_max:
                timestamp_max, timestamp_min = timestamp_min, timestamp_max

            tweets = self.filter_tweets_by_timestamp(timestamp_min, timestamp_max)
            cont, keep = self.check_filtration_settings()
            valid = self.set_tweet_list(tweets, continuous=cont, keep_found=keep)
            if not valid:
                self.pop_window("New list is empty")
            self.show_current_tweet()

        except ValueError as ve:
            self.pop_window(f"{ve}")
            self.logger.error(f"Value Error: {ve}")

    def time_spinboxes_set_current_time(self):
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        day = now.day
        hour = now.hour
        minute = now.minute

        self.spinBox_timefilter_from_year.setValue(year)
        self.spinBox_timefilter_from_month.setValue(month)
        self.spinBox_timefilter_from_day.setValue(day)
        self.spinBox_timefilter_from_hour.setValue(hour)
        self.spinBox_timefilter_from_min.setValue(minute)

        self.spinBox_timefilter_to_year.setValue(year)
        self.spinBox_timefilter_to_month.setValue(month)
        self.spinBox_timefilter_to_day.setValue(day)
        self.spinBox_timefilter_to_hour.setValue(hour)
        self.spinBox_timefilter_to_min.setValue(minute)

    def time_spinboxes_reset_time(self):
        self.spinBox_timefilter_from_year.setValue(0)
        self.spinBox_timefilter_from_month.setValue(0)
        self.spinBox_timefilter_from_day.setValue(0)
        self.spinBox_timefilter_from_hour.setValue(0)
        self.spinBox_timefilter_from_min.setValue(0)

        self.spinBox_timefilter_to_year.setValue(0)
        self.spinBox_timefilter_to_month.setValue(0)
        self.spinBox_timefilter_to_day.setValue(0)
        self.spinBox_timefilter_to_hour.setValue(0)
        self.spinBox_timefilter_to_min.setValue(10)

    def trigger_filter_by_lang(self, lang=None):
        if not lang:
            lang = self.lineEdit_FilterLangOther.text()
            lang = str(lang)
        if lang == '':
            self.logger.error('Lang box is empty!')
            return None
        tweets = self.get_tweets_by_lang(lang)
        cont, keep = self.check_filtration_settings()
        valid = self.set_tweet_list(tweets, continuous=cont, keep_found=keep)
        if not valid:
            self.pop_window("New list is empty")
        self.show_current_tweet()

    # def trigger_filter_by_non_empty_key(self):
    #     text = self.lineEdit_filterKeyinput.text()
    #     inverted = self.check_settings_inverted()
    #     valid = self.filter_by_existing_key(text, inverted=inverted)
    #     if valid:
    #         self.currTweetDF_ind = 0
    #         self.show_current_tweet_from_df()

    def trigger_filter_by_search_words(self):
        words = self.lineEdit_filter_words.text()
        case_sens = True if self.checkBox_case_sensitivity.checkState() == 2 else False
        tweets = self.get_tweets_by_words(words, case_sens=case_sens)
        cont, keep = self.check_filtration_settings()
        valid = self.set_tweet_list(tweets, continuous=cont, keep_found=keep)
        if not valid:
            self.pop_window("New list is empty")
        self.show_current_tweet()

    def trigger_filter_by_search_phrases(self):
        phrase = self.lineEdit_filter_words.text()
        case_sens = True if self.checkBox_case_sensitivity.checkState() == 2 else False
        tweets = self.get_tweets_by_phrases(phrase, case_sens=case_sens)
        cont, keep = self.check_filtration_settings()
        valid = self.set_tweet_list(tweets, continuous=cont, keep_found=keep)
        if not valid:
            self.pop_window("New list is empty")
        self.show_current_tweet()

    def trigger_filter_by_tweet_id(self):
        try:
            tweet_id = int(self.lineEdit_tweet_id.text())
        except ValueError:
            self.pop_window("This is not correct number")
            return None
        tweets = self.get_tweet_by_id(tweet_id)
        cont, keep = self.check_filtration_settings()
        valid = self.set_tweet_list(tweets, continuous=cont, keep_found=keep)
        if not valid:
            self.pop_window("New list is empty")
        self.show_current_tweet()

    def trigger_filter_retweets(self):
        tweets = self.get_retweets()
        cont, keep = self.check_filtration_settings()
        valid = self.set_tweet_list(tweets, continuous=cont, keep_found=keep)
        if not valid:
            self.pop_window("New list is empty")
        self.show_current_tweet()

    def trigger_filter_quotes(self):
        tweets = self.get_quotes()
        cont, keep = self.check_filtration_settings()
        valid = self.set_tweet_list(tweets, continuous=cont, keep_found=keep)
        if not valid:
            self.pop_window("New list is empty")
        self.show_current_tweet()

    # def trigger_filter_by_user(self):
    #     user_text = self.lineEdit_user_input.text()
    #     inverted = self.check_settings_inverted()
    #     valid = self.filter_df_by_user(user_text, inverted)
    #     if valid:
    #         self.currTweetDF_ind = 0
    #         self.show_current_tweet_from_df()

    # def trigger_merge_without_duplicates(self):
    #     files = self.current_tree_selection()
    #     self.fork_method(self.merge_without_duplicates, files)

    def validate_credentials(self):
        valid = self.verify_procedure()
        if valid:
            self.logger.info(f"Credentials are valid")
        else:
            self.logger.info(f"Credentials are invalid")

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


# if QtCore.QT_VERSION >= 0x50501:  # Showing traceback from crashes
#     def except_hook(type_, value, traceback_):
#         traceback.print_exception(type_, value, traceback_)
#         QtCore.qFatal('')


except_logger = define_logger('App_exception')


def _except_handler(type=None, value=None, tb=None):
    frames = traceback.extract_tb(tb)
    text = "\n"
    for frame in frames:
        text += f"\n {frame}"
    except_logger.exception(f"Uncaught exception: {value}, traceback: {text}")


def run_gui():
    ui = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    app = TwitterAnalyzerGUI(main_window, auto_login=False)
    # ui.setupUi(MainWindow)  # moved to class init
    error_dialog = QtWidgets.QErrorMessage()
    main_window.show()
    sys.exit(ui.exec_())


if __name__ == "__main__":
    # sys.excepthook = _except_handler
    run_gui()
