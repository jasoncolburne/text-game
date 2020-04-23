from random import randint
import re
import yaml

DEBUG = False
DICE_RE = re.compile('^(\d+)d(\d+)$')
MONSTERS_CONFIG_PATH = './monsters.yml'
CHARACTERS_CONFIG_PATH = './characters.yml'
ALLOWED_SIDES = [4, 6, 8, 10, 12, 20]

xxx = ("-"*30)

class Combatant:
    def __init__(self, name, data):
        self.name = name
        self.attacks = data['attacks']
        self.defence = data['defence']
        self.health = data.get('health', data['maximum_health'])
        self.maximum_health = data['maximum_health']

    def damage(self, health):
        self.health = max(0, self.health - health)

    def heal(self, health):
        self.health = min(self.maximum_health, self.health + health)

    def as_dict(self):
        return {
            'attacks': self.attacks,
            'defence': self.defence,
            'health': self.health,
            'maximum_health': self.maximum_health,
        }

    def print_stats(self):
        print("combatant stats printed here")
        pass

class NonPlayerCharacter(Combatant):
    pass

class Player(Combatant):
    pass

class TextEngine:
    def prompt(self, question):
        return input(question + ' ')

    def menu(self, choices, question, display_values = False):
        index = 0
        if isinstance(choices, list):
            values = choices
            for label in choices:
                print(f"{index + 1}. {label}")
                index +=1
        elif isinstance(choices, dict):
            values = []
            for label, value in choices.items():
                values.append(value)
                suffix = ""
                if display_values:
                    suffix = f" ({value})"
                print(f"{index + 1}. {label}" + suffix)
                index += 1
        else:
            raise("Unknown choices type")

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


class World:
    def __init__(self, text_engine = None):
        self.text_engine = text_engine or TextEngine()

        with open(CHARACTERS_CONFIG_PATH) as f:
            self.characters_data = yaml.load(f, Loader=yaml.FullLoader)
        with open(MONSTERS_CONFIG_PATH) as f:
            self.monsters_data = yaml.load(f, Loader=yaml.FullLoader)

    def enter(self):
        print("Characters:")
        character_name = self.text_engine.menu(list(self.characters_data.keys()), "Choose your Adventurer!")
        self.character = Player(character_name, self.characters_data[character_name])

    def spawn(self, monster_name):
        return NonPlayerCharacter(monster_name, self.monsters_data[monster_name])

class CombatEngine:
    def __init__(self, player, enemy, text_engine = None):
        self.player = player
        self.enemy = enemy
        self.text_engine = text_engine or TextEngine()

    def fight(self):
        player = self.player
        enemy = self.enemy
        print(f"You have encountered a {enemy.name}!")
        while True:
            self.player_turn(enemy)
            if enemy.health <= 0:
                print(f"Congratulations! You have defeated the {enemy.name}!")
                break
            self.enemy_turn(enemy)
            if player.health <= 0:
                print("You have been slain")
                exit()

    def print_stats(self, player, enemy):
        print(f"Your health: {player.health}")
        print(f"{enemy.name} health: {enemy.health}")

    def player_turn(self, enemy):
        player = self.player
        print("Your turn to attack!")
        self.print_stats(player, enemy)
        attack = self.text_engine.menu(player.attacks, "Your choice?", True)
        damage = self.sum_dice(attack)
        print(f"You have damaged the {enemy.name} by {damage} health!")
        enemy.damage(damage)

    def enemy_turn(self, enemy):
        player = self.player
        print(f"It's the {enemy.name}'s turn!")
        self.print_stats(player, enemy)
        number_of_attacks = len(enemy.attacks)
        attack_index = randint(0, number_of_attacks - 1)
        attack_name = list(enemy.attacks.keys())[attack_index]
        attack_value = enemy.attacks[attack_name]
        damage = self.sum_dice(attack_value)
        print(f"The {enemy.name} has used {attack_name}! You lose {damage} health!")
        player.damage(damage)

    def roll(self, number, sides):
        result = []
        if sides not in ALLOWED_SIDES:
            print('Invalid choice')
            return []
        for i in range(number):
            result.append(randint(1, sides))
        if DEBUG:
            print('Rolled ' + str(result))
        return result

    def sum_dice(self, desired):
        match = DICE_RE.match(desired)
        number_of_dice = int(match.group(1))
        number_of_sides = int(match.group(2))
        return sum(self.roll(number_of_dice, number_of_sides), 0)



#story creation begins here

answer = input("would you like to adventure? (yes/no) ")
# world = world() loaded world assets (characters, monsters) world.enter adds 'choose character'
world = World()
world.enter()

if answer.lower().strip() == "yes":

    answer = input("You approach a cave, You are hungry and freezing, with only one flint left to light your torch, Do you light it?").lower().strip()
    if answer == "yes":
        answer = input("Your torch illuminates the cave infront of you. There are bones littered all over the ground. You hear a low growl, sounded like it came from within the cave. Would would you like to proceed forward?")

    elif answer == "no":
        print("You hear footsteps creep up behind you.")
        #added monster spawn
        goblin = world.spawn('Goblin')
        CombatEngine(world.character, goblin).fight()

        answer = input("You approach a cave, You are hungry and freezing fight? y/n")


else:
    print ("That is too bad. You die of old age")
