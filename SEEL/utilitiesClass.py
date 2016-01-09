import time,random,functools
import numpy as np


from PyQt4 import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl

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
