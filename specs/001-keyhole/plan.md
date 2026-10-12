# Implementation Plan: Keyhole

**Branch**: `001-keyhole` | **Date**: 2026-10-12 | **Spec**: [spec.md](spec.md)

## Summary

A pure-Python world engine behind a stdio MCP server with five tools, narrated by a tool-scoped Game Master persona, running in a GitHub Codespace.

## Technical Context

- **Language/Version**: Python 3.12
- **Primary Dependencies**: `mcp` 2.x (`MCPServer`), `pytest`, both pinned
- **Storage**: `keyhole/world.json` (read-only) and `state.json` (save file, git-ignored)
- **Testing**: pytest against the engine only
- **Target Platform**: GitHub Codespace (`mcr.microsoft.com/devcontainers/python:3.12`)
- **Constraints**: stdio transport only, no ports; imports limited to `json`, `pathlib` and `mcp`

## Constitution Check

| Principle | How the design satisfies it |
|---|---|
| I. Engine is the only authority | Every tool loads world and state through `Game`; the persona has no other tools |
| II. Facts, not prose | Every method returns `{"ok": ...}` dicts |
| III–V. GM rules | The persona file states them; the engine enforces locks, light and visibility |
| VI. Minimal footprint | Standard library plus `mcp`; `mcp.run(transport="stdio")` |
| VII. Tests | `tests/test_engine.py` covers every refusal and the win |
| VIII. Small | Four rooms, five items, five tools |

## Project Structure

```
keyhole/
  engine.py      # Game: rules, load and save; no MCP import
  server.py      # MCPServer "keyhole": five tools, each loads, acts and saves
  world.json
tests/
  test_engine.py
.github/agents/game-master.agent.md
.devcontainer/devcontainer.json
.vscode/mcp.json
pyproject.toml
requirements.txt
```

## Design Notes

- **Visible items** = room items, plus items under revealed fixtures, minus taken items.
- **Validation order** in each verb: game over, then existence, then lock, then light. The first failure wins.
- **Per-call load and save** makes `state.json` the single source of truth, so deleting it resets the game.
