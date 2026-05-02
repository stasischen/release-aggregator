#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"

PIPELINE_DIST="${PIPELINE_DIST:-${ROOT_DIR}/../content-pipeline/dist}"
CORE_SCHEMA="${CORE_SCHEMA:-${ROOT_DIR}/../core-schema}"
SOURCE_REPO="${SOURCE_REPO:-content-pipeline}"
SOURCE_COMMIT="${SOURCE_COMMIT:-unknown}"
PIPELINE_VERSION="${PIPELINE_VERSION:-unknown}"
SCHEMA_VERSION="${SCHEMA_VERSION:-unknown}"
PACKAGE_VERSION="${PACKAGE_VERSION:-}"
SOURCE_MANIFEST="${SOURCE_MANIFEST:-}"
SCOPE="${SCOPE:-}"
OUTPUT_DIR="${OUTPUT_DIR:-}"
VERSION=""
CLEAN_OUTPUT=0
ALLOW_UNMANIFESTED=0

usage() {
  cat <<'EOF'
Usage:
  ./scripts/release.sh --version X.Y.Z --scope <scope> --source-manifest <path> --pipeline-version <version> --schema-version <version> [--source-commit <sha>]
  ./scripts/release.sh --output <path> --version X.Y.Z --scope <scope> --source-manifest <path> --pipeline-version <version> --schema-version <version>

Required:
  --version <semver>
  --scope <scope>
  --pipeline-version <version>
  --schema-version <version>
  --source-manifest <path> OR --allow-unmanifested

Optional:
  --pipeline-dist <path>  (default: ../content-pipeline/dist)
  --core-schema <path>    (default: ../core-schema)
  --source-repo <name>    (default: content-pipeline)
  --source-commit <sha>   (default: unknown)
  --package-version <semver> (default: release version)
  --output <path>         (default: staging/<version>)
  --clean-output          Remove non-empty output directory before staging
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --version)
      VERSION="$2"
      shift 2
      ;;
    --scope)
      SCOPE="$2"
      shift 2
      ;;
    --output)
      OUTPUT_DIR="$2"
      shift 2
      ;;
    --pipeline-dist)
      PIPELINE_DIST="$2"
      shift 2
      ;;
    --core-schema)
      CORE_SCHEMA="$2"
      shift 2
      ;;
    --source-repo)
      SOURCE_REPO="$2"
      shift 2
      ;;
    --source-commit)
      SOURCE_COMMIT="$2"
      shift 2
      ;;
    --pipeline-version)
      PIPELINE_VERSION="$2"
      shift 2
      ;;
    --schema-version)
      SCHEMA_VERSION="$2"
      shift 2
      ;;
    --package-version)
      PACKAGE_VERSION="$2"
      shift 2
      ;;
    --source-manifest)
      SOURCE_MANIFEST="$2"
      shift 2
      ;;
    --allow-unmanifested)
      ALLOW_UNMANIFESTED=1
      shift
      ;;
    --clean-output)
      CLEAN_OUTPUT=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ -z "${OUTPUT_DIR}" && -n "${VERSION}" ]]; then
  OUTPUT_DIR="${ROOT_DIR}/staging/${VERSION}"
fi

if [[ -z "${PACKAGE_VERSION}" ]]; then
  PACKAGE_VERSION="${VERSION}"
fi

if [[ -z "${VERSION}" ]]; then
  echo "Error: provide --version." >&2
  usage
  exit 1
fi

if [[ -z "${OUTPUT_DIR}" ]]; then
  echo "Error: provide --output or use --version to derive the staging path." >&2
  usage
  exit 1
fi

if [[ -z "${SCOPE}" ]]; then
  echo "Error: provide --scope." >&2
  usage
  exit 1
fi

if [[ "${PIPELINE_VERSION}" == "unknown" ]]; then
  echo "Error: provide --pipeline-version or set PIPELINE_VERSION." >&2
  usage
  exit 1
fi

if [[ "${SCHEMA_VERSION}" == "unknown" ]]; then
  echo "Error: provide --schema-version or set SCHEMA_VERSION." >&2
  usage
  exit 1
fi

if [[ -z "${SOURCE_MANIFEST}" && "${ALLOW_UNMANIFESTED}" -ne 1 ]]; then
  echo "Error: provide --source-manifest or pass --allow-unmanifested." >&2
  usage
  exit 1
fi

echo "🔍 Running pre-release quality gates..."
"${PYTHON_BIN}" "${ROOT_DIR}/scripts/check_quality.py" --scope "${SCOPE}"

release_args=(
  "${ROOT_DIR}/scripts/release.py"
  --pipeline-dist "${PIPELINE_DIST}"
  --output "${OUTPUT_DIR}"
  --core-schema "${CORE_SCHEMA}"
  --source-repo "${SOURCE_REPO}"
  --source-commit "${SOURCE_COMMIT}"
  --release-version "${VERSION}"
  --package-version "${PACKAGE_VERSION}"
  --pipeline-version "${PIPELINE_VERSION}"
  --schema-version "${SCHEMA_VERSION}"
)

if [[ -n "${SOURCE_MANIFEST}" ]]; then
  release_args+=(--source-manifest "${SOURCE_MANIFEST}")
fi

if [[ "${ALLOW_UNMANIFESTED}" -eq 1 ]]; then
  release_args+=(--allow-unmanifested)
fi

if [[ "${CLEAN_OUTPUT}" -eq 1 ]]; then
  release_args+=(--clean-output)
fi

exec "${PYTHON_BIN}" "${release_args[@]}"
