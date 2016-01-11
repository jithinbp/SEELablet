import time,random,functools,pkgutil,importlib,functools,pkg_resources
import numpy as np

import os
os.environ['QT_API'] = 'pyqt'
import sip
sip.setapi("QString", 2)
sip.setapi("QVariant", 2)

from PyQt4 import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from SEEL.templates.widgets import dial,button,selectAndButton,sineWidget

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

#pg.setConfigOption('background', 'w')
#pg.setConfigOption('foreground', 'k')

class utilitiesClass():
	"""
	This class contains methods that simplify setting up and running
	an experiment.
	
	"""
	timers=[]
	viewBoxes=[]
	plots3D=[]
	plots2D=[]
	axisItems=[]
	total_plot_areas=0
	funcList=[]
	def __init__(self):
		pass

	def updateViews(self,plot):
		for a in plot.viewBoxes:
			a.setGeometry(plot.getViewBox().sceneBoundingRect())
			a.linkedViewChanged(plot.plotItem.vb, a.XAxis)

	def random_color(self):
		c=QtGui.QColor(random.randint(20,255),random.randint(20,255),random.randint(20,255))
		if np.average(c.getRgb())<150:
			c=self.random_color()
		return c

	def add2DPlot(self,plot_area):
		plot=pg.PlotWidget()
		plot.setMinimumHeight(250)
		plot_area.addWidget(plot)
		plot.viewBoxes=[]
		self.plots2D.append(plot)
		return plot


	def add3DPlot(self,plot_area):
		plot3d = gl.GLViewWidget()
		#gx = gl.GLGridItem();gx.rotate(90, 0, 1, 0);gx.translate(-10, 0, 0);self.plot.addItem(gx)
		#gy = gl.GLGridItem();gy.rotate(90, 1, 0, 0);gy.translate(0, -10, 0);self.plot.addItem(gy)
		gz = gl.GLGridItem();#gz.translate(0, 0, -10);
		plot3d.addItem(gz);
		plot3d.opts['distance'] = 40
		plot3d.opts['elevation'] = 5
		plot3d.opts['azimuth'] = 20
		plot3d.setMinimumHeight(250)
		plot_area.addWidget(plot3d)
		self.plots3D.append(plot3d)
		plot3d.plotLines3D=[]
		return plot3d


	def addCurve(self,plot,name='',col=(255,255,255),axis='left'):
		#if(len(name)):curve = plot.plot(name=name)
		#else:curve = plot.plot()
		if(len(name)):curve = pg.PlotCurveItem(name=name)
		else:curve = pg.PlotCurveItem()
		plot.addItem(curve)
		curve.setPen(color=col, width=1)
		return curve

	def rebuildLegend(self,plot):
		return plot.addLegend(offset=(-10,30))



	def addAxis(self,plot,**args):
		p3 = pg.ViewBox()
		ax3 = pg.AxisItem('right')
		plot.plotItem.layout.addItem(ax3, 2, 3+len(self.axisItems))
		plot.plotItem.scene().addItem(p3)
		ax3.linkToView(p3)
		p3.setXLink(plot.plotItem)
		ax3.setZValue(-10000)
		if args.get('label',False):
			ax3.setLabel(args.get('label',False), color=args.get('color','#ffffff'))
		plot.viewBoxes.append(p3)

		p3.setGeometry(plot.plotItem.vb.sceneBoundingRect())
		p3.linkedViewChanged(plot.plotItem.vb, p3.XAxis)
		## Handle view resizing 
		Callback = functools.partial(self.updateViews,plot)		
		plot.getViewBox().sigStateChanged.connect(Callback)
		self.axisItems.append(ax3)
		return p3

	def enableRightAxis(self,plot):
		p = pg.ViewBox()
		plot.showAxis('right')
		plot.setMenuEnabled(False)
		plot.scene().addItem(p)
		plot.getAxis('right').linkToView(p)
		p.setXLink(plot)
		plot.viewBoxes.append(p)
		Callback = functools.partial(self.updateViews,plot)		
		plot.getViewBox().sigStateChanged.connect(Callback)
		return p


	def updateViews(self,plot):
		for a in plot.viewBoxes:
			a.setGeometry(plot.getViewBox().sceneBoundingRect())
			a.linkedViewChanged(plot.plotItem.vb, a.XAxis)



	def loopTask(self,interval,func,*args):
			timer = QtCore.QTimer()
			timerCallback = functools.partial(func,*args)
			timer.timeout.connect(timerCallback)
			timer.start(interval)
			self.timers.append(timer)
			return timer
		
	def delayedTask(self,interval,func,*args):
			timer = QtCore.QTimer()
			timerCallback = functools.partial(func,*args)
			timer.singleShot(interval,timerCallback)
			self.timers.append(timer)



	def displayDialog(self,txt=''):
			QtGui.QMessageBox.about(self, 'Message',  txt)


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
			super(utilitiesClass.dialIcon, self).__init__()
			self.setupUi(self)
			self.name = C.TITLE
			self.title.setText(self.name)
			self.func = C.FUNC
			self.units = C.UNITS
			self.scale = C.SCALE_FACTOR
			if C.TOOLTIP:self.widgetFrameOuter.setToolTip(C.TOOLTIP)

			self.dial.setMinimum(C.MIN)
			self.dial.setMaximum(C.MAX)
			self.linkFunc = C.LINK

		def setValue(self,val):
			retval = self.func(val)
			self.value.setText('%.3f %s '%(retval*self.scale,self.units))
			if self.linkFunc:
				self.linkFunc(retval*self.scale,self.units)
				#self.linkObj.setText('%.3f %s '%(retval*self.scale,self.units))


	class buttonIcon(QtGui.QFrame,button.Ui_Form):
		def __init__(self,C):
			super(utilitiesClass.buttonIcon, self).__init__()
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
			super(utilitiesClass.selectAndButtonIcon, self).__init__()
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

	class experimentIcon(QtGui.QPushButton):
		def __init__(self,name,launchfunc):
			super(utilitiesClass.experimentIcon, self).__init__()
			self.name = name
			tmp = importlib.import_module('SEEL.apps.'+name)
			self.setText(tmp.params.get('name',name))
			self.func = launchfunc			
			self.clicked.connect(self.func)
			self.setMinimumHeight(70)
			self.setMaximumWidth(170)
			self.setStyleSheet("border-image: url(%s) 0 0 0 0 stretch stretch;color:white;"%(pkg_resources.resource_filename('SEEL.apps', _fromUtf8(tmp.params.get('image','') ))))



	class controlIcon(QtGui.QPushButton):
		def __init__(self,name,launchfunc,**kwargs):
			super(utilitiesClass.controlIcon, self).__init__()
			self.name = name
			tmp = importlib.import_module('SEEL.controls.'+name)
			self.setText(tmp.params.get('name',name))
			self.func = launchfunc
			self.clicked.connect(self.func)
			if 'tooltip' in kwargs:self.widgetFrameOuter.setToolTip(kwargs.get('tooltip',''))
			self.setMinimumHeight(70)
			self.setMinimumWidth(470)
			self.setStyleSheet("border-image: url(%s) 0 0 0 0 stretch stretch;color:white;"%(pkg_resources.resource_filename('SEEL.controls', _fromUtf8(tmp.params.get('image','') ))))

	class sineWidget(QtGui.QWidget,sineWidget.Ui_Form):
		def __init__(self,I):
			super(utilitiesClass.sineWidget, self).__init__()
			self.setupUi(self)
			self.I = I


		def loadSineTable(self):
			if self.I:
				from SEEL.utilityApps import loadSineTable
				inst = loadSineTable.AppWindow(self,I=self.I)
				inst.show()
			else:
				print (self.setWindowTitle('Device Not Connected!'))

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


