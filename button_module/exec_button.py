import machine

PIN_BTN = 25

button_pin = machine.Pin(PIN_BTN, machine.Pin.IN, machine.Pin.PULL_UP)  # 버튼 핀 초기화

def value():
    return button_pin.value() # 버튼 상태 반환