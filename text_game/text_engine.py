from random import random
from time import sleep
from typing import Any, Dict, List, Union
import curses

from .characters import PlayerCharacter
from .constants import DEFAULT_PRINTING_DELAY_MAXIMUM, DEFAULT_PRINTING_DELAY_MINIMUM


class TextEngine:
    def __init__(
        self,
        printing_delay_minimum: float = DEFAULT_PRINTING_DELAY_MINIMUM,
        printing_delay_maximum: float = DEFAULT_PRINTING_DELAY_MAXIMUM,
    ) -> None:
        # pylint: disable=no-member
        self.printing_delay_minimum = printing_delay_minimum
        self.printing_delay_maximum = printing_delay_maximum

        curses.noecho()
        curses.curs_set(False)

        self.status_bar = curses.newwin(2, curses.COLS, 0, 0)
        self.main_window = curses.newwin(curses.LINES - 4, curses.COLS, 2, 0)
        self.prompt_bar = curses.newwin(1, curses.COLS, curses.LINES - 1, 0)

        self.main_window.scrollok(True)

        self.main_window.addstr('\n' * (curses.LINES - 2))
        self.main_window.refresh()

    def anykey(self) -> None:
        self.prompt_bar.getkey()

    def get_status_width(self) -> int:
        # pylint: disable=no-member
        return curses.COLS

    def set_player_status(self, player: PlayerCharacter):
        # pylint: disable=no-member
        self._set_status_bar(player.status_bar_text(curses.COLS))

    def _set_status_bar(self, text: str) -> None:
        self.status_bar.clear()
        self.status_bar.addstr(text, curses.A_REVERSE)
        self.status_bar.refresh()

    def prompt(self, question: str) -> str:
        self.prompt_bar.clear()
        self.prompt_bar.addstr(question + ' ')
        self.prompt_bar.refresh()

        answer = ''
        count = 0
        while True:
            key = self.prompt_bar.getkey()
            # self.main_window.addstr(repr(key) + '\n')
            # self.main_window.refresh()
            if key == '\x7f':
                if count > 0:
                    answer = answer[0:-1]
                    self.prompt_bar.clear()
                    self.prompt_bar.addstr(question + ' ' + answer)
                    self.prompt_bar.refresh()
                    count -= 1
            elif key == '\n':
                break
            elif len(key) == 1:
                self.prompt_bar.addch(key)
                self.prompt_bar.refresh()
                count += 1
                answer += key

        self.prompt_bar.clear()
        self.prompt_bar.refresh()
        return answer

    def print(self, text: str = None) -> None:
        self.main_window.addch('\n')

        if text:
            for character in text:
                self.main_window.addch(character)
                self.main_window.refresh()
                delay = random() * (self.printing_delay_maximum - self.printing_delay_minimum) + self.printing_delay_minimum
                sleep(delay)

        self.main_window.refresh()

    def menu(self, choices: Union[List, Dict], question: str, display_values: bool = False) -> Any:
        index = 0
        if isinstance(choices, list):
            values = choices
            for label in choices:
                self.print(f"{index + 1}. {label}")
                index += 1
        elif isinstance(choices, dict):
            values = []
            for label, value in choices.items():
                values.append(value)
                suffix = f" ({value})" if display_values else ""
                self.print(f"{index + 1}. {label}" + suffix)
                index += 1
        else:
            raise AttributeError("Unrecognized choices type")

        result = None
        while result is None:
            try:
                choice = int(self.prompt(question))
                if choice < 1:
                    raise IndexError("list index out of range")
                result = values[choice - 1]
            except (ValueError, IndexError):
                self.print("Please select a valid choice.")

        return result
