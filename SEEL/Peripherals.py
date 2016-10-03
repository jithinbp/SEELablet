from __future__ import print_function
import commands_proto as CP
import numpy as np 
import time,inspect

	
class I2C():
	"""
	Methods to interact with the I2C port.



	.. code-block:: python

		#Code Example : Read Values from an HMC5883L 3-axis Magnetometer(compass) [GY-273 sensor] connected to the I2C port
		ADDRESS = 0x1E
		from SEEL import interface
		I = interface.connect() 
		
		# writing to 0x1E, set gain(0x01) to smallest(0 : 1x)
		I.I2C.bulkWrite(ADDRESS,[0x01,0])
		
		# writing to 0x1E, set mode conf(0x02), continuous measurement(0)
		I.I2C.bulkWrite(ADDRESS,[0x02,0])

		# read 6 bytes from addr register on I2C device located at ADDRESS
		vals = I.I2C.bulkRead(ADDRESS,addr,6)
			
		from numpy import int16
		#conversion to signed datatype
		x=int16((vals[0]<<8)|vals[1])
		y=int16((vals[2]<<8)|vals[3])
		z=int16((vals[4]<<8)|vals[5])
		print (x,y,z)

	"""

	def __init__(self,H):
		self.H = H
		import sensorlist
		self.SENSORS=sensorlist.sensors
		self.buff=np.zeros(10000)

	def init(self):
		try:
			self.H.__sendByte__(CP.I2C_HEADER)
			self.H.__sendByte__(CP.I2C_INIT)
			self.H.__get_ack__()
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)

	def enable_smbus(self):
		try:
			self.H.__sendByte__(CP.I2C_HEADER)
			self.H.__sendByte__(CP.I2C_ENABLE_SMBUS)
			self.H.__get_ack__()
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)

	def pullSCLLow(self,uS):
		"""
		Hold SCL pin at 0V for a specified time period. Used by certain sensors such
		as MLX90316 PIR for initializing.
		
		.. tabularcolumns:: |p{3cm}|p{11cm}|
		
		================    ============================================================================================
		**Arguments** 
		================    ============================================================================================
		uS                  Time(in uS) to hold SCL output at 0 Volts
		================    ============================================================================================

		"""
		try:
			self.H.__sendByte__(CP.I2C_HEADER)
			self.H.__sendByte__(CP.I2C_PULLDOWN_SCL)
			self.H.__sendInt__(uS)
			self.H.__get_ack__()
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)
		 
	def config(self,freq,verbose=True):
		"""
		Sets frequency for I2C transactions
		
		.. tabularcolumns:: |p{3cm}|p{11cm}|
		
		================    ============================================================================================
		**Arguments** 
		================    ============================================================================================
		freq                I2C frequency
		================    ============================================================================================
		"""
		try:
			self.H.__sendByte__(CP.I2C_HEADER)
			self.H.__sendByte__(CP.I2C_CONFIG)
			#freq=1/((BRGVAL+1.0)/64e6+1.0/1e7)
			BRGVAL=int( (1./freq-1./1e7)*64e6-1 )
			if BRGVAL>511:
				BRGVAL=511
				if verbose:print ('Frequency too low. Setting to :',1/((BRGVAL+1.0)/64e6+1.0/1e7))
			self.H.__sendInt__(BRGVAL) 
			self.H.__get_ack__()
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)

	def start(self,address,rw):
		"""
		Initiates I2C transfer to address via the I2C port
		
		.. tabularcolumns:: |p{3cm}|p{11cm}|
		
		================    ============================================================================================
		**Arguments** 
		================    ============================================================================================
		address             I2C slave address\n
		rw                  Read/write.
							- 0 for writing
							- 1 for reading.
		================    ============================================================================================
		"""
		try:
			self.H.__sendByte__(CP.I2C_HEADER)
			self.H.__sendByte__(CP.I2C_START)
			self.H.__sendByte__(((address<<1)|rw)&0xFF) # address
			return self.H.__get_ack__()>>4
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)

	def stop(self):
		"""
		stops I2C transfer
		
		:return: Nothing
		"""
		try:
			self.H.__sendByte__(CP.I2C_HEADER)
			self.H.__sendByte__(CP.I2C_STOP)
			self.H.__get_ack__()
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)

	def wait(self):
		"""
		wait for I2C

		:return: Nothing
		"""
		try:
			self.H.__sendByte__(CP.I2C_HEADER)
			self.H.__sendByte__(CP.I2C_WAIT)
			self.H.__get_ack__()
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)

	def send(self,data):
		"""
		SENDS data over I2C.
		The I2C bus needs to be initialized and set to the correct slave address first.
		Use I2C.start(address) for this.
		
		.. tabularcolumns:: |p{3cm}|p{11cm}|
		
		================    ============================================================================================
		**Arguments** 
		================    ============================================================================================
		data                Sends data byte over I2C bus
		================    ============================================================================================

		:return: Nothing
		"""
		try:
			self.H.__sendByte__(CP.I2C_HEADER)
			self.H.__sendByte__(CP.I2C_SEND)
			self.H.__sendByte__(data)        #data byte
			return self.H.__get_ack__()>>4
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)
		
	def send_burst(self,data):
		"""
		SENDS data over I2C. The function does not wait for the I2C to finish before returning.
		It is used for sending large packets quickly.
		The I2C bus needs to be initialized and set to the correct slave address first.
		Use start(address) for this.

		.. tabularcolumns:: |p{3cm}|p{11cm}|
		
		================    ============================================================================================
		**Arguments** 
		================    ============================================================================================
		data                Sends data byte over I2C bus
		================    ============================================================================================

		:return: Nothing
		"""
		try:
			self.H.__sendByte__(CP.I2C_HEADER)
			self.H.__sendByte__(CP.I2C_SEND_BURST)
			self.H.__sendByte__(data)        #data byte
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)

	def restart(self,address,rw):
		"""
		Initiates I2C transfer to address

		.. tabularcolumns:: |p{3cm}|p{11cm}|
		
		================    ============================================================================================
		**Arguments** 
		================    ============================================================================================
		address             I2C slave address
		rw                  Read/write.
							* 0 for writing
							* 1 for reading.
		================    ============================================================================================

		"""
		try:
			self.H.__sendByte__(CP.I2C_HEADER)
			self.H.__sendByte__(CP.I2C_RESTART)
			self.H.__sendByte__(((address<<1)|rw)&0xFF) # address
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)
		return self.H.__get_ack__()>>4

	def simpleRead(self,addr,numbytes):
		"""
		Read bytes from I2C slave without first transmitting the read location.
		
		.. tabularcolumns:: |p{3cm}|p{11cm}|
		
		================    ============================================================================================
		**Arguments** 
		================    ============================================================================================
		addr                Address of I2C slave
		numbytes            Total Bytes to read
		================    ============================================================================================
		"""
		self.start(addr,1)
		vals=self.read(numbytes)
		return vals

	def read(self,length):
		"""
		Reads a fixed number of data bytes from I2C device. Fetches length-1 bytes with acknowledge bits for each, +1 byte
		with Nack.

		.. tabularcolumns:: |p{3cm}|p{11cm}|
		
		================    ============================================================================================
		**Arguments** 
		================    ============================================================================================
		length              number of bytes to read from I2C bus
		================    ============================================================================================
		"""
		data=[]
		try:
			for a in range(length-1):
				self.H.__sendByte__(CP.I2C_HEADER)
				self.H.__sendByte__(CP.I2C_READ_MORE)
				data.append(self.H.__getByte__())
				self.H.__get_ack__()
			self.H.__sendByte__(CP.I2C_HEADER)
			self.H.__sendByte__(CP.I2C_READ_END)
			data.append(self.H.__getByte__())
			self.H.__get_ack__()
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)
		return data

	def read_repeat(self):
		try:
			self.H.__sendByte__(CP.I2C_HEADER)
			self.H.__sendByte__(CP.I2C_READ_MORE)
			val=self.H.__getByte__()
			self.H.__get_ack__()
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)
		return val

	def read_end(self):
		try:
			self.H.__sendByte__(CP.I2C_HEADER)
			self.H.__sendByte__(CP.I2C_READ_END)
			val=self.H.__getByte__()
			self.H.__get_ack__()
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)
		return val


	def read_status(self):
		try:
			self.H.__sendByte__(CP.I2C_HEADER)
			self.H.__sendByte__(CP.I2C_STATUS)
			val=self.H.__getInt__()
			self.H.__get_ack__()
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)
		return val

	def readBulk(self,device_address,register_address,bytes_to_read):
		try:
			self.H.__sendByte__(CP.I2C_HEADER)
			self.H.__sendByte__(CP.I2C_READ_BULK)
			self.H.__sendByte__(device_address)
			self.H.__sendByte__(register_address)
			self.H.__sendByte__(bytes_to_read)
			data=self.H.fd.read(bytes_to_read)
			self.H.__get_ack__()
			try:
				return [ord(a) for a in data]
			except:
				print ('Transaction failed')
				return False
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)
		
	def writeBulk(self,device_address,bytestream):
		"""
		write bytes to I2C slave
		
		.. tabularcolumns:: |p{3cm}|p{11cm}|
		
		================    ============================================================================================
		**Arguments** 
		================    ============================================================================================
		device_address      Address of I2C slave
		bytestream          List of bytes to write
		================    ============================================================================================
		"""
		try:
			self.H.__sendByte__(CP.I2C_HEADER)
			self.H.__sendByte__(CP.I2C_WRITE_BULK)
			self.H.__sendByte__(device_address)
			self.H.__sendByte__(len(bytestream))
			for a in bytestream:
				self.H.__sendByte__(a)
			self.H.__get_ack__()
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)

	def scan(self,frequency = 100000,verbose=False):
		"""
		Scan I2C port for connected devices
		
		.. tabularcolumns:: |p{3cm}|p{11cm}|
		
		================    ============================================================================================
		**Arguments** 
		================    ============================================================================================
		Frequency           I2C clock frequency
		================    ============================================================================================

		:return: Array of addresses of connected I2C slave devices

		"""

		self.config(frequency,verbose)
		addrs=[]
		n=0
		if verbose:
			print ('Scanning addresses 0-127...')
			print ('Address','\t','Possible Devices')
		for a in range(0,128):
			x = self.start(a,0)
			if x&1 == 0:    #ACK received
				addrs.append(a)
				if verbose: print (hex(a),'\t\t',self.SENSORS.get(a,'None'))
				n+=1
			self.stop()
		return addrs

	def capture(self,address,location,sample_length,total_samples,tg,*args):
		"""
		Blocking call that fetches data from I2C sensors like an oscilloscope fetches voltage readings
		
		.. tabularcolumns:: |p{3cm}|p{11cm}|
		
		==================  ============================================================================================
		**Arguments** 
		==================  ============================================================================================
		address             Address of the I2C sensor
		location            Address of the register to read from
		sample_length       Each sample can be made up of multiple bytes startng from <location> . such as 3-axis data
		total_samples       Total samples to acquire. Total bytes fetched = total_samples*sample_length
		tg                  timegap between samples (in uS)
		==================  ============================================================================================

		Example

		>>> from pylab import *
		>>> I=interface.Interface()
		>>> x,y1,y2,y3,y4 = I.capture_multiple(800,1.75,'CH1','CH2','MIC','SEN')
		>>> plot(x,y1)              
		>>> plot(x,y2)              
		>>> plot(x,y3)              
		>>> plot(x,y4)              
		>>> show()              
		
		:return: Arrays X(timestamps),Y1,Y2 ...

		"""
		if(tg<20):tg=20
		total_bytes = total_samples*sample_length
		print ('total bytes calculated : ',total_bytes)
		if(total_bytes>MAX_SAMPLES*2):
			print ('Sample limit exceeded. 10,000 int / 20000 bytes total')
			total_samples = MAX_SAMPLES*2/sample_length  #2* because sample array is in Integers, and we're using it to store bytes
			total_bytes = MAX_SAMPLES*2

		if('int' in args):
			total_chans = sample_length/2
			channel_length = total_bytes/sample_length/2
		else:
			total_chans = sample_length
			channel_length = total_bytes/sample_length

		print ('total channels calculated : ',total_chans)
		print ('length of each channel : ',channel_length)
		try:
			self.H.__sendByte__(CP.I2C_HEADER)
			self.H.__sendByte__(CP.I2C_START_SCOPE)       
			self.H.__sendByte__(address)
			self.H.__sendByte__(location)
			self.H.__sendByte__(sample_length)
			self.H.__sendInt__(total_samples)           #total number of samples to record
			self.H.__sendInt__(tg)        #Timegap between samples.  1MHz timer clock
			self.H.__get_ack__()
			print ( 'done', total_chans, channel_length)

			print ('sleeping for : ',1e-6*total_samples*tg+.01)

			time.sleep(1e-6*total_samples*tg+0.5)
			data=b''
			total_int_samples = total_bytes/2

			print ('fetchin samples : ',total_int_samples,'   split',DATA_SPLITTING)

			data=b''
			for i in range(int(total_int_samples/DATA_SPLITTING)):
				self.H.__sendByte__(CP.ADC)
				self.H.__sendByte__(CP.GET_CAPTURE_CHANNEL)
				self.H.__sendByte__(0)   #starts with A0 on PIC
				self.H.__sendInt__(DATA_SPLITTING)
				self.H.__sendInt__(i*DATA_SPLITTING)
				rem = DATA_SPLITTING*2+1
				for a in range(200):
					partial = self.H.fd.read(rem)       #reading int by int sometimes causes a communication error. this works better.
					rem -=len(partial)
					data+=partial
					#print ('partial: ',len(partial), end=",")
					if rem<=0:
						break
				data=data[:-1]
				#print ('Pass : len=',len(data), ' i = ',i)

			if total_int_samples%DATA_SPLITTING:
				self.H.__sendByte__(CP.ADC)
				self.H.__sendByte__(CP.GET_CAPTURE_CHANNEL)
				self.H.__sendByte__(0)   #starts with A0 on PIC
				self.H.__sendInt__(total_int_samples%DATA_SPLITTING)
				self.H.__sendInt__(total_int_samples-total_int_samples%DATA_SPLITTING)
				rem = 2*(total_int_samples%DATA_SPLITTING)+1
				for a in range(200):
					partial = self.H.fd.read(rem)       #reading int by int sometimes causes a communication error. this works better.
					rem -=len(partial)
					data+=partial
					#print ('partial: ',len(partial), end="")
					if rem<=0:
						break
				data=data[:-1]
				#print ('Final Pass : len=',len(data))
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)


		try:
			data = [ord(a) for a in data]
			if('int' in args):
					for a in range(total_chans*channel_length): self.buff[a] = np.int16((data[a*2]<<8)|data[a*2+1])
			else:
					for a in range(total_chans*channel_length): self.buff[a] = data[a]

			#print (self.buff, 'geer')
			
			yield np.linspace(0,tg*(channel_length-1),channel_length)
			for a in range(int(total_chans)):
				yield self.buff[a:channel_length*total_chans][::total_chans]
		except Exception as ex:
			msg = "Incorrect number of bytes received"
			raise RuntimeError(msg)

