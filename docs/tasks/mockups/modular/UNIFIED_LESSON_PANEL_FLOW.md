# Unified Lesson Panel Flow

This document defines the interaction rules and coordination between the **Primary Surface** and the **Support Detail Panel** in the ULV runtime.

## 1. Node & Panel Coordination

The ULV runtime tracks two distinct levels of navigation:

### 1.1 `currentIndex` (The Horizontal Flow)
- Moving to a new node via "Next" or "Back".
- **Rule**: Changing `currentIndex` resets the `activePrimaryAnchor` (e.g., sentence selection).
- **Rule**: If the `activeSupportPanel` was open, it should **remain open** and attempt to load data for the new `currentIndex`. If no data exists for the current type in the new node, show the "No additional details" message.

### 1.2 `activeSupportType` (The Vertical Depth)
- Toggling between `grammar`, `pattern`, `usage`, or `vocab`.
- **Rule**: Selecting a type updates the `activeSupportType` runtime state.
- **Rule**: Closing the panel clears the `activeSupportType`.

---

## 2. Support Context Anchor

The `support_context_anchor` is a runtime state used to coordinate the two surfaces.

- **Trigger**: Selecting an interactive element in the **Primary Surface** (e.g., Sentence 2 in a Dialogue).
- **Effect**: Updates `activePrimaryAnchor`.
- **Panel sync**: If the **Support Detail Panel** is open, it may use the anchor to auto-scroll or filter its content (e.g., highlighting a specific Grammar Point related to Sentence 2).
- **Boundary**: This mapping is a runtime lookup (interaction contract) and does **not** require a hard-coded anchor graph in the upstream payload.

---

## 3. State Persistence Rules

We distinguish between temporary UI state and persistent learner input.

| State Tier | Persistence | Example |
| :--- | :--- | :--- |
| **Ephemeral** | Cleared on any navigation | Scroll positions, hover highlights, playback progress. |
| **Node-Scoped** | Persistent for current node | **Pattern Lab selections**, expanded/collapsed specific sections. |
| **Session-Scoped** | Persistent across lesson | **Bilingual visibility** (`prefs.showTranslation`), teaching locale. |

---

## 4. UI Behaviors

### 4.1 Back / Forward Navigation
- Triggers a change in `currentIndex`.
- If the target node has a different `primaryContentSurface` (e.g., Dialogue -> Article), the transition should ensure the primary surface is fully cleared and re-initialized.

### 4.2 Panel Close / Reopen
- If the learner closes the Support Panel, then re-opens it on the **same node**, the panel should default to the last `activeSupportType`.
- Closing the panel does **not** clear the `activePrimaryAnchor` (the primary highlight remains).

### 4.3 Primary Surface Switch
- When a node transition involves a primary surface switch (e.g., `dialogue` to `video`), the **Support Panel** remains open.
- The runtime must ensure that the `activePrimaryAnchor` is invalidated to prevent "Sentence 3" from being highlighted in a "Video" surface skip.
