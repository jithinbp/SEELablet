import time

class RadioLink():
	ADC_COMMANDS =1
	READ_ADC =0<<4

	I2C_COMMANDS =2
	I2C_TRANSACTION =0<<4
	I2C_WRITE =1<<4
	SCAN_I2C =2<<4
	PULL_SCL_LOW = 3<<4
	I2C_CONFIG = 4<<4
	I2C_READ = 5<<4
	
	NRF_COMMANDS = 3
	NRF_READ_REGISTER =0<<4
	NRF_WRITE_REGISTER =1<<4

	def __init__(self,NRF,**args):
		self.NRF = NRF
		if args.has_key('address'):
			self.ADDRESS = args.get('address',False)
		else:
			print 'Address not specified. Add "address=0x....." argument while instantiating'
			self.ADDRESS=0x010101
		

	def __selectMe__(self):
		if self.NRF.CURRENT_ADDRESS!=self.ADDRESS:
			self.NRF.selectAddress(self.ADDRESS)
		
		
	def I2C_scan(self):
		self.__selectMe__()
		import sensorlist
		print 'Scanning addresses 0-127...'
		x = self.NRF.transaction([self.I2C_COMMANDS|self.SCAN_I2C|0x80],timeout=500)
		if not x:return []
		if not sum(x):return []
		addrs=[]
		print 'Address','\t','Possible Devices'

		for a in range(16):
			if(x[a]^255):
				for b in range(8):
					if x[a]&(0x80>>b)==0:
						addr = 8*a+b
						addrs.append(addr)
						print hex(addr),'\t\t',sensorlist.sensors.get(addr,'None')
						
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
		return self.NRF.transaction([self.I2C_COMMANDS|self.I2C_WRITE]+[I2C_addr]+[regaddress]+bytes)
		
	def readI2C(self,I2C_addr,regaddress,numbytes):
		self.__selectMe__()
		return self.NRF.transaction([self.I2C_COMMANDS|self.I2C_TRANSACTION]+[I2C_addr]+[regaddress]+[numbytes])
	
	def writeBulk(self,I2C_addr,bytes):
		self.__selectMe__()
		return self.NRF.transaction([self.I2C_COMMANDS|self.I2C_WRITE]+[I2C_addr]+bytes)
		
	def readBulk(self,I2C_addr,regaddress,numbytes):
		self.__selectMe__()
		return self.NRF.transactionWithRetries([self.I2C_COMMANDS|self.I2C_TRANSACTION]+[I2C_addr]+[regaddress]+[numbytes])

	def simpleRead(self,I2C_addr,numbytes):
		self.__selectMe__()
		return self.NRF.transactionWithRetries([self.I2C_COMMANDS|self.I2C_READ]+[I2C_addr]+[numbytes])


	def readADC(self,channel):
		self.__selectMe__()
		return self.NRF.transaction([self.ADC_COMMANDS|self.READ_ADC]+[channel])
	
	def pullSCLLow(self,t_ms):
		self.__selectMe__()
		dat=self.NRF.transaction([self.I2C_COMMANDS|self.PULL_SCL_LOW]+[t_ms])
		if dat:
			return self.__decode_I2C_list__(dat)
		else:
			return []

	def configI2C(self,freq):
		self.__selectMe__()
		brgval=int(32e6/freq/4 - 1)
		print brgval
		return self.NRF.transaction([self.I2C_COMMANDS|self.I2C_CONFIG]+[brgval],listen=False)

	def write_register(self,reg,val):
		self.__selectMe__()
		print 'writing to ',reg,val
		return self.NRF.transaction([self.NRF_COMMANDS|self.NRF_WRITE_REGISTER]+[reg,val],listen=False)

	def read_register(self,reg):
		self.__selectMe__()
		x=self.NRF.transaction([self.NRF_COMMANDS|self.NRF_READ_REGISTER]+[reg])
		if x:
			return x[0]
		else:
			return False
			
