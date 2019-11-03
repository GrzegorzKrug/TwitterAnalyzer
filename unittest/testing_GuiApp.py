from PyQt5 import QtCore, QtWidgets
from TwitterAnalyzer.GUI._App import TwitterAnalyzerGUI
import sys
import unittest
import time

ui = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
app = TwitterAnalyzerGUI(MainWindow, autologin=False)


class UnitTest(unittest.TestCase):
    def test_fail_collect_Home(self):
        app = TwitterAnalyzerGUI(MainWindow, autologin=False)
        valid = app.collect_new_tweets(n=1)
        assert not valid

    def test_login(self):
        app = TwitterAnalyzerGUI(MainWindow, autologin=False)
        valid, _= app._login_procedure()
        assert valid
##
    def test_collect_Home(self):
        app = TwitterAnalyzerGUI(MainWindow, autologin=False)
        app._login_procedure()
        valid = app.collect_new_tweets(filename='unittest',n=1)
        assert valid


unittest.sortTestMethodsUsing = None
unittest.main()
