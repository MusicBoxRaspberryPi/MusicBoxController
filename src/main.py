import time

import wlan
from display import DisplayInterface, Symbols
from api import ApiInterface
from buttons import ButtonsInterface
from buzzer import BuzzerInterface
from rfid import RFIDInterface


class App:
    def __init__(self):
        self.__display = DisplayInterface(sda_pin=0, scl_pin=1)
        self.__api = ApiInterface()
        self.__buttons = ButtonsInterface(left_button_pin=12, right_button_pin=13)
        self.__buzzer = BuzzerInterface(pin=11)
        self.__rfid = RFIDInterface(sda_pin=15, sck_pin=18, mosi_pin=19, miso_pin=16, rst_pin=14)

        self.__music = {
            4117885779: "3uMUdlo47oEes3kgL4T4EC",
            4233351011: "5UW6yvwo3nVA609NgprdhK"
        }

    def run(self) -> None:
        self.__display.print_centered("Music Box", line=1)
        self.__display.print_centered("Initializing...", line=2)

        self.__connect_to_wifi()
        if not self.__check_api_health():
            return
        self.__display_current_device()

        while True:
            self.__buttons.update()

            if self.__buttons.is_left_button_pressed():
                self.__display.print("Loading...", line=2, clear_line=True)
                current_device_data = self.__api.previous_device()
                self.__change_device(current_device_data)

            if self.__buttons.is_right_button_pressed():
                self.__display.print("Loading...", line=2, clear_line=True)
                current_device_data = self.__api.next_device()
                self.__change_device(current_device_data)

            card_id = self.__rfid.read_card_id()
            if card_id:
                print(self.__music[card_id])
                self.__api.play(self.__music[card_id])
                print("Playing")
                time.sleep(5)

    def __connect_to_wifi(self) -> None:
        self.__display.print_centered("WiFi", line=2)

        wlan.connect()

        self.__display.print_centered(f"{chr(Symbols.TICK.index)} WiFi  ", line=2)
        self.__buzzer.play_success()

    def __check_api_health(self) -> bool:
        self.__display.print_centered("API", line=2)

        if not self.__api.check_health():
            self.__display.print_centered(f"{chr(Symbols.CROSS.index)} API  ", line=2)
            self.__buzzer.play_failure()
            return False

        self.__display.print_centered(f"{chr(Symbols.TICK.index)} API  ", line=2)
        self.__buzzer.play_success()
        return True

    def __display_current_device(self) -> None:
        self.__display.clear()
        self.__display.print("Devices:", line=1)

        current_device_data = self.__api.get_current_device(reset=True)
        self.__change_device(current_device_data)

    def __change_device(self, device_data: dict) -> None:
        text = f"{device_data['index'] + 1}/{device_data['total']} {device_data['device']['name']}"
        self.__display.print(text, line=2)


if __name__ == "__main__":
    app = App()
    app.run()
