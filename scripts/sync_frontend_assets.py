#!/usr/bin/env python3
"""Orchestrate the current stable frontend asset sync bridge.

This script intentionally wires only generators that are currently safe to run
against the frontend repo. Dictionary and learning-library regeneration remain
validated by the frontend asset gate, but are not overwritten here until their
candidate exporters are promoted. This is a bridge for the current asset flow;
the long-term release path should move these writes behind PRG.
"""

from __future__ import annotations

import argparse
import copy
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
RELEASE_AGGREGATOR_ROOT = SCRIPT_DIR.parent
LINGO_ROOT = RELEASE_AGGREGATOR_ROOT.parent
DEFAULT_STAGING_ROOT = RELEASE_AGGREGATOR_ROOT / "staging" / "frontend_asset_bridge"

PRODUCTION_REL = Path("assets/content/production")
GRAMMAR_REL = Path("assets/content/grammar")
VIDEO_METADATA_REL = Path("assets/config/video_metadata.json")
VIDEO_CORE_REL = Path("assets/content/production/packages/ko/video/core")
PACKAGE_MANIFEST_REL = Path("assets/content/production/packages/ko/manifest.json")
PRODUCTION_MANIFEST_REL = Path("assets/content/production/manifest.json")


def run(command: list[str], cwd: Path) -> None:
    printable = " ".join(command)
    print(f"\n$ {printable}\n  cwd={cwd}", flush=True)
    subprocess.run(command, cwd=cwd, check=True)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def existing_dir(path: Path, label: str) -> Path:
    resolved = path.resolve()
    if not resolved.is_dir():
        raise SystemExit(f"{label} not found: {resolved}")
    return resolved


def copy_tree(source: Path, target: Path) -> None:
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(source, target)


def copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def prepare_worktree(frontend_repo: Path, staging_root: Path) -> Path:
    worktree = staging_root / "worktree"
    if worktree.exists():
        shutil.rmtree(worktree)

    for rel_path in [PRODUCTION_REL, GRAMMAR_REL]:
        copy_tree(frontend_repo / rel_path, worktree / rel_path)
    copy_file(frontend_repo / VIDEO_METADATA_REL, worktree / VIDEO_METADATA_REL)
    return worktree


def list_video_files(worktree: Path) -> list[Path]:
    video_core_dir = worktree / VIDEO_CORE_REL
    if not video_core_dir.exists():
        return []
    return sorted([path for path in video_core_dir.glob("*.json") if path.is_file()])


def update_package_manifest(worktree: Path, video_files: list[Path], langs: list[str]) -> None:
    manifest_path = worktree / PACKAGE_MANIFEST_REL
    manifest = read_json(manifest_path) if manifest_path.exists() else {"lang": "ko", "modules": [], "files": {}}
    original_manifest = copy.deepcopy(manifest)
    existing_updated_at = manifest.get("updated_at")
    video_filenames = sorted(file.name for file in video_files)

    modules = manifest.get("modules")
    if isinstance(modules, dict):
        video_module = modules.get("video") or {}
        video_module["core"] = video_filenames
        video_module["i18n"] = {lang: video_filenames for lang in langs}
        modules["video"] = video_module
        manifest["modules"] = modules
    else:
        module_list = list(modules or [])
        if "video" not in module_list:
            module_list.append("video")
        manifest["modules"] = module_list
        manifest["files"] = manifest.get("files") or {}
        manifest["files"]["video"] = video_filenames

    original_without_timestamp = copy.deepcopy(original_manifest)
    original_without_timestamp.pop("updated_at", None)
    next_without_timestamp = copy.deepcopy(manifest)
    next_without_timestamp.pop("updated_at", None)
    if original_without_timestamp != next_without_timestamp:
        manifest["updated_at"] = utc_now()
    elif existing_updated_at is not None:
        manifest["updated_at"] = existing_updated_at
    write_json(manifest_path, manifest)


def build_video_lesson_entry(file: Path) -> dict[str, Any]:
    payload = read_json(file)
    metadata = payload.get("metadata", {})
    title = metadata.get("title", file.stem)
    return {
        "level_id": file.stem,
        "lesson_id": file.stem,
        "unit_id": "video_library",
        "path": f"assets/content/production/packages/ko/video/core/{file.name}",
        "lang": "ko",
        "type": "video",
        "category": "lesson",
        "title": {
            "ko": title,
            "zh_tw": title,
            "en": title,
        },
    }


