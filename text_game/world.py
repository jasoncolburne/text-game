from os import walk
from typing import List
import yaml

from .characters import PlayerCharacter, NonPlayerCharacter
from .constants import DEFAULT_CHARACTERS_PATH, DEFAULT_NON_PLAYER_CHARACTER_PATH


class World:
    def __init__(
        self,
        characters_path: str = DEFAULT_CHARACTERS_PATH,
        non_player_character_path: str = DEFAULT_NON_PLAYER_CHARACTER_PATH,
    ) -> None:
        self.characters_path = characters_path
        with open(non_player_character_path, 'r') as f:
            self.npc_data = yaml.load(f, Loader=yaml.FullLoader)

    def character_names(self) -> List[str]:
        filenames = []
        for (_, _, f) in walk(self.characters_path):
            filenames.extend(f)
            break
        return [filename.split('.')[0] for filename in filenames]

    def enter(self, name: str) -> None:
        with open(self.characters_path + '/' + name + '.yml', 'r') as f:
            self.character = PlayerCharacter(name, yaml.load(f, Loader=yaml.FullLoader))

    def leave(self) -> None:
        with open(self.characters_path + '/' + self.character.name + '.yml', 'w') as f:
            f.write(self.character.as_yaml())

    def spawn(self, npc_name: str) -> NonPlayerCharacter:
        return NonPlayerCharacter(npc_name, self.npc_data[npc_name])
