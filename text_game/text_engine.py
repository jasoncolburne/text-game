from typing import List, Dict, Union, Any, Optional


class TextEngine:
    def prompt(self, question: str) -> str:
        return input(question + ' ')

    def print(self, text: str = None) -> None:
        print(text or '')

    def menu(self, choices: Union[List, Dict], question: str, display_values: bool = False) -> Any:
        index = 0
        if isinstance(choices, list):
            values = choices
            for label in choices:
                print(f"{index + 1}. {label}")
                index += 1
        elif isinstance(choices, dict):
            values = []
            for label, value in choices.items():
                values.append(value)
                suffix = f" ({value})" if display_values else ""
                print(f"{index + 1}. {label}" + suffix)
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
                print("Please select a valid choice.")

        return result
