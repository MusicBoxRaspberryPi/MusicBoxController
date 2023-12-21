from machine import Pin


class ButtonsInterface:
    def __init__(self, left_button_pin: int, right_button_pin: int):
        self.__left_button = Pin(left_button_pin, Pin.IN, Pin.PULL_UP)
        self.__right_button = Pin(right_button_pin, Pin.IN, Pin.PULL_UP)

        self.__left_button.irq(trigger=Pin.IRQ_RISING, handler=self.__set_left_button_pressed)
        self.__right_button.irq(trigger=Pin.IRQ_RISING, handler=self.__set_right_button_pressed)

        self.__left_button_pressed = False
        self.__right_button_pressed = False

    def __set_left_button_pressed(self, pin):
        self.__left_button_pressed = True

    def __set_right_button_pressed(self, pin):
        self.__right_button_pressed = True

    def was_left_button_pressed(self):
        return self.__left_button_pressed

    def was_right_button_pressed(self):
        return self.__right_button_pressed

    def reset(self):
        self.__left_button_pressed = False
        self.__right_button_pressed = False

