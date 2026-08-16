#!/bin/bash
set -e

# --- adjust these two paths for your machine ---
SYNC_DIR=~/dev/rover-docs-sync
REPO_DIR=~/dev/rover-documentation
# -------------------------------------------------

# --- email report (optional) ---
# Required for publish_staging.py to send the changelog email.
# For Gmail, use an App Password: https://myaccount.google.com/apppasswords
# Put this export in your shell profile (~/.zshrc etc.), NOT in this file,
# so it never ends up in git even by accident.
#   export SYNC_SMTP_USER="you@gmail.com"
#   export SYNC_SMTP_PASSWORD="your-16-char-app-password"
# To publish everything regardless of underscore prefix for one run:
#   SYNC_REQUIRE_UNDERSCORE=0 ./run_sync.sh
# ---------------------------------

cd "$SYNC_DIR"

# activate a venv if you're using one (safe to remove if not)
if [ -f venv/bin/activate ]; then
  source venv/bin/activate
fi

echo "== Syncing Drive -> staging/ =="
python3 drive_sync.py

echo "== Publishing staging/ -> docs/ =="
python3 publish_staging.py

cd "$REPO_DIR"
git pull origin main

git add docs/
if ! git diff --cached --quiet; then
  git commit -m "Automated docs sync $(date +%Y-%m-%d)"
  git push origin main
  echo "Pushed changes."
else
  echo "No changes to sync."
fi