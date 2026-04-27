# Flutter Shell Contract for Unified Lesson View (ULV)

This document defines the technical contract for the `ModularLessonRuntimeShell` and its interaction with the ULV Runtime.

## 1. Screen Layout & Regions

The Shell MUST implement a responsive layout with the following regions:

### 1.1 Primary Content Region
- **Occupancy**: Takes the majority of the screen.
- **Responsibility**: Renders the `PrimarySurface` (Dialogue, Video, Article) or `ActivitySurface` (Practice, Review).
- **Flex**: Flexible height/width depending on orientation.

### 1.2 Support Detail Region
- **Modes**:
  - **Master-Detail (Wide)**: A side panel (e.g., right 30%) that stays visible alongside the Primary Region.
  - **Overlay (Narrow)**: A temporary surface (e.g., `endDrawer` or `BottomSheet`) that covers the screen when active.
- **Responsibility**: Renders supplemental panels (Grammar, Pattern, Usage, Vocab).

### 1.3 Navigation & Meta Region
- **Header**: Displays lesson title, progress indicator, and global actions (e.g., Search).
- **Footer**: Navigation controls (Previous/Next buttons).

## 2. Runtime Entry Points (Widget Interfaces)

### 2.1 Shell Interface
```dart
class ModularLessonRuntimeShell extends StatelessWidget {
  final String lessonId;
  final Widget primarySurface; // The active primary renderer
  final Widget? supportSurface; // The active support panel (if any)
  final bool isSupportPanelVisible;
  
  final Widget header;
  final Widget footer;
  final Widget navigationDrawer; // For quick node switching
  
  // Callbacks
  final VoidCallback onToggleSupport;
  final VoidCallback onCloseSupport;
}
```

### 2.2 Primary Adapter Contract
```dart
class UlvPrimarySurfaceAdapter extends StatelessWidget {
  final String contentForm;
  final dynamic payload;
  final String? activeAnchor;
  final Function(String anchorId) onAnchorSelected;
}
```

### 2.3 Support Adapter Contract
```dart
class UlvSupportSurfaceAdapter extends StatelessWidget {
  final SupportSurfaceType type;
  final String supportId;
  final dynamic payload;
}
```

## 3. Panel Allocation Rules

| Support Type | Allocation Priority | Renderer |
| :--- | :--- | :--- |
| **Grammar** | Support Region | `UlvGrammarRenderer` |
| **Pattern** | Support Region | `UlvPatternLabRenderer` |
| **Usage** | Support Region | `UlvUsageRenderer` |
| **Vocab** | Support Region | `UlvVocabRenderer` (Reserved) |
| **Search** | Support Region | `UlvSearchPanel` |

## 4. Interaction Flow

1.  **Anchor Selection**: User taps an element in `PrimarySurface` -> `onAnchorSelected(id)` is triggered.
2.  **State Update**: Runtime updates `activePrimaryAnchor` and automatically resolves/sets `activeSupportType` and `activeSupportId`.
3.  **Shell Rebuild**: Shell detects `isSupportPanelVisible` (based on `activeSupportType != null`) and updates the layout.
4.  **Automatic Scrolling**: If a support panel is already open, it SHOULD attempt to scroll to the relevant section for the new anchor.

## 5. Fail-Soft Policy

- If `contentForm` is unknown: Render `UlvFailSoftRenderer(payload: payload)`.
- If `supportType` data is missing: Render "No details available for this selection".

## 6. Manifest-Driven Loading (Batch D/E Integration)

The Shell and its adapters MUST support loading content based on the `manifest.json` or unified `modular_lessons.json` artifact structure:
- **Resource Resolution**: Media assets (videos, audio) must be resolved via the `StudyContentLocator` (as established in Batch E).
- **Dynamic Module Loading**: Support details (Grammar/Usage) should be loaded lazily based on the manifest entries for the current lesson node.
- **Fallbacks**: If a manifest entry points to a missing resource, the Fail-Soft policy (Section 5) applies.
