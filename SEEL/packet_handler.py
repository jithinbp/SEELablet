from __future__ import print_function
import time
ST=time.time()
def timeit(arg=''):
	global ST
	T = time.time()
	print(arg," : ",T-ST)
	ST=T

timeit('packet start')

import SEEL.commands_proto as CP
import serial, subprocess
timeit('serial,sub,comm')



class Handler():
	def __init__(self,timeout=1.0,**kwargs):
		self.burstBuffer=b''
		self.loadBurst=False
		self.inputQueueSize=0
		self.BAUD = 1000000
		self.BASE_PORT_NAME = "/dev/ttyACM"
		self.timeout=timeout
		self.version_string=b''
		self.connected=False
		self.fd = None
		self.expected_version=b'CS'
		self.occupiedPorts=[]
		if 'port' in kwargs:
			self.portname=kwargs.get('port',None)
			self.fd,self.version_string,self.connected=self.connectToPort(self.portname)
			print('Connected to device at ',self.portname,' ,Version:',self.version_string)
			return
		else:	#Scan and pick a port	
			timeit('ready')
			for a in range(10):
				try:
					self.portname=self.BASE_PORT_NAME+str(a)
					timeit('attempt %s'%self.portname)
					self.fd,self.version_string,self.connected=self.connectToPort(self.portname)
					if self.connected:return
					#print(self.BASE_PORT_NAME+str(a)+' .yes.',version)
				except IOError:
					#print(self.BASE_PORT_NAME+str(a)+' .no.')
					pass
			if not self.connected:
					print('Device not found')
		
	def connectToPort(self,portname):
		try:
			import socket
			self.s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
			self.s.bind( '\0SEELablet%s'%portname) 
			fd = serial.Serial(portname, 9600, stopbits=1, timeout = 0.02)
			fd.read(100);fd.close()
			fd = serial.Serial(portname, self.BAUD, stopbits=1, timeout = 1.0)
			if(fd.inWaiting()):
				fd.setTimeout(0.1)
				fd.read(1000)
				fd.flush()
				fd.setTimeout(1.0)
			version= self.get_version(fd)
			if version[:len(self.expected_version)]==self.expected_version:
				return fd,version,True
		except socket.error as e:
			error_code = e.args[0]
			error_string = e.args[1]
			self.occupiedPorts.append(portname)
			print("Process already using %s (%d). Exiting" % (portname, error_code) )

		return None,'',False

	def get_version(self,fd):
		fd.write(CP.COMMON)
		fd.write(CP.GET_VERSION)
		x=fd.readline()
		#print('remaining',[ord(a) for a in fd.read(10)])
		if len(x):
			x=x[:-1]
		return x

	def reconnect(self,**kwargs):
		if 'port' in kwargs:
			self.portname=kwargs.get('port',None)

		try:
			time.sleep(1.0)
			self.fd = serial.Serial(self.portname, 9600, stopbits=1, timeout = 0.1)
			self.fd.close()
			time.sleep(0.2)
			self.fd = serial.Serial(self.portname, self.BAUD, stopbits=1, timeout = self.timeout)
			if(self.fd.inWaiting()):
				self.fd.read(1000)
				self.fd.flush()
			version = self.get_version(self.fd)
			print('Connected to device at:',self.portname,' ,Version:',version)
			self.connected=True
			self.version_string=version
		except serial.SerialException as ex:
			print("failed to connect. Check device connections ,Or\nls /dev/TestBench\nOr, check if symlink has been created in /etc/udev/rules.d/proto.rules for the relevant Vid,Pid")

	def __del__(self):
		#print('closing port')
		try:self.fd.close()
		except: pass

	def __get_ack__(self):
		"""
		fetches the response byte
		1 SUCCESS
		2 ARGUMENT_ERROR
		3 FAILED
		used as a handshake
		"""
		if not self.loadBurst:
			x=self.fd.read(1)
		else:
			self.inputQueueSize+=1
			return 1
		try:
			return CP.Byte.unpack(x)[0]
		except:
			return 3

	def __sendInt__(self,val):
		"""
		transmits an integer packaged as two characters
		:params int val: int to send
		"""
		if not self.loadBurst:self.fd.write(CP.ShortInt.pack(int(val)))
		else: self.burstBuffer+=CP.ShortInt.pack(int(val))

	def __sendByte__(self,val):
		"""
		transmits a BYTE
		val - byte to send
		"""
		#print (val)
		if(type(val)==int):
			if not self.loadBurst:self.fd.write(CP.Byte.pack(val))
			else:self.burstBuffer+=CP.Byte.pack(val)
		else:
			if not self.loadBurst:self.fd.write(val)
			else:self.burstBuffer+=val
			
	def __getByte__(self):
		"""
		reads a byte from the serial port and returns it
		"""
		ss=self.fd.read(1)
		if len(ss): return CP.Byte.unpack(ss)[0]
		else:
			print('byte communication error.',time.ctime())
			return -1
			#sys.exit(1)

	def __getInt__(self):
		"""
		reads two bytes from the serial port and
		returns an integer after combining them
		"""
		ss = self.fd.read(2)
		if len(ss)==2: return CP.ShortInt.unpack(ss)[0]
		else:
			print('int communication error.',time.ctime())
			return -1
			#sys.exit(1)

	def __getLong__(self):
		"""
		reads four bytes.
		returns long
		"""
		ss = self.fd.read(4)
		if len(ss)==4: return CP.Integer.unpack(ss)[0]
		else:
			#print('.')
			return -1

	def waitForData(self,timeout=0.2):
		start_time = time.time()
		while time.time()-start_time<timeout:
			time.sleep(0.02)
			if self.fd.inWaiting():return True
		return False


	def sendBurst(self):
		"""
		Transmits the commands stored in the burstBuffer.
		empties input buffer
		empties the burstBuffer.
		
		The following example initiates the capture routine and sets OD1 HIGH immediately.
		
		It is used by the Transient response experiment where the input needs to be toggled soon
		after the oscilloscope has been started.
		
		>>> I.loadBurst=True
		>>> I.capture_traces(4,800,2)
		>>> I.set_state(I.OD1,I.HIGH)
		>>> I.sendBurst()
		
		
		"""
		#print([Byte.unpack(a)[0] for a in self.burstBuffer],self.inputQueueSize)
		self.fd.write(self.burstBuffer)
		self.burstBuffer=''
		self.loadBurst=False
		acks=self.fd.read(self.inputQueueSize)
		self.inputQueueSize=0
		return [Byte.unpack(a)[0] for a in acks]

				
