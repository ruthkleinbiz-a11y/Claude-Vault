#!/usr/bin/env bash
# Republishes the Ruth Klein Weekly Signal artifact using the latest dashboard-data.json.
# Requires: ANTHROPIC_API_KEY env var, claude CLI installed, dashboard-data.json to exist.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_FILE="${SCRIPT_DIR}/../reports/dashboard-data.json"
ARTIFACT_URL="https://claude.ai/code/artifact/3104f5d6-4502-4aef-9502-1c1ae51e482d"

if [[ ! -f "$DATA_FILE" ]]; then
  echo "[dashboard] No dashboard-data.json found — skipping artifact update." >&2
  exit 0
fi

echo "[dashboard] Republishing Weekly Signal artifact..."

claude --dangerously-skip-permissions --print "$(cat <<PROMPT
You are updating a published artifact. Do exactly this and nothing else:

1. Read the file at: ${DATA_FILE}
2. Read the existing artifact at URL: ${ARTIFACT_URL}
3. In the artifact's <script> block, replace the entire \`const DASH = { ... };\` object with a new one whose values come from the JSON you read in step 1. Keep every key the platform cards, glance tiles, email, resonance, and website sections expect — use null for any field not present in the JSON. Keep all HTML, CSS, and JS outside the DASH object exactly as it is.
4. Republish the artifact to the same URL with label "auto-update $(date -u +%Y-%m-%d)".

Do not explain, do not ask questions. Just read, update, and republish.
PROMPT
)"

echo "[dashboard] Artifact republished."
