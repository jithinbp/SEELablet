from __future__ import print_function
# Set the QT API to PyQt4
import os
import pkg_resources
os.environ['QT_API'] = 'pyqt'
import sip
sip.setapi("QString", 2)
sip.setapi("QVariant", 2)

from PyQt4 import QtGui,QtCore

import sys
import functools,random

from SEEL.templates import template_exp
import time,sys
import SEEL.custom_widgets as Widgets
 
import numpy as np
import sys


class ConvenienceClass():
        """
        This class contains methods that simplify setting up and running
        an experiment.

        The :func:`arbitFit` method accepts two arrays, the fitting function,
        and a keyword argument 'guess' that is an array containing
        guess values for the various fiting parameters.
        Guess values can be obtained using the :func:`getGuessValues` based on
        a keyword argument 'func' which as of this moment can be either 'sine' 
        or 'damped sine'
        """

        timers=[]
        def __init__(self):
                print ('initializing convenience class')
                try:
                        import scipy.optimize as optimize
                        import scipy.fftpack as fftpack
                except ImportError:
                        print ('imports failed for scipy.optimize,scipy.fftpack')
                        self.optimize = None;self.fftpack=None
                else:
                        self.optimize = optimize;self.fftpack=fftpack
                self.timers=[]

        def loopTask(self,interval,func,*args):
                """
                Creates a QTimer that executes 'func' every 'interval' milliseconds
                all additional arguments passed to this function are passed on as
                arguments to func

                Refer to the source code for experiments such as diodeIV, Bandpass filter etc.


                """
                timer = QtCore.QTimer()
                timerCallback = functools.partial(func,*args)
                timer.timeout.connect(timerCallback)
                timer.start(interval)
                self.timers.append(timer)
                return timer

        def delayedTask(self,interval,func,*args):
                """
                Creates a QTimer that executes 'func' once after 'interval' milliseconds.

                all additional arguments passed to this function are passed on as
                arguments to func


                """
                timer = QtCore.QTimer()
                timerCallback = functools.partial(func,*args)
                timer.singleShot(interval,timerCallback)
                self.timers.append(timer)

        def random_color(self):
                c=QtGui.QColor(random.randint(20,255),random.randint(20,255),random.randint(20,255))
                if np.average(c.getRgb())<150:
                        c=self.random_color()
                return c

        def displayObjectContents(self,d):
                """
                The contents of the dictionary 'd' are displayed in a new QWindow

                """
                self.tree = self.pg.DataTreeWidget(data=d)
                self.tree.show()
                self.tree.setWindowTitle('Data')
                self.tree.resize(600,600)

        def dampedSine(self,x, amp, freq, phase,offset,damp):
                """
                A damped sine wave function

                """
                return offset + amp*np.exp(-damp*x)*np.sin(abs(freq)*x + phase)


        def fitData(self,xReal,yReal,**args):
                def mysine(x, a1, a2, a3,a4):
                    return a4 + a1*np.sin(abs(a2)*x + a3)
                N=len(xReal)
                yhat = self.fftpack.rfft(yReal)
                idx = (yhat**2).argmax()
                freqs = self.fftpack.rfftfreq(N, d = (xReal[1]-xReal[0])/(2*np.pi))
                frequency = freqs[idx]

                amplitude = (yReal.max()-yReal.min())/2.0
                offset = yReal.max()-yReal.min()
                frequency=args.get('frequency',1e6*abs(frequency)/(2*np.pi))*(2*np.pi)/1e6
                phase=args.get('phase',0.)
                guess = [amplitude, frequency, phase,offset]
                try:
                        (amplitude, frequency, phase,offset), pcov = self.optimize.curve_fit(mysine, xReal, yReal, guess)
                        ph = ((phase)*180/(np.pi))

                        if(frequency<0):
                                #print ('negative frq')
                                return 0,0,0,0,pcov

                        if(amplitude<0):
                                #print ('AMP<0')
                                ph-=180

                        if(ph<-90):ph+=360
                        if(ph>360):ph-=360
                        freq=1e6*abs(frequency)/(2*np.pi)
                        amp=abs(amplitude)
                        if(frequency):	period = 1./frequency
                        else: period = 0
                        pcov[0]*=1e6
                        return amp,freq,ph,offset,pcov
                except:
                        return 0,0,0,0,[[]]

        def getGuessValues(self,xReal,yReal,func='sine'):
                if(func=='sine' or func=='damped sine'):
                        N=len(xReal)
                        offset = np.average(yReal)
                        yhat = self.fftpack.rfft(yReal-offset)
                        idx = (yhat**2).argmax()
                        freqs = self.fftpack.rfftfreq(N, d = (xReal[1]-xReal[0])/(2*np.pi))
                        frequency = freqs[idx]

                        amplitude = (yReal.max()-yReal.min())/2.0
                        phase=0.
                        if func=='sine':
                                return amplitude, frequency, phase,offset
                        if func=='damped sine':
                                return amplitude, frequency, phase,offset,0

        def arbitFit(self,xReal,yReal,func,**args):
                N=len(xReal)
                guess=args.get('guess',[])
                try:
                        results, pcov = self.optimize.curve_fit(func, xReal, yReal,guess)
                        pcov[0]*=1e6
                        return True,results,pcov
                except:
                        return False,[],[]


