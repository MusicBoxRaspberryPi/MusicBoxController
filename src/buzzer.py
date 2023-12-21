from machine import Pin

from lib.buzzer import Buzzer


class BuzzerInterface:
    def __init__(self, pin: int):
        self.__buzzer = Buzzer(Pin(pin))

    def play_success(self):
        self.__buzzer.beep([[500, 50], [900, 150]])

    def play_failure(self):
        self.__buzzer.beep([[392, 200], [330, 200], [261, 400]])

    def play_ok(self):
        self.__buzzer.beep([[2000, 100]])
