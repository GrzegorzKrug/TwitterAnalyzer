from PyQt5 import QtCore, QtGui, QtWidgets
from TwitterAnalyzer import TwitterAnalyzer
from GUI import Ui_MainWindow
import random
import time

class TwitterAnalyzerGUI(TwitterAnalyzer, Ui_MainWindow):
    def __init__(self, mainWindow):        
        Ui_MainWindow.__init__(self)
        self.setupUi(mainWindow)
        TwitterAnalyzer.__init__(self, autologin=True)

        self.init_triggers()
        self.refresh_gui()
        
    def init_triggers(self):
        self.pushButton.clicked.connect(lambda: self.clicker(self.pushButton))
        self.pushButton_2.clicked.connect(lambda: self.clicker(self.pushButton_2))

        self.actionLogin.triggered.connect(self._login_procedure)
        self.label_login_status.mousePressEvent  = self.update_status

    def update_status(self, event):
    def fork_method(self, method_to_fork):
        subprocess = threading.Thread(target=method_to_fork)
        subprocess.start()
        return subprocess

    def afk(self, *args):
        print("AFK: ", args)
        for x in range(10):
            print('x :', x)
            time.sleep(0.5)

        if self.logged_in:
            self.label_login_status.setText('True')
            self.label_login_status.setStyleSheet("background-color: rgb(30, 255, 180);")
        else:
            self.label_login_status.setText('False')
            self.label_login_status.setStyleSheet("background-color: rgb(255, 149, 151);\n"
                                                  "color: rgb(255, 255, 255);")

    def refresh_gui(self):
        self.update_status(None)

    @staticmethod
    def run_next_method(method, next_method):
        def wrapper(*args, **kwargs):
            out = method(*args, **kwargs)
            next_method()
            return out
        return wrapper

    def clicker(self, button):
        print('Console Clicked')
        r = random.random()
        print('\t R =',r)
        if r > 0.5:
            button.setText("True")
        else:
            button.setText("False")

        time.sleep(0.5)
            
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = TwitterAnalyzerGUI(MainWindow)
    # ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    