class SPI():
	"""
	Methods to interact with the SPI port. An instance of Packet_Handler must be passed to the init function

	"""
	def __init__(self,H):
		self.H = H

	def set_parameters(self,primary_prescaler=0,secondary_prescaler=2,CKE=1,CKP=0,SMP=1):
		"""
		sets SPI parameters.
		
		.. tabularcolumns:: |p{3cm}|p{11cm}|
		
		================    ============================================================================================
		**Arguments** 
		================    ============================================================================================
		primary_pres        Primary Prescaler(0,1,2,3) for 64MHz clock->(64:1,16:1,4:1,1:1)
		secondary_pres      Secondary prescaler(0,1,..7)->(8:1,7:1,..1:1)
		CKE                 CKE 0 or 1.
		CKP                 CKP 0 or 1.
		================    ============================================================================================

		"""
		try:
			self.H.__sendByte__(CP.SPI_HEADER)
			self.H.__sendByte__(CP.SET_SPI_PARAMETERS)
			#0Bhgfedcba - > <g>: modebit CKP,<f>: modebit CKE, <ed>:primary pre,<cba>:secondary pre
			self.H.__sendByte__(secondary_prescaler|(primary_prescaler<<3)|(CKE<<5)|(CKP<<6)|(SMP<<7)) 
			self.H.__get_ack__()
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)

	def start(self,channel):
		"""
		selects SPI channel to enable.
		Basically lowers the relevant chip select pin .
		
		.. tabularcolumns:: |p{3cm}|p{11cm}|
		
		================    ============================================================================================
		**Arguments** 
		================    ============================================================================================
		channel             'CS1','CS2'
		================    ============================================================================================
		
		"""
		self.set_cs(channel,0)

	def set_cs(self,channel,state):
		"""
		Enable or disable a chip select
		
		.. tabularcolumns:: |p{3cm}|p{11cm}|
		
		================    ============================================================================================
		**Arguments** 
		================    ============================================================================================
		channel             'CS1','CS2'
		state               1 for HIGH, 0 for LOW
		================    ============================================================================================
		
		"""
		try:
			channel = channel.upper()
			if channel in ['CS1','CS2']:
				csnum=['CS1','CS2'].index(channel)+9  #chip select number 9=CSOUT1,10=CSOUT2
				self.H.__sendByte__(CP.SPI_HEADER)
				if state:self.H.__sendByte__(CP.STOP_SPI)
				else:self.H.__sendByte__(CP.START_SPI)
				self.H.__sendByte__(csnum)   
			else: print('Channel does not exist')
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)
		
	def stop(self,channel):
		"""
		selects SPI channel to disable.
		Sets the relevant chip select pin to HIGH.
		
		
		.. tabularcolumns:: |p{3cm}|p{11cm}|
		
		================    ============================================================================================
		**Arguments** 
		================    ============================================================================================
		channel             'CS1','CS2'
		================    ============================================================================================
		
		"""
		self.set_cs(channel,1)

	def send8(self,value):
		"""
		SENDS 8-bit data over SPI
		
		.. tabularcolumns:: |p{3cm}|p{11cm}|
		
		================    ============================================================================================
		**Arguments** 
		================    ============================================================================================
		value               value to transmit
		================    ============================================================================================

		:return: value returned by slave device
		"""
		try:
			self.H.__sendByte__(CP.SPI_HEADER)
			self.H.__sendByte__(CP.SEND_SPI8)
			self.H.__sendByte__(value)  #value byte
			v=self.H.__getByte__()
			self.H.__get_ack__()
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)
		return v

	def send16(self,value):
		"""
		SENDS 16-bit data over SPI

		.. tabularcolumns:: |p{3cm}|p{11cm}|
		
		================    ============================================================================================
		**Arguments** 
		================    ============================================================================================
		value               value to transmit
		================    ============================================================================================

		:return: value returned by slave device
		:rtype: int
		"""
		try:
			self.H.__sendByte__(CP.SPI_HEADER)
			self.H.__sendByte__(CP.SEND_SPI16)
			self.H.__sendInt__(value)   #value byte
			v=self.H.__getInt__()
			self.H.__get_ack__()
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)
		return v

	def send8_burst(self,value):
		"""
		SENDS 8-bit data over SPI
		No acknowledge/return value

		.. tabularcolumns:: |p{3cm}|p{11cm}|
		
		================    ============================================================================================
		**Arguments** 
		================    ============================================================================================
		value               value to transmit
		================    ============================================================================================

		:return: Nothing
		"""
		try:
			self.H.__sendByte__(CP.SPI_HEADER)
			self.H.__sendByte__(CP.SEND_SPI8_BURST)
			self.H.__sendByte__(value)  #value byte
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)

	def send16_burst(self,value):
		"""
		SENDS 16-bit data over SPI
		no acknowledge/return value

		.. tabularcolumns:: |p{3cm}|p{11cm}|
		
		==============  ============================================================================================
		**Arguments** 
		==============  ============================================================================================
		value           value to transmit
		==============  ============================================================================================

		:return: nothing
		"""
		try:
			self.H.__sendByte__(CP.SPI_HEADER)
			self.H.__sendByte__(CP.SEND_SPI16_BURST)
			self.H.__sendInt__(value)   #value byte
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)

	def xfer(self,chan,data):
		self.start(chan)
		reply=[]
		for a in data:
			reply.append(self.send8(a))
		self.stop(chan)
		return reply

