import yaml

class Character:
    def __init__(self, name, data):
        self.name = name
        self.attacks = data['attacks']
        self.defense = data['defense']
        self.health = data.get('health', data['maximum_health'])
        self.maximum_health = data['maximum_health']

    def damage(self, health):
        self.health = max(0, self.health - health)

    def heal(self, health):
        self.health = min(self.maximum_health, self.health + health)

    def as_dict(self):
        return {
            'attacks': self.attacks,
            'defense': self.defense,
            'health': self.health,
            'maximum_health': self.maximum_health,
        }

    def as_yaml(self):
        return yaml.dump({ self.name: self.as_dict() })

    def print_stats(self):
        print(f"{self.name}: Health {self.health}/{self.maximum_health} Mana")
        pass

class NonPlayerCharacter(Character):
    pass

class PlayerCharacter(Character):
    pass