#!/usr/bin/env bash
#
# Re-encrypt the source HTML and produce a fresh index.html for GitHub Pages.
#
# Usage:
#   1. Put updated unencrypted file at source/Portfolio_Trajectory_Review.html
#   2. Run: ./update.sh
#   3. Commit + push: git add index.html && git commit -m "Refresh" && git push
#

set -euo pipefail

# ---- Config ----
PASSWORD='Base10Automation!'
SOURCE_FILE="source/Portfolio_Trajectory_Review.html"
OUTPUT_FILE="index.html"
LABEL="Base10 Portfolio Review v2"
INSTRUCTIONS="Enter the password to access the Base10 portfolio trajectory review."
REMEMBER_DAYS=14

# ---- Sanity checks ----
if [ ! -f "$SOURCE_FILE" ]; then
  echo "ERROR: $SOURCE_FILE not found."
  exit 1
fi

if ! command -v node &> /dev/null; then
  echo "ERROR: Node.js not installed. Install from https://nodejs.org/"
  exit 1
fi

# ---- Encrypt ----
echo "Encrypting $SOURCE_FILE -> $OUTPUT_FILE ..."

# Read salt from the committed config (keeps password hash stable across updates).
SALT=$(python3 -c "import json; print(json.load(open('.staticrypt.json'))['salt'])" 2>/dev/null || echo "")

# Install staticrypt into /tmp (avoids filling user disk in restricted shells)
mkdir -p /tmp/npm-stage /tmp/npm-cache
if [ ! -x "/tmp/npm-stage/node_modules/.bin/staticrypt" ]; then
  echo "Installing staticrypt to /tmp/npm-stage ..."
  npm install --cache /tmp/npm-cache --prefix /tmp/npm-stage staticrypt > /dev/null 2>&1
fi
STATICRYPT_BIN="/tmp/npm-stage/node_modules/.bin/staticrypt"

"$STATICRYPT_BIN" \
  "$SOURCE_FILE" \
  -p "$PASSWORD" \
  --short \
  --remember "$REMEMBER_DAYS" \
  --label "$LABEL" \
  --instructions "$INSTRUCTIONS" \
  ${SALT:+-s "$SALT" -c false} \
  -d ./_tmp_encrypted

# Move the encrypted output to index.html and customize the title
SOURCE_BASENAME=$(basename "$SOURCE_FILE")
mv "./_tmp_encrypted/$SOURCE_BASENAME" "$OUTPUT_FILE"
sed -i.bak 's|<title>Protected Page</title>|<title>Base10 Portfolio Review v2</title>|' "$OUTPUT_FILE"
rm -f "${OUTPUT_FILE}.bak"
rm -rf ./_tmp_encrypted

echo ""
echo "Done. $OUTPUT_FILE updated."
echo ""
echo "Next steps:"
echo "  git add index.html"
echo "  git commit -m \"Refresh portfolio review v2 ($(date +%Y-%m-%d))\""
echo "  git push"
echo ""