class Experiment(QtGui.QMainWindow,template_exp.Ui_MainWindow,Widgets.CustomWidgets):
	timers=[]
	def __init__(self,**args):
			self.qt_app = args.get('qt_app',QtGui.QApplication(sys.argv))
			self.showSplash()
			super(Experiment, self).__init__(args.get('parent',None))
			self.updateSplash(10)
			try:
				import pyqtgraph as pg
				import pyqtgraph.opengl as gl
			except ImportError:
				self.pg = None;self.gl=None
			else:
				self.pg = pg
				self.gl=gl
			self.updateSplash(10)
			self.setupUi(self)
			Widgets.CustomWidgets.__init__(self);self.updateSplash(10)
			self.I = args.get('I',None)
			self.graphContainer2_enabled=False
			self.graphContainer1_enabled=False
			self.console_enabled=False
			self.output_enabled=False
			self.viewBoxes=[]
			self.plot_areas=[]
			self.plots3D=[]
			self.plots2D=[]
			self.axisItems=[]
			self.total_plot_areas=0
			self.widgetBay = False
			self.help_url = pkg_resources.resource_filename(__name__, os.path.join('helpfiles','interface.html'))
			#self.additional_handle = QSplitterHandle(Qt.Horizontal,self.graph_splitter)
			#self.graph_splitter.addWidget(self.additional_handle)
			if(args.get('showresult',True)):
				dock = QtGui.QDockWidget()
				dock.setFeatures(QtGui.QDockWidget.DockWidgetMovable|QtGui.QDockWidget.DockWidgetFloatable)#|QDockWidget.DockWidgetVerticalTitleBar)
				dock.setWindowTitle("Results")
				self.output_text = QtGui.QTextEdit()
				self.output_text.setReadOnly(True)
				fr = QtGui.QFrame()
				plt = QtGui.QGridLayout(fr)
				plt.setMargin(0)
				plt.addWidget(self.output_text)
				self.output_enabled=True
				sys.stdout = self.relay_to_console(self.output_text)
				dock.setWidget(fr)
				self.result_dock=dock
				self.output_text.setStyleSheet("color: rgb(255, 255, 255);")
				self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, dock)
			else:
				self.result_dock=False
				self.output_enabled=False
			self.updateSplash(10)
			if(args.get('handler',False)):
				self.addHandler(args.get('handler'))
			while(self.progressBar.value()<100):
				self.updateSplash(1)
				time.sleep(0.01)

	def updateSplash(self,x,txt=''):
		self.progressBar.setValue(self.progressBar.value()+x)
		if(len(txt)):self.splashMsg.setText('  '+txt)
		self.qt_app.processEvents()
		self.splash.repaint()

	def showSplash(self):
		import pkg_resources
		splash_pix = QtGui.QPixmap(pkg_resources.resource_filename('v0.stylesheets', "splash3.png"))
		self.splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
		# adding progress bar
		self.progressBar = QtGui.QProgressBar(self.splash)
		self.progressBar.resize(self.splash.width(),20)
		css = pkg_resources.resource_string('v0', "stylesheets/splash.css")
		if css:
			self.splash.setStyleSheet(css)
		self.splashMsg = QtGui.QLabel(self.splash);self.splashMsg.setStyleSheet("font-weight:bold;color:purple")
		self.splash.setMask(splash_pix.mask())
		self.splashMsg.setText('Loading....');self.splashMsg.resize(self.progressBar.width(),20)
		self.splash.show()
		self.splash.repaint()

	
	def run(self):
			def __resizeHack__():
						if self.result_dock:
							self.result_dock.setMaximumHeight(100)
							self.result_dock.setMaximumHeight(2500)
			self.delayedTask(0,__resizeHack__)
			self.show()
			self.splash.finish(self)
			self.qt_app.exec_()

	def addPlotArea(self):
			fr = QtGui.QFrame(self.graph_splitter)
			fr.setFrameShape(QtGui.QFrame.StyledPanel)
			fr.setFrameShadow(QtGui.QFrame.Raised)
			fr.setMinimumHeight(250)
			self.total_plot_areas+=1
			fr.setObjectName("plot"+str(self.total_plot_areas))
			plt = QtGui.QGridLayout(fr)
			plt.setMargin(0)
			self.plot_areas.append(plt)
			return len(self.plot_areas)-1

	def add3DPlot(self):
			plot3d = self.gl.GLViewWidget()
			#gx = gl.GLGridItem();gx.rotate(90, 0, 1, 0);gx.translate(-10, 0, 0);self.plot.addItem(gx)
			#gy = gl.GLGridItem();gy.rotate(90, 1, 0, 0);gy.translate(0, -10, 0);self.plot.addItem(gy)
			gz = self.gl.GLGridItem();#gz.translate(0, 0, -10);
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
			plot=self.pg.PlotWidget()
			pos=self.addPlotArea()
			self.plot_areas[pos].addWidget(plot)
			plot.viewBoxes=[]
			self.plotLegend=plot.addLegend(offset=(-1,1))
			self.plots2D.append(plot)
			return plot

	def add2DPlots(self,num):
			for a in range(num):yield self.add2DPlot() 

	def add3DPlots(self,num):
			for a in range(num):yield self.add3DPlot() 

	def addAxis(self,plot,**args):
		p3 = self.pg.ViewBox()
		ax3 = self.pg.AxisItem('right')
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
		p = self.pg.ViewBox()
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


	def configureWidgetBay(self,name='controls'):
		if(self.widgetBay):return
		dock = QtGui.QDockWidget()
		dock.setFeatures(QtGui.QDockWidget.DockWidgetMovable|QtGui.QDockWidget.DockWidgetFloatable)#|QDockWidget.DockWidgetVerticalTitleBar)
		dock.setWindowTitle(name)
		fr = QtGui.QFrame()
		fr.setStyleSheet("QLineEdit {color: rgb(0,0,0);}QPushButton, QLabel ,QComboBox{color: rgb(255, 255, 255);}")
		dock.setWidget(fr)
		self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)
		self.frame_area = QtGui.QVBoxLayout(fr)
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
			print ('Device Not Connected.')
		
	def addConsole(self,**args):
                try:
                        #read arguments
                        self.I = args.get('I',self.I)
                        self.showSplash();self.updateSplash(10,'Importing iPython Widgets...')
                        from iPythonEmbed import QIPythonWidget;self.updateSplash(10,'Creating Dock Widget...')
                        #-------create an area for it to sit------
                        dock = QtGui.QDockWidget()
                        dock.setFeatures(QtGui.QDockWidget.DockWidgetMovable|QtGui.QDockWidget.DockWidgetFloatable)#|QDockWidget.DockWidgetVerticalTitleBar)
                        dock.setWindowTitle("Interactive Python Console")
                        fr = QtGui.QFrame();self.updateSplash(10)
                        dock.setWidget(fr)
                        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, dock)
                        fr.setFrameShape(QtGui.QFrame.StyledPanel)
                        fr.setFrameShadow(QtGui.QFrame.Raised);self.updateSplash(10,'Embedding IPython Widget...')

                        #--------instantiate the iPython class-------
                        self.ipyConsole = QIPythonWidget(customBanner="An interactive Python Console!\n");self.updateSplash(10)
                        layout = QtGui.QVBoxLayout(fr)
                        layout.setMargin(0)
                        layout.addWidget(self.ipyConsole);self.updateSplash(10,'Preparing default command dictionary...')        
                        cmdDict = {"delayedTask":self.delayedTask,"loopTask":self.loopTask,"addWidget":self.addWidget,"setCommand":self.setCommand,"Widgets":Widgets}
                        #if self.graphContainer1_enabled:cmdDict["graph"]=self.graph
                        if self.I :
                                cmdDict["I"]=self.I
                                self.ipyConsole.printText("Access hardware using the Instance 'I'.  e.g.  I.get_average_voltage('CH1')")
                        self.ipyConsole.pushVariables(cmdDict);self.updateSplash(10,'Winding up...')
                        self.console_enabled=True
                        self.splash.finish(dock);self.updateSplash(10)
                        dock.widget().setMaximumSize(QtCore.QSize(self.width(), self.height()/3))
                        dock.widget().setMinimumSize(QtCore.QSize(self.width(), self.height()/3))
                        print (dock.width(),dock.height())
                        def dockResize():
                                dock.widget().setMaximumSize(65535,65535)
                                dock.widget().setMinimumSize(60,60)
                        self.delayedTask(0,dockResize)
                        return self.ipyConsole
                except:
                        self.splash.finish(self);self.updateSplash(10)
                        errbox = QtGui.QMessageBox()
                        errbox.setStyleSheet('background:#fff;')
                        print (errbox.styleSheet())
                        errbox.about(self, "Error", "iPython-qtconsole not found.\n Please Install the module")

	def showHelp(self):
                from PyQt4 import QtWebKit
                dock = QtGui.QMainWindow()
                self.helpView = QtWebKit.QWebView()
                dock.setCentralWidget(self.helpView)
                dock.setWindowTitle("Help window")
                dock.show()
                self.helpView.setUrl(QtCore.QUrl(self.help_url))			
                self.helpWindow = dock

	def showFullHelp(self):
                from PyQt4 import QtWebKit
                dock = QtGui.QMainWindow()
                self.helpView = QtWebKit.QWebView()
                dock.setCentralWidget(self.helpView)
                dock.setWindowTitle("Help window")
                dock.show()
                URL = pkg_resources.resource_filename(__name__, os.path.join('helpfiles','interface.html'))
                self.helpView.setUrl(QtCore.QUrl(URL))			
                self.fullHelpWindow = dock

	def showImageMap(self):
                from PyQt4 import QtWebKit
                dock = QtGui.QMainWindow()
                self.helpView = QtWebKit.QWebView()
                dock.setCentralWidget(self.helpView)
                dock.setWindowTitle("Help window")
                dock.show()
                URL = pkg_resources.resource_filename(__name__, os.path.join('helpfiles','imagemap.html'))
                self.helpView.setUrl(QtCore.QUrl(URL))			
                self.imageMapHelp = dock


	def setHelpUrl(self,url):
		if 'http' in url:
			self.help_url = url
		else:
			self.help_url = pkg_resources.resource_filename(__name__, os.path.join('helpfiles',url))
		
	def new3dSurface(self,plot,**args):
			import scipy.ndimage as ndi
			surface3d = self.gl.GLSurfacePlotItem(z=np.array([[0.1,0.1],[0.1,0.1]]), **args)
			#surface3d.shader()['colorMap']=self.pg.ColorMap(np.array([0.2,0.4,0.6]),np.array([[255,0,0,255],[0,255,0,255],[0,255,255,255]])).getLookupTable()
			#surface3d.shader()['colorMap'] = np.array([0.2, 2, 0.5, 0.2, 1, 1, 0.2, 0, 2])
			plot.addItem(surface3d)
			return surface3d

	def setSurfaceData(self,surf,z):
			surf.setData(z=np.array(z))

	def draw3dLine(self,plot,x,y,z,color=(100,100,100)):
			pts = np.vstack([x,y,z]).transpose()
			plt = self.gl.GLLinePlotItem(pos=pts, color=self.pg.glColor(color),width=2)
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
				self.cursor.movePosition(QtGui.QTextCursor.End)
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
		if(len(name)):curve = self.pg.PlotCurveItem(name=name)
		else:curve = self.pg.PlotCurveItem()
		plot.addItem(curve)
		curve.setPen(color=col, width=1)
		return curve

	def rebuildLegend(self,plot):
		self.plotLegend = plot.addLegend(offset=(-10,30))

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

	
	def addButton(self,name,command,*args):
			b=QtGui.QPushButton(None)
			b.setText(name)
			self.updateWidgetBay(b)
			self.setCommand(b,"clicked()",command,*args)
			return b


	def addWidget(self,widget_type,**args):
			b=widget_type(**args)
			if('object_name' in args): b.setObjectName(args.get('object_name'))
			if('text' in args): b.setText(args.get('text'))
			if('items' in args):
				for a in args.get('items'): b.addItem(a)
			self.updateWidgetBay(b)
			return b

	def setCommand(self,widget,signal,slot,*args):
			buttonCallback = functools.partial(slot,*args)
			QObject.connect(widget, SIGNAL(signal), buttonCallback)

	'''
	class WorkThread(QtCore.QThread):
		punched = QtCore.pyqtSignal()		 
		def __init__(self):
			QtCore.QThread.__init__(self)			 
		def __del__(self):
			self.wait()			 
		def run(self):
			for i in range(11):
				time.sleep(0.5)
				self.punched.emit()
			self.terminate()

	progress = QtGui.QProgressDialog("Copying...", "Cancel", 0, 10)
	progress.show()
	T = self.WorkThread()
	T.punched.connect(lambda: progress.setValue(progress.value()+1))
	T.start() 
	'''

