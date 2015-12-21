import time
import numpy as np
import scipy.optimize as optimize
import scipy.fftpack as fftpack
from scipy import signal

class analyticsClass():
	"""
	This class contains methods that allow mathematical analysis such as curve fitting
	
	"""
	def __init__(self):
		pass

	def sineFunc(self,x, a1, a2, a3,a4):
	    return a4 + a1*np.sin(abs(a2*(2*np.pi))*x + a3)

	def squareFunc(self,x, amp,freq,phase,dc,offset):
	    return offset + amp*signal.square(2 * np.pi * freq * (x - phase), duty=dc)

	def squareFit(self,xReal,yReal):
		N=len(xReal)
		mx = yReal.max()
		mn = yReal.min()
		OFFSET = (mx+mn)/2.
		amplitude = (np.average(yReal[yReal>OFFSET]) - np.average(yReal[yReal<OFFSET]) )/2.0
		yTmp = np.select([yReal<OFFSET,yReal>OFFSET],[0,2])
		bools = abs(np.diff(yTmp))>1
		edges = xReal[bools]
		levels = yTmp[bools]
		frequency = 1./(edges[2]-edges[0])
		
		phase=edges[0]#.5*np.pi*((yReal[0]-offset)/amplitude)
		dc=0.5
		if len(edges)>=4:
			if levels[0]==0:
				dc = (edges[1]-edges[0])/(edges[2]-edges[0])
			else:
				dc = (edges[2]-edges[1])/(edges[3]-edges[1])
				phase = edges[1]

		guess = [amplitude, frequency, phase,dc,0]

		try:
			(amplitude, frequency, phase,dc,offset), pcov = optimize.curve_fit(self.squareFunc, xReal, yReal-OFFSET, guess)
			offset+=OFFSET

			if(frequency<0):
				#print 'negative frq'
				return False

			freq=1e6*abs(frequency)
			amp=abs(amplitude)
			pcov[0]*=1e6
			#print pcov
			if(abs(pcov[-1][0])>1e-6):
				False
			return [amp, freq, phase,dc,offset]
		except:
			return False

	def sineFit(self,xReal,yReal):
		N=len(xReal)
		OFFSET = (yReal.max()+yReal.min())/2.
		yhat = fftpack.rfft(yReal-OFFSET)
		idx = (yhat**2).argmax()
		freqs = fftpack.rfftfreq(N, d = (xReal[1]-xReal[0])/(2*np.pi))
		frequency = freqs[idx]/(2*np.pi)  #Convert angular velocity to freq

		amplitude = (yReal.max()-yReal.min())/2.0
		phase=0#.5*np.pi*((yReal[0]-offset)/amplitude)
		guess = [amplitude, frequency, phase,0]
		try:
			(amplitude, frequency, phase,offset), pcov = optimize.curve_fit(self.sineFunc, xReal, yReal-OFFSET, guess)
			offset+=OFFSET
			ph = ((phase)*180/(np.pi))
			if(frequency<0):
				#print 'negative frq'
				return False

			if(amplitude<0):
				ph-=180

			if(ph<0):ph = (ph+720)%360
			freq=1e6*abs(frequency)
			amp=abs(amplitude)
			pcov[0]*=1e6
			#print pcov
			if(abs(pcov[-1][0])>1e-6):
				False
			return [amp, freq, offset,ph]
		except:
			return False

	def dampedSine(self,x, amp, freq, phase,offset,damp):
		"""
		A damped sine wave function
		
		"""
		return offset + amp*np.exp(-damp*x)*np.sin(abs(freq)*x + phase)

	def getGuessValues(self,xReal,yReal,func='sine'):
		if(func=='sine' or func=='damped sine'):
			N=len(xReal)
			offset = np.average(yReal)
			yhat = fftpack.rfft(yReal-offset)
			idx = (yhat**2).argmax()
			freqs = fftpack.rfftfreq(N, d = (xReal[1]-xReal[0])/(2*np.pi))
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
			results, pcov = optimize.curve_fit(func, xReal, yReal,guess)
			pcov[0]*=1e6
			return True,results,pcov
		except:
			return False,[],[]


