# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI_QT.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1117, 771)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.gridLayout.setObjectName("gridLayout")
        self.MainGrid = QtWidgets.QGridLayout()
        self.MainGrid.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.MainGrid.setContentsMargins(0, -1, -1, -1)
        self.MainGrid.setObjectName("MainGrid")
        self.pushButton_check_threads = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_check_threads.setStyleSheet("")
        self.pushButton_check_threads.setObjectName("pushButton_check_threads")
        self.MainGrid.addWidget(self.pushButton_check_threads, 1, 3, 1, 1)
        self.plainTextEdit_info = QtWidgets.QPlainTextEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.plainTextEdit_info.setFont(font)
        self.plainTextEdit_info.setStyleSheet("background-color: rgb(220, 220, 220);\n"
"\n"
"")
        self.plainTextEdit_info.setFrameShape(QtWidgets.QFrame.Panel)
        self.plainTextEdit_info.setFrameShadow(QtWidgets.QFrame.Plain)
        self.plainTextEdit_info.setLineWidth(1)
        self.plainTextEdit_info.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.plainTextEdit_info.setObjectName("plainTextEdit_info")
        self.MainGrid.addWidget(self.plainTextEdit_info, 1, 0, 2, 2)
        self.pushButton_clear_log = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_clear_log.setStyleSheet("background-color: qlineargradient(spread:reflect, x1:0.5, y1:0.5, x2:0, y2:0.028, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(255, 144, 144, 255));")
        self.pushButton_clear_log.setObjectName("pushButton_clear_log")
        self.MainGrid.addWidget(self.pushButton_clear_log, 1, 4, 1, 1)
        self.textEdit_log = QtWidgets.QTextEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.textEdit_log.setFont(font)
        self.textEdit_log.setFrameShape(QtWidgets.QFrame.Box)
        self.textEdit_log.setFrameShadow(QtWidgets.QFrame.Raised)
        self.textEdit_log.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.textEdit_log.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.textEdit_log.setLineWrapColumnOrWidth(0)
        self.textEdit_log.setObjectName("textEdit_log")
        self.MainGrid.addWidget(self.textEdit_log, 2, 2, 1, 3)
        self.pushButton_Info_screenLog = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Info_screenLog.setStyleSheet("")
        self.pushButton_Info_screenLog.setObjectName("pushButton_Info_screenLog")
        self.MainGrid.addWidget(self.pushButton_Info_screenLog, 1, 2, 1, 1)
        self.treeView = QtWidgets.QTreeView(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.treeView.setFont(font)
        self.treeView.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.treeView.setObjectName("treeView")
        self.MainGrid.addWidget(self.treeView, 0, 2, 1, 3)
        self.DisplayTweetsGrid = QtWidgets.QGridLayout()
        self.DisplayTweetsGrid.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.DisplayTweetsGrid.setSpacing(5)
        self.DisplayTweetsGrid.setObjectName("DisplayTweetsGrid")
        self.pushButton_reload_DF = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_reload_DF.setObjectName("pushButton_reload_DF")
        self.DisplayTweetsGrid.addWidget(self.pushButton_reload_DF, 2, 0, 1, 2)
        self.pushButton_PreviousTweet = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_PreviousTweet.setObjectName("pushButton_PreviousTweet")
        self.DisplayTweetsGrid.addWidget(self.pushButton_PreviousTweet, 12, 0, 1, 1)
        self.pushButton_showTweets = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_showTweets.setStyleSheet("")
        self.pushButton_showTweets.setObjectName("pushButton_showTweets")
        self.DisplayTweetsGrid.addWidget(self.pushButton_showTweets, 3, 0, 1, 2)
        self.checkBox_HideEmptyValues = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_HideEmptyValues.setChecked(True)
        self.checkBox_HideEmptyValues.setObjectName("checkBox_HideEmptyValues")
        self.DisplayTweetsGrid.addWidget(self.checkBox_HideEmptyValues, 10, 0, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.DisplayTweetsGrid.addItem(spacerItem, 4, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.DisplayTweetsGrid.addItem(spacerItem1, 0, 0, 1, 1)
        self.pushButton_NextTweet = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_NextTweet.setObjectName("pushButton_NextTweet")
        self.DisplayTweetsGrid.addWidget(self.pushButton_NextTweet, 12, 1, 1, 1)
        self.pushButton_ShowTweet = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_ShowTweet.setObjectName("pushButton_ShowTweet")
        self.DisplayTweetsGrid.addWidget(self.pushButton_ShowTweet, 11, 0, 1, 2)
        self.pushButton_JumpToTweet = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_JumpToTweet.setObjectName("pushButton_JumpToTweet")
        self.DisplayTweetsGrid.addWidget(self.pushButton_JumpToTweet, 13, 0, 1, 1)
        self.checkBox_DisplayShortUserinfo = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_DisplayShortUserinfo.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.checkBox_DisplayShortUserinfo.setAutoFillBackground(False)
        self.checkBox_DisplayShortUserinfo.setChecked(True)
        self.checkBox_DisplayShortUserinfo.setObjectName("checkBox_DisplayShortUserinfo")
        self.DisplayTweetsGrid.addWidget(self.checkBox_DisplayShortUserinfo, 9, 0, 1, 2)
        self.lineEdit_JumpToTweet = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_JumpToTweet.setObjectName("lineEdit_JumpToTweet")
        self.DisplayTweetsGrid.addWidget(self.lineEdit_JumpToTweet, 13, 1, 1, 1)
        self.pushButton_load_selected_csv_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_load_selected_csv_2.setObjectName("pushButton_load_selected_csv_2")
        self.DisplayTweetsGrid.addWidget(self.pushButton_load_selected_csv_2, 1, 0, 1, 2)
        self.checkBox_DisplayShortQuoteStatus = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_DisplayShortQuoteStatus.setChecked(True)
        self.checkBox_DisplayShortQuoteStatus.setObjectName("checkBox_DisplayShortQuoteStatus")
        self.DisplayTweetsGrid.addWidget(self.checkBox_DisplayShortQuoteStatus, 8, 0, 1, 2)
        self.DisplayTweetsGrid.setColumnStretch(0, 1)
        self.MainGrid.addLayout(self.DisplayTweetsGrid, 0, 1, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setToolTip("")
        self.tabWidget.setToolTipDuration(-1)
        self.tabWidget.setObjectName("tabWidget")
        self.Files = QtWidgets.QWidget()
        self.Files.setObjectName("Files")
        self.pushButton_delete100 = QtWidgets.QPushButton(self.Files)
        self.pushButton_delete100.setGeometry(QtCore.QRect(10, 180, 91, 21))
        self.pushButton_delete100.setToolTipDuration(-1)
        self.pushButton_delete100.setObjectName("pushButton_delete100")
        self.pushButton_deleteSelected = QtWidgets.QPushButton(self.Files)
        self.pushButton_deleteSelected.setGeometry(QtCore.QRect(10, 240, 91, 23))
        self.pushButton_deleteSelected.setStyleSheet("background-color: qlineargradient(spread:reflect, x1:0.5, y1:0.5, x2:0, y2:0.028, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(255, 144, 144, 255));")
        self.pushButton_deleteSelected.setObjectName("pushButton_deleteSelected")
        self.pushButton_delete500 = QtWidgets.QPushButton(self.Files)
        self.pushButton_delete500.setGeometry(QtCore.QRect(10, 210, 91, 21))
        self.pushButton_delete500.setToolTipDuration(-1)
        self.pushButton_delete500.setObjectName("pushButton_delete500")
        self.pushButton_merge_selected = QtWidgets.QPushButton(self.Files)
        self.pushButton_merge_selected.setGeometry(QtCore.QRect(10, 40, 91, 23))
        self.pushButton_merge_selected.setToolTipDuration(-1)
        self.pushButton_merge_selected.setObjectName("pushButton_merge_selected")
        self.frame = QtWidgets.QFrame(self.Files)
        self.frame.setGeometry(QtCore.QRect(0, 150, 111, 121))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame.setObjectName("frame")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(30, 10, 47, 13))
        self.label_3.setObjectName("label_3")
        self.pushButton_load_selected_csv = QtWidgets.QPushButton(self.Files)
        self.pushButton_load_selected_csv.setGeometry(QtCore.QRect(10, 10, 91, 23))
        self.pushButton_load_selected_csv.setObjectName("pushButton_load_selected_csv")
        self.frame.raise_()
        self.pushButton_delete100.raise_()
        self.pushButton_deleteSelected.raise_()
        self.pushButton_delete500.raise_()
        self.pushButton_merge_selected.raise_()
        self.pushButton_load_selected_csv.raise_()
        self.tabWidget.addTab(self.Files, "")
        self.Request = QtWidgets.QWidget()
        self.Request.setObjectName("Request")
        self.pushButton_collect1 = QtWidgets.QPushButton(self.Request)
        self.pushButton_collect1.setGeometry(QtCore.QRect(10, 10, 141, 23))
        self.pushButton_collect1.setObjectName("pushButton_collect1")
        self.pushButton_collect10 = QtWidgets.QPushButton(self.Request)
        self.pushButton_collect10.setGeometry(QtCore.QRect(10, 40, 141, 23))
        self.pushButton_collect10.setObjectName("pushButton_collect10")
        self.label = QtWidgets.QLabel(self.Request)
        self.label.setGeometry(QtCore.QRect(220, 10, 81, 21))
        self.label.setObjectName("label")
        self.label_login_status = QtWidgets.QLabel(self.Request)
        self.label_login_status.setGeometry(QtCore.QRect(220, 40, 91, 21))
        self.label_login_status.setMouseTracking(False)
        self.label_login_status.setStyleSheet("background-color: rgb(255, 149, 151);\n"
"color: rgb(255, 255, 255);")
        self.label_login_status.setAlignment(QtCore.Qt.AlignCenter)
        self.label_login_status.setObjectName("label_login_status")
        self.pushButton_11111111111111 = QtWidgets.QPushButton(self.Request)
        self.pushButton_11111111111111.setGeometry(QtCore.QRect(10, 70, 141, 23))
        self.pushButton_11111111111111.setObjectName("pushButton_11111111111111")
        self.pushButton_Request_Status = QtWidgets.QPushButton(self.Request)
        self.pushButton_Request_Status.setGeometry(QtCore.QRect(10, 100, 141, 23))
        self.pushButton_Request_Status.setObjectName("pushButton_Request_Status")
        self.lineEdit_request_statusId = QtWidgets.QLineEdit(self.Request)
        self.lineEdit_request_statusId.setGeometry(QtCore.QRect(160, 100, 151, 23))
        self.lineEdit_request_statusId.setObjectName("lineEdit_request_statusId")
        self.tabWidget.addTab(self.Request, "")
        self.PrepareData = QtWidgets.QWidget()
        self.PrepareData.setObjectName("PrepareData")
        self.pushButton_export_DF = QtWidgets.QPushButton(self.PrepareData)
        self.pushButton_export_DF.setGeometry(QtCore.QRect(10, 10, 91, 23))
        self.pushButton_export_DF.setObjectName("pushButton_export_DF")
        self.lineEdit_DF_comment = QtWidgets.QLineEdit(self.PrepareData)
        self.lineEdit_DF_comment.setGeometry(QtCore.QRect(110, 10, 133, 23))
        self.lineEdit_DF_comment.setObjectName("lineEdit_DF_comment")
        self.pushButton_export_DF_7 = QtWidgets.QPushButton(self.PrepareData)
        self.pushButton_export_DF_7.setGeometry(QtCore.QRect(10, 40, 91, 23))
        self.pushButton_export_DF_7.setObjectName("pushButton_export_DF_7")
        self.lineEdit_DF_comment_3 = QtWidgets.QLineEdit(self.PrepareData)
        self.lineEdit_DF_comment_3.setGeometry(QtCore.QRect(110, 40, 31, 23))
        self.lineEdit_DF_comment_3.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_DF_comment_3.setObjectName("lineEdit_DF_comment_3")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.PrepareData)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(10, 70, 371, 271))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.Vertical_Filters = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.Vertical_Filters.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.Vertical_Filters.setContentsMargins(0, 0, 0, 0)
        self.Vertical_Filters.setSpacing(8)
        self.Vertical_Filters.setObjectName("Vertical_Filters")
        self.gridLayout_DataFilters = QtWidgets.QGridLayout()
        self.gridLayout_DataFilters.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.gridLayout_DataFilters.setSpacing(5)
        self.gridLayout_DataFilters.setObjectName("gridLayout_DataFilters")
        self.pushButton_FilterDF_Lang_Polish = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.pushButton_FilterDF_Lang_Polish.setObjectName("pushButton_FilterDF_Lang_Polish")
        self.gridLayout_DataFilters.addWidget(self.pushButton_FilterDF_Lang_Polish, 1, 2, 1, 1)
        self.pushButton_FilterDF_TweetID = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.pushButton_FilterDF_TweetID.setToolTip("")
        self.pushButton_FilterDF_TweetID.setObjectName("pushButton_FilterDF_TweetID")
        self.gridLayout_DataFilters.addWidget(self.pushButton_FilterDF_TweetID, 1, 1, 1, 1)
        self.pushButton_FilterDF_by_NonEmptyKey = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.pushButton_FilterDF_by_NonEmptyKey.setObjectName("pushButton_FilterDF_by_NonEmptyKey")
        self.gridLayout_DataFilters.addWidget(self.pushButton_FilterDF_by_NonEmptyKey, 3, 3, 1, 1)
        self.pushButton_export_DF_6 = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.pushButton_export_DF_6.setToolTip("")
        self.pushButton_export_DF_6.setObjectName("pushButton_export_DF_6")
        self.gridLayout_DataFilters.addWidget(self.pushButton_export_DF_6, 1, 0, 1, 1)
        self.lineEdit_FilterLangOther = QtWidgets.QLineEdit(self.verticalLayoutWidget_3)
        self.lineEdit_FilterLangOther.setObjectName("lineEdit_FilterLangOther")
        self.gridLayout_DataFilters.addWidget(self.lineEdit_FilterLangOther, 4, 2, 1, 1)
        self.pushButton_export_DF_11 = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.pushButton_export_DF_11.setToolTip("")
        self.pushButton_export_DF_11.setObjectName("pushButton_export_DF_11")
        self.gridLayout_DataFilters.addWidget(self.pushButton_export_DF_11, 3, 1, 1, 1)
        self.lineEdit_DF_comment_5 = QtWidgets.QLineEdit(self.verticalLayoutWidget_3)
        self.lineEdit_DF_comment_5.setObjectName("lineEdit_DF_comment_5")
        self.gridLayout_DataFilters.addWidget(self.lineEdit_DF_comment_5, 4, 1, 1, 1)
        self.lineEdit_DF_comment_7 = QtWidgets.QLineEdit(self.verticalLayoutWidget_3)
        self.lineEdit_DF_comment_7.setObjectName("lineEdit_DF_comment_7")
        self.gridLayout_DataFilters.addWidget(self.lineEdit_DF_comment_7, 4, 0, 1, 1)
        self.pushButton_FilterDF_Lang_English = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.pushButton_FilterDF_Lang_English.setObjectName("pushButton_FilterDF_Lang_English")
        self.gridLayout_DataFilters.addWidget(self.pushButton_FilterDF_Lang_English, 2, 2, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        self.gridLayout_DataFilters.addItem(spacerItem2, 5, 1, 1, 1)
        self.pushButton_FilterDF_Lang_Other = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.pushButton_FilterDF_Lang_Other.setObjectName("pushButton_FilterDF_Lang_Other")
        self.gridLayout_DataFilters.addWidget(self.pushButton_FilterDF_Lang_Other, 3, 2, 1, 1)
        self.pushButton_export_DF_9 = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.pushButton_export_DF_9.setToolTip("")
        self.pushButton_export_DF_9.setObjectName("pushButton_export_DF_9")
        self.gridLayout_DataFilters.addWidget(self.pushButton_export_DF_9, 3, 0, 1, 1)
        self.lineEdit_filterKeyinput = QtWidgets.QLineEdit(self.verticalLayoutWidget_3)
        self.lineEdit_filterKeyinput.setObjectName("lineEdit_filterKeyinput")
        self.gridLayout_DataFilters.addWidget(self.lineEdit_filterKeyinput, 4, 3, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout_DataFilters.addWidget(self.label_6, 0, 0, 1, 4)
        self.lineEdit_tweet_id = QtWidgets.QLineEdit(self.verticalLayoutWidget_3)
        self.lineEdit_tweet_id.setObjectName("lineEdit_tweet_id")
        self.gridLayout_DataFilters.addWidget(self.lineEdit_tweet_id, 2, 1, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.verticalLayoutWidget_3)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout_DataFilters.addWidget(self.lineEdit_2, 2, 0, 1, 1)
        self.gridLayout_DataFilters.setColumnStretch(0, 2)
        self.gridLayout_DataFilters.setRowStretch(0, 1)
        self.Vertical_Filters.addLayout(self.gridLayout_DataFilters)
        self.gridLayout_TimeFilters = QtWidgets.QGridLayout()
        self.gridLayout_TimeFilters.setHorizontalSpacing(5)
        self.gridLayout_TimeFilters.setVerticalSpacing(2)
        self.gridLayout_TimeFilters.setObjectName("gridLayout_TimeFilters")
        self.pushButton_filter_by_Age = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.pushButton_filter_by_Age.setObjectName("pushButton_filter_by_Age")
        self.gridLayout_TimeFilters.addWidget(self.pushButton_filter_by_Age, 1, 0, 1, 1)
        self.pushButton_export_DF_18 = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.pushButton_export_DF_18.setObjectName("pushButton_export_DF_18")
        self.gridLayout_TimeFilters.addWidget(self.pushButton_export_DF_18, 0, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_10.setFont(font)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.gridLayout_TimeFilters.addWidget(self.label_10, 1, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout_TimeFilters.addWidget(self.label_5, 2, 3, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.gridLayout_TimeFilters.addWidget(self.label_9, 0, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout_TimeFilters.addWidget(self.label_4, 2, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout_TimeFilters.addWidget(self.label_7, 2, 4, 1, 1)
        self.spinBox_timefilter_from_day = QtWidgets.QSpinBox(self.verticalLayoutWidget_3)
        self.spinBox_timefilter_from_day.setMaximum(365)
        self.spinBox_timefilter_from_day.setObjectName("spinBox_timefilter_from_day")
        self.gridLayout_TimeFilters.addWidget(self.spinBox_timefilter_from_day, 0, 2, 1, 1)
        self.spinBox_timefilter_from_hour = QtWidgets.QSpinBox(self.verticalLayoutWidget_3)
        self.spinBox_timefilter_from_hour.setMaximum(24)
        self.spinBox_timefilter_from_hour.setObjectName("spinBox_timefilter_from_hour")
        self.gridLayout_TimeFilters.addWidget(self.spinBox_timefilter_from_hour, 0, 3, 1, 1)
        self.spinBox_timefilter_to_hour = QtWidgets.QSpinBox(self.verticalLayoutWidget_3)
        self.spinBox_timefilter_to_hour.setMaximum(24)
        self.spinBox_timefilter_to_hour.setObjectName("spinBox_timefilter_to_hour")
        self.gridLayout_TimeFilters.addWidget(self.spinBox_timefilter_to_hour, 1, 3, 1, 1)
        self.spinBox_timefilter_to_day = QtWidgets.QSpinBox(self.verticalLayoutWidget_3)
        self.spinBox_timefilter_to_day.setMaximum(365)
        self.spinBox_timefilter_to_day.setObjectName("spinBox_timefilter_to_day")
        self.gridLayout_TimeFilters.addWidget(self.spinBox_timefilter_to_day, 1, 2, 1, 1)
        self.spinBox_timefilter_to_min = QtWidgets.QSpinBox(self.verticalLayoutWidget_3)
        self.spinBox_timefilter_to_min.setMaximum(60)
        self.spinBox_timefilter_to_min.setProperty("value", 10)
        self.spinBox_timefilter_to_min.setObjectName("spinBox_timefilter_to_min")
        self.gridLayout_TimeFilters.addWidget(self.spinBox_timefilter_to_min, 1, 4, 1, 1)
        self.spinBox_timefilter_from_min = QtWidgets.QSpinBox(self.verticalLayoutWidget_3)
        self.spinBox_timefilter_from_min.setMaximum(60)
        self.spinBox_timefilter_from_min.setObjectName("spinBox_timefilter_from_min")
        self.gridLayout_TimeFilters.addWidget(self.spinBox_timefilter_from_min, 0, 4, 1, 1)
        self.gridLayout_TimeFilters.setRowMinimumHeight(0, 5)
        self.gridLayout_TimeFilters.setRowMinimumHeight(1, 5)
        self.gridLayout_TimeFilters.setRowMinimumHeight(2, 5)
        self.gridLayout_TimeFilters.setColumnStretch(0, 2)
        self.gridLayout_TimeFilters.setColumnStretch(1, 1)
        self.gridLayout_TimeFilters.setColumnStretch(2, 1)
        self.gridLayout_TimeFilters.setColumnStretch(3, 1)
        self.gridLayout_TimeFilters.setColumnStretch(4, 1)
        self.gridLayout_TimeFilters.setRowStretch(0, 1)
        self.gridLayout_TimeFilters.setRowStretch(1, 1)
        self.gridLayout_TimeFilters.setRowStretch(2, 1)
        self.Vertical_Filters.addLayout(self.gridLayout_TimeFilters)
        spacerItem3 = QtWidgets.QSpacerItem(0, 15, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.Vertical_Filters.addItem(spacerItem3)
        self.Vertical_Filters.setStretch(0, 1)
        self.Vertical_Filters.setStretch(1, 1)
        self.tabWidget.addTab(self.PrepareData, "")
        self.Analyze = QtWidgets.QWidget()
        self.Analyze.setObjectName("Analyze")
        self.tabWidget.addTab(self.Analyze, "")
        self.Model = QtWidgets.QWidget()
        self.Model.setObjectName("Model")
        self.tabWidget.addTab(self.Model, "")
        self.MainGrid.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.MainGrid.setColumnMinimumWidth(0, 400)
        self.MainGrid.setColumnMinimumWidth(1, 100)
        self.MainGrid.setColumnMinimumWidth(2, 150)
        self.MainGrid.setColumnMinimumWidth(3, 150)
        self.MainGrid.setColumnMinimumWidth(4, 150)
        self.MainGrid.setRowMinimumHeight(0, 370)
        self.MainGrid.setRowMinimumHeight(1, 20)
        self.MainGrid.setRowMinimumHeight(2, 300)
        self.MainGrid.setColumnStretch(0, 3)
        self.MainGrid.setColumnStretch(2, 1)
        self.MainGrid.setColumnStretch(3, 1)
        self.MainGrid.setColumnStretch(4, 1)
        self.MainGrid.setRowStretch(0, 1)
        self.MainGrid.setRowStretch(2, 2)
        self.gridLayout.addLayout(self.MainGrid, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1117, 22))
        self.menubar.setObjectName("menubar")
        self.actionMenuAuth = QtWidgets.QMenu(self.menubar)
        self.actionMenuAuth.setObjectName("actionMenuAuth")
        self.actionMenuRefresh_Gui = QtWidgets.QMenu(self.menubar)
        self.actionMenuRefresh_Gui.setObjectName("actionMenuRefresh_Gui")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionLogin = QtWidgets.QAction(MainWindow)
        self.actionLogin.setObjectName("actionLogin")
        self.actionRefresh_GUI = QtWidgets.QAction(MainWindow)
        self.actionRefresh_GUI.setObjectName("actionRefresh_GUI")
        self.actionWho_am_I = QtWidgets.QAction(MainWindow)
        self.actionWho_am_I.setObjectName("actionWho_am_I")
        self.actionTweet_Description = QtWidgets.QAction(MainWindow)
        self.actionTweet_Description.setObjectName("actionTweet_Description")
        self.actionMenuAuth.addAction(self.actionLogin)
        self.actionMenuAuth.addAction(self.actionWho_am_I)
        self.actionMenuRefresh_Gui.addAction(self.actionRefresh_GUI)
        self.menuHelp.addAction(self.actionTweet_Description)
        self.menubar.addAction(self.actionMenuAuth.menuAction())
        self.menubar.addAction(self.actionMenuRefresh_Gui.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_check_threads.setToolTip(_translate("MainWindow", "Check currently runing threads and print status."))
        self.pushButton_check_threads.setText(_translate("MainWindow", "Check Threads"))
        self.plainTextEdit_info.setPlainText(_translate("MainWindow", "None"))
        self.pushButton_clear_log.setText(_translate("MainWindow", "Clear Log"))
        self.textEdit_log.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8.25pt;\"><br /></p></body></html>"))
        self.pushButton_Info_screenLog.setText(_translate("MainWindow", "Copy info To Log ->"))
        self.pushButton_reload_DF.setToolTip(_translate("MainWindow", "Reload DF from the same files again."))
        self.pushButton_reload_DF.setText(_translate("MainWindow", "Reload DF"))
        self.pushButton_PreviousTweet.setToolTip(_translate("MainWindow", "Show previous Tweet from DF"))
        self.pushButton_PreviousTweet.setText(_translate("MainWindow", "<< Prev"))
        self.pushButton_showTweets.setToolTip(_translate("MainWindow", "Shows currently loaded DF"))
        self.pushButton_showTweets.setText(_translate("MainWindow", "DF Info"))
        self.checkBox_HideEmptyValues.setText(_translate("MainWindow", "Hide empty values"))
        self.pushButton_NextTweet.setToolTip(_translate("MainWindow", "Show next Tweet from DF"))
        self.pushButton_NextTweet.setText(_translate("MainWindow", "Next >>"))
        self.pushButton_ShowTweet.setToolTip(_translate("MainWindow", "Show first Tweet from DF"))
        self.pushButton_ShowTweet.setText(_translate("MainWindow", "Show Tweet"))
        self.pushButton_JumpToTweet.setToolTip(_translate("MainWindow", "Jumps to Tweet in DF, define index in box."))
        self.pushButton_JumpToTweet.setText(_translate("MainWindow", "Jump"))
        self.checkBox_DisplayShortUserinfo.setText(_translate("MainWindow", "Short user info"))
        self.lineEdit_JumpToTweet.setToolTip(_translate("MainWindow", "Input index for Jump button."))
        self.pushButton_load_selected_csv_2.setToolTip(_translate("MainWindow", "Loads files from tree."))
        self.pushButton_load_selected_csv_2.setText(_translate("MainWindow", "Load selected"))
        self.checkBox_DisplayShortQuoteStatus.setText(_translate("MainWindow", "Short quote and retweet"))
        self.pushButton_delete100.setToolTip(_translate("MainWindow", "Delete CSV files that have less than 100 Tweets"))
        self.pushButton_delete100.setText(_translate("MainWindow", "Delete < 100"))
        self.pushButton_deleteSelected.setToolTip(_translate("MainWindow", "Delete files selected in Tree"))
        self.pushButton_deleteSelected.setText(_translate("MainWindow", "Delete Selected"))
        self.pushButton_delete500.setToolTip(_translate("MainWindow", "Delete CSV files that have less than 500 Tweets"))
        self.pushButton_delete500.setText(_translate("MainWindow", "Delete < 500"))
        self.pushButton_merge_selected.setToolTip(_translate("MainWindow", "Merge Selected Files to new file."))
        self.pushButton_merge_selected.setText(_translate("MainWindow", "Merge Selected"))
        self.label_3.setText(_translate("MainWindow", "Cleanup:"))
        self.pushButton_load_selected_csv.setText(_translate("MainWindow", "Load selected"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Files), _translate("MainWindow", "Files"))
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.Files), _translate("MainWindow", "Manage Tweet Files in \'tweets\' directory"))
        self.pushButton_collect1.setText(_translate("MainWindow", "1 Chunk"))
        self.pushButton_collect10.setText(_translate("MainWindow", "10 Chunks : 10mins"))
        self.label.setText(_translate("MainWindow", "Logged in:"))
        self.label_login_status.setText(_translate("MainWindow", "Not logged in"))
        self.pushButton_11111111111111.setText(_translate("MainWindow", "Request parent Tweets"))
        self.pushButton_Request_Status.setToolTip(_translate("MainWindow", "Put Tweet id (status) number in box"))
        self.pushButton_Request_Status.setText(_translate("MainWindow", "Request tweet"))
        self.lineEdit_request_statusId.setToolTip(_translate("MainWindow", "Input index for Jump button."))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Request), _translate("MainWindow", "Request"))
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.Request), _translate("MainWindow", "Collect Tweets from tweeter"))
        self.pushButton_export_DF.setToolTip(_translate("MainWindow", "Save DF to .csv File"))
        self.pushButton_export_DF.setText(_translate("MainWindow", "Save DF"))
        self.lineEdit_DF_comment.setToolTip(_translate("MainWindow", "You can Add some comment to file name"))
        self.pushButton_export_DF_7.setToolTip(_translate("MainWindow", "Split DF into X pieces and saves."))
        self.pushButton_export_DF_7.setText(_translate("MainWindow", "Split DF"))
        self.lineEdit_DF_comment_3.setToolTip(_translate("MainWindow", "Number of pieces to split."))
        self.lineEdit_DF_comment_3.setText(_translate("MainWindow", "2"))
        self.pushButton_FilterDF_Lang_Polish.setToolTip(_translate("MainWindow", "Filter DF, polish"))
        self.pushButton_FilterDF_Lang_Polish.setText(_translate("MainWindow", "Lang PL"))
        self.pushButton_FilterDF_TweetID.setText(_translate("MainWindow", "TweetId"))
        self.pushButton_FilterDF_by_NonEmptyKey.setToolTip(_translate("MainWindow", "Filter Tweets with non empty fields. Display field in Help menu"))
        self.pushButton_FilterDF_by_NonEmptyKey.setText(_translate("MainWindow", "Non Empty"))
        self.pushButton_export_DF_6.setText(_translate("MainWindow", "User"))
        self.lineEdit_FilterLangOther.setToolTip(_translate("MainWindow", "input for Lang Button"))
        self.pushButton_export_DF_11.setText(_translate("MainWindow", "Words"))
        self.lineEdit_DF_comment_5.setToolTip(_translate("MainWindow", "You can Add some comment to file name"))
        self.lineEdit_DF_comment_7.setToolTip(_translate("MainWindow", "You can Add some comment to file name"))
        self.pushButton_FilterDF_Lang_English.setToolTip(_translate("MainWindow", "Filter DF, english"))
        self.pushButton_FilterDF_Lang_English.setText(_translate("MainWindow", "Lang En"))
        self.pushButton_FilterDF_Lang_Other.setToolTip(_translate("MainWindow", "Filter DF, put language below"))
        self.pushButton_FilterDF_Lang_Other.setText(_translate("MainWindow", "Lang"))
        self.pushButton_export_DF_9.setText(_translate("MainWindow", "Text"))
        self.lineEdit_filterKeyinput.setToolTip(_translate("MainWindow", "Key input"))
        self.label_6.setText(_translate("MainWindow", "- - - - Filter DF - - - - "))
        self.pushButton_filter_by_Age.setToolTip(_translate("MainWindow", "Save DF to .csv File"))
        self.pushButton_filter_by_Age.setText(_translate("MainWindow", "Age"))
        self.pushButton_export_DF_18.setToolTip(_translate("MainWindow", "Save DF to .csv File"))
        self.pushButton_export_DF_18.setText(_translate("MainWindow", "Posting Time"))
        self.label_10.setText(_translate("MainWindow", "to:"))
        self.label_5.setText(_translate("MainWindow", "Hour"))
        self.label_9.setText(_translate("MainWindow", "from:"))
        self.label_4.setText(_translate("MainWindow", "Day"))
        self.label_7.setText(_translate("MainWindow", "Min"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.PrepareData), _translate("MainWindow", "Prepare Data"))
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.PrepareData), _translate("MainWindow", "Analyze loaded DF"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Analyze), _translate("MainWindow", "Analyze"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Model), _translate("MainWindow", "NN Model"))
        self.actionMenuAuth.setTitle(_translate("MainWindow", "Auth"))
        self.actionMenuRefresh_Gui.setTitle(_translate("MainWindow", "GUI"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionLogin.setText(_translate("MainWindow", "Login"))
        self.actionRefresh_GUI.setText(_translate("MainWindow", "Refresh"))
        self.actionWho_am_I.setText(_translate("MainWindow", "Who am I?"))
        self.actionTweet_Description.setText(_translate("MainWindow", "Tweet Description"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

