# _run_GUI_mode.py
# Grzegorz Krug
from PyQt5 import QtCore, QtWidgets # QtGui
from twitter_analyzer.analyzer.analyzer import Analyzer
# from twitter_analyzer.analyzer.twitter_api import TwitterApi
from twitter_analyzer.gui.gui import Ui_MainWindow

import webbrowser
import datetime
import threading
import traceback
import sys
import os
import ast
import pandas as pd
import time


class TwitterAnalyzerGUI(Analyzer, Ui_MainWindow):
    def __init__(self, mainWindow, autologin=False):
        Ui_MainWindow.__init__(self)
        self.setupUi(mainWindow)
        Analyzer.__init__(self, autologin=autologin, log_ui=self.log_ui)

        self._init_wrappers()
        self._init_triggers()
        self._init_settings()
        self.refresh_gui()

        self._loaded_files = []  # Last loaded files, for reloading
        self.threads = []  # Thread reference list
        self.th_num = 0  # Thread counter
        self.currTweetDF_ind = -1 # Current tweet index from DF

    def _init_triggers(self):
        self.actionLogin.triggered.connect(self.login_to_twitter_ui)
        self.actionWho_am_I.triggered.connect(self.pop_window)
        self.actionRefresh_GUI.triggered.connect(self.refresh_gui)
        self.actionTweet_Description.triggered.connect(self.whatTweetis)

        # self.label_login_status.mousePressEvent = self.update_status

        'Requesting methods'
        self.pushButton_collect1.clicked.connect(lambda: self.fork_method(self.downloadFullChunk))
        self.pushButton_collect10.clicked.connect(lambda f: self.fork_method(self.download10_chunks))
        self.pushButton_Request_Status.clicked.connect(self.requestStatusFromBox)

        'Settings'
        self.checkBox_wrap_console.clicked.connect(self.change_info_settings)

        'Buttons'
        self.pushButton_load_selected_csv.clicked.connect(self.load_selected)
        self.pushButton_load_selected_csv_2.clicked.connect(self.load_selected)
        self.pushButton_clear_log.clicked.connect(self.clear_log)
        self.pushButton_delete100.clicked.connect(lambda: self.delete_less(100))
        self.pushButton_delete500.clicked.connect(lambda: self.delete_less(500))
        self.pushButton_deleteSelected.clicked.connect(self.delete_selected)
        self.pushButton_merge_selected.clicked.connect(self.merge_selected)
        self.pushButton_export_DF.clicked.connect(lambda: self.save_current_DF(self.lineEdit_DF_comment.text()))
        self.pushButton_Info_screenLog.clicked.connect(self.copyInfoToLog)
        self.pushButton_showTweets.clicked.connect(self.showDF)
        self.pushButton_reload_DF.clicked.connect(self.resetDF)
        self.pushButton_check_threads.clicked.connect(self.check_threads)
        self.pushButton_open_in_browser.clicked.connect(self.open_in_broswer)
        self.pushButton_merge_without_duplicates.clicked.connect(self.merge_without_duplicates_trigger)

        'Displaying Tweets'
        self.pushButton_ShowTweet.clicked.connect(self.showTweetfromDF)
        self.pushButton_NextTweet.clicked.connect(self.showNextTweetfromDF)
        self.pushButton_PreviousTweet.clicked.connect(self.showPrevTweetfromDF)
        self.pushButton_JumpToTweet.clicked.connect(self.showTweetJump)
        self.pushButton_drop_current_tweet.clicked.connect(self.trigger_drop_current_tweet)

        'Filtration Buttons'
        self.pushButton_FilterDF_Lang_Polish.clicked.connect(lambda: self.filterdata_Language('pl'))
        self.pushButton_FilterDF_Lang_English.clicked.connect(lambda: self.filterdata_Language('en'))
        self.pushButton_FilterDF_Lang_Other.clicked.connect(self.filterdata_Language)
        self.pushButton_FilterDF_by_NonEmptyKey.clicked.connect(self.filterdata_ByNonEmptyKey)
        self.pushButton_FilterDF_TweetID.clicked.connect(self.filtedata_ByTweetId)
        self.pushButton_filter_by_Age.clicked.connect(self.trigger_filter_DF_age)
        self.pushButton_filter_by_Date.clicked.connect(self.trigger_filter_DF_date)
        self.pushButton_filter_search_words.clicked.connect(self.trigger_search_words)
        self.pushButton_drop_new_duplicates.clicked.connect(self.trigger_drop_new_duplicates)
        self.pushButton_drop_old_duplicates.clicked.connect(self.trigger_drop_old_duplicates)

        'Analyze Buttons'
        self.pushButton_analyze_unique_vals.clicked.connect(self.trigger_analyze_unique)

        'DEBUG'
        self.pushButton_Magic_Debug.clicked.connect(self.go_debug)

    def _init_wrappers(self):
        self.login_procedure = self.post_action(self.login_procedure, self.update_loginBox)

    def _init_settings(self):
        self.change_info_settings()

    def go_debug(self):
        print(self.get_distinct_from_DF('lang'))

    @staticmethod
    def add_timestamp_to_text(text):
        text = str(text)
        now = datetime.datetime.now()
        h = now.hour
        m = now.minute
        s = now.second
        timestamp = str(h).rjust(2, '0') + '-' + str(m).rjust(2, '0') + '-' + str(s).rjust(2, '0') + ': '
        return timestamp + text

    # # @staticmethod
    # def afk(self, *args, **kwargs):
    #     print("AFK_fork: ", args)
    #     for x in range(10):
    #         self.log_ui(str('x :{}'.format(x)))
    #         # time.sleep(0.2)

    def check_threads(self):
        threads = self.threads
        self.threads = []
        for th in threads:
            if th.isAlive():
                self.log_ui(f'{th.__name__} is still alive')
                self.threads += [th]
            else:
                pass
                # self.log_ui(f'{th.__name__} is finished, removing from list')

        if self.threads == []:
            self.log_ui(f'All tasks are complete')
            return False

    @staticmethod
    def downloadFullChunk():
        app = Analyzer(autologin=True)
        app.collect_new_tweets(n=1, chunk_size=200, interval=0)

    def change_info_settings(self):
        checked = True if self.checkBox_wrap_console.checkState() == 2 else False
        if checked:
            self.plainTextEdit_info.setLineWrapMode(QtWidgets.QPlainTextEdit.WidgetWidth)
        else:
            self.plainTextEdit_info.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)

    def copyInfoToLog(self):
        text = '=== Info:'
        for line in self.plainTextEdit_info.toPlainText().split('\n'):
            text += '\n\t' + line
        self.log_ui(text)
        time.sleep(0.8)

    def clear_log(self):
        self.textEdit_log.setPlainText('')

    def current_tree_selection(self, ignore_name=False, ignore_extension=False):
        '''Loads currently selected csv file from tree'''
        files_list = []
        selected_list = self.treeView.selectedIndexes()
        for i, item in enumerate(selected_list):
            if item.column() == 0:
                files_list += [item.data()]
        # files_list = [item.data() if item.column() == 0 else None for item in selected_list]
        good_files = []
        for file in files_list:
            if file[-4:] == '.csv' or ignore_extension:
                good_files += [file]
            #                if file[:7] == 'tweets_' or file[:7] == 'merged_' or file[:10] == 'dataframe_' or ignore_name:
            #                    good_files += [file]
            #                else:
            #                    self.log_ui("Invalid file name, missing 'tweets_': {}".format(file))
            else:
                self.log_ui("Invalid extension, not CSV: {}".format(file))
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
        filelist = self.current_tree_selection(ignore_name=True, ignore_extension=True)
        if filelist == []:
            self.log_ui('Make selection!')
            return None

        for f in filelist:
            try:
                os.remove(os.path.join(self._data_dir, f))
                self.log_ui(f'Removed {f}')

            except PermissionError:
                self.log_ui(f'PermissionError!!!: Close Files {f}')

    @staticmethod
    def download10_chunks():
        app = Analyzer(autologin=True)
        app.collect_new_tweets(n=10, chunk_size=200, interval=60)

    def filterdata_ByNonEmptyKey(self):
        text = self.lineEdit_filterKeyinput.text()
        valid = self.filtrerDF_ByExistingKey(text)
        if valid:
            self.currTweetDF_ind = 0
            self.showTweetfromDF()

    def filtedata_ByTweetId(self):
        text = self.lineEdit_tweet_id.text()
        if len(text) < 0:
            self.log_ui("This is not valid ID")
        valid = self.filteDF_ByTweetId(text)
        if valid:
            self.currTweetDF_ind = 0
            self.showTweetfromDF()

    def filterdata_Language(self, lang=None):
        if not lang:
            lang = self.lineEdit_FilterLangOther.text()
            lang = str(lang)
        if lang == '':
            self.log_ui('Box is empty!')
            return None
        valid = self.filterDF_byLang(lang)
        if valid:
            self.currTweetDF_ind = 0
            self.showTweetfromDF()

    # @staticmethod
    def fork_method(self, method_to_fork, *args, **kwargs):
        subprocess = threading.Thread(target=lambda: method_to_fork(*args, **kwargs))
        subprocess.__name__ = f'Thread #{self.th_num} ' + method_to_fork.__name__
        subprocess.start()
        # self.log_ui(f'New Thread: {subprocess.__name__}')
        self.threads += [subprocess]
        self.th_num += 1
        return subprocess

    def load_selected(self):
        self.currTweetDF_ind = -1
        files = self.current_tree_selection()
        self.load_DF(files)
        if self.DF is not None:
            # self.display(f'DF size: {self.DF.shape}')
            # self.display_add(str(self.DF.head()))
            self.currTweetDF_ind = 0
            self.showTweetfromDF()

    def log_ui(self, text_line):
        text_line = str(text_line)
        print(text_line)
        text = str(text_line) + '\n' + self.textEdit_log.toPlainText()
        text = self.add_timestamp_to_text(text)
        self.textEdit_log.setPlainText(text)

    def login_to_twitter_ui(self):
        valid, message = self.login_procedure()
        self.log_ui(message)

    def merge_selected(self):
        filelist = self.current_tree_selection()
        if not filelist:
            self.log_ui('Error. Select files!')
            return None
        if len(filelist) <= 1:
            self.log_ui('You can not merge this.')
            return None

        now = datetime.datetime.now()
        merged_file = 'merged_' \
                      + f'{now.year}'.ljust(4, '0') \
                      + f'{now.month}'.ljust(2, '0') \
                      + f'{now.day}'.ljust(2, '0') \
                      + f'_{now.hour}'.ljust(3, '0') \
                      + f'-{now.minute}'.ljust(3, '0') \
                      + f'-{now.second}'.ljust(3, '0') \
                      + '.csv'

        file_path = os.path.join(self._data_dir, merged_file)
        with open(file_path, 'wt', encoding='utf8') as f:
            for i, file in enumerate(filelist):
                curr_file_path = os.path.join(self._data_dir, file)
                df = pd.read_csv(curr_file_path, sep=';', encoding='utf8')
                if i == 0:
                    df.to_csv(f, header=True, sep=';', encoding='utf8', index=False)
                else:
                    df.to_csv(f, header=False, sep=';', encoding='utf8', index=False)
                try:
                    os.remove(curr_file_path)
                except PermissionError:
                    self.log_ui(f'Merged, but can not remove {file}')

        self.log_ui(f'Merged to file: {merged_file}')

    def merge_without_duplicates_trigger(self):
        files = self.current_tree_selection()
        self.fork_method(self.merge_without_duplicates, files)

    def merge_without_duplicates(self, files):
        app = Analyzer()
        valid = app.load_DF(files)
        if valid:
            resp = app.drop_duplicates_DF()
        if valid and resp is not False:
            valid = app.save_current_DF('Auto_Merge')
        if valid:
            for curr_file in files:
                curr_file_path = os.path.join(self._data_dir, curr_file)
                try:
                    os.remove(curr_file_path)
                except PermissionError:
                    self.log_ui(f'Merged, but can not remove {curr_file_path}')

    def open_in_broswer(self):
        if self.DF is not None:
            if 0 <= self.currTweetDF_ind < len(self.DF):
                tweet = self.DF.iloc[self.currTweetDF_ind]
                # author = tweet['user']
                author = ast.literal_eval(tweet['user'])['screen_name']
                status_id = tweet['id']
                url = f'https://twitter.com/{author}/status/{status_id}'
                self.fork_method(self._open_browser, url)

    def _open_browser(self, url):
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

    def refresh_gui(self):
        self.update_loginBox()
        self.show_tree()

    def resetDF(self):
        '''Loads last used files'''
        self.reloadDF()
        self.currTweetDF_ind = 0
        self.showTweetfromDF()

    def requestStatusFromBox(self):
        text = self.lineEdit_request_statusId.text()
        try:
            num = int(text)
        except ValueError:
            self.log_ui('This is not a number')
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

    def showDF(self):
        if self.DF is None:
            self.log_ui('DF is None!')
            return None
        else:
            self.display(f'DF size: {self.DF.shape}')
            self.display_add(str(self.DF.head()))

    def showTweet(self, ind):
        try:
            ind = int(ind)
        except ValueError:
            self.log_ui('This is not a number')
            return None
        flag_hide_empty = True if self.checkBox_HideEmptyValues.checkState() == 2 else False
        flag_short_user = True if self.checkBox_DisplayShortUserinfo.checkState() == 2 else False
        flag_short_quote = True if self.checkBox_DisplayShortQuoteStatus.checkState() == 2 else False
        if ind < 0 or ind >= len(self.DF):
            self.log_ui(f'Index is not correct!')
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
                # if "quoted_status" in user_dict: # and key == "quoted_status":
                #     print("FOUND", self.currTweetDF_ind)
            else:
                text += f'{key}:'.ljust(25) + f'{value}\n'
        self.display(text)

    def showTweetJump(self):
        if self.DF is None:
            self.log_ui('DF not loaded!')
            return None
        ind_str = self.lineEdit_JumpToTweet.text()
        self.showTweet(ind_str)

    def showTweetfromDF(self):
        if self.DF is None:
            self.log_ui('DF not loaded!')
            return None
        if self.currTweetDF_ind < 0:
            self.currTweetDF_ind = 0
        elif self.currTweetDF_ind >= len(self.DF):
            self.currTweetDF_ind = len(self.DF) - 1

        self.showTweet(self.currTweetDF_ind)

    def showNextTweetfromDF(self):
        if self.DF is None:
            self.log_ui('DF not loaded!')
            return None
        self.currTweetDF_ind += 1
        if self.currTweetDF_ind < 0 or self.currTweetDF_ind >= len(self.DF):
            self.currTweetDF_ind = 0  # First Tweet index            

        self.showTweet(self.currTweetDF_ind)

    def showPrevTweetfromDF(self):
        if self.DF is None:
            self.log_ui('DF not loaded!')
            return None
        self.currTweetDF_ind -= 1
        if self.currTweetDF_ind < 0:
            self.currTweetDF_ind = len(self.DF)-1  # Last Tweet index
        elif self.currTweetDF_ind >= len(self.DF):
            self.currTweetDF_ind = 0

        self.showTweet(self.currTweetDF_ind)

    def show_user_info(self, user_data):
        text = ''
        for key in ['screen_name', 'name', 'id', 'friends_count', 'followers_count', 'following', 'location',
                    'verified', 'lang']:
            text += str(key + ':').ljust(25) + str(user_data[key]) + '\n'
        self.display(text)

    def trigger_analyze_unique(self):
        key = self.lineEdit_analyze_unique_key.text()
        unique = self.get_distinct_from_DF(key)
        text = f"Unique values [{key}]:\n"
        if unique is None:
            return False
        else:
            for val in unique:
                text += f"'{val}'\n"
        print(f"'{text}'")
        self.display(text)

    def trigger_drop_current_tweet(self):
        self.drop_tweet_DF(self.currTweetDF_ind)
        self.showTweetfromDF()

    def trigger_drop_new_duplicates(self):
        valid = self.drop_duplicates_DF(keep_new=False)
        if valid:
            self.currTweetDF_ind = 0
            self.showTweetfromDF()

    def trigger_drop_old_duplicates(self):
        valid = self.drop_duplicates_DF(keep_new=True)
        if valid:
            self.currTweetDF_ind = 0
            self.showTweetfromDF()

    def trigger_filter_DF_date(self):
        try:
            year = self.spinBox_timefilter_from_year.value()
            month = self.spinBox_timefilter_from_month.value()
            day = self.spinBox_timefilter_from_day.value()
            hour = self.spinBox_timefilter_from_hour.value()
            minute = self.spinBox_timefilter_from_min.value()
            timestmp_min = self.timestamp_from_date(year=year, month=month, day=day, hour=hour, minute=minute)

            year = self.spinBox_timefilter_to_year.value()
            month = self.spinBox_timefilter_to_month.value()
            day = self.spinBox_timefilter_to_day.value()
            hour = self.spinBox_timefilter_to_hour.value()
            minute = self.spinBox_timefilter_to_min.value()
            timestmp_max = self.timestamp_from_date(year=year, month=month, day=day, hour=hour, minute=minute)

            valid = self.filterDF_by_timestamp(timestmp_min, timestmp_max)
            if valid:
                self.currTweetDF_ind = 0
                self.showTweetfromDF()

        except ValueError as ve:
            self.log_ui(f"Value Error: {ve}")

    def trigger_filter_DF_age(self):
        '''Function is reading input from gui spinboxes and translates it to timestamp, later calls filtration'''
        year = self.spinBox_timefilter_from_year.value()
        month = self.spinBox_timefilter_from_month.value()
        day = self.spinBox_timefilter_from_day.value()
        hour = self.spinBox_timefilter_from_hour.value()
        minute = self.spinBox_timefilter_from_min.value()
        timestmp_min = self.timestamp_offset(year=-year, month=-month, day=-day, hour=-hour, minute=-minute)

        year = self.spinBox_timefilter_to_year.value()
        month = self.spinBox_timefilter_to_month.value()
        day = self.spinBox_timefilter_to_day.value()
        hour = self.spinBox_timefilter_to_hour.value()
        minute = self.spinBox_timefilter_to_min.value()
        timestmp_max = self.timestamp_offset(year=-year, month=-month, day=-day, hour=-hour, minute=-minute)

        valid = self.filterDF_by_timestamp(timestmp_min, timestmp_max)
        if valid:
            self.currTweetDF_ind = 0
            self.showTweetfromDF()

    def trigger_search_words(self):
        words = self.lineEdit_filter_words.text()
        valid = self.filterDF_search_words(words)
        if valid:
            self.currTweetDF_ind = 0
            self.showTweetfromDF()

    def update_loginBox(self):
        if self.logged_in:
            self.label_login_status.setText('True')
            self.label_login_status.setStyleSheet("background-color: rgb(30, 255, 180);")
            self.show_user_info(self.me)
        else:
            self.label_login_status.setText('False')
            self.label_login_status.setStyleSheet("background-color: rgb(255, 149, 151);\n"
                                                  "color: rgb(255, 255, 255);")

    def whatTweetis(self):
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
    def excepthook(type_, value, traceback_):
        traceback.print_exception(type_, value, traceback_)
        QtCore.qFatal('')
sys.excepthook = excepthook

def runGUI():
    ui = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    app = TwitterAnalyzerGUI(MainWindow, autologin=True)
    # ui.setupUi(MainWindow)  # moved to class init
    error_dialog = QtWidgets.QErrorMessage()
    MainWindow.show()
    sys.exit(ui.exec_())
    
if __name__ == "__main__":
    runGUI()
