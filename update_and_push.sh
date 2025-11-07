#!/bin/bash
set -euo pipefail

REPO_DIR="$HOME/Projects/UIN_Screener"
PY="/opt/miniconda3/envs/cellpose/bin/python"

cd "$REPO_DIR"

# 1) Run the aggregator
$PY Settlement.py

# 2) Stage only the outputs (safe)
git add Settlement_Output/*.csv

# 3) Commit only if there are changes
if ! git diff --cached --quiet; then
  MSG="Daily data update $(date '+%Y-%m-%d %H:%M')"
  git commit -m "$MSG"
  git push origin main
  echo "✅ Pushed: $MSG"
else
  echo "ℹ️ No changes detected; nothing to commit."
fi


