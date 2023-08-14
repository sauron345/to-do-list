from colorama import Fore, Back, Style
from typing import Optional


class Message:

    fg = Fore
    bg = Back

    @staticmethod
    def __color(text: str, fg: Fore, bg: Optional[Back] | None = None):
        colored_text = f'{fg}{text}{Style.RESET_ALL}'
        return colored_text if bg is None else bg + colored_text

    @staticmethod
    def error(text: str):
        return f'{Message.__color(text, Message.fg.LIGHTRED_EX)}'

    @staticmethod
    def success(text: str):
        return f'{Message.__color(text, Message.fg.LIGHTGREEN_EX)}'

    @staticmethod
    def info(text: str):
        return f'{Message.__color(text, Message.fg.LIGHTYELLOW_EX)}'