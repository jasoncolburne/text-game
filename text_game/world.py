from os import walk
from typing import List
import yaml

from .characters import PlayerCharacter, NonPlayerCharacter
from .constants import DEFAULT_DATA_PATH


class World:
    def __init__(
        self,
        data_path: str = DEFAULT_DATA_PATH,
    ) -> None:
        self.characters_path = data_path + '/characters'
        with open(data_path + '/non_player_characters.yml', 'r') as f:
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
