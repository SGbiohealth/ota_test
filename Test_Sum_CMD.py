import machine
import time
from machine import Pin, Timer, SoftI2C
from time import sleep_ms

import ota_module.exec_ota as ota 				#ota
import led_module.exec_led as led 				#led
from buzzer_module.exec_buzzer import buzzer 		#buzzer
from vibration_module.exec_vibration import vmot	#vmot
import button_module.exec_button as btn 			#btn
import mpu9250_mod.exec_mpu9250 as mpu9250			#gyro

# 모드에 숫자 할당
IDLE_MODE = 0
DIS_MODE =1
ANG_MODE =2
TRN_MODE =3
RUN_MODE = 4
STOP_MODE = 5
EMERGENCY_MODE = 6
SPECIAL_MODE = 7
POWER_SAVING_MODE = 8

#핀번호
PIN_VMOT = 23
PIN_LED = 5
PIN_LED_DATA = 18
PIN_BZ = 27

buzzer = buzzer()
vmot = vmot()
btn_pin = btn.value()

def btn_pushed():
    #비프음, 진동
    vmot.on()  # 진동 모터 켜기
    buzzer.on()
    sleep_ms(100)
    vmot.off()  # 진동 모터 끄기
    buzzer.off()
    
def init_dvs():
    print("init Mode...")
    led.led('OFF')
    # GPIO 초기화
    machine.Pin(18, machine.Pin.OUT).off()  # LED 핀 초기화
    machine.Pin(23, machine.Pin.OUT).off()  # 진동 모터 핀 초기화
    machine.Pin(27, machine.Pin.OUT).off()  # BUZZER 핀 초기화
    machine.Pin(25, machine.Pin.IN, machine.Pin.PULL_UP)  # START 버튼 핀 초기화
    sleep_ms(100)
    print("finished Init...!!!")
    
    #ble

def Idle_mode():
    # 전역 변수 사용 선언
    global CNT, wwa, IDLE_TO_POWER_SAVING_FLAG, IDLE_START_FLAG, idle_mode_start_time

    if not IDLE_START_FLAG:
        # 최초 진입시에만 실행
        IDLE_START_FLAG = True
        RUN_START_FLAG=False
        led.led('G')
        print("Enterd Idle Mode!!!")
        idle_mode_start_time = time.ticks_ms()
        print("inIdle_MODE:", idle_mode_start_time)
        print("I.", end="")
    else:
        if CNT < 100:
            led.led('G')
        else:
            led.led('OFF')

    if CNT > 5000:
        print("I.", end="")
        CNT = 0
    
def run_mode():
    global CNT, IDLE_TO_POWER_SAVING_FLAG, IDLE_START_FLAG,RUN_START_FLAG
    IDLE_TO_POWER_SAVING_FLAG=False
    IDLE_START_FLAG=False
    
    if not RUN_START_FLAG:
        #led.led('B')
        btn_pushed()
        RUN_STAT_FLAG=True
    else:
        #btn_pushed()
    b_uart.write(mpu9250.get_Sensor_value())
    
    if CNT%4 == 0:
        led.led('B')
    else:
        led.led('OFF')
    if CNT > 100:
        CNT = 0

def emergency_mode():
    print("Entering Emergency Mode...")

def special_mode():
    print("Entering Special Mode...")
    
def setup_info():
    print("Entering setup_info...")

def power_saving_mode():
    global CNT, IDLE_TO_POWER_SAVING_FLAG
    IDLE_TO_POWER_SAVING_FLAG=False
    RUN_START_FLAG=False
    
    if CNT < 100:
        led.led('RB')
    else:
        led.led('OFF')
    
    if CNT > 5000:
        print('PS.', end="")
        CNT = 0
    CNT= CNT+1

def chg_ssid_pw(ssid, pw):
    print("CHG_ID_PW")
    
