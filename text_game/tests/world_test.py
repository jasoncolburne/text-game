from text_game.world import World


def _setup_world():
    return World('text_game/tests/fixtures')


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
    gimp = world.spawn('Gimp')
    assert gimp is not None
