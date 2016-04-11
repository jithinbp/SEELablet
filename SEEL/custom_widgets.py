"""
These widgets will be used by the Experiment framework

"""
from __future__ import print_function
import sip,os

os.environ['QT_API'] = 'pyqt'
sip.setapi("QString", 2)
sip.setapi("QVariant", 2)
# Import the core and GUI elements of Qt
from PyQt4  import QtGui,QtCore

import SEEL.interface as interface

from SEEL.widgets.sliding import Ui_Form as Ui_Sliding
from SEEL.widgets.clicking import Ui_Form as Ui_Clicking
from SEEL.widgets.clickingOptions import Ui_Form as Ui_ClickingOptions

class CustomWidgets:
	parent=None
	def __init__(self):
		print ("widgets imported")
		self.I=interface.Interface()
	

	def newWidget(self,widget_type,**args):
			b=widget_type(**args)
			if('object_name' in args): b.setObjectName(args.get('object_name'))
			if('text' in args): b.setText(args.get('text'))
			if('items' in args):
				for a in args.get('items'): b.addItem(a)
			self.updateWidgetBay(b)
			return b

	def assignCommand(self,widget,signal,slot,*args):
			buttonCallback = functools.partial(slot,*args)
			QObject.connect(widget, SIGNAL(signal), buttonCallback)

	class sineHandler(QtGui.QFrame,Ui_Sliding):
		def __init__(self):
			super(CustomWidgets.sineHandler, self).__init__()
			#QtGui.QFrame.__init__(self)
			#Ui_Sliding.__init__(self)
			self.I=interface.Interface()
			self.setupUi(self)
			self.name='DDS'
			self.label.setText(self.name)
			self.slider.setMinimum(0)
			self.slider.setMaximum(500000)
		def setValue(self,val):
			self.label.setText(self.name+':'+str(val)+' Hz')
			self.I.set_sine(val)

	def widget_sine(self):
		self.updateWidgetBay(self.sineHandler())


	class gainHandler(QtGui.QFrame,Ui_Sliding):
		def __init__(self,chan,alternate_name=None):
			super(CustomWidgets.gainHandler, self).__init__()
			self.I=interface.Interface()
			self.setupUi(self)
			self.slider.setMinimum(0)
			self.slider.setMaximum(7)
			self.gaintxt=['1x','2x','4x','5x','8x','10x','16x','32x']
			self.name=chan
			if alternate_name:
				self.labeltxt=alternate_name
			else:
				self.labeltxt=chan
			self.label.setText(self.labeltxt)
		def setValue(self,val):
			self.label.setText(self.labeltxt+':'+self.gaintxt[val])
			self.I.set_gain(self.name,val)
			
	def widget_ch1(self):
		self.updateWidgetBay(self.gainHandler('CH1'))
	def widget_ch2(self):
		self.updateWidgetBay(self.gainHandler('CH2'))
	def widget_ch3(self):
		self.updateWidgetBay(self.gainHandler('CH3'))
	def widget_ch4(self):
		self.updateWidgetBay(self.gainHandler('CH4'))
	def widget_ch5(self):
		self.updateWidgetBay(self.gainHandler('CH5','CH5-CH9,PCS'))


	class voltHandler(QtGui.QFrame,Ui_Clicking):
		def __init__(self,chan):
			super(CustomWidgets.voltHandler, self).__init__()
			#QtGui.QFrame.__init__(self)
			#Ui_Sliding.__init__(self)
			self.I=interface.Interface()
			self.setupUi(self)
			self.name='READ '+chan
			self.button.setText(self.name)
			self.chan=chan
		def clicked(self):
			val = self.I.get_average_voltage(self.chan)
			self.label.setText('%.3f V'%(val))

	def widget_volt1(self):
		self.updateWidgetBay(self.voltHandler('CH1'))
	def widget_volt2(self):
		self.updateWidgetBay(self.voltHandler('CH2'))
	def widget_volt3(self):
		self.updateWidgetBay(self.voltHandler('CH3'))
	def widget_volt4(self):
		self.updateWidgetBay(self.voltHandler('CH4'))
	def widget_volt5(self):
		self.updateWidgetBay(self.voltHandler('CH5'))


	class voltAllHandler(QtGui.QFrame,Ui_ClickingOptions):
		def __init__(self):
			super(CustomWidgets.voltAllHandler, self).__init__()
			#QtGui.QFrame.__init__(self)
			#Ui_Sliding.__init__(self)
			self.I=interface.Interface()
			self.setupUi(self)
			self.names=['CH1','CH2','CH3','CH4','CH5','CH6','CH7','CH8','CH9','5V','9V','IN1','SEN']
			self.button.setText('Read')
			self.items.addItems(self.names)

		def clicked(self):
			val = self.I.get_average_voltage(self.items.currentText())
			self.label.setText('%.3f V'%(val))

	def widget_voltAll(self):
		self.updateWidgetBay(self.voltAllHandler())


	def widget_inductance(self):
		class Handler(QtGui.QFrame,Ui_Clicking):
			def __init__(self):
				super(Handler, self).__init__()
				self.I=interface.Interface()
				self.setupUi(self)
				self.button.setText('INDUCTANCE')
			def clicked(self):
				val = self.I.get_inductance()
				self.label.setText('%.3f'%(val))

		self.updateWidgetBay(Handler())

	class timingHandler(QtGui.QFrame,Ui_ClickingOptions):
		def __init__(self,cmd):
			super(CustomWidgets.timingHandler, self).__init__()
			#QtGui.QFrame.__init__(self)
			#Ui_Sliding.__init__(self)
			self.I=interface.Interface()
			self.setupUi(self)
			self.cmd = getattr(self.I,cmd)
			self.cmdname=cmd
			self.button.setText(cmd)
			self.items.addItems(['ID1','ID2','ID3','ID4','CH4'])

		def clicked(self):
			val = self.cmd(self.items.currentText())
			if self.cmdname=='duty_cycle':
				if(val[0]!=-1):p=100*val[1]/val[0]
				else: p=0
				self.label.setText(' %.2f %%'%(p))
			elif 'time' in self.cmdname:self.label.setText('%.2e S'%(val))
			else:self.label.setText('%.1f Hz'%(val))

	def widget_freq(self):
		self.updateWidgetBay(self.timingHandler('get_freq'))

	def widget_high_freq(self):
		self.updateWidgetBay(self.timingHandler('get_high_freq'))

	def widget_f2ftime(self):
		self.updateWidgetBay(self.timingHandler('f2f_time'))

	def widget_r2rtime(self):
		self.updateWidgetBay(self.timingHandler('r2r_time'))

	def widget_dutycycle(self):
		self.updateWidgetBay(self.timingHandler('duty_cycle'))

	def widget_pulse(self):
		self.updateWidgetBay(self.timingHandler('pulse_time'))

	class sourceHandler(QtGui.QFrame,Ui_Sliding):
		def __init__(self,name):
			super(CustomWidgets.sourceHandler, self).__init__()
			self.I=interface.Interface()
			self.setupUi(self)
			self.name=name
			if name=='PV1':
				self.slider.setRange(0,4095)
			if name=='PV2':
				self.slider.setRange(0,4095)
			elif name=='PV3':
				self.slider.setRange(0,4095)
			elif name=='PCS':
				self.slider.setRange(0,4095)

		def setValue(self,val):
			if self.name=='PV1':
				retval=self.I.DAC.__setRawVoltage__('PV1',val)
			elif self.name=='PV2':
				retval=self.I.DAC.__setRawVoltage__('PV2',val)
			elif self.name=='PV3':
				retval=self.I.DAC.__setRawVoltage__('PV3',val)
			elif self.name=='PCS':
				retval=self.I.DAC.__setRawVoltage__('PCS',val)

			self.label.setText(self.name+': %.3f'%(retval))

	def widget_PV1(self):
		self.updateWidgetBay(self.sourceHandler('PV1'))
	def widget_PV2(self):
		self.updateWidgetBay(self.sourceHandler('PV2'))
	def widget_PV3(self):
		self.updateWidgetBay(self.sourceHandler('PV3'))
	def widget_pcs(self):
		self.updateWidgetBay(self.sourceHandler('PCS'))




