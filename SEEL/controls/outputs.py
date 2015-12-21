#!/usr/bin/python
'''
Output Peripheral control for the vLabtool - version 0.
'''

import os
os.environ['QT_API'] = 'pyqt'
import sip
sip.setapi("QString", 2)
sip.setapi("QVariant", 2)


from PyQt4 import QtCore, QtGui
import time,sys
from SEEL.templates import outputs

import sys,os,string
import time
import sys


params = {
'image' : 'dials.png',
'name' :u'Measurement\n& Control'
}

class AppWindow(QtGui.QMainWindow, outputs.Ui_MainWindow):
	def __init__(self, parent=None,**kwargs):
		super(AppWindow, self).__init__(parent)
		self.setupUi(self)
		self.I=kwargs.get('I',None)

		self.setWindowTitle('vLabtool output Peripherals : '+self.I.H.version_string)
		self.sqrDict={'SQ1':[0,0.5],'SQ2':[0,0.5],'OD1':[0,0.5],'OD2':[0,0.5]}

		
	def setPVS1(self,val):
		val=self.I.DAC.__setRawVoltage__('PVS1',val)
		self.PVS1_LABEL.setText('%.3f V'%(val))

	def setPVS2(self,val):
		val=self.I.DAC.__setRawVoltage__('PVS2',val)
		self.PVS2_LABEL.setText('%.3f V'%(val))

	def setPVS3(self,val):
		val=self.I.DAC.__setRawVoltage__('PVS3',val)
		self.PVS3_LABEL.setText('%.3f V'%(val))

	def setPCS(self,val):
		val=3.3-self.I.DAC.__setRawVoltage__('PCS',val)
		self.PCS_LABEL.setText('%.3f mA'%(val))

	def setSINE1(self,val):
		f=self.I.set_sine1(val)
		self.WAVE1_FREQ.setText('%.2f'%(f))

	def setSINE2(self,val):
		f=self.I.set_sine2(val)
		self.WAVE2_FREQ.setText('%.2f'%(f))

	def setSinePhase(self):
		freq = self.sinePhase_freq.value()
		phase = self.sinePhase_phase.value()
		#print freq,phase
		f=self.I.set_sine_phase(freq,phase)
		self.WAVE1_FREQ.setText('%.2f'%(f))
		self.WAVE2_FREQ.setText('%.2f'%(f))
		


	def sqr_phase(self,val):
		self.sqrDict[str(self.SQR_NM.currentText())][0]=val/360.

	def sqr_dc(self,val):
		self.sqrDict[str(self.SQR_NM.currentText())][1]=val/100.

	def sqr_update(self):
		self.sqrDict[str(self.SQR_NM.currentText())][0]=self.SQR_PH.value()/360.
		self.sqrDict[str(self.SQR_NM.currentText())][1]=self.SQR_DC.value()/100.
		
		self.I.sqr4_continuous(self.SQR_FREQ.value(),self.sqrDict['SQ1'][1],self.sqrDict['SQ2'][0],self.sqrDict['SQ2'][1],
		self.sqrDict['OD1'][0],self.sqrDict['OD1'][1],self.sqrDict['OD2'][0],self.sqrDict['OD2'][1])


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
		print 'bye'
        		
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
