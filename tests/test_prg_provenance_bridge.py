import importlib.util
import contextlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
ASSEMBLER_PATH = REPO_ROOT / "scripts" / "prg" / "assembler_prototype.py"


spec = importlib.util.spec_from_file_location("assembler_prototype", ASSEMBLER_PATH)
assembler = importlib.util.module_from_spec(spec)
spec.loader.exec_module(assembler)


def write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def release_entry(lesson_id="ko_l1_dialogue_a1_01"):
    return {
        "unit_id": "a1_u01",
        "lesson_id": lesson_id,
        "release_status": "production",
        "content_type": "dialogue",
        "course_type": "lesson",
        "contract_version": "cm-v1.0.0",
        "viewer_verified": True,
        "qa_gate_passed": True,
        "staging_only": False,
        "source_refs": [f"fixture:{lesson_id}"],
        "lang": "ko",
        "title": {"zh_tw": "第一課"},
        "unit_title": {"zh_tw": "A1 單元 1"},
        "unit_level": "A1",
    }


class PrgProvenanceBridgeTest(unittest.TestCase):
    def test_global_manifest_happy_path_and_provenance_carry_through(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            staged_file = root / "core" / "dialogue" / "ko_l1_dialogue_a1_01.json"
            staged_file.parent.mkdir(parents=True)
            staged_file.write_text("{}", encoding="utf-8")

            global_manifest = root / "global_manifest.json"
            provenance = {
                "source_repo": "content-pipeline",
                "source_commit": "abc123",
                "pipeline_version": "pipeline-1",
                "schema_version": "1.0.0",
                "built_at": "2026-05-02T00:00:00+00:00",
            }
            write_json(
                global_manifest,
                {
                    "version": "1.2.3",
                    "packages": [
                        {
                            "id": "ko_l1_dialogue_a1_01",
                            "version": "1.2.3",
                            "path": "core/dialogue/ko_l1_dialogue_a1_01.json",
                            "hash": "sha256:testhash",
                            "provenance": provenance,
                        }
                    ],
                },
            )
            release_manifest = root / "prd.release_manifest.json"
            write_json(release_manifest, {"entries": [release_entry()]})

            inventory = assembler.CandidateInventory.load_from_global_manifest(global_manifest)
            out = root / "out"
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
            artifact = plan["packaged_artifacts"][0]
            self.assertEqual(artifact["lesson_id"], "ko_l1_dialogue_a1_01")
            self.assertEqual(artifact["hash"], "sha256:testhash")
            self.assertEqual(artifact["provenance"], provenance)

            plan_json = json.loads((out / "production_plan.json").read_text(encoding="utf-8"))
            self.assertEqual(plan_json["packaged_artifacts"][0]["hash"], "sha256:testhash")
            self.assertEqual(plan_json["packaged_artifacts"][0]["provenance"]["source_commit"], "abc123")

    def test_missing_global_manifest_package_fails_in_strict_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            global_manifest = root / "global_manifest.json"
            write_json(global_manifest, {"version": "1.2.3", "packages": []})
            release_manifest = root / "prd.release_manifest.json"
            write_json(release_manifest, {"entries": [release_entry("missing_lesson")]})

            inventory = assembler.CandidateInventory.load_from_global_manifest(global_manifest)
            with contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaisesRegex(ValueError, "validation gaps"):
                    assembler.assemble_release(
                        release_manifest_path=release_manifest,
                        candidate_inventory=inventory,
                        output_dir=root / "out",
                        strict_mode=True,
                        allow_unassigned_units=False,
                        lang="ko",
                        study_discovery_path="assets/content/production/lesson_catalog.json",
                    )

    def test_cli_rejects_raw_directory_scan_in_strict_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            candidate_dir = root / "staging"
            candidate_dir.mkdir()
            release_manifest = root / "prd.release_manifest.json"
            write_json(release_manifest, {"entries": [release_entry()]})

            result = subprocess.run(
                [
                    sys.executable,
                    str(ASSEMBLER_PATH),
                    "--release-manifest",
                    str(release_manifest),
                    "--candidate-source",
                    str(candidate_dir),
                    "--output-dir",
                    str(root / "out"),
                ],
                capture_output=True,
                text=True,
                cwd=REPO_ROOT,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Strict production assembly requires a manifest source", result.stdout)

    def test_cli_rejects_legacy_manifest_in_strict_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            legacy_manifest = root / "manifest.json"
            write_json(legacy_manifest, {"lessons": [{"level_id": "ko_l1_dialogue_a1_01"}]})
            release_manifest = root / "prd.release_manifest.json"
            write_json(release_manifest, {"entries": [release_entry()]})

            result = subprocess.run(
                [
                    sys.executable,
                    str(ASSEMBLER_PATH),
                    "--release-manifest",
                    str(release_manifest),
                    "--candidate-source",
                    str(legacy_manifest),
                    "--output-dir",
                    str(root / "out"),
                ],
                capture_output=True,
                text=True,
                cwd=REPO_ROOT,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("requires Phase 1 global_manifest.json", result.stdout)


if __name__ == "__main__":
    unittest.main()
