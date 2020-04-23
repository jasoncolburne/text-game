from random import randint
import re
import yaml

from .text_engine import TextEngine

DEBUG = False
DICE_RE = re.compile(r'^(\d+)\+(\d+)d(\d+)$')
ALLOWED_SIDES = [4, 6, 8, 10, 12, 20]

class CombatEngine:
    def __init__(self, player, enemy, text_engine = None):
        self.player = player
        self.enemy = enemy
        self.text_engine = text_engine or TextEngine()

    def fight(self):
        player = self.player
        enemy = self.enemy
        print(f"You have encountered a {enemy.name}!")
        player.print_stats()
        enemy.print_stats()
        while True:
            self.player_turn()
            if enemy.health <= 0:
                print(f"Congratulations! You have defeated the {enemy.name}!")
                break
            self.enemy_turn()
            if player.health <= 0:
                print("You have been slain")
                exit()

    def player_turn(self):
        player = self.player
        enemy = self.enemy

        print("Your turn to attack!")
        attack = self.text_engine.menu(player.attacks, "Your choice?", True)
        damage = self.sum_dice(attack)
        print(f"You have damaged the {enemy.name} by {damage} health!")
        enemy.damage(damage)
        enemy.print_stats()

    def enemy_turn(self):
        player = self.player
        enemy = self.enemy

        print(f"It's the {enemy.name}'s turn!")
        number_of_attacks = len(enemy.attacks)
        attack_index = randint(0, number_of_attacks - 1)
        attack_name = list(enemy.attacks.keys())[attack_index]
        attack_value = enemy.attacks[attack_name]
        damage = self.sum_dice(attack_value)
        print(f"The {enemy.name} has used {attack_name}! You lose {damage} health!")
        player.damage(damage)
        player.print_stats()

    def roll(self, number, sides):
        result = []
        if sides not in ALLOWED_SIDES:
            raise AttributeError('Disallowed number of sides')
        for _ in range(number):
            result.append(randint(1, sides))
        if DEBUG:
            print('Rolled ' + str(result))
        return result

    def sum_dice(self, desired):
        match = DICE_RE.match(desired)
        base_damage = int(match.group(1))
        number_of_dice = int(match.group(2))
        number_of_sides = int(match.group(3))
        return base_damage + sum(self.roll(number_of_dice, number_of_sides), 0)


# world = World()
# world.enter()

#         goblin = world.spawn('Goblin')
#         CombatEngine(world.character, goblin).fight()
