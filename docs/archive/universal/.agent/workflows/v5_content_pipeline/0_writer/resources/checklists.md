# Phase 0 Writer Checklists

## 🟢 Yarn Dialogue Check

- [ ] **Target Language Only**: Ensure the main dialogue block contains NO English or other source languages.
- [ ] **No Inline Tags**: Ensure `#mood` or `#grammar` tags are ONLY in the bottom mirror block.
- [ ] **Line IDs Preserved**: Every line has a unique `#line:ID`.
- [ ] **Mirror Sync**: Verify the bottom English block has the exact same number of lines and IDs as the top block.

## 🔵 Article Markdown Check

- [ ] **Plain Text**: Confirm no markdown formatting (`**`, `__`, `[]`) is used in the body.
- [ ] **Paragraph Separation**: Check that paragraphs are separated by at least one empty line.
- [ ] **Segmentation (Space)**: (For TH/CJK only) Confirm words are separated by spaces.
- [ ] **English Separation**: English reference is strictly below the `---` separator at the bottom.

## 🟣 Language Style Check

- [ ] **KO**: Ends in `-다` (Plain form), not `-요`.
- [ ] **DE**: Uses Präteritum for narrative past tense.
- [ ] **TH**: No spoken particles (`krub/ka`) in narrative.
