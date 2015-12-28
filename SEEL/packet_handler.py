from __future__ import print_function

from commands_proto import *
import serial,commands

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
        if kwargs.has_key('port'):
            self.portname=kwargs.get('port',None)
            if not self.portname:
                print ('device not found',self.portname)
                sys.exit(1)
            self.fd = serial.Serial(self.portname, 9600, stopbits=1, timeout = 0.02)
            self.fd.read(100)
            self.fd = serial.Serial(self.portname, self.BAUD, stopbits=1, timeout = 1.0)
            if(self.fd.inWaiting()):
                self.fd.read(1000)
                self.fd.flush()
            version = self.get_version(self.fd)
            print ('Connected to device at ',self.portname,' ,Version:',version)
            self.connected=True
            self.version_string=version
            return
        else:	#Scan and pick a port	
            for a in range(10):
                res = commands.getoutput('lsof -t '+ self.BASE_PORT_NAME+str(a))
                if res == '':
                    try:
                        self.fd = serial.Serial(self.BASE_PORT_NAME+str(a), 9600, stopbits=1, timeout = 0.01)
                        #self.fd.read(100)
                        self.fd.close()
                        self.fd = serial.Serial(self.BASE_PORT_NAME+str(a), self.BAUD, stopbits=1, timeout = 0.2)
                        self.portname=self.BASE_PORT_NAME+str(a)
                        self.fd.read(1000)
                        self.fd.flush()
                        version = self.get_version(self.fd)
                        self.version_string=version
                        #print (version,self.portname)
                        if(version[:6]=='LTS-v0'):
                            #print ('Connected to device at ',self.portname,' ,Version:',version)
                            self.fd.setTimeout(1.)
                            self.connected=True
                            break
                        #print (self.BASE_PORT_NAME+str(a)+' .yes.',version)
                    except IOError:
                        #print (self.BASE_PORT_NAME+str(a)+' .no.')
                        pass
            if not self.connected:
                    print ('Device not found')
		
    def get_version(self,fd):
        fd.write(COMMON)
        fd.write(GET_VERSION)
        x=fd.readline()
        #print ('remaining',[ord(a) for a in fd.read(10)])
        if len(x):
            x=x[:-1]
        return x

    def reconnect(self,**kwargs):
        if kwargs.has_key('port'):
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
            print ('Connected to device at:',self.portname,' ,Version:',version)
            self.connected=True
            self.version_string=version
        except serial.SerialException as ex:
            print ("failed to connect. Check device connections ,Or\nls /dev/TestBench\nOr, check if symlink has been created in /etc/udev/rules.d/proto.rules for the relevant Vid,Pid")

    def __del__(self):
        #print ('closing port')
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
        return Byte.unpack(x)[0]

    def __sendInt__(self,val):
        """
        transmits an integer packaged as two characters
        :params int val: int to send
        """
        if not self.loadBurst:self.fd.write(InttoString(val))
        else: self.burstBuffer+=InttoString(val)

    def __sendByte__(self,val):
        """
        transmits a BYTE
        val - byte to send
        """
        if(type(val)==int):
            if not self.loadBurst:self.fd.write(Byte.pack(val))
            else:self.burstBuffer+=Byte.pack(val)
        else:
            if not self.loadBurst:self.fd.write(val)
            else:self.burstBuffer+=val
			
    def __getByte__(self):
        """
        reads a byte from the serial port and returns it
        """
        ss=self.fd.read(1)
        if len(ss): return Byte.unpack(ss)[0]
        else:
            print ('byte communication error.',time.ctime())
            return -1
            #sys.exit(1)
	
    def __getInt__(self):
        """
        reads two bytes from the serial port and
        returns an integer after combining them
        """
        ss = self.fd.read(2)
        if len(ss)==2: return ShortInt.unpack(ss)[0]
        else:
            print ('int communication error.',time.ctime())
            return -1
			#sys.exit(1)

    def __getLong__(self):
        """
        reads four bytes.
        returns long
        """
        ss = self.fd.read(4)
        if len(ss)==4: return Integer.unpack(ss)[0]
        else:
            #print ('.')
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
        #print ([Byte.unpack(a)[0] for a in self.burstBuffer],self.inputQueueSize)
        self.fd.write(self.burstBuffer)
        self.burstBuffer=''
        self.loadBurst=False
        acks=self.fd.read(self.inputQueueSize)
        self.inputQueueSize=0
        return [Byte.unpack(a)[0] for a in acks]

    def send_char(self,c):
        """
        Relays a character through the second UART(9-bit mode)
        
        ==============	============================================================================================
        **Arguments** 
        ==============	============================================================================================
        c		value to transmit
        ==============	============================================================================================

        :return: nothing
        """
        self.__sendByte__(UART_2)
        self.__sendByte__(SEND_CHAR)
        self.__sendByte__(c)
        self.__get_ack__()
                
