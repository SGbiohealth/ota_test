import utime
from machine import I2C, Pin
from mpu9250_mod.mpu9250 import MPU9250

i2c = I2C(scl=Pin(22), sda=Pin(21))
sensor = MPU9250(i2c)

def read_value(x,y,z):
    return "{:.2f},{:.2f},{:.2f}".format(x, y, z)

def get_Sensor_value():
    accel_data_str = read_value(sensor.acceleration[0],sensor.acceleration[1],sensor.acceleration[2])
    gyro_data_str = read_value(sensor.gyro[0],sensor.gyro[1],sensor.gyro[2])
    mag_data_str = read_value(sensor.magnetic[0],sensor.magnetic[1],sensor.magnetic[2])
    combined_data_str = accel_data_str + "," + gyro_data_str + "," + mag_data_str
    print("tx :", combined_data_str)
    return combined_data_str
