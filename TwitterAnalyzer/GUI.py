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
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 431, 351))
        self.tabWidget.setToolTip("")
        self.tabWidget.setToolTipDuration(-1)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.pushButton_collect1 = QtWidgets.QPushButton(self.tab)
        self.pushButton_collect1.setGeometry(QtCore.QRect(10, 10, 141, 23))
        self.pushButton_collect1.setObjectName("pushButton_collect1")
        self.pushButton_collect10 = QtWidgets.QPushButton(self.tab)
        self.pushButton_collect10.setGeometry(QtCore.QRect(10, 40, 141, 23))
        self.pushButton_collect10.setObjectName("pushButton_collect10")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(260, 10, 81, 21))
        self.label.setObjectName("label")
        self.label_login_status = QtWidgets.QLabel(self.tab)
        self.label_login_status.setGeometry(QtCore.QRect(320, 10, 91, 21))
        self.label_login_status.setMouseTracking(False)
        self.label_login_status.setStyleSheet("background-color: rgb(255, 149, 151);\n"
"color: rgb(255, 255, 255);")
        self.label_login_status.setAlignment(QtCore.Qt.AlignCenter)
        self.label_login_status.setObjectName("label_login_status")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.pushButton_delete100 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_delete100.setGeometry(QtCore.QRect(10, 230, 91, 21))
        self.pushButton_delete100.setToolTipDuration(-1)
        self.pushButton_delete100.setObjectName("pushButton_delete100")
        self.pushButton_deleteSelected = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_deleteSelected.setGeometry(QtCore.QRect(10, 290, 91, 23))
        self.pushButton_deleteSelected.setStyleSheet("background-color: qlineargradient(spread:reflect, x1:0.5, y1:0.5, x2:0, y2:0.028, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(255, 144, 144, 255));")
        self.pushButton_deleteSelected.setObjectName("pushButton_deleteSelected")
        self.pushButton_delete500 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_delete500.setGeometry(QtCore.QRect(10, 260, 91, 21))
        self.pushButton_delete500.setToolTipDuration(-1)
        self.pushButton_delete500.setObjectName("pushButton_delete500")
        self.pushButton_merge_selected = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_merge_selected.setGeometry(QtCore.QRect(10, 10, 91, 21))
        self.pushButton_merge_selected.setToolTipDuration(-1)
        self.pushButton_merge_selected.setObjectName("pushButton_merge_selected")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.pushButton_load_selected_csv = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_load_selected_csv.setGeometry(QtCore.QRect(10, 10, 81, 23))
        self.pushButton_load_selected_csv.setObjectName("pushButton_load_selected_csv")
        self.pushButton_export_DF = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_export_DF.setGeometry(QtCore.QRect(10, 40, 81, 23))
        self.pushButton_export_DF.setObjectName("pushButton_export_DF")
        self.tabWidget.addTab(self.tab_3, "")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 370, 91, 16))
        self.label_2.setObjectName("label_2")
        self.treeView = QtWidgets.QTreeView(self.centralwidget)
        self.treeView.setGeometry(QtCore.QRect(460, 30, 481, 361))
        self.treeView.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.treeView.setObjectName("treeView")
        self.plainTextEdit_info = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_info.setGeometry(QtCore.QRect(10, 400, 481, 311))
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.plainTextEdit_info.setFont(font)
        self.plainTextEdit_info.setStyleSheet("background-color: rgb(220, 220, 220);\n"
"\n"
"")
        self.plainTextEdit_info.setFrameShape(QtWidgets.QFrame.Panel)
        self.plainTextEdit_info.setFrameShadow(QtWidgets.QFrame.Plain)
        self.plainTextEdit_info.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.plainTextEdit_info.setObjectName("plainTextEdit_info")
        self.textEdit_log = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_log.setGeometry(QtCore.QRect(510, 440, 431, 271))
        self.textEdit_log.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.textEdit_log.setLineWrapMode(QtWidgets.QTextEdit.WidgetWidth)
        self.textEdit_log.setLineWrapColumnOrWidth(0)
        self.textEdit_log.setObjectName("textEdit_log")
        self.pushButton_clear_log = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_clear_log.setGeometry(QtCore.QRect(860, 410, 81, 23))
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
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_collect1.setText(_translate("MainWindow", "1 Chunk"))
        self.pushButton_collect10.setText(_translate("MainWindow", "10 Chunks : 10mins"))
        self.label.setText(_translate("MainWindow", "Logged in:"))
        self.label_login_status.setText(_translate("MainWindow", "Not logged in"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Collect"))
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Collect Tweets from tweeter"))
        self.pushButton_delete100.setToolTip(_translate("MainWindow", "Delete CSV files that have less than 100 Tweets"))
        self.pushButton_delete100.setText(_translate("MainWindow", "Delete < 100"))
        self.pushButton_deleteSelected.setToolTip(_translate("MainWindow", "Delete files selected in Tree"))
        self.pushButton_deleteSelected.setText(_translate("MainWindow", "Delete Selected"))
        self.pushButton_delete500.setToolTip(_translate("MainWindow", "Delete CSV files that have less than 500 Tweets"))
        self.pushButton_delete500.setText(_translate("MainWindow", "Delete < 500"))
        self.pushButton_merge_selected.setToolTip(_translate("MainWindow", "Merge Selected Files to new file."))
        self.pushButton_merge_selected.setText(_translate("MainWindow", "Merge Selected"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Manage"))
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Manage Tweet Files in \'tweets\' directory"))
        self.pushButton_load_selected_csv.setText(_translate("MainWindow", "Load selected"))
        self.pushButton_export_DF.setToolTip(_translate("MainWindow", "Save DF to .csv File"))
        self.pushButton_export_DF.setText(_translate("MainWindow", "Save DF"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Analyze CSV"))
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Analyze loaded DF"))
        self.label_2.setText(_translate("MainWindow", "Current info:"))
        self.plainTextEdit_info.setPlainText(_translate("MainWindow", "None"))
        self.textEdit_log.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
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
