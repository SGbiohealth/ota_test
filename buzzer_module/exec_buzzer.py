import machine

# 사용할 핀 번호 입력
PIN_BZ = 23

def buzzer():
    return machine.Pin(PIN_BZ, machine.Pin.OUT)
