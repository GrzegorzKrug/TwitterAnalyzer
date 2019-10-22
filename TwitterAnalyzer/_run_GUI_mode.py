# _run_GUI_mode.py
# Grzegorz Krug
from PyQt5 import QtCore, QtGui, QtWidgets
from TwitterAnalyzer import TwitterAnalyzer
from GUI import Ui_MainWindow
import random
import time
import datetime
import threading
import traceback
import sys
import os
import pandas as pd


class TwitterAnalyzerGUI(TwitterAnalyzer, Ui_MainWindow):
    def __init__(self, mainWindow):        
        Ui_MainWindow.__init__(self)
        TwitterAnalyzer.__init__(self, autologin=False, log_ui=self.log_ui)
        self.setupUi(mainWindow)

        self._init_wrappers()
        self._init_triggers()
        self.refresh_gui()

        self._loaded_files = []


    def _init_triggers(self):
        self.actionLogin.triggered.connect(lambda f: self.login_to_twitter_ui())
        self.actionWho_am_I.triggered.connect(lambda f: self.pop_window())

        self.label_login_status.mousePressEvent = lambda f: self.update_status()

        self.pushButton_collect1.clicked.connect(lambda f: self.collect_tweets_ui())
        self.pushButton_collect10.clicked.connect(lambda f: self.fork_method(self.download10_chunks, parent=self))
        self.pushButton_find_csv.clicked.connect(lambda f: self.find_local_tweets())
        self.pushButton_load_csv.clicked.connect(lambda f: self.load_files())
        self.pushButton_clear_log.clicked.connect(lambda f: self.clear_log())

    def _init_wrappers(self):
        self._login_procedure = self.post_action(self._login_procedure, self.update_status)

    @staticmethod
    def add_timestamp_to_text(text):
        text = str(text)
        now = datetime.datetime.now()
        h = now.hour
        m = now.minute
        s = now.second
        timestamp = str(h).rjust(2, '0') + '-' + str(m).rjust(2, '0') + '-' + str(s).rjust(2, '0') + ':  '
        return timestamp + text

    # # @staticmethod
    # def afk(self, *args, **kwargs):
    #     print("AFK_fork: ", args)
    #     for x in range(10):
    #         self.log_ui(str('x :{}'.format(x)))
    #         # time.sleep(0.2)

    def collect_tweets_ui(self):
        valid = self.collect_new_tweets(n=1, chunk_size=200, interval=0)
        return valid

    def clear_log(self):
        self.textEdit_log.setPlainText('')

    def current_tree_selection(self, override_file_name=False):
        'Loads currently selected csv file from tree'
        files_list = []
        selected_list = self.treeView.selectedIndexes()
        for i,item in enumerate(selected_list):
            if item.column() == 0:
                files_list += [item.data()]
        # files_list = [item.data() if item.column() == 0 else None for item in selected_list]

        for file in files_list:
            if file[-4:] == '.csv':
                if file[:7] == 'tweets_' and not override_file_name:
                    self.log_ui('Loading {}'.format(file))
                else:
                    self.log_ui("Invalid file name, missing 'tweets_': {}".format(file))
            else:
                self.log_ui("Invalid extension, not CSV: {}".format(file))
        return files_list

    @staticmethod
    def download10_chunks(*args, **kwargs):
        print(f'ARGS: {args}, Kwargs:{kwargs}')
        app = TwitterAnalyzer()
        # try:
        #     if kwargs['parent']:
        #         print('TRUE parent')
        #         kwargs['parent'].log_ui('THIS IS THREAD')
        #
        #         app.log_ui = kwargs['parent'].log_ui
        # except KeyError:
        #     pass
        app.collect_new_tweets(n=10, chunk_size=200, interval=60)

    # @staticmethod
    def fork_method(self, method_to_fork, *args, **kwargs):
        self.log_ui(f'New Thread: {method_to_fork.__name__}')
        subprocess = threading.Thread(target=lambda: method_to_fork(*args, **kwargs))
        subprocess.start()
        return subprocess

    def load_files(self):
        files = self.current_tree_selection()
        self.reload_files(files)
        self.log_ui(f'DF size: {self.DF.shape}')

    def log_ui(self, text_line):
        text = str(text_line) + '\n' + self.textEdit_log.toPlainText()
        text = self.add_timestamp_to_text(text)
        self.textEdit_log.setPlainText(text)

    def login_to_twitter_ui(self):
        valid, message = self._login_procedure()
        self.log_ui(message)

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
        self.update_status()
        self.show_tree()

    def show_tree(self):
        path = os.path.dirname(__file__) + '\\' + self._data_dir
        model = QtWidgets.QFileSystemModel()
        model.setRootPath(path)
        self.treeView.setModel(model)
        self.treeView.setRootIndex(model.index(path))
        self.treeView.setColumnWidth(0, 40*8)
        self.treeView.setColumnWidth(1, 10*8)
        self.treeView.setColumnWidth(2, 10*8)
        self.treeView.setColumnWidth(3, 15*8)
        # self.treeView.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)  # its defined in GUI.py

    def show_user_info(self, user_data):
        text = ''
        for key in ['screen_name', 'name', 'id', 'friends_count', 'followers_count', 'following', 'location',
                    'verified', 'lang']:
            text += str(key + ':').ljust(20) + str(user_data[key]) + '\n'
        self.plainTextEdit_selected_user.setPlainText(text)

    def update_status(self):
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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = TwitterAnalyzerGUI(MainWindow)
    # ui.setupUi(MainWindow)  # moved to class init
    error_dialog = QtWidgets.QErrorMessage()
    MainWindow.show()
    sys.exit(app.exec_())
    
