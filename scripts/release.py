import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import datetime
from pathlib import Path
from typing import Dict, Any, List

def calculate_hash(file_path):
    """Calculates SHA256 of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def validate_manifest(validator_path, schema_path, manifest_path):
    """Validates the generated manifest against core-schema."""
    cmd = [
        sys.executable, validator_path,
        "--schema", schema_path,
        "--target", manifest_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Manifest validation failed!")
        print(result.stdout)
        print(result.stderr)
        return False
    return True

def release(pipeline_dist, output_dir, core_schema_dir, source_repo, source_commit):
    """
    Aggregates artifacts from pipeline_dist and generates global manifest.
    """
    dist_root = Path(pipeline_dist)
    staging_root = Path(output_dir)
    staging_root.mkdir(parents=True, exist_ok=True)

    if not dist_root.exists() or not dist_root.is_dir():
        print(f"❌ Pipeline dist path not found or not a directory: {dist_root}")
        return False
    
    # Manifest Metadata
    manifest = {
        "version": "1.0.0", # Release version
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "packages": []
    }

    print(f"📦 Scanning artifacts in {dist_root}...")
    
    # 1. Collect Artifacts
    # We walk the dist directory.
    # Structure in dist: {lang_target}/{lang_learner}/{type}/{id}.json
    # We treat each JSON file as a "package" item in the global manifest for this granularity level.
    # OR, if we had zipped packages, we'd pick those up. For now, individual files.
    
    files_found: int = 0
    for root, dirs, files in os.walk(dist_root):
        dirs.sort()
        files.sort()
        for file in files:
            if not file.endswith(".json"):
                continue
            
            src_path = Path(root) / file
            relative_path = src_path.relative_to(dist_root)
            dest_path = staging_root / relative_path
            
            # Integrity Check 1: File exists (implicit by os.walk)
            
            # Copy to staging
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_path, dest_path)
            
            # Hash
            file_hash = calculate_hash(src_path)
            
            # Add to Manifest
            # ID is filename stem for now
            pkg_id = file.replace(".json", "") 
            
            package_entry = {
                "id": pkg_id,
                "version": "1.0.0", # Placeholder, would come from file content if parsed
                "path": str(relative_path),
                "hash": f"sha256:{file_hash}",
                "provenance": {
                    "source_repo": source_repo,
                    "source_commit": source_commit,
                    "pipeline_version": "v1.0.0-alpha", # MVP constant
                    "schema_version": "1.0.0",          # MVP constant
                    "built_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
                }
            }
            # Explicit cast for linter
            packages_list: list = manifest["packages"] # type: ignore
            packages_list.append(package_entry)
            files_found = files_found + 1 # type: ignore
            print(f"  └── Added {pkg_id}")

    if files_found == 0:
        print("❌ No artifacts found to release.")
        return False

    # 2. Generate Manifest File
    manifest_path = staging_root / "global_manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    
    print(f"📄 Generated global_manifest.json with {len(manifest['packages'])} packages.")

    # 3. Validate Manifest
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
    
    args = parser.parse_args()
    
    print("🚀 Starting Release Aggregation...")
    success = release(
        args.pipeline_dist, 
        args.output, 
        args.core_schema,
        args.source_repo,
        args.source_commit
    )
    
    if success:
        print("✅ Release Staged Successfully")
        sys.exit(0)
    else:
        print("💥 Release Failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
