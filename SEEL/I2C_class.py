from __future__ import print_function
from SEEL.commands_proto import *
import numpy as np 

class I2C():
    """
    Methods to interact with the I2C port. An instance of Labtools.Packet_Handler must be passed to the init function
    
    
    Example::  Read Values from an HMC5883L 3-axis Magnetometer(compass) [GY-273 sensor] connected to the I2C port
        >>> ADDRESS = 0x1E
        >>> from Labtools import interface
        >>> I = interface.Interface() 
        #Alternately, you may skip using I2C as a child instance of Interface, 
        #and instead use I2C=Labtools.I2C_class.I2C(Labtools.packet_handler.Handler())
        
        # writing to 0x1E, set gain(0x01) to smallest(0)
        >>> I.I2C.bulkWrite(ADDRESS,[0x01,0])
        
        # writing to 0x1E, set mode conf(0x02), continuous measurement(0)
        >>> I.I2C.bulkWrite(ADDRESS,[0x02,0])

        # read 6 bytes from addr register on I2C device located at ADDRESS
        >>> vals = I.I2C.bulkRead(ADDRESS,addr,6)
            
        >>> from numpy import int16
        #conversion to signed datatype
        >>> x=int16((vals[0]<<8)|vals[1])
        >>> y=int16((vals[2]<<8)|vals[3])
        >>> z=int16((vals[4]<<8)|vals[5])
        >>> print (x,y,z)

    """

    def __init__(self,H):
        self.H = H
        from SEEL import sensorlist
        self.SENSORS=sensorlist.sensors
        self.buff=np.zeros(10000)

    def init(self):
        self.H.__sendByte__(I2C_HEADER)
        self.H.__sendByte__(I2C_INIT)
        self.H.__get_ack__()

    def enable_smbus(self):
        self.H.__sendByte__(I2C_HEADER)
        self.H.__sendByte__(I2C_ENABLE_SMBUS)
        self.H.__get_ack__()

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
        self.H.__sendByte__(I2C_HEADER)
        self.H.__sendByte__(I2C_PULLDOWN_SCL)
        self.H.__sendInt__(uS)
        self.H.__get_ack__()
        
         
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
        self.H.__sendByte__(I2C_HEADER)
        self.H.__sendByte__(I2C_CONFIG)
        #freq=1/((BRGVAL+1.0)/64e6+1.0/1e7)
        BRGVAL=int( (1./freq-1./1e7)*64e6-1 )
        if BRGVAL>511:
            BRGVAL=511
            if verbose:print ('Frequency too low. Setting to :',1/((BRGVAL+1.0)/64e6+1.0/1e7))
        self.H.__sendInt__(BRGVAL) 
        self.H.__get_ack__()

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
        self.H.__sendByte__(I2C_HEADER)
        self.H.__sendByte__(I2C_START)
        self.H.__sendByte__(((address<<1)|rw)&0xFF) # address
        return self.H.__get_ack__()>>4

    def stop(self):
        """
        stops I2C transfer
        
        :return: Nothing
        """
        self.H.__sendByte__(I2C_HEADER)
        self.H.__sendByte__(I2C_STOP)
        self.H.__get_ack__()

    def wait(self):
        """
        wait for I2C

        :return: Nothing
        """
        self.H.__sendByte__(I2C_HEADER)
        self.H.__sendByte__(I2C_WAIT)
        self.H.__get_ack__()

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
        self.H.__sendByte__(I2C_HEADER)
        self.H.__sendByte__(I2C_SEND)
        self.H.__sendByte__(data)        #data byte
        return self.H.__get_ack__()>>4
        
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
        self.H.__sendByte__(I2C_HEADER)
        self.H.__sendByte__(I2C_SEND_BURST)
        self.H.__sendByte__(data)        #data byte
        #No handshake. for the sake of speed. e.g. loading a frame buffer onto an I2C display such as ssd1306

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
        self.H.__sendByte__(I2C_HEADER)
        self.H.__sendByte__(I2C_RESTART)
        self.H.__sendByte__(((address<<1)|rw)&0xFF) # address
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
        for a in range(length-1):
            self.H.__sendByte__(I2C_HEADER)
            self.H.__sendByte__(I2C_READ_MORE)
            data.append(self.H.__getByte__())
            self.H.__get_ack__()
        self.H.__sendByte__(I2C_HEADER)
        self.H.__sendByte__(I2C_READ_END)
        data.append(self.H.__getByte__())
        self.H.__get_ack__()
        return data

    def read_repeat(self):
        self.H.__sendByte__(I2C_HEADER)
        self.H.__sendByte__(I2C_READ_MORE)
        val=self.H.__getByte__()
        self.H.__get_ack__()
        return val

    def read_end(self):
        self.H.__sendByte__(I2C_HEADER)
        self.H.__sendByte__(I2C_READ_END)
        val=self.H.__getByte__()
        self.H.__get_ack__()
        return val


    def read_status(self):
        self.H.__sendByte__(I2C_HEADER)
        self.H.__sendByte__(I2C_STATUS)
        val=self.H.__getInt__()
        self.H.__get_ack__()
        return val


    def readBulk(self,device_address,register_address,bytes_to_read):
        self.H.__sendByte__(I2C_HEADER)
        self.H.__sendByte__(I2C_READ_BULK)
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
        self.H.__sendByte__(I2C_HEADER)
        self.H.__sendByte__(I2C_WRITE_BULK)
        self.H.__sendByte__(device_address)
        self.H.__sendByte__(len(bytestream))
        for a in bytestream:
            self.H.__sendByte__(a)
        self.H.__get_ack__()

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

        self.H.__sendByte__(I2C_HEADER)
        self.H.__sendByte__(I2C_START_SCOPE)       
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
            self.H.__sendByte__(ADC)
            self.H.__sendByte__(GET_CAPTURE_CHANNEL)
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
            self.H.__sendByte__(ADC)
            self.H.__sendByte__(GET_CAPTURE_CHANNEL)
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



        data = [ord(a) for a in data]
        if('int' in args):
                for a in range(total_chans*channel_length): self.buff[a] = np.int16((data[a*2]<<8)|data[a*2+1])
        else:
                for a in range(total_chans*channel_length): self.buff[a] = data[a]

        #print (self.buff, 'geer')
        
        yield np.linspace(0,tg*(channel_length-1),channel_length)
        for a in range(int(total_chans)):
            yield self.buff[a:channel_length*total_chans][::total_chans]