class DACCHAN:
	def __init__(self,name,span,channum,**kwargs):
		self.name = name
		self.channum=channum
		self.VREF = kwargs.get('VREF',0)
		self.SwitchedOff = kwargs.get('STATE',0)
		self.range = span
		slope = (span[1]-span[0])
		intercept = span[0]
		self.VToCode = np.poly1d([4095./slope,-4095.*intercept/slope ])
		self.CodeToV = np.poly1d([slope/4095.,intercept ])
		self.calibration_enabled = False
		self.calibration_table = []
		self.slope=1
		self.offset=0

	def load_calibration_table(self,table):
		self.calibration_enabled='table'
		self.calibration_table = table

	def load_calibration_twopoint(self,slope,offset):
		self.calibration_enabled='twopoint'
		self.slope = slope
		self.offset = offset


	def apply_calibration(self,v):
		if self.calibration_enabled=='table':			#Each point is individually calibrated 
			return int(np.clip(v+self.calibration_table[v]	,0,4095))
		elif self.calibration_enabled=='twopoint':		#Overall slope and offset correction is applied
			#print (self.slope,self.offset,v)
			return int(np.clip(v*self.slope+self.offset,0,4095)	)
		else:
			return v

class PCSCHAN:
	def __init__(self,name,span,channum,**kwargs):
		self.name = name
		self.channum=channum
		self.VREF = kwargs.get('VREF',3.3)
		self.RES = 1e3 #resistor connected before the transistor
		self.SwitchedOff = kwargs.get('STATE',0)
		self.range = span
		slope = (span[1]-span[0])
		intercept = span[0]
		self._VToCode = np.poly1d([4095./slope,-4095.*intercept/slope ])
		self._CodeToV = np.poly1d([slope/4095.,intercept ])
		self.calibration_enabled = False
		self.calibration_table = []
		self.slope=1
		self.offset=0

	def VToCode(self,cur):
		V = (self.VREF - cur*self.RES)
		#print (V,cur)
		return self._VToCode(V)

	def CodeToV(self,code):
		v = self._CodeToV(code)
		cur = (self.VREF - v)/self.RES
		#print ('rev ',v,cur)
		return cur


	def load_calibration_table(self,table):
		self.calibration_enabled='table'
		self.calibration_table = table

	def load_calibration_twopoint(self,slope,offset):
		self.calibration_enabled='twopoint'
		self.slope = slope
		#print('########################',slope,offset)
		self.offset = offset
		#print(offset)


	def apply_calibration(self,v):
		if self.calibration_enabled=='table':			#Each point is individually calibrated 
			return int(np.clip(v+self.calibration_table[v]	,0,4095))
		elif self.calibration_enabled=='twopoint':		#Overall slope and offset correction is applied
			#print (self.slope,self.offset,v)
			return int(np.clip(v*self.slope+self.offset,0,4095)	)
		else:
			return v
		