def update_production_manifest(worktree: Path, video_files: list[Path]) -> None:
    manifest_path = worktree / PRODUCTION_MANIFEST_REL
    manifest = read_json(manifest_path)
    original_manifest = copy.deepcopy(manifest)
    existing_last_updated = manifest.get("last_updated")
    existing_package_updated = (manifest.get("packages") or {}).get("ko", {}).get("updated")
    lessons = manifest.get("lessons") or []
    non_video_lessons = [lesson for lesson in lessons if lesson.get("type") != "video"]
    manifest["lessons"] = non_video_lessons + [build_video_lesson_entry(file) for file in video_files]
    packages = manifest.get("packages") or {}
    ko_pkg = packages.get("ko") or {}
    packages["ko"] = ko_pkg
    manifest["packages"] = packages
    files = manifest.get("files") or {}
    files.setdefault("study_discovery", "assets/content/production/lesson_catalog.json")
    manifest["files"] = files

    original_without_timestamps = copy.deepcopy(original_manifest)
    original_without_timestamps.pop("last_updated", None)
    if "packages" in original_without_timestamps and "ko" in original_without_timestamps["packages"]:
        original_without_timestamps["packages"]["ko"].pop("updated", None)

    next_without_timestamps = copy.deepcopy(manifest)
    next_without_timestamps.pop("last_updated", None)
    next_without_timestamps["packages"]["ko"].pop("updated", None)

    if original_without_timestamps != next_without_timestamps:
        timestamp = utc_now()
        manifest["last_updated"] = timestamp
        manifest["packages"]["ko"]["updated"] = timestamp
    else:
        if existing_last_updated is not None:
            manifest["last_updated"] = existing_last_updated
        if existing_package_updated is not None:
            manifest["packages"]["ko"]["updated"] = existing_package_updated
    write_json(manifest_path, manifest)


def update_video_manifests(worktree: Path, langs: list[str]) -> None:
    video_files = list_video_files(worktree)
    if not video_files:
        raise SystemExit(f"No video files found in staged worktree: {worktree / VIDEO_CORE_REL}")
    update_package_manifest(worktree, video_files, langs)
    update_production_manifest(worktree, video_files)


def deploy_from_worktree(worktree: Path, frontend_repo: Path, *, deploy_video: bool, deploy_grammar: bool) -> None:
    if deploy_video:
        copy_tree(worktree / PRODUCTION_REL, frontend_repo / PRODUCTION_REL)
        copy_file(worktree / VIDEO_METADATA_REL, frontend_repo / VIDEO_METADATA_REL)
    if deploy_grammar:
        copy_tree(worktree / GRAMMAR_REL, frontend_repo / GRAMMAR_REL)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync current stable frontend assets and run the frontend asset integrity gate."
    )
    parser.add_argument(
        "--content-pipeline-repo",
        type=Path,
        default=LINGO_ROOT / "content-pipeline",
        help="Path to content-pipeline repo.",
    )
    parser.add_argument(
        "--content-ko-repo",
        type=Path,
        default=LINGO_ROOT / "content-ko",
        help="Path to content-ko repo.",
    )
    parser.add_argument(
        "--frontend-repo",
        type=Path,
        default=LINGO_ROOT / "lingo-frontend-web",
        help="Path to lingo-frontend-web repo.",
    )
    parser.add_argument(
        "--staging-root",
        type=Path,
        default=DEFAULT_STAGING_ROOT,
        help="Local staging root used before deploying allowed asset paths into the frontend repo.",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Do not sync assets; only run the frontend asset validation gate.",
    )
    parser.add_argument(
        "--skip-video",
        action="store_true",
        help="Skip video package sync.",
    )
    parser.add_argument(
        "--video-langs",
        default="zh_tw",
        help="Comma-separated video i18n language list to merge into package manifests.",
    )
    parser.add_argument(
        "--skip-grammar",
        action="store_true",
        help="Skip grammar note export.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    content_pipeline_repo = existing_dir(args.content_pipeline_repo, "content-pipeline repo")
    content_ko_repo = existing_dir(args.content_ko_repo, "content-ko repo")
    frontend_repo = existing_dir(args.frontend_repo, "frontend repo")
    video_langs = [lang.strip() for lang in args.video_langs.split(",") if lang.strip()]

    if args.validate_only:
        print("validate-only mode: skipping asset sync steps.", flush=True)
    else:
        staging_root = args.staging_root.resolve()
        worktree = prepare_worktree(frontend_repo, staging_root)
        print(f"staging frontend asset worktree: {worktree}", flush=True)

        if not args.skip_video:
            run(
                [
                    "make",
                    "sync-video-frontend",
                    f"CONTENT_REPO={content_ko_repo}",
                    f"FRONTEND_REPO={worktree}",
                    f"LANGS={','.join(video_langs)}",
                ],
                content_pipeline_repo,
            )
            update_video_manifests(worktree, video_langs)

        if not args.skip_grammar:
            run(
                [
                    "python3",
                    "scripts/ops/export_frontend_grammar.py",
                    "--frontend-repo",
                    str(worktree),
                ],
                content_ko_repo,
            )

        deploy_from_worktree(
            worktree,
            frontend_repo,
            deploy_video=not args.skip_video,
            deploy_grammar=not args.skip_grammar,
        )

    print(
        "\nDictionary and learning-library assets are validation-gated here but "
        "not regenerated by this bridge yet.",
        flush=True,
    )
    run(["make", "validate-assets"], frontend_repo)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        raise SystemExit(exc.returncode) from exc
