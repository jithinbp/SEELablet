from __future__ import print_function
from SEEL.commands_proto import *

import SEEL.I2C_class as I2C_class
import numpy as np

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
		self.I2C = I2C_class.I2C(self.H)
		print (int( (1./2e6-1./1e7)*64e6-1 ))
		self.SWITCHEDOFF=[0,0,0,0]
		self.VREFS=[0,0,0,0]  #0=Vdd,1=Internal reference
		self.CHANS = {'PCS':DACCHAN('PCS',[3.3e-3,0],0),'PVS3':DACCHAN('PVS3',[0,3.3],1),'PVS2':DACCHAN('PVS2',[-3.3,3.3],2),'PVS1':DACCHAN('PVS1',[-5.,5.],3)}
		self.CHANNEL_MAP={0:'PCS',1:'PVS3',2:'PVS2',3:'PVS1'}
		self.calibration_enabled={'PVS1':False,'PVS2':False,'PVS3':False,'PCS':False}
		self.calibration_tables={'PVS1':[],'PVS2':[],'PVS3':[],'PCS':[]}


	def load_calibration(self,name,table):
		self.calibration_enabled[name]=True
		self.calibration_tables[name] = table

	def setVoltage(self,name,v):
		chan = self.CHANS[name]
		v = int(round(chan.VToCode(v)))		
		return  self.__setRawVoltage__(name,v)

	def __setRawVoltage__(self,name,v):
		v=int(np.clip(v,0,4095))
		CHAN = self.CHANS[name]
		'''
		self.H.__sendByte__(DAC) #DAC write coming through.(MCP4728)
		self.H.__sendByte__(SET_DAC)
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
		if self.calibration_enabled[name]:
			val = int(v+self.calibration_tables[name][v])
			#print (val,v,self.calibration_tables[name][v])
			self.I2C.writeBulk(self.addr,[64|(CHAN.channum<<1),(val>>8)&0x0F,val&0xFF])
		else:
			self.I2C.writeBulk(self.addr,[64|(CHAN.channum<<1),(v>>8)&0x0F,v&0xFF])

		return CHAN.CodeToV(v)


	def __samplewriteall__(self,v1):
		self.I2C.start(self.addr,0)
		self.I2C.send((v1>>8)&0xF )
		self.I2C.send(v1&0xFF)
		self.I2C.send((v1>>8)&0xF )
		self.I2C.send(v1&0xFF)
		self.I2C.send((v1>>8)&0xF )
		self.I2C.send(v1&0xFF)
		self.I2C.send((v1>>8)&0xF )
		self.I2C.send(v1&0xFF)
		self.I2C.stop()



	def __writeall__(self,v1,v2,v3,v4):
		self.I2C.start(self.addr,0)
		self.I2C.send((v1>>8)&0xF )
		self.I2C.send(v1&0xFF)
		self.I2C.send((v2>>8)&0xF )
		self.I2C.send(v2&0xFF)
		self.I2C.send((v3>>8)&0xF )
		self.I2C.send(v3&0xFF)
		self.I2C.send((v4>>8)&0xF )
		self.I2C.send(v4&0xFF)
		self.I2C.stop()

	def stat(self):
		self.I2C.start(self.addr,0)
		self.I2C.send(0x0) #read raw values starting from address
		self.I2C.restart(self.addr,1)
		vals=self.I2C.read(24)
		self.I2C.stop()
		print (vals)


