from __future__ import print_function
import numpy as np
from SEEL.commands_proto import *
digital_channel_names=['ID1','ID2','ID3','ID4']


class digital_channel:
	EVERY_SIXTEENTH_RISING_EDGE = 5
	EVERY_FOURTH_RISING_EDGE    = 4
	EVERY_RISING_EDGE           = 3
	EVERY_FALLING_EDGE          = 2
	EVERY_EDGE                  = 1
	DISABLED				    = 0
	def __init__(self,a):
		self.name=''
		self.gain=0
		self.channel_number=a
		self.digital_channel_names=digital_channel_names
		self.xaxis=np.zeros(20000)
		self.yaxis=np.zeros(20000)
		self.timestamps=np.zeros(10000)
		self.length=100
		self.initial_state=0
		self.prescaler = 0
		self.datatype='int'
		self.trigger=0
		self.dlength=0
		self.plot_length = 0
		self.maximum_time =0
		self.maxT = 0
		self.initial_state_override = False
		self.mode=self.EVERY_EDGE

	def set_params(self,**keys):
		self.channel_number = keys.get('channel_number',self.channel_number)	
		self.name = digital_channel_names[self.channel_number]

	def load_data(self,initial_state,timestamps):
		if self.initial_state_override:
			self.initial_state = (self.initial_state_override-1)==1
			self.initial_state_override = False
		else: self.initial_state = initial_state[self.channel_number]
		self.timestamps=timestamps
		self.dlength = len(self.timestamps)
		#print(self.channel_number,self.dlength,len(self.timestamps),self.initial_state)
		if(self.prescaler==0): prescale = 1.0/64		#convert to uSeconds
		elif(self.prescaler==1): prescale = 1.0/8
		elif(self.prescaler==2): prescale = 1.0/1
		elif(self.prescaler==3): prescale = 4.0/1
		self.timestamps = np.array(self.timestamps)*prescale

		if self.dlength:self.maxT=self.timestamps[-1]
		else: self.maxT=0

	def generate_axes(self):
		HIGH = (4-self.channel_number)*(3)
		LOW = HIGH - 2.5
		state = HIGH if self.initial_state else LOW


		if self.mode==self.DISABLED:
			self.xaxis[0]=0; self.yaxis[0]=state
			n=1
			self.plot_length = n

		elif self.mode==self.EVERY_EDGE:
			self.xaxis[0]=0; self.yaxis[0]=state
			n=1
			for a in range(self.dlength):
				self.xaxis[n] = self.timestamps[a]
				self.yaxis[n] = state
				state = LOW if state==HIGH else HIGH
				n+=1
				self.xaxis[n] = self.timestamps[a]
				self.yaxis[n] = state
				n+=1

			self.plot_length = n

		elif self.mode==self.EVERY_FALLING_EDGE:
			self.xaxis[0]=0; self.yaxis[0]=HIGH
			n=1
			for a in range(self.dlength):
				self.xaxis[n] = self.timestamps[a]
				self.yaxis[n] = HIGH
				n+=1
				self.xaxis[n] = self.timestamps[a]
				self.yaxis[n] = LOW
				n+=1
				self.xaxis[n] = self.timestamps[a]
				self.yaxis[n] = HIGH
				n+=1
			state=HIGH
			self.plot_length = n
		
		elif self.mode==self.EVERY_RISING_EDGE or self.mode==self.EVERY_FOURTH_RISING_EDGE or self.mode==self.EVERY_SIXTEENTH_RISING_EDGE:
			self.xaxis[0]=0; self.yaxis[0]=LOW
			n=1
			for a in range(self.dlength):
				self.xaxis[n] = self.timestamps[a]
				self.yaxis[n] = LOW
				n+=1
				self.xaxis[n] = self.timestamps[a]
				self.yaxis[n] = HIGH
				n+=1
				self.xaxis[n] = self.timestamps[a]
				self.yaxis[n] = LOW
				n+=1
			state = LOW
			self.plot_length = n
		#print(self.channel_number,self.dlength,self.mode,len(self.yaxis),self.plot_length)

	def get_xaxis(self):
		return self.xaxis[:self.plot_length]
	def get_yaxis(self):
		return self.yaxis[:self.plot_length]

