import machine
import neopixel

PIN_LED = 18
LED_NUM = 1 # 사용할 LED 개수

LED_pin = machine.Pin(PIN_LED) # 사용할 핀 번호
np = neopixel.NeoPixel(LED_pin, LED_NUM)

def led(color):
    if color == 'R':
        np.fill((100, 0, 0)) #B
    elif color == 'G':
        np.fill((0, 100, 0)) #B
    elif color == 'B':
        np.fill((0, 0, 100)) #B
    elif color == 'RB':
        np.fill((100, 0, 100)) #B
    elif color == 'RG':
        np.fill((100, 100, 0)) #B        
    elif color == 'GB':
        np.fill((0, 100, 100)) #B
    elif color == 'RGB':
        np.fill((100, 100, 100))
    elif color == 'OFF':
        np.fill((0, 0, 0))    
    else:
         pass           
    np.write()