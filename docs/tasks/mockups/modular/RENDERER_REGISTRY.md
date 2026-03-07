# Renderer Registry Contract & Fallback Strategy

This document defines the contract for content rendering in the modular mockup system, ensuring consistent behavior between the current HTML prototype and future Flutter implementations.

## 1. Registry Mechanism

Renderers are managed by `window.RendererRegistry`, which supports three types of registration:

- **Content Renderers**: Handles the primary visual representation based on `content_form`.
- **Interaction Renderers**: Handles user input and logic based on `output_mode`.
- **Combined Renderers**: Handles special cases where a specific form-mode combination requires integrated logic.

### Dispatch Keys
- Primary Key: `content_form`
- Secondary Key: `output_mode`
- Combined Key (Priority): `${content_form}:${output_mode}`

## 2. Dispatch Flow

1. **Combined Check**: Check if a combined renderer exists for `${content_form}:${output_mode}`.
2. **Sequential Load**:
   - Dispatch `content_form` to its registered renderer.
   - Dispatch `output_mode` to its registered renderer (if mode is not `none` or `unknown`).
3. **Fallback Injection**: If any part of the chain is missing, inject the appropriate fallback UI.

## 3. Fallback Strategies

| Scenario | Behavior | Visual Cue |
| :--- | :--- | :--- |
| **Unknown `content_form`** | Renders an Error Panel with raw data preview. | Yellow border, "Warning" icon. |
| **Unsupported `output_mode`** | Renders a "Coming Soon" or "Not Supported" placeholder. | Dashed border, "Info" icon. |
| **Malformed Payload** | Renders an error box highlighting missing mandatory fields. | Red border, "Error" icon. |
| **Unexpected Crash** | Trapped in `dispatch` try-catch (if implemented) or top-level shell. | Standard error screen. |

## 4. Adapter-Safe Payload Requirements

To ensure renderers function correctly, payloads must adhere to the following field naming:

- **Dialogue**: `dialogue_turns` (Array of `{speaker, text, zh_tw}`).
- **Notice**: `notice_items` (Array), `notice_items_zh_tw` (Array).
- **Practice Cards**: `tasks` or `items` (Array), `prompt_zh_tw`.
- **Glossary/Dictionary**: `item_gloss_by_ko` (Object/Map).

## 5. Future Alignment (Flutter)

The Flutter `ContentAdapter` should mirror this registry logic:
- A `RendererFactory` will map JSON strings to Dart Widget builders.
- Fallback widgets must be provided for every abstract `BaseContent` class.
- The `adapter_hints` field in the blueprint should be used to override or steer specific renderer selections if needed.

## 6. Pattern Builder I18n Contract

For `pattern_lab` / pattern-builder style payloads, i18n must be contract-driven rather than locale-by-locale patching.

- `register_templates` define the Korean surface sentence.
- `translation_templates` define locale-specific gloss output.
- If a control changes sentence meaning in one locale, the same semantic switch must be reflected in every locale gloss.
- Locale gloss templates must reuse the same dynamic tokens rather than hard-coding one language's default wording.
- Example: if Korean switches on `{demo_base}` (`이/그/저`), then `zh_tw` and `en` gloss templates must also include `{demo_base}` or an equivalent semantic token.
- English glosses must be complete surface strings, including articles where needed (`a book`, `an apple`, `a phone`).
- Mixed-language labels such as `앞말 / front part / 문체` are not allowed in final mockups; control labels must be fully localized.
- Unresolved template tokens such as `{translation}` or `{demo_base}` are considered contract failures.

### QA Gate

Before a mockup fixture is considered stable:

- no unresolved `{token}` placeholders may remain in sentence or gloss output
- `zh_tw` and `en` must both reflect the same control-driven switches
- gloss text must read as natural learner-facing copy, not raw schema fragments or partial translations
