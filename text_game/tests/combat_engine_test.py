from text_game.combat_engine import CombatEngine, ALLOWED_SIDES
from text_game.text_engine import TextEngine
from text_game.world import World


class FakeTextEngine(TextEngine):
    def __init__(self):
        pass

    def set_expected_data(self, expected_data, response_data):
        self.expected_data = expected_data
        self.response_data = response_data
        self.print_index = 0

    def menu(self, choices, question, display_values=False):
        assert choices == self.expected_data['choices']
        assert question == self.expected_data['question']
        return self.response_data['menu']

    def prompt(self, question):
        assert question == self.expected_data['question']
        return self.response_data['prompt']

    def print(self, text):
        assert text == self.expected_data['text'][self.print_index]
        self.print_index += 1


def _setup_world():
    return World('text_game/tests/fixtures')


def _setup_combat_engine(text_engine=None):
    text_engine = text_engine or FakeTextEngine()
    return CombatEngine(text_engine, 'text_game/tests/fixtures')


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
