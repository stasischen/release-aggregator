import json
import tempfile
import unittest
from pathlib import Path

from scripts import sync_frontend_assets


class FrontendAssetBridgeTests(unittest.TestCase):
    def test_dictionary_sync_requires_complete_runtime_package(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            worktree = root / "worktree"
            source.mkdir()
            self._write_package_manifest(worktree)

            with self.assertRaises(SystemExit) as raised:
                sync_frontend_assets.sync_dictionary_assets(worktree, source)

            self.assertIn("dictionary bridge source is incomplete", str(raised.exception))
            self.assertIn("dictionary_core.json", str(raised.exception))
            self.assertIn("Strings_zh_tw.json", str(raised.exception))
            self.assertIn("mapping_v2.json", str(raised.exception))

    def test_dictionary_sync_copies_assets_and_preserves_manifest_modules(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            worktree = root / "worktree"
            self._write_dictionary_source(source)
            self._write_package_manifest(worktree)

            sync_frontend_assets.sync_dictionary_assets(worktree, source)

            package_root = worktree / "assets/content/production/packages/ko"
            for rel_path in sync_frontend_assets.DICTIONARY_FILES:
                self.assertTrue((package_root / rel_path).is_file(), rel_path)

            manifest = self._read_json(package_root / "manifest.json")
            self.assertEqual(manifest["modules"]["dictionary"]["core"], "dictionary_core.json")
            self.assertEqual(
                manifest["modules"]["dictionary"]["i18n"],
                ["dict_ko_zh_tw.json", "Strings_zh_tw.json", "mapping.json", "mapping_v2.json"],
            )
            self.assertIn("video", manifest["modules"])
            self.assertNotEqual(manifest["updated_at"], "2026-05-03T00:00:00+00:00")

    def _write_dictionary_source(self, source: Path) -> None:
        for rel_path in sync_frontend_assets.DICTIONARY_FILES:
            self._write_json(source / rel_path, {"fixture": rel_path.name})

    def _write_package_manifest(self, worktree: Path) -> None:
        self._write_json(
            worktree / "assets/content/production/packages/ko/manifest.json",
            {
                "version": "5.0.0",
                "target": "ko",
                "learner_lang": "zh_tw",
                "modules": {
                    "dictionary": {
                        "core": "old_dictionary_core.json",
                        "i18n": ["old_dict.json"],
                    },
                    "video": {
                        "core": ["video.json"],
                        "i18n": {"zh_tw": ["video.json"]},
                    },
                },
                "updated_at": "2026-05-03T00:00:00+00:00",
            },
        )

    def _write_json(self, path: Path, payload: object) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def _read_json(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
