Plug n Play Sensors
===================

The SEELablet library package supports a variety of commonly available add-ons
to measure a wide range of parameters, as well as generate complex signals.

e.g. , for an HMC5883L 3-axis magnetometer connected to the I2C port on the device

.. code-block:: python

	from SEEL import interface
	I= interface.connect()
	
	from SEEL.SENSORS import HMC5883L
	magnetometer = HMC5883L.connect(I.I2C) #Specify that it is connected to the I2C port
	print (magnetometer.getRaw()) # read all values, and print an array of 3 elements : 1 reading per axis



AD9833 28-bit DDS generator
---------------------------

.. automodule:: SEEL.SENSORS.AD9833
   :members:


BH1750 Luminosity Sensor
--------------------------

.. automodule:: SEEL.SENSORS.BH1750
    :members:

BMP180 Pressure and Altitude sensor
-----------------------------------

.. automodule:: SEEL.SENSORS.BMP180
    :members:


HMC5883L 3-axis magnetometer
----------------------------

.. automodule:: SEEL.SENSORS.HMC5883L
    :members:


MLX90614 PIR temperature sensor
-------------------------------

.. automodule:: SEEL.SENSORS.MLX90614
    :members:


MPU6050 3-Axis Accelerometer & 3-Axis gyroscope
-----------------------------------------------

.. automodule:: SEEL.SENSORS.MPU6050
    :members:

SHT21 Humidity and Temperature sensor
--------------------------------------

.. automodule:: SEEL.SENSORS.SHT21
    :members:

SSD1306 128*64 OLED Display
---------------------------

.. automodule:: SEEL.SENSORS.SSD1306
    :members:

TSL2561  Luminosity Sensor
---------------------------

.. automodule:: SEEL.SENSORS.TSL2561
    :members:


MF522 RFID Reader & Writer
--------------------------

.. automodule:: SEEL.SENSORS.MF522
    :members:

