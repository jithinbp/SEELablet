# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wirelessTemplate.ui'
#
# Created: Fri Nov 13 17:28:06 2015
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
        MainWindow.resize(818, 550)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setMaximumSize(QtCore.QSize(300, 16777215))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.checkBox = QtGui.QCheckBox(self.frame)
        self.checkBox.setStyleSheet(_fromUtf8("color: rgb(255,255,255);"))
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.verticalLayout.addWidget(self.checkBox)
        self.pushButton = QtGui.QPushButton(self.frame)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.verticalLayout.addWidget(self.pushButton)
        self.scrollArea = QtGui.QScrollArea(self.frame)
        self.scrollArea.setStyleSheet(_fromUtf8("background-color: rgb(21, 107, 113);\n"
""))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollLayout = QtGui.QWidget()
        self.scrollLayout.setGeometry(QtCore.QRect(0, 0, 296, 220))
        self.scrollLayout.setObjectName(_fromUtf8("scrollLayout"))
        self.nodeArea = QtGui.QVBoxLayout(self.scrollLayout)
        self.nodeArea.setSpacing(0)
        self.nodeArea.setMargin(0)
        self.nodeArea.setObjectName(_fromUtf8("nodeArea"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.nodeArea.addItem(spacerItem)
        self.scrollArea.setWidget(self.scrollLayout)
        self.verticalLayout.addWidget(self.scrollArea)
        self.scrollArea_2 = QtGui.QScrollArea(self.frame)
        self.scrollArea_2.setStyleSheet(_fromUtf8("background-color: rgb(21, 107, 113);\n"
""))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName(_fromUtf8("scrollArea_2"))
        self.scroll2layout = QtGui.QWidget()
        self.scroll2layout.setGeometry(QtCore.QRect(0, 0, 296, 219))
        self.scroll2layout.setStyleSheet(_fromUtf8("QMenu{color:rgb(255,255,255);}\n"
""))
        self.scroll2layout.setObjectName(_fromUtf8("scroll2layout"))
        self.paramMenus = QtGui.QVBoxLayout(self.scroll2layout)
        self.paramMenus.setSpacing(0)
        self.paramMenus.setMargin(0)
        self.paramMenus.setObjectName(_fromUtf8("paramMenus"))
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.paramMenus.addItem(spacerItem1)
        self.scrollArea_2.setWidget(self.scroll2layout)
        self.verticalLayout.addWidget(self.scrollArea_2)
        self.horizontalLayout.addWidget(self.frame)
        self.logs = QtWebKit.QWebView(self.centralwidget)
        self.logs.setMaximumSize(QtCore.QSize(250, 150))
        self.logs.setProperty("url", QtCore.QUrl(_fromUtf8("about:blank")))
        self.logs.setObjectName(_fromUtf8("logs"))
        self.horizontalLayout.addWidget(self.logs)
        self.frame_2 = QtGui.QFrame(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.plot_area = QtGui.QGridLayout(self.frame_2)
        self.plot_area.setMargin(2)
        self.plot_area.setSpacing(2)
        self.plot_area.setObjectName(_fromUtf8("plot_area"))
        self.horizontalLayout.addWidget(self.frame_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 818, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.checkBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), MainWindow.toggleListen)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.reloadNodeList)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.checkBox.setText(_translate("MainWindow", "Register New Nodes", None))
        self.pushButton.setText(_translate("MainWindow", "Refresh Node List", None))

from PyQt4 import QtWebKit
