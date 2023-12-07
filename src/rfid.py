from lib.mfrc522 import MFRC522


class RFIDInterface:
    def __init__(self, sda_pin: int, sck_pin: int, mosi_pin: int, miso_pin: int, rst_pin: int):
        self.__rfid = MFRC522(sck=sck_pin, miso=miso_pin, mosi=mosi_pin, cs=sda_pin, rst=rst_pin)

    def read_card_id(self):
        self.__rfid.init()
        (stat, tag_type) = self.__rfid.request(self.__rfid.REQIDL)
        if stat == self.__rfid.OK:
            (stat, uid) = self.__rfid.SelectTagSN()
            if stat == self.__rfid.OK:
                return int.from_bytes(bytes(uid), "little", False)
