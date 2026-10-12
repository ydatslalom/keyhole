"""Keyhole world engine: pure game rules over world.json and state.json.

Every method returns facts, never prose: {"ok": True, ...facts} or
{"ok": False, "refusal": "..."}. Refusals are the only fixed sentences the
engine produces. This module knows nothing about MCP.
"""

import json
from pathlib import Path

CANDLE = "candle"


def _ok(**facts):
    return {"ok": True, **facts}


def _no(refusal):
    return {"ok": False, "refusal": refusal}


def _name(thing):
    """Turn an id like "cellar-door" into "cellar door" for refusals."""
    return thing.replace("-", " ")


class Game:
    def __init__(self, world, state=None):
        self.world = world
        self.state = state if state is not None else self.fresh_state(world)

    @staticmethod
    def fresh_state(world):
        return {
            "room": world["start"],
            "inventory": [],
            "taken": [],
            "revealed": [],
            "unlocked": [],
            "lit": False,
            "won": False,
        }

    @classmethod
    def load(cls, world_path, state_path):
        """Load the world and the save file; a missing save file means a fresh game."""
        world = json.loads(Path(world_path).read_text(encoding="utf-8"))
        state_path = Path(state_path)
        state = None
        if state_path.exists():
            state = json.loads(state_path.read_text(encoding="utf-8"))
        return cls(world, state)

    def save(self, state_path):
        Path(state_path).write_text(json.dumps(self.state, indent=2), encoding="utf-8")

    # Derived state

    def _room(self):
        return self.world["rooms"][self.state["room"]]

    def _visible_items(self):
        """Room items, plus anything under a revealed fixture, minus anything taken."""
        room = self._room()
        items = list(room.get("items", []))
        for fixture, hidden in room.get("hidden", {}).items():
            if fixture in self.state["revealed"]:
                items += hidden
        return [item for item in items if item not in self.state["taken"]]

    def _fixtures(self):
        return list(self._room().get("fixtures", []))

    def _locked(self, exit_):
        return "locked_by" in exit_ and exit_["door"] not in self.state["unlocked"]

    def _doors_here(self):
        return [exit_["door"] for exit_ in self._room()["exits"].values() if "door" in exit_]

    def _has_light(self):
        return CANDLE in self.state["inventory"] and self.state["lit"]

    # The five verbs

    def look(self):
        room = self._room()
        if room.get("dark") and not self._has_light():
            return _ok(room=self.state["room"], dark=True, desc="It is pitch dark.")
        exits = {}
        for direction, exit_ in room["exits"].items():
            fact = {"to": exit_["to"]}
            if "door" in exit_:
                fact["door"] = exit_["door"]
                fact["locked"] = self._locked(exit_)
            exits[direction] = fact
        return _ok(
            room=self.state["room"],
            desc=room["desc"],
            items=self._visible_items(),
            fixtures=self._fixtures(),
            exits=exits,
        )

    def move(self, direction):
        if self.state["won"]:
            return _no("The game is over.")
        exit_ = self._room()["exits"].get(direction)
        if exit_ is None:
            return _no("You can't go that way.")
        if self._locked(exit_):
            return _no(f"The {_name(exit_['door'])} is locked.")
        if exit_["to"] not in self.world["rooms"]:
            return _no("You can't go that way.")
        if self.world["rooms"][exit_["to"]].get("dark") and not self._has_light():
            return _no(f"It is too dark to go {direction}.")
        self.state["room"] = exit_["to"]
        return self.look()

    def take(self, item):
        if self.state["won"]:
            return _no("The game is over.")
        if item in self._fixtures():
            return _no(f"The {_name(item)} won't come with you.")
        if item not in self._visible_items():
            return _no(f"There is no {_name(item)} here.")
        self.state["inventory"].append(item)
        self.state["taken"].append(item)
        return _ok(taken=item, inventory=list(self.state["inventory"]))

    def use(self, item, target=None):
        if self.state["won"]:
            return _no("The game is over.")
        if item not in self.state["inventory"] and item not in self._fixtures():
            return _no("You don't have that.")
        entry = self.world["uses"].get(item)
        if entry is None:
            return _no("Nothing happens.")
        action = entry["action"]

        if action == "read":
            return _ok(action="read", item=item, text=entry["text"])

        if action == "reveal":
            if item in self.state["revealed"]:
                return _no(f"Nothing more under the {_name(item)}.")
            self.state["revealed"].append(item)
            found = self._room().get("hidden", {}).get(item, [])
            return _ok(action="reveal", item=item, found=list(found))

        # unlock and light both need a target
        if target is None:
            return _no(f"Use the {_name(item)} on what?")
        if target != entry["target"]:
            return _no("That doesn't work on that.")

        if action == "unlock":
            if target not in self._doors_here():
                return _no(f"There is no {_name(target)} here.")
            if target in self.state["unlocked"]:
                return _no("It is already unlocked.")
            self.state["unlocked"].append(target)
            win = self.world["win"]
            if item == win["item"] and target == win["target"]:
                self.state["won"] = True
                return _ok(action="unlock", door=target, won=True)
            return _ok(action="unlock", door=target)

        if action == "light":
            if target not in self.state["inventory"]:
                return _no(f"You don't have the {_name(target)}.")
            if self.state["lit"]:
                return _no(f"The {_name(target)} is already lit.")
            self.state["lit"] = True
            return _ok(action="light", item=target, lit=True)

        return _no("Nothing happens.")

    def inventory(self):
        facts = {"items": list(self.state["inventory"])}
        if CANDLE in self.state["inventory"]:
            facts["candle_lit"] = self.state["lit"]
        return _ok(**facts)
