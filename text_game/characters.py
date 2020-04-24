from abc import abstractmethod
from typing import Dict, Any
import yaml

PLAYER_LEVEL_MAPPING = {
    1: 0,
    2: 10,
    3: 50,
    4: 250,
    5: 1000,
    6: 2500,
    7: 5000,
    8: 10000,
    9: 25000,
    10: 50000,
}

NON_PLAYER_LEVEL_MAPPING = {
    1: 0,
    2: 10,
    3: 20,
    4: 30,
    5: 40,
    6: 50,
    7: 60,
    8: 70,
    9: 80,
    10: 90,
}


class Character:
    def __init__(self, name: str, data: Dict[str, Any]) -> None:
        self.name = name
        self.attacks = data['attacks']
        self.defense = data['defense']
        self.health = data.get('health', data['maximum_health'])
        self.maximum_health = data['maximum_health']
        self.mana = data.get('mana', data['maximum_mana'])
        self.maximum_mana = data['maximum_mana']
        self.experience = data['experience']

    def damage(self, health: int) -> None:
        self.health = max(0, self.health - health)

    def heal(self, health: int) -> None:
        self.health = min(self.maximum_health, self.health + health)

    def consume_mana(self, mana: int) -> None:
        self.mana = max(0, self.mana - mana)

    def as_dict(self) -> Dict[str, Any]:
        return {
            'attacks': self.attacks,
            'defense': self.defense,
            'health': self.health,
            'maximum_health': self.maximum_health,
        }

    def as_yaml(self) -> str:
        return yaml.dump({self.name: self.as_dict()})

    def identify(self) -> str:
        text = f'{self.name}: Health {self.health}/{self.maximum_health}'
        if self.maximum_mana:
            text += f' Mana {self.mana}/{self.maximum_mana}'

        return text

    @abstractmethod
    def level(self) -> int:
        pass

    def _level(self, mapping: Dict[int, int]) -> int:
        for level, experience in mapping.items():
            if self.experience < experience:
                return level - 1
        return list(mapping.keys())[-1]


class PlayerCharacter(Character):
    def level(self) -> int:
        return super()._level(PLAYER_LEVEL_MAPPING)

    def identify(self) -> str:
        text = super().identify()
        return text + f' Experience: {self.experience} Level: {self.level()}'


class NonPlayerCharacter(Character):
    def level(self) -> int:
        return super()._level(NON_PLAYER_LEVEL_MAPPING)

    def identify(self) -> str:
        text = super().identify()
        return text + f' Level: {self.level()}'
