# Set the QT API to PyQt4
import os
os.environ['QT_API'] = 'pyqt'
import sip
sip.setapi("QString", 2)
sip.setapi("QVariant", 2)

# Import the core and GUI elements of Qt
from PyQt4.QtGui  import *
from PyQt4.QtCore import *
import PyQt4.QtGui as Widgets

import sys
import functools,random
import scipy.optimize as optimize
import scipy.fftpack as fftpack

from Labtools.templates import template_exp_standalone
import time,sys
from Labtools.customui_rc import *

import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import sys

#_fromUtf8 = QString.fromUtf8
 

class Experiment(QMainWindow,template_exp_standalone.Ui_MainWindow):		#,interface_rev4.Interface
	def __init__(self,**args):
			self.qt_app = QApplication(sys.argv)
			super(Experiment, self).__init__(args.get('parent',None))
			#interface_rev4.Interface.__init__(self)
			self.setupUi(self)
			self.timers=[]
			self.I = None
			self.graphContainer2_enabled=False
			self.graphContainer1_enabled=False
			self.console_enabled=False
			self.output_enabled=False
			self.viewBoxes=[]
			self.plot_areas=[]
			self.plots3D=[]
			self.plots2D=[]
			self.total_plot_areas=0
			self.widgetBay = False
			#self.additional_handle = QSplitterHandle(Qt.Horizontal,self.graph_splitter)
			#self.graph_splitter.addWidget(self.additional_handle)
			if(args.get('showresult',True)):
				dock = QDockWidget()
				dock.setFeatures(QDockWidget.DockWidgetMovable|QDockWidget.DockWidgetFloatable)#|QDockWidget.DockWidgetVerticalTitleBar)
				dock.setWindowTitle("Results")
				self.output_text = QTextEdit()
				self.output_text.setReadOnly(True)
				fr = QFrame()
				plt = QGridLayout(fr)
				plt.setMargin(0)
				plt.addWidget(self.output_text)
				self.output_enabled=True
				sys.stdout = self.relay_to_console(self.output_text)
				dock.setWidget(fr)
				self.result_dock=dock
				self.output_text.setStyleSheet("color: rgb(255, 255, 255);")
				self.addDockWidget(Qt.BottomDockWidgetArea, dock)
				def __resizeHack__():
							self.result_dock.setMaximumHeight(100)
							self.qt_app.processEvents()
							self.result_dock.setMaximumHeight(2500)
				self.delayedTask(0,__resizeHack__)

			if(args.get('handler',False)):
				self.addHandler(args.get('handler'))

	
	def addPlotArea(self):
			fr = QFrame(self.graph_splitter)
			fr.setFrameShape(QFrame.StyledPanel)
			fr.setFrameShadow(QFrame.Raised)
			fr.setMinimumHeight(250)
			self.total_plot_areas+=1
			fr.setObjectName("plot"+str(self.total_plot_areas))
			plt = QGridLayout(fr)
			plt.setMargin(0)
			self.plot_areas.append(plt)
			return len(self.plot_areas)-1

	def add3DPlot(self):
			plot3d = gl.GLViewWidget()
			#gx = gl.GLGridItem();gx.rotate(90, 0, 1, 0);gx.translate(-10, 0, 0);self.plot.addItem(gx)
			#gy = gl.GLGridItem();gy.rotate(90, 1, 0, 0);gy.translate(0, -10, 0);self.plot.addItem(gy)
			gz = gl.GLGridItem();#gz.translate(0, 0, -10);
			plot3d.addItem(gz);
			plot3d.opts['distance'] = 40
			plot3d.opts['elevation'] = 5
			plot3d.opts['azimuth'] = 20
			pos=self.addPlotArea()
			self.plot_areas[pos].addWidget(plot3d)
			self.plots3D.append(plot3d)
			plot3d.plotLines3D=[]
			return plot3d

	def add2DPlot(self):
			plot=pg.PlotWidget()
			pos=self.addPlotArea()
			self.plot_areas[pos].addWidget(plot)
			plot.viewBoxes=[]
			plot.addLegend(offset=(-1,1))
			self.plots2D.append(plot)
			return plot

	def add2DPlots(self,num):
			for a in range(num):yield self.add2DPlot() 

	def add3DPlots(self,num):
			for a in range(num):yield self.add3DPlot() 

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


	def configureWidgetBay(self,name='controls'):
		if(self.widgetBay):return
		dock = QDockWidget()
		dock.setFeatures(QDockWidget.DockWidgetMovable|QDockWidget.DockWidgetFloatable)#|QDockWidget.DockWidgetVerticalTitleBar)
		dock.setWindowTitle(name)
		fr = QFrame()
		fr.setStyleSheet("QLineEdit {color: rgb(0,0,0);}QPushButton, QLabel ,QComboBox{color: rgb(255, 255, 255);}")
		dock.setWidget(fr)
		self.addDockWidget(Qt.LeftDockWidgetArea, dock)
		self.frame_area = QVBoxLayout(fr)
		self.frame_area.setMargin(0)
		self.widgetBay = True
	
	def updateWidgetBay(self,obj):
		self.configureWidgetBay()
		self.frame_area.addWidget(obj)
		
	def addHandler(self,handler,name = 'Controls'):
		'''
		Add handler instance(subclass of QFrame) to the left side of the window.
		The contents of the handler are QWidgets which control various aspects
		of the experiment that the handler has been designed for.
		'''		
		
		self.configureWidgetBay(name)
		self.frame=handler
		self.updateWidgetBay(self.frame)
		#self.updateWidgetBay(self.frame)
		try:
			self.I = handler.I
			if(self.console_enabled):
				self.ipyConsole.pushVariables({"I":self.I})
				self.ipyConsole.printText("Access hardware using the Instance 'I'.  e.g.  I.get_average_voltage(0)")                           
		except:
			print 'Device Not Connected.'


	def new3dSurface(self,plot,**args):
			import scipy.ndimage as ndi
			surface3d = gl.GLSurfacePlotItem(z=np.array([[0.1,0.1],[0.1,0.1]]), **args)
			#surface3d.shader()['colorMap']=pg.ColorMap(np.array([0.2,0.4,0.6]),np.array([[255,0,0,255],[0,255,0,255],[0,255,255,255]])).getLookupTable()
			#surface3d.shader()['colorMap'] = np.array([0.2, 2, 0.5, 0.2, 1, 1, 0.2, 0, 2])
			plot.addItem(surface3d)
			return surface3d

	def setSurfaceData(self,surf,z):
			surf.setData(z=np.array(z))

	def draw3dLine(self,plot,x,y,z,color=(100,100,100)):
			pts = np.vstack([x,y,z]).transpose()
			plt = gl.GLLinePlotItem(pos=pts, color=pg.glColor(color),width=2)
			plot.addItem(plt)
			plot.plotLines3D.append(plt)
			return plt

	def clearLinesOnPlane(self,plot):
			for a in plot.plotLines3D:
				plot.removeItem(a)# a.setData(pos=[[0,0,0]])
			plot.plotLines3D=[]

	class relay_to_console():
			def __init__(self,console):
				self.console = console
				self.cursor = self.console.textCursor()
				self.scroll=self.console.verticalScrollBar()

			def write(self,arg):
				f=open('b.txt','at')
				self.cursor.movePosition(QTextCursor.End)
				self.console.setTextCursor(self.cursor)
				self.console.insertPlainText(arg)
				#self.scroll.setValue(self.scroll.maximum())
				f.write(arg)
			def flush(self):
				pass
		
	def graph(self,x,y):
			if(self.graphContainer1_enabled):	self.reserved_curve.setData(x,y)

	def setRange(self,plot,x,y,width,height):
			plot.setRange(QtCore.QRectF(x,y,width,height)) 

	def addCurve(self,plot,name='',col=(255,255,255),axis='left'):
		#if(len(name)):curve = plot.plot(name=name)
		#else:curve = plot.plot()
		if(len(name)):curve = pg.PlotCurveItem(name=name)
		else:curve = pg.PlotCurveItem()
		plot.addItem(curve)
		curve.setPen(color=col, width=1)
		return curve

	def rebuildLegend(plot,self):
		self.plotLegend = plot.addLegend(offset=(-10,30))

	def loopTask(self,interval,func,*args):
			timer = QTimer()
			timerCallback = functools.partial(func,*args)
			timer.timeout.connect(timerCallback)
			timer.start(interval)
			self.timers.append(timer)
			return timer
		
	def delayedTask(self,interval,func,*args):
			timer = QTimer()
			timerCallback = functools.partial(func,*args)
			timer.singleShot(interval,timerCallback)
			self.timers.append(timer)

	def run(self):
			self.show()
			self.qt_app.exec_()


	def add_a_widget(self):
			self.addButton('testing')
	
	def addButton(self,name,command,*args):
			b=QPushButton(None)
			b.setText(name)
			self.updateWidgetBay(b)
			self.setCommand(b,"clicked()",command,*args)
			return b


	def addWidget(self,widget_type,**args):
			b=widget_type(**args)
			if(args.has_key('object_name')): b.setObjectName(args.get('object_name'))
			if(args.has_key('text')): b.setText(args.get('text'))
			if(args.has_key('items')):
				for a in args.get('items'): b.addItem(a)
			self.updateWidgetBay(b)
			return b

	def setCommand(self,widget,signal,slot,*args):
			buttonCallback = functools.partial(slot,*args)
			QObject.connect(widget, SIGNAL(signal), buttonCallback)



