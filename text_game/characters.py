from typing import Dict, Any
import yaml


class Character:
    def __init__(self, name, data):
        self.name = name
        self.attacks = data['attacks']
        self.defense = data['defense']
        self.health = data.get('health', data['maximum_health'])
        self.maximum_health = data['maximum_health']
        self.mana = data.get('mana', data['maximum_mana'])
        self.maximum_mana = data['maximum_mana']

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

    def as_yaml(self):
        return yaml.dump({self.name: self.as_dict()})

    def print_stats(self):
        print(f"{self.name}: Health {self.health}/{self.maximum_health} Mana {self.mana}/{self.maximum_mana}")


class NonPlayerCharacter(Character):
    pass


class PlayerCharacter(Character):
    pass
