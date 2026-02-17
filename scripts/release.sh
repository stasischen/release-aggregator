#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"

PIPELINE_DIST="${PIPELINE_DIST:-${ROOT_DIR}/../content-pipeline/dist}"
CORE_SCHEMA="${CORE_SCHEMA:-${ROOT_DIR}/../core-schema}"
SOURCE_REPO="${SOURCE_REPO:-content-pipeline}"
SOURCE_COMMIT="${SOURCE_COMMIT:-unknown}"
OUTPUT_DIR="${OUTPUT_DIR:-}"
VERSION=""

usage() {
  cat <<'EOF'
Usage:
  ./scripts/release.sh --version vX.Y.Z [--source-commit <sha>] [--source-repo <name>]
  ./scripts/release.sh --output <path> [--pipeline-dist <path>] [--core-schema <path>] [--source-repo <name>] [--source-commit <sha>]

Required:
  --version <tag>  OR  --output <path>

Optional:
  --pipeline-dist <path>  (default: ../content-pipeline/dist)
  --core-schema <path>    (default: ../core-schema)
  --source-repo <name>    (default: content-pipeline)
  --source-commit <sha>   (default: unknown)
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --version)
      VERSION="$2"
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

if [[ -z "${OUTPUT_DIR}" ]]; then
  echo "Error: provide --version or --output." >&2
  usage
  exit 1
fi

exec "${PYTHON_BIN}" "${ROOT_DIR}/scripts/release.py" \
  --pipeline-dist "${PIPELINE_DIST}" \
  --output "${OUTPUT_DIR}" \
  --core-schema "${CORE_SCHEMA}" \
  --source-repo "${SOURCE_REPO}" \
  --source-commit "${SOURCE_COMMIT}"
