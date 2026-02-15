#!/usr/bin/env bash
set -euo pipefail

MODE="dry-run"
if [[ "${1:-}" == "--apply" ]]; then
  MODE="apply"
elif [[ "${1:-}" == "--dry-run" || -z "${1:-}" ]]; then
  MODE="dry-run"
else
  echo "Usage: $0 [--dry-run|--apply]"
  exit 1
fi

SRC="/Users/ywchen/Dev/Lingourmet_universal"
DST="/Users/ywchen/Dev/lingo/release-aggregator/docs/archive/universal"

paths=(
  "docs/planning"
  "docs/handoffs"
  "docs/guides"
  "docs/project"
  ".agent/workflows"
  ".agent/templates"
)

echo "Mode: $MODE"
echo "Source: $SRC"
echo "Target: $DST"

mkdir -p "$DST"

for p in "${paths[@]}"; do
  if [[ -d "$SRC/$p" ]]; then
    if [[ "$MODE" == "dry-run" ]]; then
      echo "[DRY] rsync -a --delete '$SRC/$p/' '$DST/$p/'"
    else
      mkdir -p "$DST/$p"
      rsync -a --delete "$SRC/$p/" "$DST/$p/"
      echo "[OK] migrated $p"
    fi
  else
    echo "[SKIP] missing $SRC/$p"
  fi
done

echo "Done: $MODE"
