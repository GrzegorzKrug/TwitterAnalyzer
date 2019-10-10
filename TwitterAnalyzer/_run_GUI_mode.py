from PyQt5 import QtCore, QtGui, QtWidgets
from TwitterAnalyzer import TwitterAnalyzer
from GUI import Ui_MainWindow
import random

class TwitterAnalyzerGUI(TwitterAnalyzer, Ui_MainWindow):
    def __init__(self, mainWindow):        
        Ui_MainWindow.__init__(self)
        self.setupUi(mainWindow)
        TwitterAnalyzer.__init__(self, autologin=False)

        self.init_triggers()
        
    def init_triggers(self):
        self.pushButton.clicked.connect(lambda: self.clicker())
        
    def clicker(self):
        print('Console Clicked')
        r = random.random()
        print('\t R =',r)
        if r > 0.5:
            self.pushButton.setText("True")
        else:
            self.pushButton.setText("False")
            
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = TwitterAnalyzerGUI(MainWindow)
    # ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    
