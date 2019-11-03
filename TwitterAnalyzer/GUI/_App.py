# _run_GUI_mode.py
# Grzegorz Krug
from PyQt5 import QtCore, QtWidgets # QtGui
from TwitterAnalyzer.Analyzer.Analyzer import Analyzer
from TwitterAnalyzer.GUI.GUI import Ui_MainWindow
#import random
#import time
import datetime
import threading
import traceback
import sys
import os
import pandas as pd
import time


class TwitterAnalyzerGUI(Analyzer, Ui_MainWindow):
    def __init__(self, mainWindow, autologin=True):
        Ui_MainWindow.__init__(self)
        self.setupUi(mainWindow)
        Analyzer.__init__(self, autologin=autologin, log_ui=self.log_ui)

        self._init_wrappers()
        self._init_triggers()
        self.refresh_gui()
        self._loaded_files = []  # Last loaded files, for reloading
        self.threads = []  # Thread reference list
        self.th_num = 0  # Thread counter
        self.currTweetDF_ind = -1 # Current tweet index from DF

    def _init_triggers(self):
        self.actionLogin.triggered.connect(self.login_to_twitter_ui)
        self.actionWho_am_I.triggered.connect(self.pop_window)
        self.actionRefresh_GUI.triggered.connect(self.refresh_gui)

        # self.label_login_status.mousePressEvent = self.update_status

        self.pushButton_collect1.clicked.connect(lambda: self.fork_method(self.downloadFullChunk))
        self.pushButton_collect10.clicked.connect(lambda f: self.fork_method(self.download10_chunks))
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

        self.pushButton_ShowTweet.clicked.connect(self.showTweetfromDF)
        self.pushButton_NextTweet.clicked.connect(self.showNextTweetfromDF)
        self.pushButton_PreviousTweet.clicked.connect(self.showPrevTweetfromDF)
        self.pushButton_JumpToTweet.clicked.connect(self.showTweetJump)

        self.pushButton_Request_Status.clicked.connect(self.requestStatusFromBox)
        self.pushButton_FilterDF_Lang_Polish.clicked.connect(lambda: self.filterDF_Language('pl'))
        self.pushButton_FilterDF_Lang_English.clicked.connect(lambda: self.filterDF_Language('en'))
        self.pushButton_FilterDF_Lang_Other.clicked.connect(self.filterDF_Language)
        
    def _init_wrappers(self):
        self._login_procedure = self.post_action(self._login_procedure, self.update_loginBox)

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
                self.log_ui(f'{th.__name__} is finished, removing from list')
                
        if self.threads == []:
            self.log_ui(f'All tasks are complete')
            return False

    @staticmethod
    def downloadFullChunk():
        app = Analyzer()
        app.collect_new_tweets(n=1, chunk_size=200, interval=0)        

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
##                if file[:7] == 'tweets_' or file[:7] == 'merged_' or file[:10] == 'dataframe_' or ignore_name:
##                    good_files += [file]
##                else:
##                    self.log_ui("Invalid file name, missing 'tweets_': {}".format(file))
            else:
                self.log_ui("Invalid extension, not CSV: {}".format(file))
        return good_files

    def display_add(self, text):
        old_text = self.plainTextEdit_info.toPlainText()
        text = old_text + '\n' + text
        self.plainTextEdit_info.setPlainText(text)

    def display(self, text):
        self.plainTextEdit_info.setPlainText(text)

    def delete_selected(self):
        filelist = self.current_tree_selection(ignore_name=True, ignore_extension=True)
        if filelist == []:
            self.log_ui('Make selection!')
            return None

        for f in filelist:
            try:
                os.remove(self._data_dir + '\\' + f)
                self.log_ui(f'Removed {f}')

            except PermissionError:
                self.log_ui(f'PermissionError!!!: Close Files {f}')

    @staticmethod
    def download10_chunks():
        app = Analyzer()
        # try:
        #     if kwargs['parent']:
        #         print('TRUE parent')
        #         kwargs['parent'].log_ui('THIS IS THREAD')
        #
        #         app.log_ui = kwargs['parent'].log_ui
        # except KeyError:
        #     pass
        app.collect_new_tweets(n=2, chunk_size=200, interval=5)

    def filterDF_Language(self, lang=None):
        if lang:
            self.filterDF_byLang(lang)
        else:
            lang = self.lineEdit_FilterLangOther.text()
            lang = str(lang)
            if lang == '':
                self.log_ui('This is not language!')
                return None
            self.filterDF_byLang(lang)
        self.showDF()
        
    # @staticmethod
    def fork_method(self, method_to_fork, *args, **kwargs):        
        subprocess = threading.Thread(target=lambda: method_to_fork(*args, **kwargs))
        subprocess.__name__ = f'Thread #{self.th_num} ' + method_to_fork.__name__        
        subprocess.start()
        self.log_ui(f'New Thread: {subprocess.__name__}')
        self.threads += [subprocess]
        self.th_num += 1
        return subprocess

    def load_selected(self):
        self.currTweetDF_ind = -1
        files = self.current_tree_selection()
        self.load_DF(files)
        if self.DF is not None:
            self.display(f'DF size: {self.DF.shape}')
            self.display_add(str(self.DF.head()))

    def log_ui(self, text_line):
        text_line = str(text_line)
        print(text_line)
        text = str(text_line) + '\n' + self.textEdit_log.toPlainText()
        text = self.add_timestamp_to_text(text)
        self.textEdit_log.setPlainText(text)

    def login_to_twitter_ui(self):
        valid, message = self._login_procedure()
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
                    + f'{now.day}'.ljust(2, '0')  \
                    + f'_{now.hour}'.ljust(3, '0')  \
                    + f'-{now.minute}'.ljust(3, '0') \
                    + f'-{now.second}'.ljust(3, '0') \
                    + '.csv'
        with open(self._data_dir + '\\' + merged_file, 'wt', encoding='utf8') as f:
            for i, file in enumerate(filelist):
                df = pd.read_csv(self._data_dir + '\\' + file, sep=';', encoding='utf8')

                if i == 0:
                    df.to_csv(f, header=True, sep=';', encoding='utf8', index=False)
                else:
                    df.to_csv(f, header=False, sep=';', encoding='utf8', index=False)
                try:
                    os.remove(self._data_dir + '\\' + file)
                except PermissionError:
                    self.log_ui(f'Merged, but can not remove {file}')

        self.log_ui(f'Merged to file: {merged_file}')

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
            msg.setText('Currently logged in: {} ({}).'
                        .format(self.me['screen_name'], self.me['name']))
        else:
            msg.setText('Currently not logged in.')
        msg.exec()

    def refresh_gui(self):
        self.update_loginBox()
        self.show_tree()

    def resetDF(self):
        self.currTweetDF_ind = -1
        self.reloadDF()
        self.showDF()

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

    def showTweetJump(self):
        if self.DF is None:
            self.log_ui('DF not loaded!')
            return None
        ind_str = self.lineEdit_JumpToTweet.text()        
        try:
            ind = int(ind_str)
        except ValueError:
            self.log_ui('This is not a number')
            return None
        
        if ind < 0 or ind >= len(self.DF):
            self.log_ui(f'Index is not correct!')
            return None        
        self.currTweetDF_ind = ind
        text = f'Tweet index: {self.currTweetDF_ind} / {len(self.DF)-1}\n'
        for key, value in self.DF.iloc[self.currTweetDF_ind].items():
            text += f'{key}:'.ljust(20) + f'{value}\n'
        self.display(text)
        
    def showTweetfromDF(self):
        if self.DF is None:
            self.log_ui('DF not loaded!')
            return None
        if self.currTweetDF_ind < 0:
            self.currTweetDF_ind = 0
        elif self.currTweetDF_ind >= len(self.DF):
            self.currTweetDF_ind = len(self.DF) - 1
        text = f'Tweet index: {self.currTweetDF_ind} / {len(self.DF)-1}\n'
        for key, value in self.DF.iloc[self.currTweetDF_ind].items():
            text += f'{key}:'.ljust(20) + f'{value}\n'
        self.display(text)
                
    def showNextTweetfromDF(self):
        if self.DF is None:
            self.log_ui('DF not loaded!')
            return None
        self.currTweetDF_ind += 1
        if self.currTweetDF_ind < 0 or self.currTweetDF_ind >= len(self.DF):
            self.currTweetDF_ind = 0  # First Tweet index            
        text = f'Tweet index: {self.currTweetDF_ind} / {len(self.DF)-1}\n'
        for key, value in self.DF.iloc[self.currTweetDF_ind].items():
            text += f'{key}:'.ljust(20) + f'{value}\n'
        self.display(text)
        
    def showPrevTweetfromDF(self):
        if self.DF is None:
            self.log_ui('DF not loaded!')
            return None
        self.currTweetDF_ind -= 1
        if self.currTweetDF_ind < 0:
            self.currTweetDF_ind = len(self.DF)-1  # Last Tweet index
        elif self.currTweetDF_ind >= len(self.DF):
            self.currTweetDF_ind = 0
        text = f'Tweet index: {self.currTweetDF_ind} / {len(self.DF)-1}\n'
        for key, value in self.DF.iloc[self.currTweetDF_ind].items():
            text += f'{key}:'.ljust(20) + f'{value}\n'
        self.display(text)
           
    def show_user_info(self, user_data):
        text = ''
        for key in ['screen_name', 'name', 'id', 'friends_count', 'followers_count', 'following', 'location',
                    'verified', 'lang']:
            text += str(key + ':').ljust(20) + str(user_data[key]) + '\n'
        self.display(text)

    def update_loginBox(self):
        if self.logged_in:
            self.label_login_status.setText('True')
            self.label_login_status.setStyleSheet("background-color: rgb(30, 255, 180);")
            self.show_user_info(self.me)
        else:
            self.label_login_status.setText('False')
            self.label_login_status.setStyleSheet("background-color: rgb(255, 149, 151);\n"
                                                  "color: rgb(255, 255, 255);")
# ------ Sorted methods are above --------------------------------------------------------------------------------------


if QtCore.QT_VERSION >= 0x50501:  # Showing traceback from crashes
    def excepthook(type_, value, traceback_):
        traceback.print_exception(type_, value, traceback_)
        QtCore.qFatal('')
sys.excepthook = excepthook

def runGUI():
    ui = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    app = TwitterAnalyzerGUI(MainWindow)
    # ui.setupUi(MainWindow)  # moved to class init
    error_dialog = QtWidgets.QErrorMessage()
    MainWindow.show()
    sys.exit(ui.exec_())
    
if __name__ == "__main__":
    runGUI()
