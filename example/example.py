import os
import sys

from curses import wrapper

# this seems like a silly hack but i can't figure out anything else
path = os.path.abspath(".")
sys.path.append(path)

from text_game.combat_engine import CombatEngine  # noqa: E402
from text_game.world import World  # noqa: E402
from text_game.text_engine import TextEngine  # noqa: E402


def main(stdscr):
    te = TextEngine()

    world = World('example/data')
    ce = CombatEngine(te, 'example/data')

    te.print('Welcome to the Arena!')
    te.print()
    te.print('Load your character:')
    name = te.menu(world.character_names(), '>')

    world.enter(name)

    if name == 'New':
        te.print('Ahhh, a new recruit!')
        while True:
            name = te.prompt('What is your name?')
            if name not in world.character_names():
                break
            te.print('Sorry, that name is taken!')
        world.character.name = name

    player = world.character
    te.set_player_status(player)

    while True:
        te.print()
        te.print('What would you like to do?')

        action = te.menu(['Fight', 'Sleep', 'Leave'], '>')

        te.print()

        if action == 'Fight':
            te.print('What would you like to fight?')
            enemy_name = te.menu(list(world.npc_data.keys()), '>')
            enemy = world.spawn(enemy_name)
            te.print()
            won = ce.fight(player, enemy)
            if not won:
                # player has died.
                te.print('[Press any key to continue]')
                te.anykey()
                break

        if action == 'Sleep':
            te.print('You feel much better after sleeping. This is a really long line to test whether wrapping without breaking words will work.')

            player.health = max(int(player.maximum_health * 0.75), player.health)
            player.mana = max(int(player.maximum_mana * 0.75), player.mana)
            te.set_player_status(player)

        if action == 'Leave':
            world.leave()

            te.print('You leave the arena, tired from a day of fighting.')
            te.print('[Press any key to exit]')

            te.anykey()
            break


wrapper(main)
