# Feature Specification: Keyhole

**Feature Branch**: `001-keyhole`
**Created**: 2026-10-12
**Status**: Approved

## User Scenarios & Testing

### User Story 1: Escape the house (Priority: P1)

The player talks to the Game Master and escapes by finding the keys in order.

**Acceptance Scenarios**:

1. **Given** a fresh game, **When** the player follows the chain (read the note, lift the rug, take the brass key, unlock the cellar door, light the candle, go down, take the iron key, go up, unlock the front door), **Then** the game is won and ends.
2. **Given** the game is won, **When** the player tries any further action, **Then** it is refused with "The game is over."

### User Story 2: The narrator cannot be talked around (Priority: P1)

The player tries to cheat, and the world holds.

**Acceptance Scenarios**:

1. **Given** the hall, **When** the player asks about a secret passage, **Then** the answer is no, because no such exit exists.
2. **Given** a locked door, **When** the player asks the Game Master to just unlock it, **Then** it is refused.
3. **Given** the cellar door is unlocked, **When** the player goes down without a lit candle, **Then** it is refused with "It is too dark to go down."

### User Story 3: Resume or restart (Priority: P2)

1. **Given** a game in progress, **When** the server restarts, **Then** play continues from the save file.
2. **Given** the save file is deleted, **When** the player looks around, **Then** a fresh game starts in the study.

### Edge Cases

- Taking a fixture (the rug) is always refused.
- Taking the brass key before the rug is lifted is refused, because it isn't visible yet.
- Using an item the player doesn't carry, using it on the wrong target, or on a target that isn't in this room, is refused.
- Lifting the rug twice reveals nothing more.

## Requirements

### Functional Requirements

- **FR-001**: The world MUST have four rooms: study (start), hall, kitchen and cellar.
- **FR-002**: Exits MUST be keyed by direction. Doors and locks MUST live on exits, not rooms.
- **FR-003**: The hall MUST have the cellar door (down, opened by the brass key) and the front door (out, opened by the iron key).
- **FR-004**: The cellar MUST be dark. Entering it MUST require carrying a lit candle.
- **FR-005**: The brass key MUST be hidden under the rug fixture until the rug is used.
- **FR-006**: `look()` MUST report the room description, visible items, fixtures, and exits with doors flagged locked or unlocked.
- **FR-007**: `move(direction)` MUST refuse missing exits, locked doors and dark destinations without light.
- **FR-008**: `take(item)` MUST accept only visible, takeable items.
- **FR-009**: `use(item, target?)` MUST support read, reveal, unlock and light, and refuse everything else plainly.
- **FR-010**: `inventory()` MUST report carried items and whether the candle is lit.
- **FR-011**: Unlocking the front door MUST win the game exactly once. Afterwards, every action except look and inventory MUST be refused.
- **FR-012**: State (room, inventory, taken, revealed, unlocked, lit, won) MUST persist in `state.json`. A missing file MUST mean a fresh game.
- **FR-013**: Tools MUST return facts or fixed refusals, never prose.
- **FR-014**: The Game Master MUST be able to call only the five keyhole tools, with no file, terminal or search access.
- **FR-015**: The Game Master MUST follow three hard rules: describe only tool output, no mercy, honest absence.

### Key Entities

- **Room**: description, items, optional fixtures, hidden items, a dark flag, and exits.
- **Exit**: destination, plus an optional door id and the key that unlocks it.
- **Item**: a takeable thing identified by id (note, brass-key, candle, matches, iron-key).
- **Fixture**: a non-takeable thing in a room (rug).
- **State**: the save file.

## Success Criteria

- **SC-001**: All engine tests pass with no AI and no server.
- **SC-002**: The demo (look, take the note, the secret-passage question, the unlock request, the full chain, the win) runs in three minutes or less.
- **SC-003**: In playtesting, every Game Master sentence traces to tool output.
