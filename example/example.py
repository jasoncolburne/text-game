import os
import sys

from curses import wrapper

# this seems like a silly hack but i can't figure out anything else
path = os.path.abspath(".")
sys.path.append(path)

from text_game.combat_engine import CombatEngine
from text_game.world import World
from text_game.text_engine import TextEngine

def main(stdscr):
    te = TextEngine()

    world = World('example/data/characters', 'example/data/non_player_characters.yml')
    ce = CombatEngine(te, 'example/data/attacks.yml', 'example/data/phrases.yml')

    te.print('Welcome to the Arena!')
    te.print('Load your character:')
    name = te.menu(world.character_names(), '>')

    world.enter(name)

    if name == 'New':
        te.print('Ahhh, a new recruit. What is your name?')
        while True:
            name = te.prompt('>')
            if name not in world.character_names():
                break
            te.print('Sorry, that name is taken!')
        world.character.name = name

    player = world.character

    # enemy = world.spawn('Troll')
    # ce.fight(player, enemy)
    enemy = world.spawn('Goblin')
    ce.fight(player, enemy)
    world.leave()

wrapper(main)