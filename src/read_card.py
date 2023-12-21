import time

from rfid import RFIDInterface
from config import Config

rfid = RFIDInterface(
    sda_pin=Config.RFID.SDA_PIN,
    sck_pin=Config.RFID.SCK_PIN,
    mosi_pin=Config.RFID.MOSI_PIN,
    miso_pin=Config.RFID.MISO_PIN,
    rst_pin=Config.RFID.RST_PIN
)


while True:
    print(rfid.read_card_id())
    time.sleep(0.5)
