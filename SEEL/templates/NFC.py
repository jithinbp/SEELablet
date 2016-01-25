# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NFC.ui'
#
# Created: Sun Jan 24 10:32:22 2016
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
        MainWindow.resize(569, 292)
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
""))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, -1)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.detect = QtGui.QLabel(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.detect.sizePolicy().hasHeightForWidth())
        self.detect.setSizePolicy(sizePolicy)
        self.detect.setObjectName(_fromUtf8("detect"))
        self.verticalLayout_2.addWidget(self.detect)
        self.dataLabel = QtGui.QLabel(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dataLabel.sizePolicy().hasHeightForWidth())
        self.dataLabel.setSizePolicy(sizePolicy)
        self.dataLabel.setObjectName(_fromUtf8("dataLabel"))
        self.verticalLayout_2.addWidget(self.dataLabel)
        self.frame_2 = QtGui.QFrame(self.frame)
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.gridLayout = QtGui.QGridLayout(self.frame_2)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.sectorEdit = QtGui.QSpinBox(self.frame_2)
        self.sectorEdit.setMinimum(8)
        self.sectorEdit.setObjectName(_fromUtf8("sectorEdit"))
        self.gridLayout.addWidget(self.sectorEdit, 0, 0, 1, 1)
        self.pushButton = QtGui.QPushButton(self.frame_2)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 0, 1, 1, 1)
        self.dataEdit = QtGui.QLineEdit(self.frame_2)
        self.dataEdit.setObjectName(_fromUtf8("dataEdit"))
        self.gridLayout.addWidget(self.dataEdit, 1, 0, 1, 1)
        self.pushButton_2 = QtGui.QPushButton(self.frame_2)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.gridLayout.addWidget(self.pushButton_2, 1, 1, 1, 1)
        self.verticalLayout_2.addWidget(self.frame_2)
        self.frame_3 = QtGui.QFrame(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.gridLayout_2 = QtGui.QGridLayout(self.frame_3)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.autoLabel = QtGui.QLabel(self.frame_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.autoLabel.sizePolicy().hasHeightForWidth())
        self.autoLabel.setSizePolicy(sizePolicy)
        self.autoLabel.setText(_fromUtf8(""))
        self.autoLabel.setObjectName(_fromUtf8("autoLabel"))
        self.gridLayout_2.addWidget(self.autoLabel, 1, 0, 1, 1)
        self.autoBox = QtGui.QCheckBox(self.frame_3)
        self.autoBox.setObjectName(_fromUtf8("autoBox"))
        self.gridLayout_2.addWidget(self.autoBox, 0, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.frame_3)
        self.verticalLayout.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 569, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.read)
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.write)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.frame.setProperty("class", _translate("MainWindow", "PeripheralCollection", None))
        self.detect.setText(_translate("MainWindow", "Detecting reader...", None))
        self.dataLabel.setText(_translate("MainWindow", ":", None))
        self.frame_2.setProperty("class", _translate("MainWindow", "PeripheralCollectionInner", None))
        self.pushButton.setText(_translate("MainWindow", "Read", None))
        self.pushButton_2.setText(_translate("MainWindow", "Write", None))
        self.frame_3.setProperty("class", _translate("MainWindow", "PeripheralCollectionInner", None))
        self.autoBox.setText(_translate("MainWindow", "Automatic Detection and reading", None))