class MCP4728:
	defaultVDD =3300
	RESET =6
	WAKEUP =9
	UPDATE =8
	WRITEALL =64
	WRITEONE =88
	SEQWRITE =80
	VREFWRITE =128
	GAINWRITE =192
	POWERDOWNWRITE =160
	GENERALCALL =0
	#def __init__(self,I2C,vref=3.3,devid=0):
	def __init__(self,H,vref=3.3,devid=0):
		self.devid = devid
		self.addr = 0x60|self.devid		#0x60 is the base address
		self.H=H
		self.VREF = vref
		self.I2C = I2C(self.H)
		self.SWITCHEDOFF=[0,0,0,0]
		self.VREFS=[0,0,0,0]  #0=Vdd,1=Internal reference
		self.CHANS = {'PCS':PCSCHAN('PCS',[0,3.3],0),'PV3':DACCHAN('PV3',[0,3.3],1),'PV2':DACCHAN('PV2',[-3.3,3.3],2),'PV1':DACCHAN('PV1',[-5.,5.],3)}
		self.CHANNEL_MAP={0:'PCS',1:'PV3',2:'PV2',3:'PV1'}
		self.values = {'PV1':0,'PV2':0,'PV3':0,'PCS':0}



	def __ignoreCalibration__(self,name):
		self.CHANS[name].calibration_enabled=False

	def setVoltage(self,name,v):
		chan = self.CHANS[name]
		v = int(round(chan.VToCode(v)))		
		return  self.__setRawVoltage__(name,v)

	def getVoltage(self,name):
		return self.values[name]

	def setCurrent(self,v):
		chan = self.CHANS['PCS']
		v = int(round(chan.VToCode(v)))		
		return self.__setRawVoltage__('PCS',v)

	def __setRawVoltage__(self,name,v):
		v=int(np.clip(v,0,4095))
		CHAN = self.CHANS[name]
		'''
		self.H.__sendByte__(CP.DAC) #DAC write coming through.(MCP4728)
		self.H.__sendByte__(CP.SET_DAC)
		self.H.__sendByte__(self.addr<<1)	#I2C address
		self.H.__sendByte__(CHAN.channum)		#DAC channel
		if self.calibration_enabled[name]:
			val = v+self.calibration_tables[name][v]
			#print (val,v,self.calibration_tables[name][v])
			self.H.__sendInt__((CHAN.VREF << 15) | (CHAN.SwitchedOff << 13) | (0 << 12) | (val) )
		else:
			self.H.__sendInt__((CHAN.VREF << 15) | (CHAN.SwitchedOff << 13) | (0 << 12) | v )

		self.H.__get_ack__()
		'''
		val = self.CHANS[name].apply_calibration(v)
		self.I2C.writeBulk(self.addr,[64|(CHAN.channum<<1),(val>>8)&0x0F,val&0xFF])
		self.values[name] =  CHAN.CodeToV(v)
		return self.values[name]


	def __writeall__(self,v1,v2,v3,v4):
		self.I2C.writeBulk(self.addr,[(v1>>8)&0xF,v1&0xFF,(v2>>8)&0xF ,v2&0xFF, (v3>>8)&0xF,v3&0xFF,(v4>>8)&0xF, v4&0xFF ])
		#self.I2C.start(self.addr,0)
		#self.I2C.send((v1>>8)&0xF )
		#self.I2C.send(v1&0xFF)
		#self.I2C.send((v2>>8)&0xF )
		#self.I2C.send(v2&0xFF)
		#self.I2C.send((v3>>8)&0xF )
		#self.I2C.send(v3&0xFF)
		#self.I2C.send((v4>>8)&0xF )
		#self.I2C.send(v4&0xFF)
		#self.I2C.stop()

	def stat(self):
		self.I2C.start(self.addr,0)
		self.I2C.send(0x0) #read raw values starting from address
		self.I2C.restart(self.addr,1)
		vals=self.I2C.read(24)
		self.I2C.stop()
		print (vals)

