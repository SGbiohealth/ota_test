                              import utime
from machine import I2C, Pin, SPI
from mpu9250 import MPU9250

import micropython_ota

i2c = I2C(scl=Pin(22), sda=Pin(21))
sensor = MPU9250(i2c)

#print("MPU9250 id: " + hex(sensor.whoami))

micropython_ota.ota_update(
    ota_host, project_name,
    filenames,
    user=user,
    passwd=passwd,
    use_version_prefix=True,
    hard_reset_device=True,
    soft_reset_device=False,
    timeout=5
    )

while True:
    #print("X=",sensor.acceleration)
    #print("X=",sensor.gyro[0])
    #print("Y=",sensor.gyro[1])
    #print("Z=",sensor.gyro[2])
    print(sensor.magnetic)
    #print(sensor.temperature)

    utime.sleep_ms(100)