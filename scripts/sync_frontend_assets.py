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
import shutil
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
RELEASE_AGGREGATOR_ROOT = SCRIPT_DIR.parent
LINGO_ROOT = RELEASE_AGGREGATOR_ROOT.parent
DEFAULT_STAGING_ROOT = RELEASE_AGGREGATOR_ROOT / "staging" / "frontend_asset_bridge"

PRODUCTION_REL = Path("assets/content/production")
GRAMMAR_REL = Path("assets/content/grammar")
VIDEO_METADATA_REL = Path("assets/config/video_metadata.json")


def run(command: list[str], cwd: Path) -> None:
    printable = " ".join(command)
    print(f"\n$ {printable}\n  cwd={cwd}", flush=True)
    subprocess.run(command, cwd=cwd, check=True)


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
                ],
                content_pipeline_repo,
            )

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
