from lib.button import Button


class ButtonsInterface:
    def __init__(self, left_button_pin: int, right_button_pin: int):
        self.__left_button = Button(left_button_pin, internal_pullup=True)
        self.__right_button = Button(right_button_pin, internal_pullup=True)

    def update(self) -> None:
        self.__left_button.update()
        self.__right_button.update()

    def is_left_button_pressed(self) -> bool:
        return self.__left_button.active

    def is_right_button_pressed(self) -> bool:
        return self.__right_button.active
