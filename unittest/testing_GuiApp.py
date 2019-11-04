from PyQt5 import QtCore, QtWidgets
from TwitterAnalyzer.GUI._App import TwitterAnalyzerGUI
import sys
import os
import unittest
import time

ui = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
app = TwitterAnalyzerGUI(MainWindow, autologin=False)

global tweet_dir
tweet_dir = os.path.join(os.path.dirname(__file__),
                        '..', 'TwitterAnalyzer', 'tweets')

class UnitTest(unittest.TestCase):
    def test_fail_collect_Home(self):
        app = TwitterAnalyzerGUI(MainWindow, autologin=False)
        valid = app.collect_new_tweets(n=1)
        self.assertFalse(valid)

    def test_login(self):
        #app = TwitterAnalyzerGUI(MainWindow, autologin=False)
        valid, _= app._login_procedure()
        self.assertTrue(valid)

    def test_collect_Home(self):
        app._login_procedure()
        valid = app.collect_new_tweets(filename='unittest',n=1)
        self.assertTrue(valid)

##    def test_save_empty(self):
##        app.export_tweet_to_database('tweets', None, 'unittest')
        
    def test_delete_csv(self):
        filepath = os.path.join(tweet_dir, 'unittest.csv')
        app.delete_csv(filepath)
        self.assertFalse(os.path.isfile(filepath))

#unittest.sortTestMethodsUsing = None
unittest.main()
