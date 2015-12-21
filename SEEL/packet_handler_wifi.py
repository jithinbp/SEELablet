from commands_proto import *
import socket,commands



class Handler(object):
	def __init__(self,timeout=1.5,**kwargs):
		self.burstBuffer=''
		self.loadBurst=False
		self.inputQueueSize=0
		self.timeout=timeout
		self.version_string=''
		self.HOST = kwargs.get('host','192.168.1.1')
		self.PORT = 23
		self.fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.fd.connect((self.HOST, self.PORT))
		self.connected=True
		self.fd.settimeout(timeout)
		print 'ready',self.get_version(self.fd)


	def get_version(self,fd):
		fd.send(chr(COMMON))
		fd.send(chr(GET_VERSION))
		x=fd.recv(100)
		try:
			print 'clear',self.fd.recv(200)
		except:
			pass
		if len(x):x=x[:-1]
		return x

	def reconnect(self,**kwargs):
		self.fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.fd.connect((self.HOST, self.PORT))
		self.fd.settimeout(self.timeout)
			
		
	def __del__(self):
		#print 'closing port'
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
		if not self.loadBurst:x=self.fd.recv(1)
		else:
			self.inputQueueSize+=1
			return 1
		return ord(x)

	def __sendInt__(self,val):
		"""
		transmits an integer packaged as two characters
		:params int val: int to send
		"""
		if not self.loadBurst:self.fd.send(InttoString(val))
		else: self.burstBuffer+=InttoString(val)

	def __sendByte__(self,val):
		"""
		transmits a BYTE
		val - byte to send
		"""
		if(type(val)==int):
			if not self.loadBurst:self.fd.send(chr(val))
			else:self.burstBuffer+=chr(val)
		else:
			if not self.loadBurst:self.fd.send(val)
			else:self.burstBuffer+=val
			
	def __getByte__(self):
		"""
		reads a byte from the serial port and returns it
		"""
		ss=self.fd.recv(1)
		if len(ss): return ord(ss)
		else:
			print 'byte communication error.',time.ctime()
			return -1
			#sys.exit(1)
	
	def __getInt__(self):
		"""
		reads two bytes from the serial port and
		returns an integer after combining them
		"""
		ss = self.fd.recv(2)
		if len(ss)==2: return ord(ss[0])|(ord(ss[1])<<8)
		else:
			print 'int communication error.',time.ctime()
			return -1
			#sys.exit(1)

	def __getLong__(self):
		"""
		reads four bytes.
		returns long
		"""
		ss = self.fd.recv(4)
		if len(ss)==4: return ord(ss[0])|(ord(ss[1])<<8)|(ord(ss[2])<<16)|(ord(ss[3])<<24)
		else:
			#print '.'
			return -1
	

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
		#print [ord(a) for a in self.burstBuffer],self.inputQueueSize
		self.fd.send(self.burstBuffer)
		self.burstBuffer=''
		self.loadBurst=False
		acks=self.fd.recv(self.inputQueueSize)
		self.inputQueueSize=0
		return [ord(a) for a in acks]

	def send_char(self,c):
		"""
		Relays a character through the second UART(9-bit mode)

		==============	============================================================================================
		**Arguments** 
		==============	============================================================================================
		c				value to transmit
		==============	============================================================================================

		:return: nothing
		"""
		self.__sendByte__(UART_2)
		self.__sendByte__(SEND_CHAR)
		self.__sendByte__(c)
		self.__get_ack__()

		
