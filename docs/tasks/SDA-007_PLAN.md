# SDA-007: Frontend Dictionary Structure Upgrade Plan

## Goal
Upgrade `lingo-frontend-web` to support the new structured dictionary data (Entry + Sense) while removing reliance on deprecated flat fields (`translation`, `meaning`).

## Proposed Changes

### [MODIFY] [dictionary_contract_models.dart](file:///Users/ywchen/Dev/lingo/lingo-frontend-web/lib/core/services/dictionary/dictionary_contract_models.dart)
- Add `DictionarySense` class:
  ```dart
  class DictionarySense {
    final String? senseId;
    final int? entryNo;
    final int? senseNo;
    final String gloss;
    final String? notes;

    const DictionarySense({
      this.senseId,
      this.entryNo,
      this.senseNo,
      required this.gloss,
      this.notes,
    });

    factory DictionarySense.fromMap(Map<String, dynamic> map) {
      return DictionarySense(
        senseId: map['sense_id']?.toString(),
        entryNo: map['entry_no'] as int?,
        senseNo: map['sense_no'] as int?,
        gloss: map['gloss']?.toString() ?? '',
        notes: map['notes']?.toString(),
      );
    }
  }
  ```
- Update `DictionaryInventoryEntry` to include `List<DictionarySense> senses`.

### [MODIFY] [dictionary_parser.dart](file:///Users/ywchen/Dev/lingo/lingo-frontend-web/lib/core/utils/dictionary_parser.dart)
- **`extractMeaning`**:
  - Exclusively use `definitions[locale]` map.
  - Iterate through entries, extract `gloss`, and join with ` / `.
  - **Hard Break**: Remove fallbacks to `translation`, `meanings`, `translations`, `senses` (legacy list), and root `meaning`.
- **`extractSenses`**:
  - Return `List<DictionarySense>` instead of `List<dynamic>`.
  - Parse `definitions[locale]` into `DictionarySense` objects.

### [MODIFY] [dictionary_meaning_section.dart](file:///Users/ywchen/Dev/lingo/lingo-frontend-web/lib/features/dictionary/presentation/widgets/dictionary_meaning_section.dart)
- Update `DictionaryMeaningSection` to accept `List<DictionarySense> senses`.
- Logic for rendering:
  - If multiple `entry_no` exist, show them as distinct groups (e.g., "1. ...", "2. ...").
  - Within each entry, if multiple senses exist, show them with sub-numbering (e.g., "①", "②").
  - Use `gloss` for the main text.

## Verification Plan

### Automated Tests
- Rely on manual verification of dictionary overlay with real data.

### Manual Verification
- Use `assets/content/production/packages/ko/i18n/dict_ko_zh_tw.json` as the data source.
- Verify Dictionary Overlay for words like `있다` (simple), `같다` (multiple senses), and words with multiple `entry_no`.
- Check console for any parsing errors.

## User Review Required
> [!IMPORTANT]
> This is a **Hard Break**. Older dictionary files without the `definitions` field will no longer display meanings correctly.
