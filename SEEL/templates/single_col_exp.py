# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'single_col_exp.ui'
#
# Created: Thu Feb 25 15:38:17 2016
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(434, 667)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        MainWindow.setStyleSheet(_fromUtf8("QPushButton{\n"
"color: #333;\n"
"border: 2px solid #555;\n"
"border-radius: 11px;\n"
"padding: 5px;\n"
"background: qradialgradient(cx: 0.3, cy: -0.4,\n"
"fx: 0.3, fy: -0.4,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #888);\n"
"min-width: 80px;\n"
"}\n"
"\n"
"QTabWidget {\n"
"background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"stop: 0 #abe, stop: 0.7 #aba);\n"
"\n"
"}\n"
"\n"
"\n"
"QTabBar::tab{\n"
"color: #000;\n"
"border-top-left-radius: 5px;\n"
"border-bottom-left-radius: 5px;\n"
"padding-top: 15px;padding-bottom:15px;\n"
"background: qradialgradient(cx: 0.3, cy: -0.4,\n"
"fx: 0.3, fy: -0.4,\n"
"radius: 1.2, stop: 0 #fff, stop: 1 #aaa);\n"
"width: 30px;\n"
"font-size: 13px;\n"
"}\n"
"QTabBar::tab:selected {\n"
"color: #000;\n"
"border-top-left-radius: 20px;\n"
"border-bottom-left-radius: 5px;\n"
"background: qradialgradient(cx: 0.3, cy: -0.4,\n"
"fx: 0.3, fy: -0.4,\n"
"radius: 1.35, stop: 0 #fcc, stop: 1 #ccf);\n"
"}\n"
"\n"
"\n"
"\n"
"QPushButton:pressed {\n"
"background: qradialgradient(cx: 0.4, cy: -0.1,\n"
"fx: 0.4, fy: -0.1,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #ddd);\n"
"}\n"
"\n"
"QFrame.PeripheralCollection{\n"
"border-top-left-radius: 5px;\n"
"border-top-right-radius: 5px;\n"
"border: 1px solid black;\n"
"background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"stop: 0 #6af, stop: 0.1 #689);\n"
"}\n"
"QFrame.PeripheralCollection QLabel {\n"
"color: white;\n"
"font-weight: bold;\n"
"}\n"
"\n"
"\n"
"\n"
"QFrame.PeripheralCollectionInner {\n"
"background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"stop: 0 #abe, stop: 0.7 #aba);\n"
"border: none;\n"
"border-top: 1px solid black;\n"
"}\n"
"\n"
"QFrame.PeripheralCollectionInner QLabel{\n"
"color: black;\n"
"}\n"
"\n"
"QWidget.PeripheralCollectionInner {\n"
"background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"stop: 0 #abe, stop: 0.7 #aba);\n"
"border: none;\n"
"border-top: 1px solid black;\n"
"}\n"
"QTextBrowser{\n"
"background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"stop: 0 #cdf, stop: 0.7 #cdc);\n"
"}\n"
"\n"
"\n"
"QWidget.PeripheralCollectionInner {\n"
"background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"stop: 0 #abe, stop: 0.7 #aba);\n"
"border: none;\n"
"border-top: 1px solid black;\n"
"}\n"
"\n"
"QWidget.PeripheralCollectionInner QLabel{\n"
"color: black;\n"
"}\n"
"\n"
"#SCF1,#SCF2,#tab_4\n"
"{\n"
"background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"stop: 0 #abe, stop: 0.7 #aba);\n"
"}\n"
"\n"
"\n"
"\n"
"\n"
""))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setStyleSheet(_fromUtf8(""))
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setSpacing(3)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setTabPosition(QtGui.QTabWidget.West)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setMovable(False)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayout = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.frame = QtGui.QFrame(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setMargin(0)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.scrollArea_4 = QtGui.QScrollArea(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea_4.sizePolicy().hasHeightForWidth())
        self.scrollArea_4.setSizePolicy(sizePolicy)
        self.scrollArea_4.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.scrollArea_4.setStyleSheet(_fromUtf8(""))
        self.scrollArea_4.setWidgetResizable(True)
        self.scrollArea_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.scrollArea_4.setObjectName(_fromUtf8("scrollArea_4"))
        self.SCF1 = QtGui.QWidget()
        self.SCF1.setGeometry(QtCore.QRect(0, 0, 400, 444))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SCF1.sizePolicy().hasHeightForWidth())
        self.SCF1.setSizePolicy(sizePolicy)
        self.SCF1.setStyleSheet(_fromUtf8(""))
        self.SCF1.setObjectName(_fromUtf8("SCF1"))
        self.gridLayout_5 = QtGui.QGridLayout(self.SCF1)
        self.gridLayout_5.setMargin(0)
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.frame_5 = QtGui.QFrame(self.SCF1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy)
        self.frame_5.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_5.setObjectName(_fromUtf8("frame_5"))
        self.gridLayout_7 = QtGui.QGridLayout(self.frame_5)
        self.gridLayout_7.setSpacing(5)
        self.gridLayout_7.setContentsMargins(0, 5, 0, 0)
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.ExperimentLayout = QtGui.QGridLayout()
        self.ExperimentLayout.setMargin(5)
        self.ExperimentLayout.setSpacing(7)
        self.ExperimentLayout.setObjectName(_fromUtf8("ExperimentLayout"))
        self.gridLayout_7.addLayout(self.ExperimentLayout, 0, 0, 1, 1)
        self.gridLayout_5.addWidget(self.frame_5, 0, 0, 1, 1)
        self.gridLayout_5.setColumnStretch(0, 1)
        self.scrollArea_4.setWidget(self.SCF1)
        self.verticalLayout_4.addWidget(self.scrollArea_4)
        self.verticalLayout.addWidget(self.frame)
        self.frame_3 = QtGui.QFrame(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.frame_3)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setMargin(0)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.hintText = QtGui.QTextBrowser(self.frame_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hintText.sizePolicy().hasHeightForWidth())
        self.hintText.setSizePolicy(sizePolicy)
        self.hintText.setMinimumSize(QtCore.QSize(0, 30))
        self.hintText.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.hintText.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.hintText.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.hintText.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard|QtCore.Qt.LinksAccessibleByMouse)
        self.hintText.setObjectName(_fromUtf8("hintText"))
        self.verticalLayout_5.addWidget(self.hintText)
        self.verticalLayout.addWidget(self.frame_3)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.helpLayout = QtGui.QVBoxLayout(self.tab_2)
        self.helpLayout.setSpacing(0)
        self.helpLayout.setMargin(0)
        self.helpLayout.setObjectName(_fromUtf8("helpLayout"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tab_3)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.scrollArea_5 = QtGui.QScrollArea(self.tab_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea_5.sizePolicy().hasHeightForWidth())
        self.scrollArea_5.setSizePolicy(sizePolicy)
        self.scrollArea_5.setMinimumSize(QtCore.QSize(400, 0))
        self.scrollArea_5.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.scrollArea_5.setStyleSheet(_fromUtf8(""))
        self.scrollArea_5.setWidgetResizable(True)
        self.scrollArea_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.scrollArea_5.setObjectName(_fromUtf8("scrollArea_5"))
        self.SCF2 = QtGui.QWidget()
        self.SCF2.setGeometry(QtCore.QRect(0, 0, 402, 611))
        self.SCF2.setStyleSheet(_fromUtf8(""))
        self.SCF2.setObjectName(_fromUtf8("SCF2"))
        self.gridLayout_6 = QtGui.QGridLayout(self.SCF2)
        self.gridLayout_6.setMargin(0)
        self.gridLayout_6.setSpacing(0)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.frame_6 = QtGui.QFrame(self.SCF2)
        self.frame_6.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_6.setObjectName(_fromUtf8("frame_6"))
        self.gridLayout_8 = QtGui.QGridLayout(self.frame_6)
        self.gridLayout_8.setSpacing(5)
        self.gridLayout_8.setContentsMargins(0, 5, 0, 0)
        self.gridLayout_8.setObjectName(_fromUtf8("gridLayout_8"))
        self.WidgetLayout = QtGui.QGridLayout()
        self.WidgetLayout.setMargin(5)
        self.WidgetLayout.setSpacing(7)
        self.WidgetLayout.setObjectName(_fromUtf8("WidgetLayout"))
        self.gridLayout_8.addLayout(self.WidgetLayout, 0, 0, 1, 1)
        self.gridLayout_6.addWidget(self.frame_6, 0, 0, 1, 1)
        self.scrollArea_5.setWidget(self.SCF2)
        self.verticalLayout_3.addWidget(self.scrollArea_5)
        self.frame_2 = QtGui.QFrame(self.tab_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame_2)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButton = QtGui.QPushButton(self.frame_2)
        self.pushButton.setMinimumSize(QtCore.QSize(94, 0))
        self.pushButton.setMaximumSize(QtCore.QSize(50, 25))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)
        self.deviceCombo = QtGui.QComboBox(self.frame_2)
        self.deviceCombo.setObjectName(_fromUtf8("deviceCombo"))
        self.horizontalLayout.addWidget(self.deviceCombo)
        self.verticalLayout_3.addWidget(self.frame_2)
        self.tabWidget.addTab(self.tab_3, _fromUtf8(""))
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName(_fromUtf8("tab_4"))
        self.advancedControlsLayout = QtGui.QVBoxLayout(self.tab_4)
        self.advancedControlsLayout.setMargin(3)
        self.advancedControlsLayout.setObjectName(_fromUtf8("advancedControlsLayout"))
        self.tabWidget.addTab(self.tab_4, _fromUtf8(""))
        self.verticalLayout_2.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 434, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuUtilities = QtGui.QMenu(self.menubar)
        self.menuUtilities.setObjectName(_fromUtf8("menuUtilities"))
        self.menuColor_scheme = QtGui.QMenu(self.menuUtilities)
        self.menuColor_scheme.setObjectName(_fromUtf8("menuColor_scheme"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        self.menuLevel = QtGui.QMenu(self.menubar)
        self.menuLevel.setObjectName(_fromUtf8("menuLevel"))
        MainWindow.setMenuBar(self.menubar)
        self.actionIPython_Console = QtGui.QAction(MainWindow)
        self.actionIPython_Console.setObjectName(_fromUtf8("actionIPython_Console"))
        self.actionIPython = QtGui.QAction(MainWindow)
        self.actionIPython.setObjectName(_fromUtf8("actionIPython"))
        self.actionReset_Device = QtGui.QAction(MainWindow)
        self.actionReset_Device.setObjectName(_fromUtf8("actionReset_Device"))
        self.actionAbout_device = QtGui.QAction(MainWindow)
        self.actionAbout_device.setObjectName(_fromUtf8("actionAbout_device"))
        self.actionWhite = QtGui.QAction(MainWindow)
        self.actionWhite.setObjectName(_fromUtf8("actionWhite"))
        self.actionBlack = QtGui.QAction(MainWindow)
        self.actionBlack.setObjectName(_fromUtf8("actionBlack"))
        self.actionBasic = QtGui.QAction(MainWindow)
        self.actionBasic.setObjectName(_fromUtf8("actionBasic"))
        self.actionAdvanced = QtGui.QAction(MainWindow)
        self.actionAdvanced.setObjectName(_fromUtf8("actionAdvanced"))
        self.menuColor_scheme.addAction(self.actionWhite)
        self.menuColor_scheme.addAction(self.actionBlack)
        self.menuUtilities.addAction(self.actionReset_Device)
        self.menuUtilities.addAction(self.actionAbout_device)
        self.menuUtilities.addAction(self.menuColor_scheme.menuAction())
        self.menuLevel.addAction(self.actionBasic)
        self.menuLevel.addAction(self.actionAdvanced)
        self.menubar.addAction(self.menuUtilities.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menubar.addAction(self.menuLevel.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.actionIPython_Console, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.addConsole)
        QtCore.QObject.connect(self.actionIPython, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.ipythonHelp)
        QtCore.QObject.connect(self.actionReset_Device, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.resetDevice)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.selectDevice)
        QtCore.QObject.connect(self.actionAbout_device, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.launchAboutDevice)
        QtCore.QObject.connect(self.actionWhite, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.setColorSchemeWhite)
        QtCore.QObject.connect(self.actionBlack, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.setColorSchemeBlack)
        QtCore.QObject.connect(self.actionBasic, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.loadBasicExperiments)
        QtCore.QObject.connect(self.actionAdvanced, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.loadAdvancedExperiments)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "SEELablet: Control Panel", None))
        self.SCF1.setProperty("class", _translate("MainWindow", "PeripheralCollectionInner", None))
        self.hintText.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Experiments ", None))
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Icons for launching experiments", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Help", None))
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Help window: This tab will automatically load the helpfile relevant to the last experiment you launched", None))
        self.SCF2.setProperty("class", _translate("MainWindow", "PeripheralCollectionInner", None))
        self.pushButton.setText(_translate("MainWindow", "SET", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", " Controls  ", None))
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Various knobs for setting the outputs such as power supplies and waveform generators. Also contains meters for voltage, frequency, and capacitance", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "  Adv. controls  ", None))
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Advanced control inputs for configuring the waveform generators and power supplies", None))
        self.menuUtilities.setTitle(_translate("MainWindow", "Utilities", None))
        self.menuColor_scheme.setTitle(_translate("MainWindow", "color scheme", None))
        self.menuHelp.setTitle(_translate("MainWindow", "Help", None))
        self.menuLevel.setTitle(_translate("MainWindow", "level", None))
        self.actionIPython_Console.setText(_translate("MainWindow", "iPython Console", None))
        self.actionIPython.setText(_translate("MainWindow", "iPython Console", None))
        self.actionReset_Device.setText(_translate("MainWindow", "Reset Device", None))
        self.actionAbout_device.setText(_translate("MainWindow", "about device", None))
        self.actionWhite.setText(_translate("MainWindow", "white", None))
        self.actionBlack.setText(_translate("MainWindow", "black", None))
        self.actionBasic.setText(_translate("MainWindow", "Basic", None))
        self.actionAdvanced.setText(_translate("MainWindow", "Advanced", None))

