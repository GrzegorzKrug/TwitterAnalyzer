from PyQt5 import QtCore, QtWidgets
from TwitterAnalyzer.GUI._App import TwitterAnalyzerGUI
import sys
import unittest

ui = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
app = TwitterAnalyzerGUI(MainWindow)


app.collect_new_tweets(1)
