import utime
from machine import I2C, Pin, SPI
from mpu9250 import MPU9250


i2c = I2C(scl=Pin(22), sda=Pin(21))
sensor = MPU9250(i2c)

#print("MPU9250 id: " + hex(sensor.whoami))

while True:
    #print("X=",sensor.acceleration)
    #print("X=",sensor.gyro[0])
    #print("Y=",sensor.gyro[1])
    #print("Z=",sensor.gyro[2])
    print(sensor.magnetic)
    #print(sensor.temperature)

    utime.sleep_ms(100)