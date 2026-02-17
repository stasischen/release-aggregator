#!/usr/bin/env bash
set -euo pipefail

SESSION_NAME="${1:-lingo-control}"
LAYOUT_FILE="/Users/ywchen/Dev/lingo/release-aggregator/tools/zellij/lingo_control_tower.kdl"

if ! command -v zellij >/dev/null 2>&1; then
  echo "zellij not found in PATH"
  exit 1
fi

if [ ! -f "$LAYOUT_FILE" ]; then
  echo "layout file not found: $LAYOUT_FILE"
  exit 1
fi

exec zellij --layout "$LAYOUT_FILE" attach --create "$SESSION_NAME"
