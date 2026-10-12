# Keyhole

A tiny locked-room game where you talk your way out and an AI Game Master narrates. The Game Master can't lie: it can only describe what the world engine reports, it can't invent exits or items, and it can't be talked into unlocking anything.

## How it works

- `keyhole/engine.py`: the world engine. Pure Python over `keyhole/world.json` and a `state.json` save file. It returns facts, never prose.
- `keyhole/server.py`: an MCP server (stdio only) exposing five tools: `look`, `move`, `take`, `use`, `inventory`.
- `.github/agents/game-master.agent.md`: the Game Master persona. It may call only the keyhole tools, and it has three hard rules: describe only what the tools say, no mercy, honest absence.

## Play

1. Open this repo in a GitHub Codespace. Dependencies install automatically.
2. Start the `keyhole` MCP server from `.vscode/mcp.json`.
3. In Copilot Chat, pick the Game Master agent and say "look around".

To start over, delete `state.json`.

## Test

```
pytest
```

The tests drive the engine directly, with no AI and no server. They show that locked doors stay locked, the dark cellar needs a lit candle, hidden items stay hidden until revealed, and the win fires exactly once.

## Course topics

| Topic | Where |
|---|---|
| GitHub Codespaces | `.devcontainer/`: runs entirely in the browser, zero setup |
| MCP | `keyhole/server.py`: the engine is the server; the GM is just the voice |
| Agents / personas | `.github/agents/game-master.agent.md`: a strict interpreter, not an improv troupe |
| Guardrails | enforced by the engine and proved by `tests/`; demoed live with "just unlock the door" |
| Speckit | `specs/`: world format, verbs, win condition and GM rules, written before code |
