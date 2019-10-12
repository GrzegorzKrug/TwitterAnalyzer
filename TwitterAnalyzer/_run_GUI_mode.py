from PyQt5 import QtCore, QtGui, QtWidgets
from TwitterAnalyzer import TwitterAnalyzer
from GUI import Ui_MainWindow
import random
import time
import threading
import traceback
import sys
import os
import glob

class TwitterAnalyzerGUI(TwitterAnalyzer, Ui_MainWindow):
    def __init__(self, mainWindow):        
        Ui_MainWindow.__init__(self)
        TwitterAnalyzer.__init__(self, autologin=False)
        self.setupUi(mainWindow)

        self.init_wrappers()
        self.init_triggers()
        self.refresh_gui()
        
    def init_triggers(self):
        self.actionLogin.triggered.connect(lambda: self._login_procedure())
        self.label_login_status.mousePressEvent  = self.update_status
        self.pushButton_collectTweets.clicked.connect(self.collect_new_tweets_fork)
        self.pushButton_find_csv.clicked.connect(lambda: self.find_local_tweets())

    def init_wrappers(self):
        self._login_procedure = self.post_action(self._login_procedure, self.update_status)

    def collect_new_tweets_fork(self):
        self.fork_method(self.collect_new_tweets)

    def fork_method(self, method_to_fork):
        subprocess = threading.Thread(target=method_to_fork)
        subprocess.start()
        return subprocess

    def afk(self, *args):
        print("AFK: ", args)
        for x in range(10):
            print('x :', x)
            time.sleep(0.5)

    def update_status(self, event=None):
        if self.logged_in:
            self.label_login_status.setText('True')
            self.label_login_status.setStyleSheet("background-color: rgb(30, 255, 180);")
        else:
            self.label_login_status.setText('False')
            self.label_login_status.setStyleSheet("background-color: rgb(255, 149, 151);\n"
                                                  "color: rgb(255, 255, 255);")

    def refresh_gui(self):
        self.update_status()
        self.show_tree()

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

    def find_local_tweets(self, path=None):
        if path == None:
            path = self._data_dir
        else:
            path = os.path.abspath(path)

        files = glob.glob(path + '\\*.csv')
        print(files)
        return files

    def load_files_info(self, files):
        if type(files) != list:
            files = [files]

        pass

    def show_tree(self):
        model = QtWidgets.QFileSystemModel()
        model.setRootPath(os.path.dirname(__file__))
        self.treeView.setModel(model)

if QtCore.QT_VERSION >= 0x50501:  # Showint traceback from crashes
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
    
