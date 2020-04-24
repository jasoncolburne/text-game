from text_game.combat_engine import CombatEngine, ALLOWED_SIDES
from text_game.text_engine import TextEngine
from text_game.world import World


class FakeTextEngine(TextEngine):
    def set_expected_data(self, data):
        self.expected_data = data
        self.text_index = 0

    def menu(self, choices, question, display_values=False):
        assert choices == self.expected_data['choices']
        assert question == self.expected_data['question']

    def prompt(self, question):
        assert question == self.expected_data['question']

    def print(self, text):
        assert text == self.expected_data['text'][self.text_index]
        self.text_index += 1


def _setup_world():
    return World('text_game/tests/fixtures/characters', 'text_game/tests/fixtures/non_player_characters.yml')


def _setup_combat_engine(text_engine=None):
    return CombatEngine('text_game/tests/fixtures/attacks.yml', 'text_game/tests/fixtures/phrases.yml', text_engine)


def test_init__loads_attacks():
    combat_engine = _setup_combat_engine()
    assert len(combat_engine.attacks) == 4


def test__get_valid_attacks():
    world = _setup_world()
    combat_engine = _setup_combat_engine()

    troll = world.spawn('Troll')
    assert combat_engine._get_valid_attacks(troll) == ['Attack']
    troll.mana = 20
    assert combat_engine._get_valid_attacks(troll) == ['Attack', 'Mana']


def test__roll():
    combat_engine = _setup_combat_engine()

    for number in range(1, 10):
        for sides in ALLOWED_SIDES:
            result = combat_engine._roll(number, sides)
            assert len(result) == number
            for die in result:
                assert die >= 1
                assert die <= sides
