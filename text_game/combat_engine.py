from random import randint
import re
from typing import List
import yaml

from .characters import Character
from .constants import DEFAULT_ATTACKS_PATH
from .text_engine import TextEngine

DICE_RE = re.compile(r'^(\d+)\+(\d+)d(\d+)$')
ALLOWED_SIDES = [4, 6, 8, 10, 12, 20]


class CombatEngine:
    def __init__(self, attacks_path: str = DEFAULT_ATTACKS_PATH, text_engine: TextEngine = None) -> None:
        self.text_engine = text_engine or TextEngine()
        with open(attacks_path, 'r') as f:
            self.attacks = yaml.load(f, Loader=yaml.FullLoader)

    def fight(self, player: Character, enemy: Character) -> bool:
        player.print_stats()
        enemy.print_stats()
        print(f"You have encountered a {enemy.name}!")
        while True:
            self.player_turn(player, enemy)
            if enemy.health <= 0:
                print(f"Congratulations! You have defeated the {enemy.name}!")
                return True
            self.enemy_turn(player, enemy)
            if player.health <= 0:
                print("You have been slain")
                return False

    def player_turn(self, player: Character, enemy: Character) -> None:
        print("Your turn to attack!")

        valid_attacks = self._get_valid_attacks(player)
        attack = self.text_engine.menu(valid_attacks, "Your choice?")

        self._execute_combat(attack, player, enemy)

    def enemy_turn(self, player: Character, enemy: Character) -> None:
        print(f"It's the {enemy.name}'s turn!")

        valid_attacks = self._get_valid_attacks(enemy)
        number_of_attacks = len(valid_attacks)
        attack_index = randint(0, number_of_attacks - 1)
        attack = valid_attacks[attack_index]

        self._execute_combat(attack, enemy, player)

    def _get_valid_attacks(self, character: Character) -> List[str]:
        def predicate(attack_name):
            return self.attacks[attack_name]['mana_required'] <= character.mana

        return list(filter(predicate, character.attacks))

    def _execute_combat(self, attack_name: str, attacker: Character, defender: Character) -> None:
        attack = self.attacks[attack_name]
        attacker.consume_mana(attack['mana_required'])

        attack_roll = self._sum_dice(attack['attack_roll'])
        defense_roll = self._sum_dice(defender.defense)

        if attack_roll > defense_roll:
            damage = self._sum_dice(attack['damage_roll'])
            defender.damage(damage)
            print(f"{attacker.name} uses {attack_name} to injure {defender.name} by {damage}!")
            defender.print_stats()
        else:
            print(f"{attacker.name} misses!")

    def _sum_dice(self, expression: str) -> int:
        match = DICE_RE.match(expression)

        base = int(match.group(1))  # type: ignore
        number_of_dice = int(match.group(2))  # type: ignore
        number_of_sides = int(match.group(3))  # type: ignore

        return base + sum(self._roll(number_of_dice, number_of_sides), 0)

    def _roll(self, number: int, sides: int) -> List[int]:
        if sides not in ALLOWED_SIDES:
            raise AttributeError('Disallowed number of sides')

        result = []
        for _ in range(number):
            result.append(randint(1, sides))

        return result
