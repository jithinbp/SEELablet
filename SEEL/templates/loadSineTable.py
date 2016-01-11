# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loadSineTable.ui'
#
# Created: Mon Jan 11 15:19:34 2016
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
        MainWindow.resize(273, 657)
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
"padding-top: 5px;padding-bottom:5px;\n"
"background: qradialgradient(cx: 0.3, cy: -0.4,\n"
"fx: 0.3, fy: -0.4,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #aaa);\n"
"width: 30px;\n"
"}\n"
"QTabBar::tab:selected {\n"
"color: #000;\n"
"border-top-left-radius: 5px;\n"
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
"\n"
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
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.frame_7 = QtGui.QFrame(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_7.sizePolicy().hasHeightForWidth())
        self.frame_7.setSizePolicy(sizePolicy)
        self.frame_7.setMaximumSize(QtCore.QSize(650, 16777215))
        self.frame_7.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_7.setObjectName(_fromUtf8("frame_7"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.frame_7)
        self.verticalLayout_5.setSpacing(3)
        self.verticalLayout_5.setContentsMargins(0, 5, 0, 0)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.label_4 = QtGui.QLabel(self.frame_7)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_5.addWidget(self.label_4)
        self.Frame_4 = QtGui.QFrame(self.frame_7)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Frame_4.sizePolicy().hasHeightForWidth())
        self.Frame_4.setSizePolicy(sizePolicy)
        self.Frame_4.setProperty("PeripheralCollectionInner", _fromUtf8(""))
        self.Frame_4.setObjectName(_fromUtf8("Frame_4"))
        self.gridLayout_4 = QtGui.QGridLayout(self.Frame_4)
        self.gridLayout_4.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.gridLayout_4.setHorizontalSpacing(6)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.tableLayout = QtGui.QVBoxLayout()
        self.tableLayout.setObjectName(_fromUtf8("tableLayout"))
        self.gridLayout_4.addLayout(self.tableLayout, 2, 0, 1, 4)
        self.setButton = QtGui.QPushButton(self.Frame_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.setButton.sizePolicy().hasHeightForWidth())
        self.setButton.setSizePolicy(sizePolicy)
        self.setButton.setObjectName(_fromUtf8("setButton"))
        self.gridLayout_4.addWidget(self.setButton, 0, 3, 1, 1)
        self.line = QtGui.QFrame(self.Frame_4)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout_4.addWidget(self.line, 1, 0, 1, 4)
        self.setButton_2 = QtGui.QPushButton(self.Frame_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.setButton_2.sizePolicy().hasHeightForWidth())
        self.setButton_2.setSizePolicy(sizePolicy)
        self.setButton_2.setObjectName(_fromUtf8("setButton_2"))
        self.gridLayout_4.addWidget(self.setButton_2, 0, 2, 1, 1)
        self.label_20 = QtGui.QLabel(self.Frame_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy)
        self.label_20.setAlignment(QtCore.Qt.AlignCenter)
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.gridLayout_4.addWidget(self.label_20, 0, 0, 1, 2)
        self.verticalLayout_5.addWidget(self.Frame_4)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButton = QtGui.QPushButton(self.frame_7)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtGui.QPushButton(self.frame_7)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.frame_7)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 273, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.setButton_2, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.loadSine1)
        QtCore.QObject.connect(self.setButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.loadSine2)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.reset1)
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.reset2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.frame_7.setProperty("class", _translate("MainWindow", "PeripheralCollection", None))
        self.label_4.setText(_translate("MainWindow", "Reload Wavegen Table", None))
        self.Frame_4.setProperty("class", _translate("MainWindow", "PeripheralCollectionInner", None))
        self.setButton.setText(_translate("MainWindow", "Set 2", None))
        self.setButton_2.setText(_translate("MainWindow", "Set 1", None))
        self.label_20.setText(_translate("MainWindow", ">", None))
        self.pushButton.setText(_translate("MainWindow", "Reset", None))
        self.pushButton_2.setText(_translate("MainWindow", "Reset", None))

