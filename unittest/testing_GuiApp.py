from PyQt5 import QtCore, QtWidgets
from twitter_analyzer.gui.app import TwitterAnalyzerGUI
import sys
import os
import unittest
import time

ui = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
app = TwitterAnalyzerGUI(MainWindow, autologin=False)

global tweet_dir
tweet_dir = os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))),
                        'TwitterAnalyzer', 'tweets')


class UnitTest(unittest.TestCase):
    def test_Login_Collect_Home(self):
        app = TwitterAnalyzerGUI(MainWindow, autologin=False)
        valid = app.collect_new_tweets(n=1)
        self.assertFalse(valid)
        
        valid, _= app._login_procedure()
        self.assertTrue(valid)
        
        valid = app.collect_new_tweets(filename='unittest_Home', n=1)
        self.assertTrue(os.path.isfile(os.path.join(tweet_dir, 'unittest_Home.csv')))
        self.assertTrue(valid)

    def test_create_delete_csv(self):
        filepath = os.path.join(tweet_dir, 'unittest.csv')
        app.export_tweet_to_database('tweets', None, 'unittest')
        self.assertTrue(os.path.exists(filepath))

        app.delete_csv(filepath)
        self.assertFalse(os.path.isfile(filepath))

#unittest.sortTestMethodsUsing = None
unittest.main()
