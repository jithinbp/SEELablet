# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'clickingOptions.ui'
#
# Created: Sun Jan 18 23:09:32 2015
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!
import os,sip

os.environ['QT_API'] = 'pyqt'
sip.setapi("QString", 2)
sip.setapi("QVariant", 2)

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(312, 30)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.frame = QtGui.QFrame(Form)
        self.frame.setFrameShape(QtGui.QFrame.Box)
        self.frame.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame.setLineWidth(2)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.items = QtGui.QComboBox(self.frame)
        self.items.setObjectName(_fromUtf8("items"))
        self.horizontalLayout.addWidget(self.items)
        self.button = QtGui.QPushButton(self.frame)
        self.button.setObjectName(_fromUtf8("button"))
        self.horizontalLayout.addWidget(self.button)
        self.label = QtGui.QLabel(self.frame)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.button, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.clicked)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.button.setText(QtGui.QApplication.translate("Form", "Get", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Results", None, QtGui.QApplication.UnicodeUTF8))

