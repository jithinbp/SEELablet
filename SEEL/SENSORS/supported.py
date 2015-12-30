import SEEL.SENSORS.HMC5883L as HMC5883L
import SEEL.SENSORS.MPU6050 as MPU6050
import SEEL.SENSORS.MLX90614 as MLX90614
import SEEL.SENSORS.BMP180 as BMP180
import SEEL.SENSORS.TSL2561 as TSL2561
import SEEL.SENSORS.SHT21 as SHT21

supported={
0x68:MPU6050,  #3-axis gyro,3-axis accel,temperature
0x1E:HMC5883L, #3-axis magnetometer
0x5A:MLX90614, #Passive IR temperature sensor
0x77:BMP180,   #Pressure, Temperature, altitude
0x39:TSL2561,  #Luminosity
0x40:SHT21,    #Temperature, Humidity
}
