from random import random
import sys
from time import sleep
from typing import Any, Dict, List, Union

from .constants import DEFAULT_PRINTING_DELAY_MAXIMUM, DEFAULT_PRINTING_DELAY_MINIMUM


class TextEngine:
    def __init__(
        self,
        printing_delay_minimum: float = DEFAULT_PRINTING_DELAY_MINIMUM,
        printing_delay_maximum: float = DEFAULT_PRINTING_DELAY_MAXIMUM,
    ) -> None:
        self.printing_delay_minimum = printing_delay_minimum
        self.printing_delay_maximum = printing_delay_maximum

    def prompt(self, question: str) -> str:
        return input(question + ' ')

    def print(self, text: str = None) -> None:
        if text:
            for character in text:
                sys.stdout.write(character)
                sys.stdout.flush()
                delay = random() * (self.printing_delay_maximum - self.printing_delay_minimum) + self.printing_delay_minimum
                sleep(delay)

        sys.stdout.write('\n')
        sys.stdout.flush()

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
