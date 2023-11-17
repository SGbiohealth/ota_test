from ota_module import ota
from ota_module.ota import OTAUpdater
from WIFI_CONFIG import SSID, PASSWORD

FIRMWARE_URL = "https://raw.githubusercontent.com/JSShinnn/ota_test/main/"
VER_URL = 'https://raw.githubusercontent.com/JSShinnn/ota_test/main/version.json'

def ota_update(firmware_url, filename, verURL) :
    # FIRMWARE_URL 폴더 내에 "firmware.py의 파일이 펌웨어 파일이 됨"

    ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, filename, verURL)

    ota_updater.download_and_install_update_if_available()

ota_update(FIRMWARE_URL, "firmware.py", VER_URL)
