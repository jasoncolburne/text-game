import os
import sys

# this seems like a silly hack but i can't figure out anything else
path = os.path.abspath(".")
sys.path.append(path)

from text_game.world import World
from text_game.combat_engine import CombatEngine

world = World('example/data/characters', 'example/data/non_player_characters.yml')
world.enter('New')
world.character.name = 'Jason'

goblin = world.spawn('Goblin')
ce = CombatEngine('example/data/attacks.yml')
ce.fight(world.character, goblin)
