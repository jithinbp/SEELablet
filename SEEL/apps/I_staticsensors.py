#!/usr/bin/python
'''
Stream data acquired from supported I2C sensors.

Currently Supports:\n

	MPU6050 - 3-Axis Accelerometer. 3-Axis Gyro  . Temperature sensor.\n
	HMC5883L - 3-Axis Magnetometer \n
	BMP180 - Temperature, Pressure, Altitude \n
	MLX90614 - Passive IR base temperature sensor (Thermopile) \n
	SHT21 - Temperature. humidity. \n



'''
from __future__ import print_function
from SEEL.templates import sensorGrid

from SEEL.SENSORS.supported import supported
from SEEL.sensorlist import sensors as sensorHints
from SEEL.templates.widgets import sensorWidget


from SEEL.utilitiesClass import utilitiesClass
import pyqtgraph as pg
import time,random,functools,sys
import numpy as np


from PyQt4 import QtCore, QtGui

params = {
'image' : 'sensors.png',
'name':'Sensor\nQuickView'
}

class AppWindow(QtGui.QMainWindow, sensorGrid.Ui_MainWindow,utilitiesClass):
	def __init__(self, parent=None,**kwargs):
		super(AppWindow, self).__init__(parent)
		self.setupUi(self)
		self.I=kwargs.get('I',None)
		if self.I:
			self.I.I2C.init()
			self.I.I2C.config(400e3)

		self.foundSensors=[]
		
		self.looptimer = QtCore.QTimer()
		self.looptimer.timeout.connect(self.updateData)
		self.looptimer.start(20)
		self.deviceMenus=[]
		self.sensorWidgets=[]
		self.availableClasses=[0x68,0x1E,0x5A,0x77,0x39,0x40]

	def updateData(self):
		for a in self.sensorWidgets:
			if a.autoRefresh.isChecked():
				a.read()

	class sensorIcon(QtGui.QFrame,sensorWidget.Ui_Form):
		def __init__(self,cls):
			super(AppWindow.sensorIcon, self).__init__()
			self.cls = cls
			self.setupUi(self)
			self.func = cls.getRaw
			self.plotnames = cls.PLOTNAMES
			self.menu = self.PermanentMenu()
			self.menu.setMinimumHeight(25)
			self.sub_menu = QtGui.QMenu('%s:%s'%(hex(cls.ADDRESS),cls.name[:15]))
			for i in cls.params: 
				mini=self.sub_menu.addMenu(i) 
				for a in cls.params[i]:
					Callback = functools.partial(getattr(cls,i),a)		
					mini.addAction(str(a),Callback) 
			self.menu.addMenu(self.sub_menu)
			self.formLayout.insertWidget(0,self.menu)

		class PermanentMenu(QtGui.QMenu):
			def hideEvent(self, event):
				self.show()


		def read(self):
			retval = self.func()
			if not retval:
				self.resultLabel.setText('err')
				return
			res = ''
			for a in range(len(retval)):
				res+=self.plotnames[a]+'\t%.3e\n'%(retval[a])
			self.resultLabel.setText(res)



	def autoScan(self):
		self.scan()

	def scan(self):
		lst = self.I.I2C.scan()
		for a in self.sensorWidgets:
			a.setParent(None)
		self.sensorWidgets=[]
		
		row=0;col=0;colLimit=3
		self.ExperimentLayout.setAlignment(QtCore.Qt.AlignTop)

		for a in lst:
			cls=False
			cls_module = supported.get(a,None)
			if cls_module:
				cls = cls_module.connect(self.I.I2C)
			else:
				cls=None
			if cls:
				if col==colLimit:
					col=0;row+=1
				newSensor=self.sensorIcon(cls)
				self.ExperimentLayout.addWidget(newSensor,row,col)
				self.sensorWidgets.append(newSensor)
				col+=1
			
	def __del__(self):
		self.looptimer.stop()
		print ('bye')

	def closeEvent(self, event):
		self.looptimer.stop()
		self.finished=True
		
if __name__ == "__main__":
	from SEEL import interface
	app = QtGui.QApplication(sys.argv)
	myapp = AppWindow(I=interface.connect(port = '/dev/ttyACM7'))
	myapp.show()
	sys.exit(app.exec_())
