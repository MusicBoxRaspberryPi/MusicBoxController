import time

import wlan
from display import DisplayInterface, Symbols
from api import ApiInterface
from buttons import ButtonsInterface
from buzzer import BuzzerInterface
from rfid import RFIDInterface
from config import Config


class App:
    def __init__(self):
        self.__display = DisplayInterface(
            sda_pin=Config.Display.SDA_PIN,
            scl_pin=Config.Display.SCL_PIN
        )
        self.__buttons = ButtonsInterface(
            left_button_pin=Config.Buttons.LEFT_PIN,
            right_button_pin=Config.Buttons.RIGHT_PIN
        )
        self.__rfid = RFIDInterface(
            sda_pin=Config.RFID.SDA_PIN,
            sck_pin=Config.RFID.SCK_PIN,
            mosi_pin=Config.RFID.MOSI_PIN,
            miso_pin=Config.RFID.MISO_PIN,
            rst_pin=Config.RFID.RST_PIN
        )
        self.__buzzer = BuzzerInterface(pin=Config.BUZZER_PIN)
        self.__api = ApiInterface(base_url=Config.API_BASE_URL)

        self.__last_rfid_successful_read_time = 0
        self.__rfid_read_delay = Config.RFID.READ_DELAY

    def handle_error(self, exception: Exception) -> None:
        self.__display.clear()
        self.__display.print_centered("Exception", line=1)
        self.__display.print_centered("occurred", line=2)
        self.__buzzer.play_failure()

        time.sleep(2)

        self.__display.print_scroll_text(f"{type(exception).__name__}:{str(exception)}", line=2)

    def run(self) -> None:
        self.__display.print_centered(f"{chr(Symbols.NOTE.index)} Music Box {chr(Symbols.NOTE.index)}", line=1)
        self.__display.print_centered("Initializing...", line=2)

        self.__connect_to_wifi()
        if not self.__check_api_health():
            return

        self.__display.print("Devices:", line=1, clear_full=True)
        self.__display_current_device(reset=True)

        while True:
            self.__check_buttons_press()
            self.__check_rfid_read()

    def __connect_to_wifi(self) -> None:
        self.__display.print_centered("WiFi", line=2)

        wlan.connect(Config.Wifi.SSID, Config.Wifi.PASSWORD)

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

    def __display_current_device(self, reset: bool = False) -> None:
        self.__display.print("Loading...", line=2, clear_line=True)
        current_device_data = self.__api.get_current_device(reset=reset)
        self.__display_device(current_device_data)

    def __display_device(self, device_data: dict) -> None:
        if device_data == {}:
            self.__display.print("No devices", line=2)
            return

        text = f"{device_data['index'] + 1}/{device_data['total']} {device_data['device']['name']}"
        self.__display.print(text, line=2)

    def __check_buttons_press(self) -> None:
        was_left_button_pressed = self.__buttons.was_left_button_pressed()
        was_right_button_pressed = self.__buttons.was_right_button_pressed()

        if not any((was_left_button_pressed, was_right_button_pressed)):
            return

        self.__display.print("Loading...", line=2, clear_line=True)

        if was_left_button_pressed:
            current_device_data = self.__api.previous_device()
        elif was_right_button_pressed:
            current_device_data = self.__api.next_device()
        else:
            return

        self.__display_device(current_device_data)
        self.__buttons.reset()

    def __check_rfid_read(self) -> None:
        if time.time() - self.__last_rfid_successful_read_time <= self.__rfid_read_delay:
            return

        card_id = self.__rfid.read_card_id()

        if not card_id:
            return

        self.__display.print("Reading card...", line=2, clear_line=True)

        if card_id not in Config.TRACKS:
            self.__display.print(f"{chr(Symbols.CROSS.index)} Unknown card", line=2, clear_line=True)
            self.__buzzer.play_failure()
        else:
            track = Config.TRACKS[card_id]
            self.__api.play(track.id)
            self.__display.print(f"{chr(Symbols.NOTE.index)} {track.name}", line=2, clear_line=True)
            self.__buzzer.play_success()

        time.sleep(1)
        self.__display_current_device()

        self.__last_rfid_successful_read_time = time.time()


if __name__ == "__main__":
    app = App()

    try:
        app.run()
    except Exception as e:
        app.handle_error(e)
