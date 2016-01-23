from SEEL.SENSORS import HMC5883L
from SEEL.SENSORS import MPU6050
from SEEL.SENSORS import MLX90614
from SEEL.SENSORS import BMP180
from SEEL.SENSORS import TSL2561
from SEEL.SENSORS import SHT21
from SEEL.SENSORS import BH1750

supported={
0x68:MPU6050,  #3-axis gyro,3-axis accel,temperature
0x1E:HMC5883L, #3-axis magnetometer
0x5A:MLX90614, #Passive IR temperature sensor
0x77:BMP180,   #Pressure, Temperature, altitude
0x39:TSL2561,  #Luminosity
0x40:SHT21,    #Temperature, Humidity
0x23:BH1750,    #Luminosity
}
