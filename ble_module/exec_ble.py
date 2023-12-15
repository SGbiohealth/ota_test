from ble_module.ble import BLE
from esp32 import raw_temperature
import ubluetooth
import utime

ble = ubluetooth.BLE()

# BLE 끄는 함수
def turn_off_ble():
    ble.active(False)

# BLE 켜는 함수
def turn_on_ble():
    ble.active(True)

def init_ble():
    return BLE(ble)

def ble_write_str(Str):
        #send to BLE
    ble.send(Str)
    
def any():
    return ble.any()
    
def on_rx():
    return BLE.on_rx(ble)

def read():
    return ble.get_ble_msg()

def callback(Str):
    ble.ble_irq(3, Str)

    




#Text = read()
#                                                                                                                                                                                                                 print(ble.rcv_msg)

# 사용 방법
# import ble_module.exec_ble as ble
# ble.init_ble()