class NRF24L01():
	"""
	Access the onboard wireless transceiver
	
	.. code-block:: python

		from SEEL import interface
		I = interface.connect()

		I.NRF.get_status()  #Returns a byte containing the value of the STATUS register of the transceiver
		I.NRF.start_token_manager() # Start listening to any IoT nodes broadcasting their presence. Whenever a node is switched on, it transmits its address on a common address to anyone who may be listening
		while I.NRF.total_tokens()<2:  #Switch on a minimum of 2 of nodes now
			time.sleep(0.1)   
		I.NRF.stop_token_manager()  #stop listening. we've received information about two ready nodes.
		list = I.NRF.get_nodelist() #returns a dict object wherein the keys are node addresses, and values are lists of I2C sensors connected on the respective nodes
		print list
		>>> {0x01010A:[58],0x01010B:[96,58]}  #two nodes detected . One has 1 sensor attached, and another has 2
		
	"""


	#Commands
	R_REG = 0x00
	W_REG = 0x20
	RX_PAYLOAD = 0x61
	TX_PAYLOAD = 0xA0
	ACK_PAYLOAD = 0xA8
	FLUSH_TX = 0xE1
	FLUSH_RX = 0xE2
	ACTIVATE = 0x50
	R_STATUS = 0xFF

	#Registers
	NRF_CONFIG = 0x00
	EN_AA = 0x01
	EN_RXADDR = 0x02
	SETUP_AW = 0x03
	SETUP_RETR = 0x04
	RF_CH = 0x05
	RF_SETUP = 0x06
	NRF_STATUS = 0x07
	OBSERVE_TX = 0x08
	CD = 0x09
	RX_ADDR_P0 = 0x0A
	RX_ADDR_P1 = 0x0B
	RX_ADDR_P2 = 0x0C
	RX_ADDR_P3 = 0x0D
	RX_ADDR_P4 = 0x0E
	RX_ADDR_P5 = 0x0F
	TX_ADDR = 0x10
	RX_PW_P0 = 0x11
	RX_PW_P1 = 0x12
	RX_PW_P2 = 0x13
	RX_PW_P3 = 0x14
	RX_PW_P4 = 0x15
	RX_PW_P5 = 0x16
	R_RX_PL_WID = 0x60
	FIFO_STATUS = 0x17
	DYNPD = 0x1C
	FEATURE = 0x1D
	PAYLOAD_SIZE = 0
	ACK_PAYLOAD_SIZE =0
	READ_PAYLOAD_SIZE =0

	NRF_COMMANDS = 3
	NRF_READ_REGISTER =0
	NRF_WRITE_REGISTER =1<<4

	#Valid for broadcast mode
	ALL_BLINK = 1
	ALL_BLINKY = 0
	ALL_BROADCAST = 1

	MISC_COMMANDS = 4  
	WS2812B_CMD  = 0
	SET_DAC = 4
	SET_IO = 6


	CURRENT_ADDRESS=0xAAAA01
	BROADCAST_ADDRESS = 0x111111
	nodelist={}
	nodepos=0
	NODELIST_MAXLENGTH=15
	connected=False
	def __init__(self,H):
		self.H = H
		self.ready=False
		self.sigs={self.CURRENT_ADDRESS:1}
		if self.H.connected:
				self.connected=self.init()

	def init(self):
		try:
			self.H.__sendByte__(CP.NRFL01)
			self.H.__sendByte__(CP.NRF_SETUP)
			self.H.__get_ack__()
			time.sleep(0.015) #15 mS settling time
			stat = self.get_status()
			if stat &0x80:
				print ("Radio transceiver not installed/not found")
				return False
			else:
				self.ready=True
			self.selectAddress(self.CURRENT_ADDRESS)
			#self.write_register(self.SETUP_RETR,0x15)
			self.rxmode()
			time.sleep(0.01)
			self.flush()
			return True
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)
		
	def rxmode(self):
		'''
		Puts the radio into listening mode.
		'''
		try:
			self.H.__sendByte__(CP.NRFL01)
			self.H.__sendByte__(CP.NRF_RXMODE)
			self.H.__get_ack__()
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)
		
	def txmode(self):
		'''
		Puts the radio into transmit mode.
		'''
		try:
			self.H.__sendByte__(CP.NRFL01)
			self.H.__sendByte__(CP.NRF_TXMODE)
			self.H.__get_ack__()
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)

	def triggerAll(self,val):
		self.txmode()
		self.selectAddress(0x111111)
		self.write_register(self.EN_AA,0x00)
		self.write_payload([val],True)
		self.write_register(self.EN_AA,0x01)
		
	def power_down(self):
		try:
			self.H.__sendByte__(CP.NRFL01)
			self.H.__sendByte__(CP.NRF_POWER_DOWN)
			self.H.__get_ack__()
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)
		
	def rxchar(self):
		'''
		Receives a 1 Byte payload
		'''
		try:
			self.H.__sendByte__(CP.NRFL01)
			self.H.__sendByte__(CP.NRF_RXCHAR)
			value = self.H.__getByte__()
			self.H.__get_ack__()
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)
		return value
		
	def txchar(self,char):
		'''
		Transmits a single character
		'''
		try:
			self.H.__sendByte__(CP.NRFL01)
			self.H.__sendByte__(CP.NRF_TXCHAR)
			self.H.__sendByte__(char)
			return self.H.__get_ack__()>>4
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)
		
	def hasData(self):
		'''
		Check if the RX FIFO contains data
		'''
		try:
			self.H.__sendByte__(CP.NRFL01)
			self.H.__sendByte__(CP.NRF_HASDATA)
			value = self.H.__getByte__()
			self.H.__get_ack__()
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)
		return value
		
	def flush(self):
		'''
		Flushes the TX and RX FIFOs
		'''
		try:
			self.H.__sendByte__(CP.NRFL01)
			self.H.__sendByte__(CP.NRF_FLUSH)
			self.H.__get_ack__()
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)

	def write_register(self,address,value):
		'''
		write a  byte to any of the configuration registers on the Radio.
		address byte can either be located in the NRF24L01+ manual, or chosen
		from some of the constants defined in this module.
		'''
		#print ('writing',address,value)
		try:
			self.H.__sendByte__(CP.NRFL01)
			self.H.__sendByte__(CP.NRF_WRITEREG)
			self.H.__sendByte__(address)
			self.H.__sendByte__(value)
			self.H.__get_ack__()
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)

	def read_register(self,address):
		'''
		Read the value of any of the configuration registers on the radio module.
		
		'''
		try:
			self.H.__sendByte__(CP.NRFL01)
			self.H.__sendByte__(CP.NRF_READREG)
			self.H.__sendByte__(address)
			val=self.H.__getByte__()
			self.H.__get_ack__()
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)
		return val

	def get_status(self):
		'''
		Returns a byte representing the STATUS register on the radio.
		Refer to NRF24L01+ documentation for further details
		'''
		try:
			self.H.__sendByte__(CP.NRFL01)
			self.H.__sendByte__(CP.NRF_GETSTATUS)
			val=self.H.__getByte__()
			self.H.__get_ack__()
			return val
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)

	def write_command(self,cmd):
		try:
			self.H.__sendByte__(CP.NRFL01)
			self.H.__sendByte__(CP.NRF_WRITECOMMAND)
			self.H.__sendByte__(cmd)
			self.H.__get_ack__()
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)

	def write_address(self,register,address):
		'''
		register can be TX_ADDR, RX_ADDR_P0 -> RX_ADDR_P5
		3 byte address.  eg 0xFFABXX . XX cannot be FF
		if RX_ADDR_P1 needs to be used along with any of the pipes
		from P2 to P5, then RX_ADDR_P1 must be updated last.
		Addresses from P1-P5 must share the first two bytes.
		'''
		try:
			self.H.__sendByte__(CP.NRFL01)
			self.H.__sendByte__(CP.NRF_WRITEADDRESS)
			self.H.__sendByte__(register)
			self.H.__sendByte__(address&0xFF);self.H.__sendByte__((address>>8)&0xFF);
			self.H.__sendByte__((address>>16)&0xFF);
			self.H.__get_ack__()
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)

	def selectAddress(self,address):
		'''
		Sets RX_ADDR_P0 and TX_ADDR to the specified address.
		
		'''
		try:
			self.H.__sendByte__(CP.NRFL01)
			self.H.__sendByte__(CP.NRF_WRITEADDRESSES)
			self.H.__sendByte__(address&0xFF);self.H.__sendByte__((address>>8)&0xFF);
			self.H.__sendByte__((address>>16)&0xFF);
			self.H.__get_ack__()
			self.CURRENT_ADDRESS=address
			if address not in self.sigs:
				self.sigs[address]=1
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)
		
	def read_payload(self,numbytes):
		try:
			self.H.__sendByte__(CP.NRFL01)
			self.H.__sendByte__(CP.NRF_READPAYLOAD)
			self.H.__sendByte__(numbytes)
			data=self.H.fd.read(numbytes)
			self.H.__get_ack__()
			return [ord(a) for a in data]
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)

	def write_payload(self,data,verbose=False,**args): 
		try:
			self.H.__sendByte__(CP.NRFL01)
			self.H.__sendByte__(CP.NRF_WRITEPAYLOAD)
			numbytes=len(data)|0x80   #0x80 implies transmit immediately. Otherwise it will simply load the TX FIFO ( used by ACK_payload)
			if(args.get('rxmode',False)):numbytes|=0x40
			self.H.__sendByte__(numbytes)
			self.H.__sendByte__(self.TX_PAYLOAD)
			for a in data:
				self.H.__sendByte__(a)
			val=self.H.__get_ack__()>>4
			if(verbose):
				if val&0x2: print (' NRF radio not found. Connect one to the add-on port')
				elif val&0x1: print (' Node probably dead/out of range. It failed to acknowledge')
				return
			return val
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)

	def transaction(self,data,**args):
		st = time.time()
		try:
			timeout = args.get('timeout',200)
			verbose = args.get('verbose',False)

			#print ('#################',args)
			if args.get('listen',True):data[0]|=0x80  # You need this if hardware must wait for a reply

			self.H.__sendByte__(CP.NRFL01)
			self.H.__sendByte__(CP.NRF_TRANSACTION)
			self.H.__sendByte__(len(data)) #total Data bytes coming through
			self.H.__sendInt__(timeout) #timeout.  		
			for a in data:
				self.H.__sendByte__(a)
			self.H.waitForData(timeout/1.e4+0.2) #convert to mS
			numbytes=self.H.__getByte__()
			if numbytes: data = [ord(a) for a in self.H.fd.read(numbytes)]
			else: data=[]
			val=self.H.__get_ack__()>>4
			
			#print ('dt send',time.time()-st,timeout,data,str(bin(val)))
			
			if(verbose):
				if val&0x1: print (time.time(),'%s Err. Node not found'%(hex(self.CURRENT_ADDRESS)))
				if val&0x2: print (time.time(),'%s Err. NRF on-board transmitter not found'%(hex(self.CURRENT_ADDRESS)))
				if val&0x4 and args.get('listen',True): print (time.time(),'%s Err. Node received command but did not reply'%(hex(self.CURRENT_ADDRESS)))
			if val&0x7:	#Something didn't go right.
				self.flush()
				self.sigs[self.CURRENT_ADDRESS] = self.sigs[self.CURRENT_ADDRESS]*50/51.
				return False
			
			self.sigs[self.CURRENT_ADDRESS] = (self.sigs[self.CURRENT_ADDRESS]*50+1)/51.
			return data
		except Exception as ex:
			print('Exception:',ex)

	def transactionWithRetries(self,data,**args):
		retries = args.get('retries',5)
		reply=False
		while retries>0:
			reply = self.transaction(data,verbose=(retries==1),**args)
			if reply:
				break
			retries-=1
		return reply

	def write_ack_payload(self,data,pipe): 
		if(len(data)!=self.ACK_PAYLOAD_SIZE):
			self.ACK_PAYLOAD_SIZE=len(data)
			if self.ACK_PAYLOAD_SIZE>15:
				print ('too large. truncating.')
				self.ACK_PAYLOAD_SIZE=15
				data=data[:15]
			else:
				print ('ack payload size:',self.ACK_PAYLOAD_SIZE)
		try:
			self.H.__sendByte__(CP.NRFL01)
			self.H.__sendByte__(CP.NRF_WRITEPAYLOAD)
			self.H.__sendByte__(len(data))
			self.H.__sendByte__(self.ACK_PAYLOAD|pipe)
			for a in data:
				self.H.__sendByte__(a)
			return self.H.__get_ack__()>>4
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)

	def start_token_manager(self):
		'''
		'''
		try:
			self.H.__sendByte__(CP.NRFL01)
			self.H.__sendByte__(CP.NRF_START_TOKEN_MANAGER)
			self.H.__get_ack__()
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)

	def stop_token_manager(self):
		'''
		'''
		try:
			self.H.__sendByte__(CP.NRFL01)
			self.H.__sendByte__(CP.NRF_STOP_TOKEN_MANAGER)
			self.H.__get_ack__()
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)

	def total_tokens(self):
		'''
		'''
		try:
			self.H.__sendByte__(CP.NRFL01)
			self.H.__sendByte__(CP.NRF_TOTAL_TOKENS)
			x = self.H.__getByte__()
			self.H.__get_ack__()
			return x
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)

	def fetch_report(self,num):
		'''
		'''
		try:
			self.H.__sendByte__(CP.NRFL01)
			self.H.__sendByte__(CP.NRF_REPORTS)
			self.H.__sendByte__(num)
			data = [self.H.__getByte__() for a in range(20)]
			self.H.__get_ack__()
			return data
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)

	def __decode_I2C_list__(self,data):
		lst=[]
		if sum(data)==0:
			return lst
		for a in range(len(data)):
			if(data[a]^255):
				for b in range(8):
					if data[a]&(0x80>>b)==0:
						addr = 8*a+b
						lst.append(addr)
		return lst
		
	def get_nodelist(self,check_alive = False):
		'''
		Refer to the variable 'nodelist' if you simply want a list of nodes that either registered while your code was
		running , or were loaded from the firmware buffer(max 15 entries)

		If you plan to use more than 15 nodes, and wish to register their addresses without having to feed them manually,
		then this function must be called each time before the buffer resets (every fifteen nodes).
		
		The dictionary object returned by this function is filtered by checking with each node if they are alive first.
		
		:return: {address_Node1:[[registered sensors(I2C Addresses 0-8 are not auto detected)],battery%],address_Node2:[[registered sensors],battery%] ... }
		
		'''
		total = self.total_tokens()
		total+=1
		if total==self.NODELIST_MAXLENGTH:total=0
		
		if self.nodepos!=total:
			#print ('pos = ',self.nodepos)
			for nm in range(self.nodepos,self.NODELIST_MAXLENGTH)+range(0,self.nodepos):
				dat = self.fetch_report(nm)
				#print (nm,dat)
				txrx=(dat[0])|(dat[1]<<8)|(dat[2]<<16)
				if not txrx:
					continue
				self.nodelist[txrx]=[self.__decode_I2C_list__(dat[3:19]),min(100,int(dat[19]*100./93))]
			self.nodepos=total
			#else:
			#	self.__delete_registered_node__(nm)

		filtered_lst={}
		for a in self.nodelist:
			if check_alive:
				if self.isAlive(a):
					filtered_lst[a]=self.nodelist[a]
					#print (self.nodelist[a][1])			
			else:
				filtered_lst[a]=self.nodelist[a]
		return filtered_lst

	def __delete_registered_node__(self,num):
		try:
			self.H.__sendByte__(CP.NRFL01)
			self.H.__sendByte__(CP.NRF_DELETE_REPORT_ROW)
			self.H.__sendByte__(num)
			self.H.__get_ack__()
		except Exception as ex:
			self.raiseException(ex, "Communication Error , Function : "+inspect.currentframe().f_code.co_name)
		
	def __delete_all_registered_nodes__(self):
			while self.total_tokens():
				print ('-')
				self.__delete_registered_node__(0)

	def isAlive(self,addr):
		self.selectAddress(addr)
		return self.transaction([self.NRF_COMMANDS,self.NRF_READ_REGISTER]+[self.R_STATUS],timeout=500,verbose=False)

	def init_shockburst_transmitter(self,**args):
		'''
		Puts the radio into transmit mode.
		Dynamic Payload with auto acknowledge is enabled.
		upto 5 retransmits with 1ms delay between each in case a node doesn't respond in time
		Receivers must acknowledge payloads
		'''
		self.PAYLOAD_SIZE=args.get('PAYLOAD_SIZE',self.PAYLOAD_SIZE)
		myaddr=args.get('myaddr',0xAAAA01)
		sendaddr=args.get('sendaddr',0xAAAA01)

		self.init()
		#shockburst
		self.write_address(self.RX_ADDR_P0,myaddr)	#transmitter's address
		self.write_address(self.TX_ADDR,sendaddr)     #send to node with this address
		self.write_register(self.RX_PW_P0,self.PAYLOAD_SIZE) 
		self.rxmode()
		time.sleep(0.1)
		self.flush()

	def init_shockburst_receiver(self,**args):
		'''
		Puts the radio into receive mode.
		Dynamic Payload with auto acknowledge is enabled.
		'''
		self.PAYLOAD_SIZE=args.get('PAYLOAD_SIZE',self.PAYLOAD_SIZE)
		if 'myaddr0' not in args:
			args['myaddr0']=0xA523B5
		#if 'sendaddr' non in args:
		#	args['sendaddr']=0xA523B5
		print (args)
		self.init()
		self.write_register(self.RF_SETUP,0x26)  #2MBPS speed

		#self.write_address(self.TX_ADDR,sendaddr)     #send to node with this address
		#self.write_address(self.RX_ADDR_P0,myaddr)	#will receive the ACK Payload from that node
		enabled_pipes = 0				#pipes to be enabled
		for a in range(0,6):
			x=args.get('myaddr'+str(a),None)
			if x: 
				print (hex(x),hex(self.RX_ADDR_P0+a))
				enabled_pipes|= (1<<a)
				self.write_address(self.RX_ADDR_P0+a,x)
		P15_base_address = args.get('myaddr1',None)
		if P15_base_address: self.write_address(self.RX_ADDR_P1,P15_base_address)

		self.write_register(self.EN_RXADDR,enabled_pipes) #enable pipes
		self.write_register(self.EN_AA,enabled_pipes) #enable auto Acknowledge on all pipes
		self.write_register(self.DYNPD,enabled_pipes) #enable dynamic payload on Data pipes
		self.write_register(self.FEATURE,0x06) #enable dynamic payload length
		#self.write_register(self.RX_PW_P0,self.PAYLOAD_SIZE)

		self.rxmode()
		time.sleep(0.1)
		self.flush()

	def __selectBroadcast__(self):
		if self.CURRENT_ADDRESS!=self.BROADCAST_ADDRESS:
			self.selectAddress(self.BROADCAST_ADDRESS)

	def broadcastBlink(self,number_of_blinks):
		'''
		initiates a blink sequence on all nearby nodes
		'''
		self.__selectBroadcast__()
		return self.transaction([self.ALL_BLINK,self.ALL_BLINKY,number_of_blinks],listen = False)

	def broadcastPing(self):
		'''
		Ping all nodes in the vicinity. All powered up nodes will respond with sensor and battery data
		'''
		self.__selectBroadcast__()
		val = self.transaction([self.ALL_BLINK,self.ALL_BROADCAST],listen = False)
		time.sleep(0.1)

	#Miscellaneous features
	def WS2812B(self,cols):
		"""
		set shade of WS2182 LED on CS1/RC0 for all devices in the vicinity
		
		.. tabularcolumns:: |p{3cm}|p{11cm}|
		
		==============  ============================================================================================
		**Arguments** 
		==============  ============================================================================================
		cols                2Darray [[R,G,B],[R2,G2,B2],[R3,G3,B3]...]
							brightness of R,G,B ( 0-255  )
		==============  ============================================================================================

		example::
		
			>>> WS2812B([[10,0,0],[0,10,10],[10,0,10]])
			#sets red, cyan, magenta to three daisy chained LEDs

		"""
		self.__selectBroadcast__()
		colarray=[]
		for a in cols:
			colarray.append(int('{:08b}'.format(int(a[1]))[::-1], 2))
			colarray.append(int('{:08b}'.format(int(a[0]))[::-1], 2))
			colarray.append(int('{:08b}'.format(int(a[2]))[::-1], 2))

		res = self.transaction([self.MISC_COMMANDS,self.WS2812B_CMD]+colarray,listen=False)
		return res



	def raiseException(self,ex, msg):
			msg += '\n' + ex.message
			#self.H.disconnect()
			raise RuntimeError(msg)


