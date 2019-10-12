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


class TwitterAnalyzerGUI(TwitterAnalyzer, Ui_MainWindow):
    def __init__(self, mainWindow):        
        Ui_MainWindow.__init__(self)
        TwitterAnalyzer.__init__(self, autologin=False)
        self.setupUi(mainWindow)

        self._init_wrappers()
        self._init_triggers()
        self.refresh_gui()

    def _init_triggers(self):
        self.actionLogin.triggered.connect(lambda: self.login_to_twitter_ui())
        self.label_login_status.mousePressEvent  = self.update_status
        self.pushButton_collectTweets.clicked.connect(lambda: self.collect_tweets_ui())
        self.pushButton_find_csv.clicked.connect(lambda: self.find_local_tweets())
        self.pushButton_load_csv.clicked.connect(lambda: self.load_selected())
        self.pushButton_clear_log.clicked.connect(lambda: self.clear_log())

    def _init_wrappers(self):
        self._login_procedure = self.post_action(self._login_procedure, self.update_status)

    # def collect_new_tweets_fork(self):
    #     self.fork_method(self.collect_new_tweets)

    def add_timestamp_to_text(self, text):
        text = str(text)
        now = datetime.datetime.now()
        h = now.hour
        m = now.minute
        s = now.second
        timestamp = str(h).rjust(2, '0') + '-' + str(m).rjust(2, '0') + '-' + str(s).rjust(2, '0') + ':  '
        return timestamp + text

    # @staticmethod
    def afk(self, *args, **kwargs):
        print("AFK_fork: ", args)
        for x in range(10):
            self.log_ui(str('x :{}'.format(x)))
            # time.sleep(0.2)

    def collect_tweets_ui(self):
        valid, message = self.collect_new_tweets(N=1, chunk_size=200, interval=0)
        self.log_ui(message)

    def clear_log(self):
        self.textEdit_log.setPlainText('')

    def fork_method(self, method_to_fork):
        subprocess = threading.Thread(target=method_to_fork)
        subprocess.start()
        return subprocess

    def load_files_info(self, files):
        if type(files) != list:
            files = [files]
        pass

    def load_selected(self):
        print('Loading')

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
            if method != None:
                out = method(*args, **kwargs)
            if next_method != None:
                next_method()
            return out

        return wrapper

    def refresh_gui(self):
        self.update_status()
        self.show_tree()

    def show_tree(self):
        path = os.path.dirname(__file__)  + '\\' + self._data_dir
        model = QtWidgets.QFileSystemModel()
        model.setRootPath((QtCore.QDir.rootPath()))
        self.treeView.setModel(model)
        self.treeView.setRootIndex(model.index(path))

    def show_user_info(self, user_data):
        text = ''
        for key in ['screen_name', 'name', 'id', 'friends_count', 'followers_count', 'following', 'location',
                    'verified', 'lang']:
            text += str(key + ':').ljust(20)  + str(user_data[key]) + '\n'
        self.plainTextEdit_selected_user.setPlainText(text)

    def update_status(self, event=None):
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
    
