# Tasks: Keyhole

**Input**: [spec.md](spec.md), [plan.md](plan.md)

## Phase 1: Setup

- [ ] T001 Devcontainer, `requirements.txt`, `pyproject.toml`, `.gitignore`
- [ ] T002 `.vscode/mcp.json` launching `python -m keyhole.server` over stdio

## Phase 2: World

- [ ] T003 `keyhole/world.json`: four rooms, five items, the rug fixture, two doors, uses table, win (FR-001 to FR-005)

## Phase 3: Engine and tests (US1, US2, US3)

- [ ] T004 `Game` load, save and fresh state (FR-012)
- [ ] T005 `look` and `inventory` (FR-006, FR-010)
- [ ] T006 `move`, with lock and dark checks (FR-007, FR-004)
- [ ] T007 `take`, with visibility and fixtures (FR-008, FR-005)
- [ ] T008 `use`: read, reveal, unlock, light, win (FR-009, FR-011)
- [ ] T009 `tests/test_engine.py`: golden path, every refusal, win once, save round-trip (SC-001)

## Phase 4: Server

- [ ] T010 `keyhole/server.py`: five FastMCP tools, stdio only (FR-013)

## Phase 5: Game Master

- [ ] T011 `.github/agents/game-master.agent.md`: tool scope and three hard rules (FR-014, FR-015)
- [ ] T012 Playtest: golden path plus the cheat attempts (SC-003)

## Phase 6: Polish

- [ ] T013 README
- [ ] T014 Demo rehearsal in a cold Codespace (SC-002)