class RadioLink():
	'''
	A simplified wrapper for interacting with IoT Nodes.
	
	.. tabularcolumns:: |p{3cm}|p{11cm}|
	
	
	==============  ============================================================================================
	**Arguments**   Description
	==============  ============================================================================================
	NRF             ~interface.NRF instance 
	*\*\args
	address         3-byte address of the node. e.g 0x01010A
	==============  ============================================================================================		
	
	Example for connecting to a wireless node, and setting the color of its on-board neopixel. Also scan the I2C bus
	
	.. code-block:: python
	
		link = I.newRadioLink(address = 0x01010A)   #This address is unique for each IoT node, and is printed on it
		link.WS2812B([[0,255,255]])  #Set the colour of the onboard RGB LED to cyan
		print link.I2C_scan()        #Scan the I2C bus of the IoT node, and return detected addresses
		>>> [58]
		
	Example for connecting to a wireless node, and reading the values from a magnetometer connected to its I2C port
	
	.. code-block:: python
	
		link = I.newRadioLink(address = 0x01010A)   #This address is unique for each IoT node, and is printed on it
		from SEEL.SENSORS import HMC5883L
		mag = HMC5883L.connect(link)  # Tell the magnetometer's class to use the IoT node with address 0x01010A as the link to the magnetometer
		print mag.getRaw()
		>>> [0.01,126.3,24.0]  # magnetic fields along the x,y, and z axes of the sensor


		
	'''
	ADC_COMMANDS =1
	CAPTURE_ADC =0
	READ_ADC =1


	SPI_COMMANDS =6
	SPI_TRANSACTION =0

	I2C_COMMANDS =2
	I2C_TRANSACTION =0
	I2C_WRITE =1
	SCAN_I2C =2
	PULL_SCL_LOW = 3
	I2C_CONFIG = 4
	I2C_READ = 5

	NRF_COMMANDS = 3
	NRF_READ_REGISTER =0
	NRF_WRITE_REGISTER =1
	NRF_BLE = 2

	MISC_COMMANDS = 4
	WS2812B_CMD  = 0
	EEPROM_WRITE = 1
	EEPROM_READ  = 2
	RESET_DEVICE = 3
	SET_DAC = 4
	SET_DOZE = 5
	SET_IO = 6
	
	PWM_COMMANDS = 5
	SET_PWM      = 0
	GET_FREQ     = 1
	
	
	def __init__(self,NRF,**args):
		self.NRF = NRF
		if 'address' in args:
			self.ADDRESS = args.get('address',False)
		else:
			print ('Address not specified. Add "address=0x....." argument while instantiating')
			self.ADDRESS=0x010101
		self.adc_map = {
			'BAT':self.adc_chan(0b100,0,6.6),
			'CS3':self.adc_chan(0b10111,0,3.3),
			'FVR':self.adc_chan(0b111111,0,3.3),
			'DAC':self.adc_chan(0b111110,0,3.3),
			'TEMP':self.adc_chan(0b111101,0,3.3),
			'AVss':self.adc_chan(0b111100,0,3.3),
		}
		#self.write_register(self.NRF.SETUP_RETR,0x12)

	def __selectMe__(self):
		if self.NRF.CURRENT_ADDRESS!=self.ADDRESS:
			self.NRF.selectAddress(self.ADDRESS)

	#ADC Commands
	class adc_chan:
		def __init__(self,AN,minV,maxV):
			self.AN = AN
			self.minV = minV
			self.maxV = maxV
			self.poly = np.poly1d([0,(maxV-minV)/1023.,minV])
		def applyCal(self,code):
			return self.poly(code)

	def captureADC(self,channel):
		'''
		Read 16 bytes from the ADC
		
		.. tabularcolumns:: |p{3cm}|p{11cm}|
		
		
		==============  ============================================================================================
		**Arguments**   Description
		==============  ============================================================================================
		channel         'BAT' , 'CS3'
		==============  ============================================================================================		
		
		'''
		self.__selectMe__()
		chan = self.adc_map.get(channel,None)
		if not chan:
			print ('channel not available')
			return False
		
		vals = self.NRF.transactionWithRetries([self.ADC_COMMANDS,self.CAPTURE_ADC]+[chan.AN],timeout=400)
		if vals:
			if len(vals)==32:
				intvals = []
				for a in range(16): intvals.append ( (vals[a*2]<<8)|vals[a*2+1]  )
				return chan.applyCal(intvals)
			else:
				print ('packet dropped')
				return False
		else:
			print ('packet dropped')
			return False

	def readADC(self,channel,verbose=False):
		'''
		Read bytes from the ADC
		
		.. tabularcolumns:: |p{3cm}|p{11cm}|
		
		
		==============  ============================================================================================
		**Arguments**   Description
		==============  ============================================================================================
		channel         'BAT' , 'CS3'
		==============  ============================================================================================		
		
		'''
		self.__selectMe__()
		chan = self.adc_map.get(channel,None)
		if not chan:
			print ('channel not available')
			return False		
		vals = self.NRF.transactionWithRetries([self.ADC_COMMANDS,self.READ_ADC]+[chan.AN],timeout=400)
		if vals:
			if len(vals)==2:
				if verbose: print (vals)
				return chan.applyCal((vals[0]<<8)|vals[1])
			else:
				print ('packet dropped')
				return False
		else:
			print ('packet dropped')
			return False

	#I2C Commands
	def I2C_scan(self):
		'''
		Scans the I2C bus and returns a list of active addresses. 
		'''
		self.__selectMe__()
		import sensorlist
		print ('Scanning addresses 0-127...')
		x = self.NRF.transaction([self.I2C_COMMANDS,self.SCAN_I2C],timeout=500)
		if not x:return []
		if not sum(x):return []
		addrs=[]
		print ('Address','\t','Possible Devices')

		for a in range(16):
			if(x[a]^255):
				for b in range(8):
					if x[a]&(0x80>>b)==0:
						addr = 8*a+b
						addrs.append(addr)
						print (hex(addr),'\t\t',sensorlist.sensors.get(addr,'None'))
						
		return addrs

	def __decode_I2C_list__(self,data):
		lst=[]
		if sum(data)==0:
			return lst
		for a in range(len(data)):
			if(data[a]^255):
				for b in range(8):
					if data[a]&(0x80>>b)==0:
						addr = 8*a+b
						lst.append(addr)
		return lst

	def writeI2C(self,I2C_addr,regaddress,bytes):
		self.__selectMe__()
		return self.NRF.transaction([self.I2C_COMMANDS,self.I2C_WRITE]+[I2C_addr]+[regaddress]+bytes)
		
	def readI2C(self,I2C_addr,regaddress,numbytes):
		self.__selectMe__()
		return self.NRF.transaction([self.I2C_COMMANDS,self.I2C_TRANSACTION]+[I2C_addr]+[regaddress]+[numbytes])

	def writeBulk(self,I2C_addr,bytes):
		'''
		Write bytes to an I2C sensor
		
		.. tabularcolumns:: |p{3cm}|p{11cm}|
		
		
		==============  ============================================================================================
		**Arguments**   Description
		==============  ============================================================================================
		I2C_addr        address of the I2C sensor
		bytes           an array of bytes to be written
		==============  ============================================================================================		
		
		'''
		self.__selectMe__()
		return self.NRF.transaction([self.I2C_COMMANDS,self.I2C_WRITE]+[I2C_addr]+bytes)
		
	def readBulk(self,I2C_addr,regaddress,numbytes):
		'''
		Read bytes from an I2C sensor
		
		.. tabularcolumns:: |p{3cm}|p{11cm}|
		
		
		==============  ============================================================================================
		**Arguments**   Description
		==============  ============================================================================================
		I2C_addr        address of the I2C sensor
		regaddress      address of the register to read from
		numbytes        number of bytes to read
		==============  ============================================================================================		
		
		'''
		self.__selectMe__()
		return self.NRF.transactionWithRetries([self.I2C_COMMANDS,self.I2C_TRANSACTION]+[I2C_addr]+[regaddress]+[numbytes],timeout = 30)

	def simpleRead(self,I2C_addr,numbytes):
		self.__selectMe__()
		return self.NRF.transactionWithRetries([self.I2C_COMMANDS,self.I2C_READ]+[I2C_addr]+[numbytes])

	def pullSCLLow(self,t_ms):
		'''
		hold the SCL line low for a defined period. Used by sensors such as MLX90316
		
		
		'''
		self.__selectMe__()
		dat=self.NRF.transaction([self.I2C_COMMANDS,self.PULL_SCL_LOW]+[t_ms])
		if dat:
			return self.__decode_I2C_list__(dat)
		else:
			return []

	def configI2C(self,freq):
		'''
		Set the frequency of the I2C port on the wireless node.
		
		.. tabularcolumns:: |p{3cm}|p{11cm}|
		
		
		==============  ============================================================================================
		**Arguments**   Description
		==============  ============================================================================================
		freq            Frequency
		==============  ============================================================================================		
		
		'''
		self.__selectMe__()
		brgval=int(32e6/freq/4 - 1)
		print (brgval)
		return self.NRF.transaction([self.I2C_COMMANDS,self.I2C_CONFIG]+[brgval],listen=False)

	#SPI commands
	def readSPI(self,chip_select,data):
		'''
		Accepts an array
		
		.. tabularcolumns:: |p{3cm}|p{11cm}|
		
		
		==============  ============================================================================================
		**Arguments**   Description
		==============  ============================================================================================
		chip_select     'CS1' or 'CS2'
		data            array of elements to write to SDO while data is simultaneously clocked in via SDI
		==============  ============================================================================================		
		
		'''
		self.__selectMe__()
		if chip_select=='CS1':cs=1
		elif chip_select=='CS2':cs=2
		else:
			print ('invalid chip select')
			return
		return self.NRF.transactionWithRetries([self.SPI_COMMANDS,self.SPI_TRANSACTION,cs]+data)


	#NRF Commands
	def write_register(self,reg,val):
		self.__selectMe__()
		#print ('writing to ',reg,val)
		return self.NRF.transaction([self.NRF_COMMANDS,self.NRF_WRITE_REGISTER]+[reg,val],listen=False)

	def read_register(self,reg):
		self.__selectMe__()
		x=self.NRF.transaction([self.NRF_COMMANDS,self.NRF_READ_REGISTER]+[reg])
		if x:
			return x[0]
		else:
			return False
			
	#Miscellaneous features
	def WS2812B(self,cols):
		"""
		set shade of WS2182 LED on CS1/RC0
		
		.. tabularcolumns:: |p{3cm}|p{11cm}|
		
		==============  ============================================================================================
		**Arguments** 
		==============  ============================================================================================
		cols                2Darray [[R,G,B],[R2,G2,B2],[R3,G3,B3]...]
							brightness of R,G,B ( 0-255  )
		==============  ============================================================================================

		example::
		
			>>> WS2812B([[10,0,0],[0,10,10],[10,0,10]])
			#sets red, cyan, magenta to three daisy chained LEDs

		"""
		self.__selectMe__()
		colarray=[]
		for a in cols:
			colarray.append(int('{:08b}'.format(int(a[1]))[::-1], 2))
			colarray.append(int('{:08b}'.format(int(a[0]))[::-1], 2))
			colarray.append(int('{:08b}'.format(int(a[2]))[::-1], 2))

		res = self.NRF.transaction([self.MISC_COMMANDS,self.WS2812B_CMD]+colarray,listen=False)
		return res

	def reset(self):
		"""
		Reset the wireless node.
		If EEPROM locations 0,1,2 were updated, the node will restart at the new address
		"""

		self.__selectMe__()
		res = self.NRF.transactionWithRetries([self.MISC_COMMANDS,self.RESET_DEVICE],listen=False)
		return res

	def batteryLevel(self):
		"""
		Read the battery status, and return a percentage value.
		Do not operate at very low levels if running on a Lithium battery. It reduces their lifetime
		"""
		return max(min((self.readADC('BAT')-3.7)*200,100),0)

	def setDAC(self,val):
		"""
		Write to 5 bit DAC 
		0 < val < 3.3
		"""
		code = int(val*31/3.3)
		self.__selectMe__()
		res = self.NRF.transactionWithRetries([self.MISC_COMMANDS,self.SET_DAC,code],timeout=100)
		if res:return 3.3*res[0]/31
		else : return False

	def lowPowerMode(self,level = False):
		"""
		Reduce the CPU frequency of the node's processor
		Level  in [False, 1 ... 7 ] 
		"""
		self.__selectMe__()
		if level : self.NRF.transactionWithRetries([self.MISC_COMMANDS,self.SET_DOZE,(1<<6)|(level)],listen = False) #111 = 1/256 scaling
		else : self.NRF.transactionWithRetries([self.MISC_COMMANDS,self.SET_DOZE,0],listen = False)  #disable low power mode

	def setIO(self,**kwargs):
		"""
		Toggle CS1 or CS2 digital output. up to 5mA sink/source capacity
		These pins also serve as chip selects for SPI devices. If any of the
		chip selects are connected to an SPI device, toggling them can cause an SPI clash and
		will result in the node becoming unresponsive until a power reset.

		==============  ============================================================================================
		**Arguments** 
		==============  ============================================================================================
		*\*\kwargs      CS1 = 1/0
						CS2 = 1/0
		==============  ============================================================================================

		example::
		
			>>> link.setIO(CS1 = False, CS2 = True)  #Set CS1 to 0V , CS2 to 3.3V
			#sets red, cyan, magenta to three daisy chained LEDs
		"""
		io=0
		if 'CS1' in kwargs: io |= 1|(kwargs.get('CS1')<<4)
		if 'CS2' in kwargs: io |= 2|(kwargs.get('CS2')<<5)
		self.__selectMe__()
		if io: return self.NRF.transaction([self.MISC_COMMANDS,self.SET_IO,io],listen = False)  #disable low power mode
		else: return False

	def readFrequency(self,prescaler = 6):
		'''
		Read frequency of input TTL signal on CS3 (0-3.3V)
		
		Select a prescaler value that obtains maximum resolution for your measurement range.
		
		.. tabularcolumns:: |p{3cm}|p{11cm}|
		
		Range = 250/(2**prescaler) - 8e6/(2**prescaler)
		
		==============  ============================================================================================
		**Prescaler**   **Frequency Range**
		==============  ============================================================================================
		2               62.5Hz to 2MHz
		3               31.25Hz to 1MHz
		4               16Hz  to 500KHz
		5               8Hz  to 250KHz
		6               4Hz  to 125KHz
		7               2Hz  to 62.5KHz
		==============  ============================================================================================		
		
		'''
		prescaler = min(7,max(2,prescaler)) # fix prescaler between 2 and 7
		self.__selectMe__()
		vals = self.NRF.transactionWithRetries([self.PWM_COMMANDS,self.GET_FREQ]+[(0b110<<4)|prescaler],timeout=int(min(max(30,40*2**prescaler),65000)) ) #0b110 = 4 edges . 0b111 = every 16 edges
		if vals:
			dcode = ((vals[2]<<8)|vals[3] ) - ((vals[0]<<8)|vals[1])
			dt = (2**prescaler)*( dcode )/8e6/4.  # prescale * counts /8e6/4
			if dcode<2:
				if prescaler<8 and dcode<0:print ('frequency too low . increase prescaler')			
				elif prescaler>0 and dcode<2:print ('frequency too high . decrease prescaler')			
				else: print ('frequency out of range')
				return False
			return 1./dt
		else:
			return False

	def readHighFrequency(self):
		'''
		Read frequencies between 10KHz and 8MHz from input TTL signal on CS3 (0-3.3V)
		'''
		self.__selectMe__()
		vals = self.NRF.transactionWithRetries([self.PWM_COMMANDS,self.GET_FREQ]+[(0b111<<4)],timeout=3000 ) # 0b111 = every 16 edges
		if vals:
			dcode = ((vals[2]<<8)|vals[3] ) - ((vals[0]<<8)|vals[1])
			dt = ( dcode )/8e6/16.  # prescale * counts /8e6/4
			if dcode<2:
				print ('frequency out of range')
				return False
			return 1./dt
		else:
			return False

	def write_eeprom(self,locations,values):
		"""
		Write to EEPROM Locations
		
		.. tabularcolumns:: |p{3cm}|p{11cm}|
		
		==============  ============================================================================================
		**Arguments** 
		==============  ============================================================================================
		locations       Array of positions between 0 and 255 e.g. : [4,5,6]
		values          Array of values to write to those locations
 		==============  ============================================================================================

		Caution : Positions 0,1,2 are used for storing the address of the wireless node. If you change these, you
		will have to reconnect to the new address once the wireless node is reset/power cycled.
		
		example::
		
			>>> write_eeprom([3,4,5],[3,3,3])
			write the value 3 to locations 3,4,5

		"""
		self.__selectMe__()
		mixarray=[]
		if len(locations) != len(values):
			print ('mismatch in number of locations and values')
			return False

		for a,b in zip(locations,values):
			mixarray+=[a,b]

		res = self.NRF.transaction([self.MISC_COMMANDS,self.EEPROM_WRITE]+mixarray,timeout=100)
		print (res)

	def read_eeprom(self,locations):
		"""
		read from EEPROM Locations
		
		.. tabularcolumns:: |p{3cm}|p{11cm}|
		
		==============  ============================================================================================
		**Arguments** 
		==============  ============================================================================================
		locations       Array of positions between 0 and 255 e.g. : [4,5,6]
 		==============  ============================================================================================

		Positions 0,1,2 are used for storing the address of the wireless node.
		
		example::
		
			>>> read_eeprom([3,4,5])
			read from locations 3,4,5

		"""
		self.__selectMe__()
		res = self.NRF.transactionWithRetries([self.MISC_COMMANDS,self.EEPROM_READ]+locations)
		return res

	def raiseException(self,ex, msg):
			msg += '\n' + ex.message
			#self.H.disconnect()
			raise RuntimeError(msg)
	def __ble__(self):
		self.__selectMe__()
		#print ('writing to ',reg,val)
		return self.NRF.transaction([self.NRF_COMMANDS,self.NRF_BLE],listen=False)
		
