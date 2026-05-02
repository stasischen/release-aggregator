import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
ASSEMBLER_PATH = REPO_ROOT / "scripts" / "prg" / "assembler_prototype.py"


spec = importlib.util.spec_from_file_location("assembler_prototype", ASSEMBLER_PATH)
assembler = importlib.util.module_from_spec(spec)
spec.loader.exec_module(assembler)


class PrgFrontendContractTest(unittest.TestCase):
    def test_planning_scan_outputs_frontend_required_manifest_and_catalog_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            candidate_root = root / "staging"
            dialogue_dir = candidate_root / "core" / "dialogue"
            dialogue_dir.mkdir(parents=True)
            (dialogue_dir / "ko_l1_dialogue_a1_01.json").write_text("{}", encoding="utf-8")

            release_manifest = root / "prd.release_manifest.json"
            release_manifest.write_text(
                json.dumps(
                    {
                        "entries": [
                            {
                                "unit_id": "a1_u01",
                                "lesson_id": "ko_l1_dialogue_a1_01",
                                "release_status": "production",
                                "content_type": "dialogue",
                                "course_type": "lesson",
                                "contract_version": "cm-v1.0.0",
                                "viewer_verified": True,
                                "qa_gate_passed": True,
                                "staging_only": False,
                                "source_refs": ["fixture:ko_l1_dialogue_a1_01"],
                                "lang": "ko",
                                "title": {"zh_tw": "第一課"},
                                "subtitle": {"zh_tw": "問候"},
                                "unit_title": {"zh_tw": "A1 單元 1"},
                                "unit_subtitle": {"zh_tw": "基礎問候"},
                                "unit_level": "A1",
                                "unit_order": 1,
                                "order_in_unit": 1,
                                "estimated_minutes": 7,
                                "theme_tags": ["greeting"],
                                "skill_tags": ["dialogue"],
                                "can_do": {"zh_tw": ["可以打招呼"]},
                                "knowledge_refs": ["ki:greeting"],
                                "key_sentence_preview": {"ko": "안녕하세요", "zh_tw": "你好"},
                                "status_flags": ["core"],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            out = root / "out"
            inventory = assembler.CandidateInventory.scan_directory(candidate_root)
            plan = assembler.assemble_release(
                release_manifest_path=release_manifest,
                candidate_inventory=inventory,
                output_dir=out,
                strict_mode=True,
                allow_unassigned_units=False,
                lang="ko",
                study_discovery_path="assets/content/production/lesson_catalog.json",
            )

            self.assertEqual(plan["summary"]["gap_count"], 0)

            manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["lang"], "ko")
            self.assertEqual(
                manifest["files"]["study_discovery"],
                "assets/content/production/lesson_catalog.json",
            )
            self.assertEqual(manifest["lessons"][0]["level_id"], "ko_l1_dialogue_a1_01")
            self.assertEqual(manifest["lessons"][0]["lesson_id"], "ko_l1_dialogue_a1_01")
            self.assertEqual(manifest["lessons"][0]["unit_id"], "a1_u01")

            catalog = json.loads((out / "lesson_catalog.json").read_text(encoding="utf-8"))
            lesson = catalog["lessons"][0]
            self.assertEqual(lesson["lesson_id"], "ko_l1_dialogue_a1_01")
            self.assertEqual(lesson["unit_id"], "a1_u01")
            self.assertEqual(lesson["can_do"], {"zh_tw": ["可以打招呼"]})
            self.assertEqual(lesson["knowledge_refs"], ["ki:greeting"])
            self.assertEqual(lesson["key_sentence_preview"]["ko"], "안녕하세요")

    def test_global_manifest_outputs_frontend_required_manifest_and_catalog_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            staged_file = root / "core" / "dialogue" / "ko_l1_dialogue_a1_01.json"
            staged_file.parent.mkdir(parents=True)
            staged_file.write_text("{}", encoding="utf-8")

            global_manifest = root / "global_manifest.json"
            global_manifest.write_text(
                json.dumps(
                    {
                        "version": "1.2.3",
                        "packages": [
                            {
                                "id": "ko_l1_dialogue_a1_01",
                                "version": "1.2.3",
                                "path": "core/dialogue/ko_l1_dialogue_a1_01.json",
                                "hash": "sha256:testhash",
                                "provenance": {
                                    "source_repo": "content-pipeline",
                                    "source_commit": "abc123",
                                    "pipeline_version": "pipeline-1",
                                    "schema_version": "1.0.0",
                                    "built_at": "2026-05-02T00:00:00+00:00",
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            release_manifest = root / "prd.release_manifest.json"
            release_manifest.write_text(
                json.dumps(
                    {
                        "entries": [
                            {
                                "unit_id": "a1_u01",
                                "lesson_id": "ko_l1_dialogue_a1_01",
                                "release_status": "production",
                                "content_type": "dialogue",
                                "course_type": "lesson",
                                "contract_version": "cm-v1.0.0",
                                "viewer_verified": True,
                                "qa_gate_passed": True,
                                "staging_only": False,
                                "source_refs": ["fixture:ko_l1_dialogue_a1_01"],
                                "lang": "ko",
                                "title": {"zh_tw": "第一課"},
                                "unit_title": {"zh_tw": "A1 單元 1"},
                                "unit_level": "A1",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            out = root / "out"
            inventory = assembler.CandidateInventory.load_from_global_manifest(global_manifest)
            assembler.assemble_release(
                release_manifest_path=release_manifest,
                candidate_inventory=inventory,
                output_dir=out,
                strict_mode=True,
                allow_unassigned_units=False,
                lang="ko",
                study_discovery_path="assets/content/production/lesson_catalog.json",
            )

            manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["lang"], "ko")
            self.assertEqual(manifest["files"]["study_discovery"], "assets/content/production/lesson_catalog.json")
            self.assertEqual(manifest["lessons"][0]["level_id"], "ko_l1_dialogue_a1_01")
            self.assertEqual(manifest["lessons"][0]["lesson_id"], "ko_l1_dialogue_a1_01")
            self.assertEqual(manifest["lessons"][0]["unit_id"], "a1_u01")


if __name__ == "__main__":
    unittest.main()
