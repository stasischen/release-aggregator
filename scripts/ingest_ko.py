import os
import subprocess
import sys
from pathlib import Path

# Path Configuration (Assuming sibling directories)
AGGREGATOR_ROOT = Path(__file__).resolve().parents[1]
DEV_ROOT = AGGREGATOR_ROOT.parent

LLLO_ROOT = DEV_ROOT / "lllo"
CONTENT_KO_ROOT = DEV_ROOT / "content-ko"

def run_command(cmd, cwd, description):
    """Utility to run a shell command and print status."""
    print(f"--- {description} ---")
    print(f"Executing: {' '.join(cmd)} in {cwd}")
    try:
        # Use shell=True for 'make' on Windows if needed, but subprocess.run with a list is generally safer.
        # On Windows, 'git' and 'python' should be in PATH. 'make' might be 'mingw32-make' or 'make'.
        # We'll try to use the raw list first.
        result = subprocess.run(cmd, cwd=cwd, check=True, text=True)
        print(f"SUCCESS: {description}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"FAILED: {description}")
        print(f"Exit code: {e.returncode}")
        return False
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return False

def main():
    print("--- Starting Unified Ingestion for Korean Content ---")
    
    # Validation
    if not LLLO_ROOT.exists():
        print(f"Error: LLLO directory not found at {LLLO_ROOT}")
        sys.exit(1)
    if not CONTENT_KO_ROOT.exists():
        print(f"Error: content-ko directory not found at {CONTENT_KO_ROOT}")
        sys.exit(1)

    # Step 1: Git Pull LLLO
    if not run_command(["git", "pull"], LLLO_ROOT, "Git Pull LLLO"):
        print("Stopping due to git pull failure.")
        sys.exit(1)

    # Step 2: Content Ingestion (import_lllo_raw.py)
    # Note: We use sys.executable to ensure we use the same Python environment
    ingest_script = CONTENT_KO_ROOT / "scripts" / "ops" / "import_lllo_raw.py"
    if not run_command([sys.executable, str(ingest_script)], CONTENT_KO_ROOT, "Content Ingestion"):
        print("Stopping due to ingestion script failure.")
        sys.exit(1)

    # Step 3: Trigger Mapping Pipeline (run_mapping_pipeline.py)
    pipeline_script = CONTENT_KO_ROOT / "scripts" / "ops" / "run_mapping_pipeline.py"
    if not run_command([sys.executable, str(pipeline_script)], CONTENT_KO_ROOT, "Trigger Mapping Pipeline"):
        print("Pipeline failed, but ingestion was completed.")
        sys.exit(1)

    print("\n[SUCCESS] Unified Ingestion completed successfully!")

if __name__ == "__main__":
    main()
