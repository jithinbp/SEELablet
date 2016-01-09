#!/usr/bin/python
'''
Output Peripheral control for the vLabtool - version 0.
'''

from __future__ import print_function
import os
os.environ['QT_API'] = 'pyqt'
import sip
sip.setapi("QString", 2)
sip.setapi("QVariant", 2)


from PyQt4 import QtCore, QtGui
import time,sys
from SEEL.templates import controlWidgets
from SEEL.templates.widgets import dial,button,selectAndButton

import sys,os,string,functools
import time
import sys


params = {
'image' : 'dials.png',
'name' :u'Measurement\n& Control'
}

class AppWindow(QtGui.QMainWindow, controlWidgets.Ui_MainWindow):
	def __init__(self, parent=None,**kwargs):
		super(AppWindow, self).__init__(parent)
		self.setupUi(self)
		self.I=kwargs.get('I',None)

		row=0;col=0;colLimit=3
		self.funcs=[]
		self.WidgetLayout.setAlignment(QtCore.Qt.AlignTop)

		autogenControls=[]
		if self.I:
			if self.I.connected:
				autogenControls.append(self.autogenControl(TITLE='Wave 1',MIN=10,MAX=5000,FUNC=self.I.set_sine1,TYPE='dial',UNITS='Hz',TOOLTIP='Frequency of waveform generator #1',LINK=self.WAVE1_FREQ))
				autogenControls.append(self.autogenControl(TITLE='Wave 2',MIN=10,MAX=5000,FUNC=self.I.set_sine2,TYPE='dial',UNITS='Hz',TOOLTIP='Frequency of waveform generator #2',LINK=self.WAVE2_FREQ))
				autogenControls.append(self.autogenControl(TITLE='square 1',MIN=10,MAX=50000,FUNC=self.I.sqr1,TYPE='dial',UNITS='Hz',TOOLTIP='Frequency of square wave generator #1'))

				tmpfunc = functools.partial(self.I.DAC.__setRawVoltage__,'PVS1')
				autogenControls.append(self.autogenControl(TITLE='PVS1',MIN=0,MAX=4095,FUNC=tmpfunc,TYPE='dial',UNITS='V',TOOLTIP='Programmable Voltage Source ',LINK=self.PVS1_LABEL))

				tmpfunc = functools.partial(self.I.DAC.__setRawVoltage__,'PVS2')
				autogenControls.append(self.autogenControl(TITLE='PVS2',MIN=0,MAX=4095,FUNC=tmpfunc,TYPE='dial',UNITS='V',TOOLTIP='Programmable Voltage Source ',LINK=self.PVS2_LABEL))

				tmpfunc = functools.partial(self.I.DAC.__setRawVoltage__,'PVS3')
				autogenControls.append(self.autogenControl(TITLE='PVS3',MIN=0,MAX=4095,FUNC=tmpfunc,TYPE='dial',UNITS='V',TOOLTIP='Programmable Voltage Source ',LINK=self.PVS3_LABEL))

				tmpfunc = lambda x: self.I.DAC.__setRawVoltage__('PCS',4095-x)
				autogenControls.append(self.autogenControl(TITLE='PCS',MIN=0,MAX=4095,FUNC=tmpfunc,TYPE='dial',UNITS='mA',TOOLTIP='Programmable Current Source ',SCALE_FACTOR = 1e3,LINK=self.PCS_LABEL))

				autogenControls.append(self.autogenControl(TITLE='CAPACITANCE',FUNC=self.I.get_capacitance,TYPE='button',UNITS='F',TOOLTIP='Read Capacitance connected to CAP input '))

				tmpfunc = functools.partial(self.I.get_average_voltage,samples=100)
				autogenControls.append(self.autogenControl(TITLE='VOLTMETER',FUNC=tmpfunc,TYPE='selectButton',UNITS='V',TOOLTIP='Voltmeter',OPTIONS=self.I.allAnalogChannels))
				autogenControls.append(self.autogenControl(TITLE='Low Frequency',FUNC=self.I.get_freq,TYPE='selectButton',UNITS='Hz',TOOLTIP='Measure Frequency. Minimum 40Hz',OPTIONS=self.I.allDigitalChannels))
				autogenControls.append(self.autogenControl(TITLE='High Frequency',FUNC=self.I.get_high_freq,TYPE='selectButton',UNITS='Hz',TOOLTIP='Measure Frequencies over 1MHz with 10Hz resolution',OPTIONS=self.I.allDigitalChannels))
				self.setWindowTitle(self.I.generic_name + ' : '+self.I.H.version_string.decode("utf-8"))
				for C in autogenControls:
					if C.TYPE=='dial':
						self.funcs.append(C.FUNC)
						self.WidgetLayout.addWidget(self.dialIcon(C),row,col)
					elif C.TYPE=='button':
						self.funcs.append(C.FUNC)
						self.WidgetLayout.addWidget(self.buttonIcon(C),row,col)
					elif C.TYPE=='selectButton':
						self.funcs.append(C.FUNC)
						self.WidgetLayout.addWidget(self.selectAndButtonIcon(C),row,col)

					col+=1
					if(col==colLimit):
						col=0;row+=1

			else:
				self.setWindowTitle(self.I.generic_name + ' : Not Connected')
		else:
			self.setWindowTitle('Not Connected!')


		self.setWindowTitle('vLabtool output Peripherals : '+self.I.H.version_string.decode("utf-8"))



	class autogenControl:
		def __init__(self,**kwargs):
			self.TYPE = kwargs.get('TYPE','dial')
			self.TITLE = kwargs.get('TITLE','TITLE')
			self.UNITS = kwargs.get('UNITS','')
			self.MAX = kwargs.get('MAX',100)
			self.MIN = kwargs.get('MIN',0)
			self.FUNC = kwargs.get('FUNC',None)
			self.TOOLTIP = kwargs.get('TOOLTIP',None)
			self.SCALE_FACTOR = kwargs.get('SCALE_FACTOR',1)
			self.options = kwargs.get('OPTIONS',[])
			self.LINK = kwargs.get('LINK',None)

	class dialIcon(QtGui.QFrame,dial.Ui_Form):
		def __init__(self,C):
			super(AppWindow.dialIcon, self).__init__()
			self.setupUi(self)
			self.name = C.TITLE
			self.title.setText(self.name)
			self.func = C.FUNC
			self.units = C.UNITS
			self.scale = C.SCALE_FACTOR
			if C.TOOLTIP:self.widgetFrameOuter.setToolTip(C.TOOLTIP)

			self.dial.setMinimum(C.MIN)
			self.dial.setMaximum(C.MAX)
			self.linkObj = C.LINK

		def setValue(self,val):
			retval = self.func(val)
			self.value.setText('%.3f %s '%(retval*self.scale,self.units))
			if self.linkObj:
				self.linkObj.setText('%.3f %s '%(retval*self.scale,self.units))


	class buttonIcon(QtGui.QFrame,button.Ui_Form):
		def __init__(self,C):
			super(AppWindow.buttonIcon, self).__init__()
			self.setupUi(self)
			self.name = C.TITLE
			self.title.setText(self.name)
			self.func = C.FUNC
			self.units = C.UNITS
			if C.TOOLTIP:self.widgetFrameOuter.setToolTip(C.TOOLTIP)

		def read(self):
			retval = self.func()
			if abs(retval)<1e4 and abs(retval)>.01:self.value.setText('%.3f %s '%(retval,self.units))
			else: self.value.setText('%.3e %s '%(retval,self.units))

	class selectAndButtonIcon(QtGui.QFrame,selectAndButton.Ui_Form):
		def __init__(self,C):
			super(AppWindow.selectAndButtonIcon, self).__init__()
			self.setupUi(self)
			self.name = C.TITLE
			self.title.setText(self.name)
			self.func = C.FUNC
			self.units = C.UNITS
			self.optionBox.addItems(C.options)
			if C.TOOLTIP:self.widgetFrameOuter.setToolTip(C.TOOLTIP)

		def read(self):
			retval = self.func(self.optionBox.currentText())
			if abs(retval)<1e4 and abs(retval)>.01:self.value.setText('%.3f %s '%(retval,self.units))
			else: self.value.setText('%.3e %s '%(retval,self.units))

		
	def setPVS1(self,val):
		val=self.I.DAC.setVoltage('PVS1',val)
		self.PVS1_LABEL.setText('%.3f V'%(val))

	def setPVS2(self,val):
		val=self.I.DAC.setVoltage('PVS2',val)
		self.PVS2_LABEL.setText('%.3f V'%(val))

	def setPVS3(self,val):
		val=self.I.DAC.setVoltage('PVS3',val)
		self.PVS3_LABEL.setText('%.3f V'%(val))

	def setPCS(self,val):
		val=3.3e-3-self.I.DAC.setVoltage('PCS',val/1.e3)
		self.PCS_LABEL.setText('%.3f mA'%(val*1e3))

	def setSINE1(self,val):
		f=self.I.set_sine1(val)
		self.WAVE1_FREQ.setText('%.2f'%(f))

	def setSINE2(self,val):
		f=self.I.set_sine2(val)
		self.WAVE2_FREQ.setText('%.2f'%(f))

	def setSinePhase(self):
		freq1 = self.SINE1BOX.value()
		freq2 = self.SINE2BOX.value()
		phase = self.SINEPHASE.value()
		f=self.I.set_sine_phase(freq1,phase,freq2)
		self.WAVE1_FREQ.setText('%.2f'%(f))
		self.WAVE2_FREQ.setText('%.2f'%(f))


	def setSQRS(self):
		P2=self.SQR2P.value()/360.
		P3=self.SQR3P.value()/360.
		P4=self.SQR4P.value()/360.
		D1=self.SQR1DC.value()
		D2=self.SQR2DC.value()
		D3=self.SQR3DC.value()
		D4=self.SQR4DC.value()
		
		self.I.sqr4_continuous(self.SQRSF.value(),D1,P2,D2,P3,D3,P4,D4)

	def measure_dcycle(self):
		inp = self.timing_input.currentText()
		v=self.I.DutyCycle(inp)
		if(v[0]!=-1):p=100*v[1]
		else: p=0
		self.timing_results.setText('Duty Cycle: %f %%'%(p))

	def measure_interval(self):
		t = self.I.MeasureInterval(self.edge1chan.currentText(),self.edge2chan.currentText(),self.edge1edge.currentText(),self.edge2edge.currentText())
		self.time_interval_label.setText('time: %.2e S'%(t))


	def __del__(self):
		print ('bye')
        		
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)

	# Create and display the splash screen
	#splash_pix = QtGui.QPixmap('cat.png')
	#splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
	#progressBar = QtGui.QProgressBar(splash)
	#progressBar.setStyleSheet("""QProgressBar::chunk { width:100%;background: #112255; }""")
	#splash.setMask(splash_pix.mask())
	#splash.show()
	#for i in range(0, 100):
	#	progressBar.setValue(i)
	#	t = time.time()
	#	while time.time() < t + 0.001:
	#		app.processEvents()
	
	myapp = MyMainWindow()
	myapp.show()
	app.processEvents()
	#splash.finish(myapp)
	sys.exit(app.exec_())
