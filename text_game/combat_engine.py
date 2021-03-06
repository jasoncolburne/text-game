from random import randint
import re
from typing import List
import yaml

from .characters import Character, PlayerCharacter
from .constants import DEFAULT_DATA_PATH
from .text_engine import TextEngine

DICE_RE = re.compile(r'^(\d+)\+(\d+)d(\d+)$')
ALLOWED_SIDES = [4, 6, 8, 10, 12, 20]


class CombatEngine:
    def __init__(
        self,
        text_engine: TextEngine = None,
        data_path: str = DEFAULT_DATA_PATH,
    ) -> None:
        self.text_engine = text_engine or TextEngine()

        with open(data_path + '/attacks.yml', 'r') as f:
            self.attacks = yaml.load(f, Loader=yaml.FullLoader)
        with open(data_path + '/phrases.yml', 'r') as f:
            self.phrases = yaml.load(f, Loader=yaml.FullLoader)
        with open(data_path + '/character_levels.yml', 'r') as f:
            self.character_levels = yaml.load(f, Loader=yaml.FullLoader)

    def _random_phrase(self, label: str) -> str:
        index = randint(0, len(self.phrases[label]) - 1)
        return self.phrases[label][index]

    def fight(self, player: PlayerCharacter, enemy: Character) -> bool:
        self.text_engine.set_player_status(player)
        self.text_engine.print(self._random_phrase('encounter').format(enemy_name=enemy.name))
        old_level = player.level()

        while True:
            self._player_turn(player, enemy)
            self.text_engine.set_player_status(player)
            if enemy.health <= 0:
                self.text_engine.print(self._random_phrase('victory').format(enemy_name=enemy.name))
                player.experience += enemy.experience
                gold = self._sum_dice(enemy.gold)
                player.gold += gold
                self.text_engine.set_player_status(player)
                self.text_engine.print(self._random_phrase('gold').format(gold=gold))
                if player.level() != old_level:
                    player.apply_new_level(self.character_levels[player.level()])
                    self.text_engine.set_player_status(player)
                    self.text_engine.print(self._random_phrase('level'))
                return True
            self._enemy_turn(player, enemy)
            self.text_engine.set_player_status(player)
            if player.health <= 0:
                self.text_engine.print(self._random_phrase('defeat').format(enemy_name=enemy.name))
                return False

    def _player_turn(self, player: Character, enemy: Character) -> None:
        self.text_engine.print()
        self.text_engine.print(self._random_phrase('player_turn').format(enemy_name=enemy.name))

        valid_attacks = self._get_valid_attacks(player)
        attack = self.text_engine.menu(valid_attacks, ">")

        self._execute_combat(attack, player, enemy)

    def _enemy_turn(self, player: Character, enemy: Character) -> None:
        self.text_engine.print()
        self.text_engine.print(self._random_phrase('enemy_turn').format(enemy_name=enemy.name))

        valid_attacks = self._get_valid_attacks(enemy)
        attack_index = randint(0, len(valid_attacks) - 1)
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
            self.text_engine.print(self._random_phrase('strike').format(
                attacker_name=attacker.name,
                attack_name=attack_name,
                defender_name=defender.name,
                damage=damage,
            ))
        else:
            self.text_engine.print(self._random_phrase('miss').format(attacker_name=attacker.name))

    def _sum_dice(self, expression: str) -> int:
        match = DICE_RE.match(expression)

        base = int(match.group(1))  # type: ignore
        number_of_dice = int(match.group(2))  # type: ignore
        number_of_sides = int(match.group(3))  # type: ignore

        return base + sum(self._roll(number_of_dice, number_of_sides), 0)

    def _roll(self, number: int, sides: int) -> List[int]:
        if sides not in ALLOWED_SIDES:
            raise AttributeError('Disallowed number of sides')

        return [randint(1, sides) for _ in range(number)]
