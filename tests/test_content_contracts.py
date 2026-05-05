import json
import tempfile
import unittest
from pathlib import Path

from scripts import validate_content_contracts


class ContentContractTests(unittest.TestCase):
    def test_learning_library_manifest_accepts_current_v1_layout(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = self._write_learning_library_package(root)

            errors = validate_content_contracts.validate_learning_library_manifest(
                manifest,
                require_locale="zh_tw",
                min_sentence_translations=2,
            )

            self.assertEqual(errors, [])

    def test_learning_library_manifest_rejects_deprecated_aliases(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = self._write_learning_library_package(root)
            payload = self._read_json(manifest)
            payload["files"]["core"] = ["sources_index.json", "sentences_index.json"]
            self._write_json(manifest, payload)

            errors = validate_content_contracts.validate_learning_library_manifest(manifest)

            self.assertTrue(any("deprecated aliases: sentences_index.json" in error for error in errors), errors)
            self.assertTrue(any("missing required files" in error for error in errors), errors)

    def test_learning_library_manifest_rejects_missing_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = self._write_learning_library_package(root)
            (root / "core" / "links.json").unlink()

            errors = validate_content_contracts.validate_learning_library_manifest(manifest)

            self.assertIn("files.core references missing artifact: core/links.json", errors)

    def test_package_manifest_rejects_learning_library_alias_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package_manifest = root / "packages" / "manifest.json"
            self._write_json(
                package_manifest,
                {
                    "version": "5.0.0",
                    "target": "ko",
                    "learner_lang": "zh_tw",
                    "modules": {
                        "learning_library": {
                            "core": ["../artifacts/ko/core/sentences_index.json"],
                            "i18n": [],
                        }
                    },
                },
            )

            errors = validate_content_contracts.validate_package_manifest(package_manifest)

            self.assertTrue(
                any(
                    "references deprecated alias: ../artifacts/ko/core/sentences_index.json" in error
                    for error in errors
                ),
                errors,
            )

    def _write_learning_library_package(self, root: Path) -> Path:
        manifest = root / "library_manifest.json"
        self._write_json(
            manifest,
            {
                "lang": "ko",
                "version": "pipeline-v2",
                "modules": ["core", "i18n"],
                "files": {
                    "core": validate_content_contracts.LL_CORE_FILES,
                    "i18n": {
                        "zh_tw": validate_content_contracts.LL_I18N_FILES,
                    },
                },
            },
        )
        for filename in validate_content_contracts.LL_CORE_FILES:
            self._write_json(root / "core" / filename, {"index": {}})
        for filename in validate_content_contracts.LL_I18N_FILES:
            payload = {"index": {}}
            if filename == "sentences.json":
                payload = {
                    "index": {
                        "shared_bank": {
                            "sentences": [
                                {"id": "ex.ko.s.000001", "translation": "你好。"},
                                {"id": "ex.ko.s.000002", "translation": "謝謝。"},
                            ]
                        }
                    }
                }
            self._write_json(root / "i18n" / "zh_tw" / filename, payload)
        return manifest

    def _write_json(self, path: Path, payload: object) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def _read_json(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
