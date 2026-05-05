# Library Reference Theme Token Plan

Date: 2026-05-05

## Goal

Define a light/dark-safe color token layer for the Library reference surfaces
before transferring Stitch mockups into Flutter.

The Library surfaces include:

- Knowledge Lab index/detail
- Sentence detail and sentence evidence surfaces
- Dictionary entry detail
- Video player learning overlay

## Source Of Truth

Stitch may propose a visual mood, but it is not the implementation contract.

Implementation authority is:

1. Flutter `ThemeData` / `ColorScheme`
2. Library-specific semantic tokens
3. Accessibility and dark-mode readability
4. Stitch visual direction

Do not copy Tailwind classes or Stitch-generated hex values directly into
widgets. Page widgets must not hardcode light-only values such as
`Colors.white`, `Colors.black`, `indigo.shade*`, or generated `surface-*`
values.

## Recommended Flutter Shape

Add a Library-specific theme extension instead of expanding the global
`SemanticColors` extension.

Recommended type:

```dart
class LibraryReferenceColors
    extends ThemeExtension<LibraryReferenceColors> {
  // surface, text, domain accent, evidence, and learning-state tokens.
}
```

Register it next to the existing `SemanticColors` extension in `AppTheme`.

Reason:

- Existing `SemanticColors` is app-wide and currently covers generic text and
  background overlays.
- Library reference screens need domain tokens for Knowledge, Sentences,
  Dictionary, Video, examples, tokens, and source evidence.
- Keeping these tokens separate prevents every app page from inheriting
  Library-specific color semantics.

## Required Token Families

### Surface Stack

| Token | Purpose |
| :--- | :--- |
| `canvas` | Page background. |
| `surface` | Normal cards and panels. |
| `surfaceRaised` | Elevated cards, sticky panels, active detail panes. |
| `surfaceInset` | Nested blocks such as examples, token rows, transcript lines. |
| `surfaceMuted` | Disabled or low-emphasis empty states. |
| `border` | Default border/divider. |
| `borderStrong` | Selected/focused border. |

### Text

| Token | Purpose |
| :--- | :--- |
| `textPrimary` | Main readable text. |
| `textSecondary` | Supporting explanation text. |
| `textMuted` | Metadata, counts, timestamps, secondary labels. |
| `textOnAccent` | Text on filled accent containers. |
| `targetText` | Target-language sentence/word/form. |
| `learnerText` | Learner-language translation/explanation. |
| `pronunciationText` | Optional pronunciation/romanization line. |

### Domain Accent

These colors identify evidence type, not page ownership. They must always be
paired with icon/label text so color is not the only indicator.

| Token | Purpose |
| :--- | :--- |
| `knowledgeAccent` | Grammar/usage/knowledge point. |
| `knowledgeContainer` | Filled Knowledge chip/card background. |
| `sentenceAccent` | Sentence evidence. |
| `sentenceContainer` | Filled Sentence chip/card background. |
| `dictionaryAccent` | Dictionary entry/sense/morphology evidence. |
| `dictionaryContainer` | Filled Dictionary chip/card background. |
| `videoAccent` | Video/source moment evidence. |
| `videoContainer` | Filled Video chip/card background. |

### Learning Interaction

| Token | Purpose |
| :--- | :--- |
| `selectedToken` | Selected atom/token highlight. |
| `selectedTokenBorder` | Selected atom/token outline. |
| `currentSubtitle` | Current subtitle focus background. |
| `loopRange` | Subtitle loop/replay range highlight. |
| `exampleSurface` | Inline examples and semantic example tables. |
| `missingSurface` | Missing localized content placeholder. |
| `warningSurface` | Recoverable artifact/content warning. |
| `successSurface` | Learned/verified/mastered state. |

## Initial Palette Direction

The current app theme is intentionally monochrome. Library reference surfaces
should keep that restraint, then add small, role-based accents:

