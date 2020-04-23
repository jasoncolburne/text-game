from os import walk, path
import yaml

from .characters import PlayerCharacter, NonPlayerCharacter

DEFAULT_CHARACTERS_PATH = './data/characters'
DEFAULT_NON_PLAYER_CHARACTER_PATH = './data/non_player_characters.yml'

class World:
    def __init__(
        self,
        characters_path = DEFAULT_CHARACTERS_PATH,
        non_player_character_path = DEFAULT_NON_PLAYER_CHARACTER_PATH,
    ):
        self.characters_path = characters_path
        with open(non_player_character_path, 'r') as f:
            self.npc_data = yaml.load(f, Loader=yaml.FullLoader)

    def character_names(self):
        filenames = []
        for (_, _, f) in walk(self.characters_path):
            filenames.extend(f)
            break
        return [filename.split('.')[0] for filename in filenames]

    def enter(self, name):
        with open(self.characters_path + '/' + name + '.yml', 'r') as f:
            self.character = PlayerCharacter(name, yaml.load(f, Loader=yaml.FullLoader))

    def spawn(self, npc_name):
        return NonPlayerCharacter(npc_name, self.npc_data[npc_name])
