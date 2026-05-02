import argparse
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ARTIFACT_SUFFIXES = (".json", ".ogg", ".mp3")


def utc_now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def calculate_hash(file_path):
    """Calculates SHA256 of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def normalize_version(version):
    """The current manifest schema requires semver without a leading v."""
    if version.startswith("v"):
        return version[1:]
    return version


def load_source_manifest(source_manifest_path):
    if not source_manifest_path:
        return None

    path = Path(source_manifest_path)
    if not path.exists():
        raise FileNotFoundError(f"Source manifest not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    expected = {}

    if isinstance(data, dict) and all(isinstance(value, str) for value in data.values()):
        expected = {key: value for key, value in data.items()}
    elif isinstance(data, dict) and isinstance(data.get("files"), dict):
        expected = {key: value for key, value in data["files"].items() if isinstance(value, str)}
    elif isinstance(data, dict) and isinstance(data.get("packages"), list):
        for package in data["packages"]:
            if not isinstance(package, dict):
                continue
            path_value = package.get("path")
            hash_value = package.get("hash") or package.get("sha256")
            if isinstance(path_value, str):
                expected[path_value] = hash_value if isinstance(hash_value, str) else ""

    if not expected:
        raise ValueError(f"Source manifest has no recognizable file list: {path}")

    return expected


def collect_artifacts(dist_root):
    artifacts = []
    for root, dirs, files in os.walk(dist_root):
        dirs.sort()
        files.sort()
        for file in files:
            if not file.endswith(ARTIFACT_SUFFIXES):
                continue
            src_path = Path(root) / file
            artifacts.append((src_path.relative_to(dist_root), src_path))
    return artifacts


def verify_source_manifest(artifacts, source_manifest):
    actual_paths = {str(relative_path) for relative_path, _ in artifacts}
    expected_paths = set(source_manifest)
    unexpected = sorted(actual_paths - expected_paths)
    missing = sorted(expected_paths - actual_paths)

    if unexpected or missing:
        if unexpected:
            print("❌ Artifacts not declared by source manifest:")
            for path in unexpected:
                print(f"  - {path}")
        if missing:
            print("❌ Source manifest entries missing from pipeline dist:")
            for path in missing:
                print(f"  - {path}")
        return False

    for relative_path, src_path in artifacts:
        expected_hash = source_manifest.get(str(relative_path))
        if not expected_hash:
            continue
        actual_hash = calculate_hash(src_path)
        normalized_hash = expected_hash.removeprefix("sha256:")
        if actual_hash != normalized_hash:
            print(f"❌ Hash mismatch for {relative_path}: expected {expected_hash}, got sha256:{actual_hash}")
            return False

    return True


def prepare_staging_root(staging_root, clean_output):
    if staging_root.exists() and any(staging_root.iterdir()):
        if not clean_output:
            print(f"❌ Output directory is not empty: {staging_root}")
            print("   Re-run with --clean-output to remove it before staging.")
            return False
        shutil.rmtree(staging_root)
    staging_root.mkdir(parents=True, exist_ok=True)
    return True


def validate_manifest(validator_path, schema_path, manifest_path):
    """Validates the generated manifest against core-schema."""
    cmd = [
        sys.executable,
        validator_path,
        "--schema",
        schema_path,
        "--target",
        manifest_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ Manifest validation failed!")
        print(result.stdout)
        print(result.stderr)
        return False
    return True


def release(
    pipeline_dist,
    output_dir,
    core_schema_dir,
    source_repo,
    source_commit,
    release_version,
    package_version,
    pipeline_version,
    schema_version,
    source_manifest_path=None,
    allow_unmanifested=False,
    clean_output=False,
):
    """
    Aggregates artifacts from pipeline_dist and generates global manifest.
    """
    dist_root = Path(pipeline_dist)
    staging_root = Path(output_dir)

    if not dist_root.exists() or not dist_root.is_dir():
        print(f"❌ Pipeline dist path not found or not a directory: {dist_root}")
        return False

    if not source_manifest_path and not allow_unmanifested:
        print("❌ Source manifest is required to prevent stale artifact aggregation.")
        print("   Provide --source-manifest, or pass --allow-unmanifested for an explicit compatibility release.")
        return False

    try:
        source_manifest = load_source_manifest(source_manifest_path)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        print(f"❌ {exc}")
        return False

    artifacts = collect_artifacts(dist_root)
    if not artifacts:
        print("❌ No artifacts found to release.")
        return False

    if source_manifest and not verify_source_manifest(artifacts, source_manifest):
        return False

    if not prepare_staging_root(staging_root, clean_output):
        return False

    built_at = utc_now()
    manifest = {
        "version": normalize_version(release_version),
        "generated_at": built_at,
        "packages": [],
    }

    print(f"📦 Scanning artifacts in {dist_root}...")

    for relative_path, src_path in artifacts:
        dest_path = staging_root / relative_path
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_path, dest_path)

        file_hash = calculate_hash(src_path)
        package_entry = {
            "id": src_path.stem,
            "version": package_version,
            "path": str(relative_path),
            "hash": f"sha256:{file_hash}",
            "provenance": {
                "source_repo": source_repo,
                "source_commit": source_commit,
                "pipeline_version": pipeline_version,
                "schema_version": schema_version,
                "built_at": built_at,
            },
        }
        manifest["packages"].append(package_entry)
        print(f"  └── Added {src_path.stem}")

    manifest_path = staging_root / "global_manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"📄 Generated global_manifest.json with {len(manifest['packages'])} packages.")

    validator_path = Path(core_schema_dir) / "validators/validate.py"
    manifest_schema = Path(core_schema_dir) / "schemas/manifest.schema.json"

    if not validator_path.exists():
        print(f"❌ Validator not found: {validator_path}")
        return False
    if not manifest_schema.exists():
        print(f"❌ Manifest schema not found: {manifest_schema}")
        return False

    if not validate_manifest(validator_path, manifest_schema, manifest_path):
        return False

    return True


def main():
    parser = argparse.ArgumentParser(description="Release Aggregator")
    parser.add_argument("--pipeline-dist", required=True, help="Path to pipeline output")
    parser.add_argument("--output", required=True, help="Staging output directory")
    parser.add_argument("--core-schema", required=True, help="Path to core-schema repo")
    parser.add_argument("--source-repo", required=True, help="Source repository URL/Name")
    parser.add_argument("--source-commit", required=True, help="Source commit hash")
    parser.add_argument("--release-version", required=True, help="Release manifest version, semver with optional leading v")
    parser.add_argument("--package-version", required=True, help="Package version to stamp on each manifest entry")
    parser.add_argument("--pipeline-version", required=True, help="Pipeline build/version that produced the artifacts")
    parser.add_argument("--schema-version", required=True, help="Schema version used by the produced artifacts")
    parser.add_argument("--source-manifest", help="Upstream manifest listing expected artifact paths and optional hashes")
    parser.add_argument("--allow-unmanifested", action="store_true", help="Explicit compatibility release without source manifest")
    parser.add_argument("--clean-output", action="store_true", help="Remove a non-empty output directory before staging")

    args = parser.parse_args()

    print("🚀 Starting Release Aggregation...")
    success = release(
        args.pipeline_dist,
        args.output,
        args.core_schema,
        args.source_repo,
        args.source_commit,
        args.release_version,
        args.package_version,
        args.pipeline_version,
        args.schema_version,
        args.source_manifest,
        args.allow_unmanifested,
        args.clean_output,
    )

    if success:
        print("✅ Release Staged Successfully")
        sys.exit(0)
    else:
        print("💥 Release Failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
