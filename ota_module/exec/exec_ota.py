from ota_module import ota
from ota_module.ota import OTAUpdater
from WIFI_CONFIG import SSID, PASSWORD, FIRMWARE_URL

firmware_url = FIRMWARE_URL
filename = "firmware.py"
ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, filename)

def ota_update(firmware_url, filename) :
    # FIRMWARE_URL 폴더 내에 "firmware.py의 파일이 펌웨어 파일이 됨"
    ota_updater.download_and_install_update_if_available()

def ota_disconnect() :
    ota_updater.Disconnect_wifi()

def ota_connect() :
    ota_updater.connect_wifi()