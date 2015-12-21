from commands_proto import *

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
        self.H.__sendByte__(SPI_HEADER)
        self.H.__sendByte__(SET_SPI_PARAMETERS)
        #0Bhgfedcba - > <g>: modebit CKP,<f>: modebit CKE, <ed>:primary pre,<cba>:secondary pre
        self.H.__sendByte__(secondary_prescaler|(primary_prescaler<<3)|(CKE<<5)|(CKP<<6)|(SMP<<7)) 
        self.H.__get_ack__()

    def start(self,channel):
        """
        selects SPI channel to enable.
        Basically lowers the relevant chip select pin .
        
        .. tabularcolumns:: |p{3cm}|p{11cm}|
        ================    ============================================================================================
        **Arguments** 
        ================    ============================================================================================
        channel             1-7 ->[PGA1 connected to CH1,PGA2,PGA3,PGA4,PGA5,external chip select 1,external chip select 2]
                            8 -> sine1
                            9 -> sine2
        ================    ============================================================================================
        
        """
        self.H.__sendByte__(SPI_HEADER)
        self.H.__sendByte__(START_SPI)
        self.H.__sendByte__(channel)    #value byte
        #self.H.__get_ack__()
        
    def stop(self,channel):
        """
        selects SPI channel to disable.
        Sets the relevant chip select pin to HIGH.
        
        .. tabularcolumns:: |p{3cm}|p{11cm}|
        ================    ============================================================================================
        **Arguments** 
        ================    ============================================================================================
        channel             1-7 ->[PGA1 connected to CH1,PGA2,PGA3,PGA4,PGA5,external chip select 1,external chip select 2]
        ================    ============================================================================================
        """
        self.H.__sendByte__(SPI_HEADER)
        self.H.__sendByte__(STOP_SPI)
        self.H.__sendByte__(channel)    #value byte
        #self.H.__get_ack__()

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
        self.H.__sendByte__(SPI_HEADER)
        self.H.__sendByte__(SEND_SPI8)
        self.H.__sendByte__(value)  #value byte
        v=self.H.__getByte__()
        self.H.__get_ack__()
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
        self.H.__sendByte__(SPI_HEADER)
        self.H.__sendByte__(SEND_SPI16)
        self.H.__sendInt__(value)   #value byte
        v=self.H.__getInt__()
        self.H.__get_ack__()
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
        self.H.__sendByte__(SPI_HEADER)
        self.H.__sendByte__(SEND_SPI8_BURST)
        self.H.__sendByte__(value)  #value byte

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
        self.H.__sendByte__(SPI_HEADER)
        self.H.__sendByte__(SEND_SPI16_BURST)
        self.H.__sendInt__(value)   #value byte

