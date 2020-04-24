from text_game.combat_engine import CombatEngine
from text_game.text_engine import TextEngine
from text_game.world import World


class FakeTextEngine(TextEngine):
    def set_expected_choices(self, choices):
        self.choices = choices

    def menu(self, choices, question, display_values=False):
        assert self.choices == choices


def _setup_world():
    return World('text_game/tests/fixtures/characters', 'text_game/tests/fixtures/non_player_characters.yml')


def _setup_combat_engine(text_engine=None):
    return CombatEngine('text_game/tests/fixtures/attacks.yml', text_engine)


def test_init__loads_attacks():
    combat_engine = _setup_combat_engine()
    assert len(combat_engine.attacks) == 4


def test_get_valid_attacks():
    world = _setup_world()
    combat_engine = _setup_combat_engine()

    result = combat_engine._get_valid_attacks(world.spawn('Troll'))

    assert result == ['Attack']