| Role | Light Direction | Dark Direction | Notes |
| :--- | :--- | :--- | :--- |
| Base surfaces | warm off-white / soft gray | near-black / charcoal | Preserve the existing app identity. |
| Knowledge | ink blue | pale blue on dark container | Stable, reference-like, good for grammar. |
| Sentence | muted teal | soft aqua on dark container | Signals examples/evidence without looking like success. |
| Dictionary | muted amber/copper | warm sand on dark container | Distinguishes lexical detail from grammar. |
| Video | muted coral/rust | soft coral on dark container | Source moment / media evidence, not error red. |
| Missing/warning | app warning/error semantics | app warning/error semantics | Must use localized text, not raw fallback strings. |

Avoid a purple-heavy system. Purple can appear only if Stitch strongly improves
readability and the Flutter token review accepts it.

## Stitch Palette Review 2026-05-05

The Stitch-proposed Knowledge Lab palette is accepted as the base visual
direction, with semantic completion for Flutter.

Accepted directly:

- `surface-primary`: `#FCFCFD` / `#0F1115`
- `surface-secondary`: `#F4F4F7` / `#1A1D23`
- `text-target`: `#0A0C10` / `#F0F2F5`
- `text-learner`: `#3C434E` / `#A0A8B6`
- `text-muted`: `#646F7F` / `#717C8C`
- `evidence-knowledge`: `#2A4B8D` / `#6C91D9`
- `evidence-sentence`: `#3E5C6B` / `#7DA4B8`
- `evidence-dictionary`: `#505A6B` / `#8E99AA`
- `evidence-source`: `#1E3A8A` / `#3B82F6`
- `state-selected`: `#E0E7FF` / `#1E293B`
- `state-current`: `#DBEAFE` / `#1E3A8A`
- `border-divider`: `#E2E8F0` / `#2D3748`

Adapted for Flutter:

- Stitch did not provide container colors for Knowledge/Sentence/Dictionary/
  Video evidence chips. Flutter derives soft containers from the accepted
  accents.
- `evidence-source` maps to `videoAccent` / `videoContainer` until a separate
  Source role is needed.
- `status-missing`, `status-warning`, and `status-success` are used only as
  state surfaces. User-facing text must still come from localized UI strings.
- `evidence-dictionary` and `evidence-sentence` are intentionally low-saturation
  and somewhat close. UI must pair these colors with labels/icons; color alone
  is not an accepted differentiator.

Rejected:

- Treating Stitch token names such as `surface-primary` as Flutter widget API.
  Flutter keeps `LibraryReferenceColors` naming.
- Using this Knowledge Lab palette as raw page-local hex values.

## Accessibility Gates

Every implementation slice must verify:

- Body text contrast is at least WCAG 4.5:1.
- Icon/chip labels and large target text are at least WCAG 3:1.
- Dark mode does not place muted text on dark container without contrast.
- Filled accent chips include both icon/label and color.
- Selected tokens remain readable when nested inside cards, video overlays, and
  dictionary panels.
- Missing localized content uses localized placeholder copy and is visibly an
  app state, not content.

## Stitch Prompt For Color Exploration

Use Stitch for palette exploration only. Ask it for semantic tokens, not page
HTML.

```text
Design a light/dark semantic color system for a multilingual language-learning
reference library app.

Context:
- The app teaches many target languages to many learner UI languages.
- Current sample content is Korean with Traditional Chinese explanations, but
  the palette must not be Korean-specific.
- Surfaces include Knowledge Lab, Sentence detail, Dictionary entry detail, and
  Video player learning overlay.
- The app's base identity is restrained monochrome, not colorful gamification.

Output requirements:
- Do not output Tailwind classes.
- Do not output page layout HTML.
- Output a semantic token table with token name, purpose, light hex, dark hex,
  contrast target, and rationale.
- Include tokens for surfaces, text hierarchy, target-language text,
  learner-language text, knowledge evidence, sentence evidence, dictionary
  evidence, video/source evidence, selected token, current subtitle, missing
  content, warning, and success.
- Keep colors suitable for a serious educational product.
- Avoid relying on purple as the default accent.
- Ensure the palette works in both light and dark mode.
```

## Acceptance Rule

Stitch suggestions are accepted only after translating them into
`LibraryReferenceColors` and verifying real Flutter widgets in both light and
dark mode.
