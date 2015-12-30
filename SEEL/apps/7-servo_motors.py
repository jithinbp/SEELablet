# -*- coding: utf-8 -*-
"""
Simple example demonstrating controlling servo motors with sliders
"""

from __future__ import print_function
import sys,time
from PyQt4 import QtGui, QtCore

params = {
'image' : 'servo.jpg',
'helpfile': 'servos.html',
'name':'Servo Motors'
}

class AppWindow(QtGui.QMainWindow):
	def __init__(self,parent=None,**kwargs):
		super(AppWindow, self).__init__(parent)
		self.I=kwargs.get('I',None)
		self.Frame=QtGui.QFrame()
		self.Holder=QtGui.QVBoxLayout()
		self.Frame.setLayout(self.Holder)
		self.setCentralWidget(self.Frame)

		self.slds = [QtGui.QSlider(QtCore.Qt.Horizontal) for a in range(4)]
		for sld in self.slds:
			self.Holder.addWidget(sld)

		self.POS=[0,0,0,0]

		import functools
		for sld in self.slds:
			sld.setRange(0,180)
			cmd = functools.partial(self.change,sld)
			sld.valueChanged[int].connect(cmd)

		#self.win.show()
		self.setWindowTitle('Control servos')

	def change(self,sld,val):
		self.POS[ self.slds.index(sld) ]=val
		self.I.servo4(*self.POS)


