import machine
from lib.i2c_lcd import I2cLcd


class Symbol:
    def __init__(self, index: int, data: bytearray):
        self.index = index
        self.data = data


class Symbols:
    TICK = Symbol(0, bytearray([0x00, 0x00, 0x01, 0x02, 0x14, 0x08, 0x00, 0x00]))
    CROSS = Symbol(1, bytearray([0x00, 0x00, 0x11, 0x0A, 0x04, 0x0A, 0x11, 0x00]))
    NOTE = Symbol(2, bytearray([0x00, 0x0F, 0x09, 0x09, 0x19, 0x1B, 0x03, 0x00]))


class DisplayInterface:
    def __init__(self, sda_pin: int, scl_pin: int):
        self.__i2c = machine.I2C(0, sda=machine.Pin(sda_pin), scl=machine.Pin(scl_pin), freq=400000)
        self.__lcd = I2cLcd(self.__i2c, 0x27, 2, 16)
        self.__init_symbols()

    def print(self, text: str, line: int = 1, position: int = 1, clear_line: bool = False, clear_full: bool = False):
        self.__validate_inputs(line, position)
        text = self.__trim_text(text)

        if clear_full:
            self.clear()

        if clear_line:
            self.clear(line)

        self.__lcd.move_to(position - 1, line - 1)
        self.__lcd.putstr(text)

    def print_centered(self, text: str, line: int = 1):
        self.__validate_inputs(line)
        text = self.__trim_text(text)

        self.__lcd.move_to(0, line - 1)
        self.__lcd.putstr(text.center(16))

    def clear(self, line: int = None):
        self.__validate_inputs(line)

        if line:
            self.__lcd.move_to(0, line - 1)
            self.__lcd.putstr(" " * 16)
        else:
            self.__lcd.clear()

    def __init_symbols(self):
        for symbol in Symbols.__dict__.values():
            if isinstance(symbol, Symbol):
                self.__lcd.custom_char(symbol.index, symbol.data)

    @staticmethod
    def __validate_inputs(line: int = None, position: int = None):
        if line and line not in [1, 2]:
            raise ValueError("Line must be 1 or 2")

        if position and position not in range(1, 16):
            raise ValueError("Position must be between 1 and 16")

    @staticmethod
    def __trim_text(text: str):
        if len(text) > 16:
            text = text[:16]

        return text
