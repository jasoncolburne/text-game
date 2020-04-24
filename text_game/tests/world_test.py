from text_game.world import World


def _setup_world():
    return World('text_game/tests/fixtures/characters', 'text_game/tests/fixtures/non_player_characters.yml')


def test_init__loads_npc_data():
    world = _setup_world()
    assert len(world.npc_data) == 2


def test_character_names():
    world = _setup_world()
    names = world.character_names()
    assert names == ['New']


def test_enter():
    world = _setup_world()
    world.enter('New')
    assert world.character is not None


def test_spawn():
    world = _setup_world()
    goblin = world.spawn('Gimp')
    assert goblin is not None
