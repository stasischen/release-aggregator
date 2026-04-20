# STITCH_UI_PROTOTYPING - Grammar Lab & Shadowing

## Goal
Implement high-fidelity UI prototypes for the **Grammar Alchemy Lab** and **Teleprompter Shadowing Mode** using Google Stitch, and subsequently translate these into modularized Flutter widgets.

## User Review Required
> [!IMPORTANT]
> **Design Vibe**: The "Alchemy" theme implies a highly interactive "workbench" feel. Please confirm if we should lean heavily into the laboratory aesthetic (flasks, bubbling effects) or keep it more abstract and modern.

> [!IMPORTANT]
> **Shadowing Feedback**: Should the shadowing UI prioritize a scrolling teleprompter or a stationary block-based comparison view?

## Proposed Changes

### [Component] Stitch Prototyping (Web Phase)
#### [NEW] [grammar_alchemy_lab.html](file:///Users/ywchen/Dev/lingo/lingo-frontend-web/docs/stitch_designs/grammar_alchemy_lab.html)
- Generate via Stitch "Super Prompt".
- Features: Drag-and-drop slots for V5 Atoms (Stem, Suffix, Ending), result display, "bubbling" animations.

#### [NEW] [shadowing_mode.html](file:///Users/ywchen/Dev/lingo/lingo-frontend-web/docs/stitch_designs/shadowing_mode.html)
- Generate via Stitch "Super Prompt".
- Features: Scrollytelling teleprompter, Dual-Track Audio toggles, Recording interaction state.

### [Component] Flutter Implementation (lingo-frontend-web)
#### [NEW] `lib/features/study/presentation/grammar_alchemy/`
- `grammar_alchemy_screen.dart`: Main entry point.
- `widgets/atom_test_tube.dart`: Individual draggable atom component.
- `widgets/alchemy_workbench.dart`: Target drop zone.

#### [NEW] `lib/features/video/presentation/shadowing/`
- shadowing_screen.dart: Main entry point.
- widgets/teleprompter_view.dart: Scrolling text renderer.
- widgets/audio_controller_panel.dart: Controls for TTS and original audio.

## Open Questions
1. **Interaction Style**: For the Grammar Lab, should the "alchemy" effect be purely visual, or should it involve complex animations (e.g., atoms merging physically)?
2. **Data Integration**: Will these prototypes be initially powered by static mock data from assets/mocks/ or should I build them to consume the V5 Atom data models immediately?

## Verification Plan

### Automated Tests
- Widget tests for the new UI components in test/features/study/ and test/features/video/.
- Verify responsive layout using Flutter's LayoutBuilder.

### Manual Verification
- Visual inspection of the Stitch HTML output.
- Manual interaction testing in the Flutter web-build to ensure drag-and-drop smoothless and teleprompter scroll synchronization.
