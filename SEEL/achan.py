from __future__ import print_function
import numpy as np
gains=[1,2,4,5,8,10,16,32,1/11.]

#-----------------------Classes for input sources----------------------
allAnalogChannels = ['CH1','CH2','CH3','MIC','CAP','SEN','AN8']

bipolars = ['CH1','CH2','CH3','MIC']

inputRanges={'CH1':[16.5,-16.5],	#Specify inverted channels explicitly by reversing range!!!!!!!!!
'CH2':[16.5,-16.5],
'CH3':[-3.3,3.3],					#external gain control analog input
'MIC':[-3.3,3.3],					#connected to MIC amplifier
'CAP':[0,3.3],
'SEN':[0,3.3],
'AN8':[0,3.3]
}

picADCMultiplex={'CH1':3,'CH2':0,'CH3':1,'MIC':2,'AN4':4,'SEN':7,'CAP':5,'AN8':8,}

class analogInputSource:
	gain_values=gains
	gainEnabled=False
	gain=None
	gainPGA=None
	inverted=False
	inversion=1.
	calPoly10 = np.poly1d([0,3.3/1023,0.])
	calPoly12 = np.poly1d([0,3.3/4095,0.])
	calibrationReady=False
	defaultOffsetCode=0
	def __init__(self,name,**args):
		self.name = name			#The generic name of the input. like 'CH1', 'IN1' etc
		self.CHOSA = picADCMultiplex[self.name]
		self.adc_shifts=[]
		self.polynomials={}

		self.R=inputRanges[name]
		
		if self.R[1]-self.R[0] < 0:
			self.inverted=True
			self.inversion=-1

		self.scaling=1.
		if name=='CH1':
			self.gainEnabled=True
			self.gainPGA = 1
			self.gain=0		#This is not the gain factor. use self.gain_values[self.gain] to find that.
		elif name=='CH2':
			self.gainEnabled=True
			self.gainPGA = 2
			self.gain=0		 
		else:
			pass


		self.gain=0
		self.regenerateCalibration()



	def setGain(self,g):
		if not	self.gainEnabled:
			print ('Analog gain is not available on',self.name)
			return False
		self.gain=self.gain_values.index(g)
		self.regenerateCalibration()

	def inRange(self,val):
		v = self.voltToCode12(val)
		return (v>=0 and v<=4095)

	def __conservativeInRange__(self,val):
		v = self.voltToCode12(val)
		return (v>=50 and v<=4000)

	def loadCalibrationTable(self,table,slope, intercept):
		self.adc_shifts = np.array(table)*slope - intercept

	def __ignoreCalibration__(self):
		self.calibrationReady = False

	def loadPolynomials(self,polys):
		for a in range(len(polys)):
			epoly = [float(b) for b in polys[a]]
			self.polynomials[a] = np.poly1d(epoly)

	def regenerateCalibration(self):
		B=self.R[1]
		A=self.R[0]
		intercept = self.R[0]
		
		if self.gain!=None:
				gain = self.gain_values[self.gain]
				B = B/gain
				A = A/gain


		slope = B-A
		intercept = A
		if self.calibrationReady and self.gain!=8 :  #special case for 1/11. gain
			self.calPoly10 = self.__cal10__
			self.calPoly12 = self.__cal12__
			
		else:
			self.calPoly10 = np.poly1d([0,slope/1023.,intercept])
			self.calPoly12 = np.poly1d([0,slope/4095.,intercept])

		self.voltToCode10 = np.poly1d([0,1023./slope,-1023*intercept/slope])
		self.voltToCode12 = np.poly1d([0,4095./slope,-4095*intercept/slope])


	def __cal12__(self,RAW):
		avg_shifts=(self.adc_shifts[np.int16(np.floor(RAW))]+self.adc_shifts[np.int16(np.ceil(RAW))])/2.
		RAW = RAW-4095*(avg_shifts)/3.3
		return self.polynomials[self.gain](RAW)

	def __cal10__(self,RAW):
		RAW*=4095/1023.
		avg_shifts=(self.adc_shifts[np.int16(np.floor(RAW))]+self.adc_shifts[np.int16(np.ceil(RAW))])/2.
		RAW = RAW-4095*(avg_shifts)/3.3
		return self.polynomials[self.gain](RAW)


