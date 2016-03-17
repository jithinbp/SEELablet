# -*- coding: utf-8 -*-
"""
Simple example demonstrating controlling servo motors with sliders
"""

from __future__ import print_function
import sys,time
from PyQt4 import QtGui, QtCore
import pyqtgraph as pg

params = {
'image' : 'rgbled.png',
'name':'WIRELESS LEDs\nWS2812B',
'hint':'''
	Control WS2812B RGB LED chains using CS1 on wireless nodes
	This utility allows setting the shades via a color widget
	'''
}

class AppWindow(QtGui.QMainWindow):
	def __init__(self,parent=None,**kwargs):
		super(AppWindow, self).__init__(parent)
		self.I=kwargs.get('I',None)
		a=self.I.WS2812B([[0xAA,0x00,0xFF]],'SQR1')
		TOTAL_PIXELS=1
		self.Frame=QtGui.QFrame()
		self.Holder=QtGui.QVBoxLayout()
		self.Frame.setLayout(self.Holder)
		self.setCentralWidget(self.Frame)
		self.setWindowTitle('Set color of WS2812B RGB LEDs')
		self.addressBox = QtGui.QLineEdit()
		self.addressBox.setText('0x010107')
		self.addressBox.returnPressed.connect(self.updateAddress)
		self.addrLabel = QtGui.QLabel('address')
		self.Holder.addWidget(self.addrLabel)
		self.Holder.addWidget(self.addressBox)
		self.LINK = self.I.newRadioLink(address=int(str(self.addressBox.text()),16))
		self.btn = pg.ColorButton()
		self.Holder.addWidget(self.btn)
		self.btn.sigColorChanging.connect(self.change)

		self.COLS=[1,0,1]

	def updateAddress(self):
		self.LINK = self.I.newRadioLink(address=int(str(self.addressBox.text()),16))
		self.addrLabel.setText('Address:'+str(self.addressBox.text()))
		
	def change(self):
		self.COLS=self.btn.color().getRgb()[:3]
		self.LINK.WS2812B([self.COLS])


if __name__ == "__main__":
    from SEEL import interface
    app = QtGui.QApplication(sys.argv)
    myapp = AppWindow(I=interface.connect())
    myapp.show()
    sys.exit(app.exec_())

