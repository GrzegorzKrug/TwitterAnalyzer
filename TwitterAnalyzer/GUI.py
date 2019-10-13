# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(955, 760)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 260, 371, 271))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.pushButton_collectTweets = QtWidgets.QPushButton(self.tab)
        self.pushButton_collectTweets.setGeometry(QtCore.QRect(10, 10, 111, 23))
        self.pushButton_collectTweets.setObjectName("pushButton_collectTweets")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 81, 21))
        self.label.setObjectName("label")
        self.label_login_status = QtWidgets.QLabel(self.centralwidget)
        self.label_login_status.setGeometry(QtCore.QRect(80, 10, 81, 21))
        self.label_login_status.setMouseTracking(False)
        self.label_login_status.setStyleSheet("background-color: rgb(255, 149, 151);\n"
"color: rgb(255, 255, 255);")
        self.label_login_status.setAlignment(QtCore.Qt.AlignCenter)
        self.label_login_status.setObjectName("label_login_status")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 91, 16))
        self.label_2.setObjectName("label_2")
        self.treeView = QtWidgets.QTreeView(self.centralwidget)
        self.treeView.setGeometry(QtCore.QRect(440, 10, 501, 351))
        self.treeView.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.treeView.setObjectName("treeView")
        self.pushButton_find_csv = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_find_csv.setGeometry(QtCore.QRect(350, 10, 81, 23))
        self.pushButton_find_csv.setObjectName("pushButton_find_csv")
        self.textEdit_input_name = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_input_name.setEnabled(True)
        self.textEdit_input_name.setGeometry(QtCore.QRect(470, 370, 161, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit_input_name.sizePolicy().hasHeightForWidth())
        self.textEdit_input_name.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(6)
        self.textEdit_input_name.setFont(font)
        self.textEdit_input_name.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEdit_input_name.setObjectName("textEdit_input_name")
        self.plainTextEdit_selected_user = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_selected_user.setGeometry(QtCore.QRect(10, 60, 331, 192))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.plainTextEdit_selected_user.setFont(font)
        self.plainTextEdit_selected_user.setStyleSheet("background-color: rgb(220, 220, 220);\n"
"\n"
"")
        self.plainTextEdit_selected_user.setFrameShape(QtWidgets.QFrame.Panel)
        self.plainTextEdit_selected_user.setFrameShadow(QtWidgets.QFrame.Plain)
        self.plainTextEdit_selected_user.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.plainTextEdit_selected_user.setObjectName("plainTextEdit_selected_user")
        self.textEdit_log = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_log.setGeometry(QtCore.QRect(10, 540, 431, 171))
        self.textEdit_log.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.textEdit_log.setLineWrapMode(QtWidgets.QTextEdit.WidgetWidth)
        self.textEdit_log.setLineWrapColumnOrWidth(0)
        self.textEdit_log.setObjectName("textEdit_log")
        self.pushButton_load_csv = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_load_csv.setGeometry(QtCore.QRect(350, 40, 81, 23))
        self.pushButton_load_csv.setObjectName("pushButton_load_csv")
        self.pushButton_clear_log = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_clear_log.setGeometry(QtCore.QRect(450, 690, 81, 23))
        self.pushButton_clear_log.setStyleSheet("background-color: qlineargradient(spread:reflect, x1:0.5, y1:0.5, x2:0, y2:0.028, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(255, 144, 144, 255));")
        self.pushButton_clear_log.setObjectName("pushButton_clear_log")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 955, 21))
        self.menubar.setObjectName("menubar")
        self.menuAcc = QtWidgets.QMenu(self.menubar)
        self.menuAcc.setObjectName("menuAcc")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        self.menuAnalyze = QtWidgets.QMenu(self.menubar)
        self.menuAnalyze.setObjectName("menuAnalyze")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionLogin = QtWidgets.QAction(MainWindow)
        self.actionLogin.setObjectName("actionLogin")
        self.actionWho_am_I = QtWidgets.QAction(MainWindow)
        self.actionWho_am_I.setObjectName("actionWho_am_I")
        self.actionabout = QtWidgets.QAction(MainWindow)
        self.actionabout.setObjectName("actionabout")
        self.menuAcc.addAction(self.actionLogin)
        self.menuAcc.addAction(self.actionWho_am_I)
        self.menuAcc.addSeparator()
        self.menuAbout.addAction(self.actionabout)
        self.menubar.addAction(self.menuAcc.menuAction())
        self.menubar.addAction(self.menuAnalyze.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_collectTweets.setText(_translate("MainWindow", "Collect new tweets!"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Menu 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Menu 2"))
        self.label.setText(_translate("MainWindow", "Logged in:"))
        self.label_login_status.setText(_translate("MainWindow", "Not logged in"))
        self.label_2.setText(_translate("MainWindow", "Current user info:"))
        self.pushButton_find_csv.setText(_translate("MainWindow", "Find CSV"))
        self.textEdit_input_name.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:6pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8.25pt;\">useless for now</span></p></body></html>"))
        self.plainTextEdit_selected_user.setPlainText(_translate("MainWindow", "None"))
        self.textEdit_log.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.pushButton_load_csv.setText(_translate("MainWindow", "Load selected"))
        self.pushButton_clear_log.setText(_translate("MainWindow", "Clear Log"))
        self.menuAcc.setTitle(_translate("MainWindow", "Start"))
        self.menuAbout.setTitle(_translate("MainWindow", "About"))
        self.menuAnalyze.setTitle(_translate("MainWindow", "Analyze"))
        self.actionLogin.setText(_translate("MainWindow", "Login"))
        self.actionWho_am_I.setText(_translate("MainWindow", "Who am I?"))
        self.actionabout.setText(_translate("MainWindow", "about"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
