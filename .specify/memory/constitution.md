# Keyhole Constitution

Keyhole is a tiny locked-room text game with an AI Game Master that cannot lie.

## Core Principles

### I. The engine is the only authority
All world facts come from `world.json` and `state.json` through the engine. Nothing else, including the Game Master, may assert what exists.

### II. Facts, not prose
The engine and the MCP tools return structured facts or a short, fixed refusal string. They never return narration.

### III. Describe only what the tools say
The Game Master narrates tool output and nothing more: no new rooms, exits, items, sounds or clues.

### IV. No mercy
Locks need their keys and darkness needs light. No request, plea or role-play changes that, and the Game Master never calls a tool the player didn't ask for.

### V. Honest absence
If the world doesn't contain something, the answer is no. Nothing is implied to exist just to be kind.

### VI. Minimal footprint
Pure Python standard library plus the `mcp` package. No shell, no subprocess, no network, stdio MCP transport only, no ports, no secrets, no repo automation.

### VII. Guardrails are proved by tests
Every guardrail has an engine test that runs without AI and without the server.

### VIII. Small on purpose
Four rooms, five items, five tools. New features need a reason tied to the course topics.

## Governance

This constitution overrides the spec, plan and tasks. A change to a principle needs a matching change to the tests.

**Version**: 1.0.0 | **Ratified**: 2026-10-12 | **Last Amended**: 2026-10-12
