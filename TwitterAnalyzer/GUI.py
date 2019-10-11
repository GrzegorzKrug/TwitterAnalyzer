# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(370, 40, 361, 241))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setGeometry(QtCore.QRect(10, 10, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.tab)
        self.pushButton_2.setGeometry(QtCore.QRect(120, 10, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 81, 31))
        self.label.setObjectName("label")
        self.label_login_status = QtWidgets.QLabel(self.centralwidget)
        self.label_login_status.setGeometry(QtCore.QRect(100, 10, 81, 31))
        self.label_login_status.setMouseTracking(False)
        self.label_login_status.setStyleSheet("background-color: rgb(255, 149, 151);\n"
"color: rgb(255, 255, 255);")
        self.label_login_status.setAlignment(QtCore.Qt.AlignCenter)
        self.label_login_status.setObjectName("label_login_status")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 91, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 60, 201, 261))
        self.label_3.setAutoFillBackground(False)
        self.label_3.setStyleSheet("background-color: rgb(220, 220, 220);\n"
"\n"
"")
        self.label_3.setObjectName("label_3")
        self.treeView = QtWidgets.QTreeView(self.centralwidget)
        self.treeView.setGeometry(QtCore.QRect(30, 350, 256, 192))
        self.treeView.setObjectName("treeView")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
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
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_2.setText(_translate("MainWindow", "PushButton"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))
        self.label.setText(_translate("MainWindow", "Logged in:"))
        self.label_login_status.setText(_translate("MainWindow", "Not logged in"))
        self.label_2.setText(_translate("MainWindow", "Current user info:"))
        self.label_3.setText(_translate("MainWindow", "ABC"))
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