'''
for a in ['CH1']:
	x=analogInputSource(a)
	print (x.name,x.calPoly10#,calfacs[x.name][0])
	print ('CAL:',x.calPoly10(0),x.calPoly10(1023))
	x.setOffset(1.65)
	x.setGain(32)
	print (x.name,x.calPoly10#,calfacs[x.name][0])
	print ('CAL:',x.calPoly10(0),x.calPoly10(1023))
'''
#---------------------------------------------------------------------



class analogAcquisitionChannel:
	'''
	This class takes care of oscilloscope trace data fetched from the device.
	
	Each instance may be linked to a particular input.
	
	Since only up to four channels may be captured at a time with the SEELablet, four instances are required to be maintained by the communications library.
	they are located at interface.achans[4] .
	
	Each instance will be linked to a particular inputSource (achan.analogInputSource) instance by the capture routines.
	When data is requested , it will return after applying calibration and gain details depending on the selected analog input.
	
	e.g. , calling interface.capture1('CH1') automatically sets interface.achans[0].source as achan.analogInputSource('CH1') . to find the Voltage range, you can use interface.achans[0].get_Y_range()
	'''
	def __init__(self,a):
		self.name=''
		self.gain=0
		self.channel=a
		'''
		List of available channel names CH1, CH2, ... AN8
		'''
		self.channel_names=allAnalogChannels
		#REFERENCE VOLTAGE = 3.3 V
		
		'''
		For tweaking the reference voltage. Users may measure the voltage reference using a much more precise voltmeter, and set this scale factor
		'''
		self.calibration_ref196=1.#measured reference voltage/3.3
		'''
		ADC resolution . 10/12
		'''
		self.resolution=10
		'''
		buffer for storing the X-axis
		'''
		self.xaxis=np.zeros(10000)
		'''
		buffer for storing the Y-axis (voltage readings)
		'''
		self.yaxis=np.zeros(10000)
		self.length=100
		self.timebase = 1.
		self.source = analogInputSource('CH1') #use CH1 for initialization. It will be overwritten by set_params

	def fix_value(self,val):
		'''
		Convert a code/np.array(codes) into corresponding voltage value(s) based on the calibration polynomials, gain settings, and input source
		
		'''
		#val[val>1020]=np.NaN
		#val[val<2]=np.NaN
		if self.resolution==12:
			return self.calibration_ref196*self.source.calPoly12(val)
		else:return self.calibration_ref196*self.source.calPoly10(val)

	def get_Y_range(self):
		'''
		return an array specifying the voltage range
		[V_min,V_max]
		
		'''
		if self.resolution==12:
			return np.sort( self.source.calPoly12(np.array([5.,4090.])))
		else:
			return np.sort( self.source.calPoly10(np.array([5.,1018.])) )

	def set_yval(self,pos,val):
		'''
		modify a certain element in the Y axis of the trace array. Internally calls `fix_value` on val, and writes to `yaxis`[pos]
		'''
		self.yaxis[pos] = self.fix_value(val)

	def set_xval(self,pos,val):
		'''
		modify a certain element in the x-axis of the trace array. writes val to `xaxis`[pos]
		'''
		self.xaxis[pos] = val

	def set_params(self,**keys):
		'''
		Set the parameters of this channel. Called by capture routines such as capture_fullspeed, and capture1 .
		This function allows storing the parameters passed to the capture routine running in the hardware.
		These parameters will be required to generate accurate X and Y data from the raw ADC codes read from the hardware after acquisition is complete
		
		Keyword arguments
		
		name : Human readable name . CH1 , CH2 ...
		source : `analogInputSource` instance. It holds all calibration data, and gain information.
		resolution : 10 or 12
		length : number of samples
		timebase : time between consecutive samples
		
		
		'''
		self.gain = keys.get('gain',self.gain)	
		self.name = keys.get('channel',self.channel)	
		self.source = keys.get('source',self.source)
		self.resolution = keys.get('resolution',self.resolution)	
		l = keys.get('length',self.length)	
		t = keys.get('timebase',self.timebase)
		if t != self.timebase or l != self.length:
			self.timebase = t
			self.length = l
			self.regenerate_xaxis()

	def regenerate_xaxis(self):
		for a in range(int(self.length)): self.xaxis[a] = self.timebase*a

	def get_xaxis(self):
		'''
		Return a list of values for the X axis
		'''
		return self.xaxis[:self.length]
	def get_yaxis(self):
		'''
		Return a list of voltage values for plotting the Y axis
		'''
		return self.yaxis[:self.length]

