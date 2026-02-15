# V5 Pipeline Checklists

## ✅ Phase 0: Pre-Flight Audit

Ensure the environment is clean and source files are valid before running expensive pipeline steps.

- [ ] **Git Status Clean**
  - _Description_: Run `git status` to ensure no uncommitted changes exist.
  - _Why_: Prevents accidental inclusion of work-in-progress files and makes rollback easier.
- [ ] **Yarn Source Validation**
  - _Check_: Run `python -m tools.v4 validate yarn {lang}`.
  - _Success_: Output returns "No errors found".
  - _Why_: Catches syntax errors (missing brackets, broken IDs) that would crash the parser later.
- [ ] **Dependency Check**
  - _Check_: Run `flutter pub get`.
  - _Why_: Ensures the Dart/Flutter environment is ready for the final build step.

## ✅ Phase 1: Sync & Update

This is the "Ingestion" phase where source content is read into the database.

- [ ] **Execute Update DB**
  - _Command_: `python -m tools.v5.core.update_db {lang}`.
  - _Success_: Script completes with exit code 0.
  - _Why_: Parses `.yarn` files, creates/updates Atom structure in `2_atoms`, and initializes `1_translation` using Translation Memory.
- [ ] **Check Logs for Warnings**
  - _Check_: unexpected warnings such as "ID mismatch" or "Encoding error".
  - _Why_: Early warning of data corruption.
- [ ] **Verify Atom CSVs**
  - _Check_: `content/2_atoms/{lang}/.../*.csv` modified timestamps updated.
  - _Why_: Confirms the structure was actually parsed.

## ✅ Phase 2: Merger & Preview

This phase combines structure and content into a human-readable format.

- [ ] **Execute Merger**
  - _Command_: `python -m tools.v5.core.merger {lang}`.
  - _Success_: Output files generated in `5_full_view`.
  - _Why_: Creates the "Product" that will actually be used for building assets.
- [ ] **Check Output Alignment**
  - _Check_: Open a generated CSV in `5_full_view`. Verify `text` and `translation` columns align correctly.
  - _Why_: If rows are misaligned strings will appear in the wrong order or language.
- [ ] **Line Count Verification**
  - _Check_: Roughly compare line count of CSV vs Yarn source.
  - _Why_: Detects if the parser skipped a block of dialogue entirely.

## ✅ Phase 3: Dictionary Sync & Repair

This phase manages the global dictionary.

- [ ] **Execute Extraction**
  - _Command_: `python -m tools.v5.core.extract {lang}`.
  - _Why_: Identifies all unique words/phrases used in the new content.
- [ ] **Execute Sync**
  - _Command_: `python -m tools.v5.core.sync {lang}`.
  - _Why_: Updates the dictionary CSVs in `4_dictionary/` with any new missing terms.
- [ ] **AI Repair ([TODO] Check)**
  - _Check_: Run `tools.v5.repair.batch_translate_v5` if dictionary has empty `[TODO]` slots.
  - _Why_: Ensures there are no undefined terms in the app.
- [ ] **Manual Quality Spot Check**
  - _Check_: Read 5-10 random dictionary entries for context accuracy.
  - _Why_: AI can make context errors (e.g. "Bank" as river vs money).

## ✅ Phase 4: Build & Finalize

This phase compiles the assets for the App.

- [ ] **Build JSON Assets**
  - _Command_: `python -m tools.v4 build {lang}`.
  - _Why_: Converts CSVs into the efficient JSON format loaded by Flutter.
- [ ] **Finalize Manifest**
  - _Command_: `python -m tools.v4 finalize {lang} --force`.
  - _Why_: Updates the `AssetManifest.json` and registry files so the App knows these files exist.
- [ ] **Deploy to App**
  - _Command_: `python -m tools.v4.core.deploy {lang}`.
  - _Why_: Moves the built assets into the actual Flutter project `assets/` folder.
- [ ] **In-App Verification**
  - _Check_: Launch the App and play the new content.
  - _Why_: Final confirmation that everything works end-to-end.
