#!/usr/bin/python
'''
Study Simple Pendulums
'''

from __future__ import print_function
import os

from SEEL.utilitiesClass import utilitiesClass

from PyQt4 import QtCore, QtGui
import time,sys
from SEEL.templates import simplePendulum

import sys

import pyqtgraph as pg

import numpy as np

params = {
'image' : 'transient.png',
'helpfile': 'diodeIV.html',
'name':'Simple Pendulum'
}

class AppWindow(QtGui.QMainWindow, simplePendulum.Ui_MainWindow,utilitiesClass):
	def __init__(self, parent=None,**kwargs):
		super(AppWindow, self).__init__(parent)
		self.setupUi(self)
		self.I=kwargs.get('I',None)
		self.I.set_gain('CH1',7)

		self.setWindowTitle(self.I.generic_name + ' : '+self.I.H.version_string.decode("utf-8"))
		self.plot=self.add2DPlot(self.plot_area)
		labelStyle = {'color': 'rgb(255,255,255)', 'font-size': '11pt'}
		self.plot.setLabel('left','Velocity -->', **labelStyle)
		self.plot.setLabel('bottom','Time -->', units='S',**labelStyle)

		self.totalpoints=2000
		self.X=[]
		self.Y=[]
		self.plotnum=0
				
		self.curves=[]
		self.curveLabels=[]
		self.looptimer = QtCore.QTimer()
		self.looptimer.timeout.connect(self.acquire)

		self.start_time = time.time()
		self.acquisitionPeriod = 10 # ten seconds
		self.pos=0
		self.state = 0

	def run(self):
		self.looptimer.stop()
		self.X=[];self.Y=[]
		self.plotnum+=1; self.pos=0
		self.curves.append( self.addCurve(self.plot ,'%.3f'%(self.plotnum),[255,255,255])  )
		P=self.plot.getPlotItem()
		P.enableAutoRange(True,True)
		self.acquisitionPeriod = self.timeBox.value() #  seconds
		self.plot.setXRange(0,self.acquisitionPeriod)
		self.start_time = time.time()
		self.looptimer.start(self.delayBox.value())   #mS

	def acquire(self):
		AMP =  self.I.get_average_voltage('CH1')

		if self.driveBox.isChecked():
			if AMP<0.025:
					self.state=1
			elif AMP>0.028 and self.state==1:
					self.I.set_state(SQR1=1)
					time.sleep(0.05)
					self.I.set_state(SQR1=0)
					time.sleep(0.02)
					print ('hit')
					self.state=0
					return

		T = time.time()-self.start_time
		self.X.append(T)
		self.Y.append(AMP)
		self.pos+=1
		if self.pos<500:
				self.curves[-1].setData(self.X,self.Y)
		self.pointCount.setText('%d'%self.pos)
		if T>self.acquisitionPeriod:
			self.looptimer.stop()
			txt='<div style="text-align: center"><span style="color: #FFF;font-size:8pt;"># %d</span></div>'%(self.plotnum)
			text = pg.TextItem(html=txt, anchor=(0,0), border='w', fill=(0, 0, 255, 100))
			self.plot.addItem(text)
			text.setPos(self.X[-1],self.Y[-1])
			self.curveLabels.append(text)
			self.tracesBox.addItem('#%d'%(self.plotnum))

	def refreshGraph(self):
			self.curves[-1].setData(self.X,self.Y)

	def delete_curve(self):
		c = self.tracesBox.currentIndex()
		if c>-1:
			self.tracesBox.removeItem(c)
			self.plot.removeItem(self.curves[c]);self.plot.removeItem(self.curveLabels[c]);
			self.curves.pop(c);self.curveLabels.pop(c);


	def __del__(self):
		self.looptimer.stop()
		print ('bye')

	def closeEvent(self, event):
		self.looptimer.stop()
		self.finished=True


if __name__ == "__main__":
    from SEEL import interface
    app = QtGui.QApplication(sys.argv)
    myapp = AppWindow(I=interface.connect())
    myapp.show()
    sys.exit(app.exec_())

