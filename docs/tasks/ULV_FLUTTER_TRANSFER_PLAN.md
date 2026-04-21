# ULV Integration in Modular Runtime (Main Input/Output)

This plan outlines the integration of the **Unified Lesson View (ULV)** coordination into the existing **Modular Runtime**, leveraging the recently migrated Knowledge Lab Read Models and the stable Video Player.

## User Review Required

> [!IMPORTANT]
> **State Alignment**: This plan strictly extends the existing `ModularSession` and `ModularSessionState` found in `lib/features/study/presentation/providers/modular_runtime_provider.dart`. It does NOT introduce a parallel `UlvController`.
>
> **Contract Expansion**: We will expand `SupportSurfaceType` to include Knowledge Lab Read Models (`topicDetail`, `knowledgeDetail`, etc.).

## Proposed Changes

### [Component] Core Models & State

#### [MODIFY] [ulv_models.dart](file:///Users/ywchen/Dev/lingo/lingo-frontend-web/lib/features/study/domain/models/ulv_models.dart)
Expand the `SupportSurfaceType` enum to support Knowledge Lab detail Read Models.

```diff
 enum SupportSurfaceType {
   @JsonValue('grammar')
   grammar,
   @JsonValue('pattern')
   pattern,
   @JsonValue('usage')
   usage,
   @JsonValue('vocab')
   vocab,
+  @JsonValue('topic_detail')
+  topicDetail,
+  @JsonValue('knowledge_detail')
+  knowledgeDetail,
 }
```

#### [MODIFY] [modular_runtime_provider.dart](file:///Users/ywchen/Dev/lingo/lingo-frontend-web/lib/features/study/presentation/providers/modular_runtime_provider.dart)
The existing `modularSessionProvider` already supports `activePrimaryAnchor` and `activeSupportType`. No changes to the state molecule are required, but we will ensure the `setSupportType` method is used correctly for the new types.

---

### [Component] Primary Surface Adapters

#### [NEW] `UlvVideoRenderer` (lib/features/study/presentation/widgets/ulv/ulv_video_renderer.dart)
Create a wrapper for the existing `LingoVideoPlayer` that:
- Coordinates with `ModularSession` to set the `activePrimaryAnchor` based on playhead/subtitle selection.
- Allows triggering a `SupportSurfaceType` change when an interactive element (e.g., a "Explain" chip) is tapped.

---

### [Component] Support Surface Adapters

#### [NEW] `UlvKnowledgeDetailRenderer` (lib/features/study/presentation/widgets/ulv/ulv_knowledge_detail_renderer.dart)
A registry-based renderer that:
- Uses `LearningLibraryLookup` to fetch `TopicDetail` or `KnowledgeDetail` based on the `activePrimaryAnchor` (or a dedicated `activeSupportId` if we add one, otherwise we'll reuse `searchQuery` or `anchorId` for resolution).
- Renders the high-fidelity UI chunks derived from the Read Models (similar to sub-sections in `topic_detail_screen.dart`).

---

### [Component] Main Shell Integration

#### [MODIFY] [modular_lesson_runtime_screen.dart](file:///Users/ywchen/Dev/lingo/lingo-frontend-web/lib/features/study/presentation/screens/modular_lesson_runtime_screen.dart)
Update the `_NodeRenderer` and `_buildDrawerContent` to support the new forms and surfaces.

- **_NodeRenderer**: Add `case 'video'` to support the new `UlvVideoRenderer`.
- **_buildDrawerContent**: Add cases for the new Knowledge Lab support types to render `UlvKnowledgeDetailRenderer`.

---

## Open Questions

> [!IMPORTANT]
> **Anchor Resolution**: How should we resolve the specific ID (e.g., `T-KO-001`) for a support panel? Currently, `activePrimaryAnchor` is used for node-local IDs (like `turn_01`). We might need a separate field in `ModularSessionState` for `activeSupportId` (canonical global ID) to avoid overloading the anchor field. **Recommendation**: Reuse `searchQuery` temporarily or add `activeSupportId` string to `ModularSessionState`.

## Verification Plan

### Automated Tests
- `flutter test test/features/study/modular_runtime_test.dart` (ensure session state behaves correctly with new types).
- `flutter test test/features/study/ulv_video_renderer_test.dart` (mock interaction from video to support panel).

### Manual Verification
- Load a modular lesson node with `contentForm: "video"`.
- Click an interactive subtitle segment.
- Verify the Drawer opens (or can be opened) and renders the correct Knowledge Lab detail (e.g., Grammar explanation for that segment).
