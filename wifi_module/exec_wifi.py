# Wi-Fi 끄는 함수
def turn_off_wifi():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(False)

def turn_on_wifi():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)