def sort_ble_cmd():
    MSG = b_uart.on_rx()
    if MSG[:4] == '^DIS':
        RTN = DIS_MODE
    elif MSG[:4] == '^ANG':
        RTN = ANG_MODE
    elif MSG[:4] == '^TRN':
        RTN = TRN_MODE
    elif MSG[:4] == '^STP':
        RTN = STOP_MODE
    elif MSG[:4] == '^SPW':
        MSG[5:]
        chg_ssid_pw("df","er")
        RTN = IDLE_MODE
    else:
        RTN = IDLE_MODE
    #print(RTN)
    return RTN
    
def check_mode(current_mode):
    global btn_pin, btn_pressed, RUN_TIMEOUT, POWER_SAVING_TIMEOUT, power_saving_start_time
    
    ble_cmd = sort_ble_cmd()
    
    if ble_cmd == STOP_MODE:
        RUN_TIMEOUT = 0
        
        # 버튼이 눌렸을 때 실행 모드로 진입
    if ble_cmd == TRN_MODE or ble_cmd == DIS_MODE or ble_cmd == ANG_MODE:
        if not btn_pressed:
            btn_pressed = True
            btn_pushed()
            if current_mode != RUN_MODE:
                current_mode = RUN_MODE
                power_saving_start_time = time.ticks_ms()  # 현재 시간 기록              
            if ble_cmd == DIS_MODE:
                RUN_TIMEOUT= DIS_TIMEOUT
            elif ble_cmd == ANG_MODE:
                RUN_TIMEOUT= ANG_TIMEOUT
            elif ble_cmd == TRN_MODE:
                RUN_TIMEOUT= TRN_TIMEOUT
    elif btn.value() and btn_pressed:
        btn_pressed = False     
    # 실행 모드에서 설정된 시간후에 대기 모드로 변경
    elif current_mode == RUN_MODE and time.ticks_diff(time.ticks_ms(), power_saving_start_time) > RUN_TIMEOUT:
        current_mode = IDLE_MODE
        Idle_mode()
    # 대기 모드에서 설정된 시간후에 절전 모드로 변경
    elif current_mode == IDLE_MODE and time.ticks_diff(time.ticks_ms(), idle_mode_start_time) > POWER_SAVING_TIMEOUT:
        current_mode = POWER_SAVING_MODE
        print(time.ticks_diff(time.ticks_ms(), idle_mode_start_time), POWER_SAVING_TIMEOUT)       
    # 초절전 모드에서 버튼이 눌리면 대기 모드로 변경
    elif current_mode == POWER_SAVING_MODE and not btn.value():
        btn_pushed()
        current_mode = IDLE_MODE
    return current_mode
    

def exec_mode(current_mode):
    # 현재 모드에 할당된 함수 실행
    if current_mode == None:
        current_mode = IDLE_MODE
        Idle_mode()
    elif current_mode == IDLE_MODE:
        Idle_mode()
    elif current_mode == DIS_MODE:
        dis_mode()        
    elif current_mode == RUN_MODE:
        run_mode()
    elif current_mode == EMERGENCY_MODE:
        emergency_mode()
    elif current_mode == SPECIAL_MODE:
        special_mode()
    elif current_mode == POWER_SAVING_MODE:
        power_saving_mode()
    return current_mode

ota.ota_update()
ota.ota_disconnect()

import ble_module.exec_ble as ble 					#BLE

b_uart = ble.init_ble()

num_leds = 1  # 사용하는 LED의 개수

#LED
led.led('RGB')
num = 0
CNT = 0
CNT_RUN=0

# 초기 설정
current_mode = None
btn_pressed = False
power_saving_start_time = None
idle_mode_start_time=time.ticks_ms()

# 초절전 모드로 진입하는 시간( *분을 밀리초로 변환 )
POWER_SAVING_TIMEOUT = 30 * 1000
ANG_TIMEOUT = 10 * 1000
DIS_TIMEOUT = 30 * 1000
RUN_TIMEOUT =  10 * 1000
TRN_TIMEOUT =  600 * 1000

# 추가된 전역 변수
IDLE_TO_POWER_SAVING_FLAG = False
IDLE_TO_RUN_FLAG = False
IDLE_START_FLAG = False
RUN_START_FLAG = False

init_dvs()

while True:
    current_mode = exec_mode(check_mode(current_mode))
    CNT= CNT+1