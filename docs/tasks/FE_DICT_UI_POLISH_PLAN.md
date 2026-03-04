# Plan: Dictionary UI Polish - Prefix Stripping and I18N POS

This plan addresses the issue where dictionary entries show technical prefixes (e.g., `ko:adj:`) and POS tags are not translated.

## Proposed Changes

### [lingo-frontend-web](file:///Users/ywchen/Dev/lingo/lingo-frontend-web)

#### [MODIFY] [dictionary_formatter.dart](file:///Users/ywchen/Dev/lingo/lingo-frontend-web/lib/core/services/dictionary/dictionary_formatter.dart)
- Update `_buildComponentEntry` to strip prefixes like `ko:pos:` from the `term` before returning.
- Add a helper method or logic to handle POS translation if possible, or ensure `pos` is passed cleanly to the UI.

#### [MODIFY] [ui_strings.dart](file:///Users/ywchen/Dev/lingo/lingo-frontend-web/lib/core/i18n/ui_strings.dart)
- [NEW] Add `DictionaryStrings` to the `UiStrings` class.
- Define common POS tags in `DictionaryStrings`.

#### [MODIFY] [ui_strings_zh-TW.json](file:///Users/ywchen/Dev/lingo/lingo-frontend-web/assets/config/ui_strings_zh-TW.json)
- [NEW] Add `dictionary` section with translated POS tags (e.g., `n: "名詞"`, `v: "動詞"`).

#### [MODIFY] [ui_strings_en.json](file:///Users/ywchen/Dev/lingo/lingo-frontend-web/assets/config/ui_strings_en.json)
- [NEW] Add `dictionary` section with POS tags (e.g., `n: "Noun"`, `v: "Verb"`).

#### [MODIFY] [dictionary_content.dart](file:///Users/ywchen/Dev/lingo/lingo-frontend-web/lib/features/dictionary/presentation/widgets/dictionary_content.dart)
- Update the POS display logic to use `UiStrings.dictionary` for translation.

## Verification Plan

### Manual Verification
- View a dictionary entry with a prefix (e.g., `ko:adj:apple`) and verify it shows as `apple`.
- Verify the POS tag is translated according to the UI language (e.g., `(形容詞)` in Chinese).
