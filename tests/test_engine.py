"""Engine tests: no AI, no server. They prove the guardrails hold."""

import copy
import json
from pathlib import Path

import pytest

from keyhole.engine import Game

WORLD = json.loads((Path(__file__).parents[1] / "keyhole" / "world.json").read_text(encoding="utf-8"))

# Study to hall, then find the brass key under the rug.
FIND_BRASS_KEY = [("move", "east"), ("use", "rug"), ("take", "brass-key")]
# From the hall: fetch and light the candle, come back.
LIGHT_CANDLE = [
    ("move", "north"),
    ("take", "candle"),
    ("take", "matches"),
    ("use", "matches", "candle"),
    ("move", "south"),
]
# The demo, start to finish.
GOLDEN_PATH = [
    ("take", "note"),
    ("use", "note"),
    *FIND_BRASS_KEY,
    *LIGHT_CANDLE,
    ("use", "brass-key", "cellar-door"),
    ("move", "down"),
    ("take", "iron-key"),
    ("move", "up"),
    ("use", "iron-key", "front-door"),
]


@pytest.fixture
def game():
    return Game(copy.deepcopy(WORLD))


def play(game, steps):
    """Run steps in order and require every one to succeed."""
    results = []
    for verb, *args in steps:
        result = getattr(game, verb)(*args)
        assert result["ok"], (verb, args, result)
        results.append(result)
    return results


def test_golden_path_wins(game):
    results = play(game, GOLDEN_PATH)
    assert results[-1] == {"ok": True, "action": "unlock", "door": "front-door", "won": True}
    assert game.state["won"] is True


def test_cellar_door_is_locked_until_unlocked(game):
    play(game, FIND_BRASS_KEY + LIGHT_CANDLE)
    assert game.move("down") == {"ok": False, "refusal": "The cellar door is locked."}
    play(game, [("use", "brass-key", "cellar-door"), ("move", "down")])
    assert game.state["room"] == "cellar"


def test_front_door_is_locked(game):
    play(game, [("move", "east")])
    assert game.move("out") == {"ok": False, "refusal": "The front door is locked."}
    assert game.state["room"] == "hall"


def test_cellar_needs_a_lit_candle(game):
    play(game, FIND_BRASS_KEY + [("use", "brass-key", "cellar-door")])
    too_dark = {"ok": False, "refusal": "It is too dark to go down."}
    assert game.move("down") == too_dark

    play(game, [("move", "north"), ("take", "candle"), ("move", "south")])
    assert game.move("down") == too_dark  # an unlit candle is not light

    play(game, [("move", "north"), ("take", "matches"), ("use", "matches", "candle"), ("move", "south")])
    assert game.move("down")["ok"]


def test_take_requires_presence(game):
    play(game, [("move", "east")])
    assert game.take("note") == {"ok": False, "refusal": "There is no note here."}


def test_brass_key_is_hidden_until_the_rug_is_lifted(game):
    play(game, [("move", "east")])
    assert "brass-key" not in game.look()["items"]
    assert game.take("brass-key") == {"ok": False, "refusal": "There is no brass key here."}
    reveal = game.use("rug")
    assert reveal == {"ok": True, "action": "reveal", "item": "rug", "found": ["brass-key"]}
    assert game.take("brass-key")["ok"]
    assert game.use("rug") == {"ok": False, "refusal": "Nothing more under the rug."}


def test_rug_can_never_be_taken(game):
    play(game, [("move", "east")])
    refusal = {"ok": False, "refusal": "The rug won't come with you."}
    assert game.take("rug") == refusal
    play(game, [("use", "rug")])
    assert game.take("rug") == refusal


def test_use_requires_carrying_the_item(game):
    play(game, [("move", "east")])
    assert game.use("iron-key", "front-door") == {"ok": False, "refusal": "You don't have that."}


def test_use_requires_the_target_to_be_here(game):
    play(game, GOLDEN_PATH[:-2])  # standing in the cellar, iron key in hand
    assert game.state["room"] == "cellar"
    assert game.use("iron-key", "front-door") == {"ok": False, "refusal": "There is no front door here."}


def test_use_requires_the_right_target(game):
    play(game, FIND_BRASS_KEY)
    assert game.use("brass-key") == {"ok": False, "refusal": "Use the brass key on what?"}
    assert game.use("brass-key", "front-door") == {"ok": False, "refusal": "That doesn't work on that."}


def test_win_fires_exactly_once(game):
    play(game, GOLDEN_PATH)
    over = {"ok": False, "refusal": "The game is over."}
    assert game.use("iron-key", "front-door") == over
    assert game.move("out") == over
    assert game.state["won"] is True
    assert game.state["unlocked"].count("front-door") == 1


def test_no_secret_passage(game):
    """Honest absence: the hall has exactly the exits the world file defines."""
    play(game, [("move", "east")])
    assert set(game.look()["exits"]) == {"west", "north", "down", "out"}
    assert game.move("trapdoor") == {"ok": False, "refusal": "You can't go that way."}


def test_state_round_trips_through_the_save_file(game, tmp_path):
    world_path = tmp_path / "world.json"
    state_path = tmp_path / "state.json"
    world_path.write_text(json.dumps(WORLD), encoding="utf-8")

    play(game, FIND_BRASS_KEY + LIGHT_CANDLE)
    game.save(state_path)
    loaded = Game.load(world_path, state_path)

    assert loaded.state == game.state
    assert loaded.look() == game.look()
    assert loaded.inventory() == game.inventory()


def test_missing_save_file_means_a_fresh_game(tmp_path):
    world_path = tmp_path / "world.json"
    world_path.write_text(json.dumps(WORLD), encoding="utf-8")
    loaded = Game.load(world_path, tmp_path / "state.json")
    assert loaded.state == Game.fresh_state(WORLD)
