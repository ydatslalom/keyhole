"""Keyhole MCP server: the five game tools over the engine.

stdio transport only: nothing listens on a port. Each call loads the save
file, acts and saves, so deleting state.json resets the game at any time.
"""

from pathlib import Path

from mcp.server.fastmcp import FastMCP

from keyhole.engine import Game

HERE = Path(__file__).parent
WORLD = HERE / "world.json"
STATE = HERE.parent / "state.json"

mcp = FastMCP("keyhole")


def _act(action):
    game = Game.load(WORLD, STATE)
    result = action(game)
    game.save(STATE)
    return result


@mcp.tool()
def look() -> dict:
    """Describe the current room as facts: its description, visible items,
    fixtures, and exits by direction, with doors flagged locked or unlocked.
    This is the only source of truth about what is here."""
    return _act(lambda game: game.look())


@mcp.tool()
def move(direction: str) -> dict:
    """Go through an exit of the current room. direction is an exit name
    exactly as look() reports it, such as "east", "down" or "out"."""
    return _act(lambda game: game.move(direction))


@mcp.tool()
def take(item: str) -> dict:
    """Pick up an item in the current room. item is an id exactly as look()
    reports it, such as "note" or "brass-key"."""
    return _act(lambda game: game.take(item))


@mcp.tool()
def use(item: str, target: str | None = None) -> dict:
    """Use a carried item, or a fixture in the current room. Reading and
    lifting need no target ("note", "rug"). Unlocking and lighting need one:
    a door id such as "cellar-door", or "candle"."""
    return _act(lambda game: game.use(item, target))


@mcp.tool()
def inventory() -> dict:
    """List what the player carries, and whether the candle is lit."""
    return _act(lambda game: game.inventory())


if __name__ == "__main__":
    mcp.run()  # stdio transport; never pass an HTTP/SSE transport or a port
