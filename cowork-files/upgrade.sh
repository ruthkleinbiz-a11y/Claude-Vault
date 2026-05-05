#!/bin/bash
# ZenithMind OS (Cowork) — Upgrade
# Run this from your NEW ZenithMind-OS-Cowork folder to migrate data from an old version.
set -e

NEW_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NEW_VERSION="$(cat "$NEW_DIR/VERSION" 2>/dev/null || echo "unknown")"

echo "═══════════════════════════════════════════════════════"
echo "  ZenithMind OS (Cowork) — Upgrade to v$NEW_VERSION"
echo "═══════════════════════════════════════════════════════"
echo ""

# ─── Check if this folder already has user data ─────────────────────────

HAS_DATA=0
if [ -f "$NEW_DIR/session-progress.md" ]; then
    # Check if it's a real progress file (not just a template placeholder)
    if grep -q "Current Lesson" "$NEW_DIR/session-progress.md" 2>/dev/null; then
        HAS_DATA=1
    fi
fi

if [ "$HAS_DATA" -eq 1 ]; then
    echo "This folder already has session data (session-progress.md)."
    echo "If you've already migrated, you're good to go — just open this folder in Cowork."
    echo ""
    read -p "Continue anyway and overwrite? (y/N): " CONFIRM
    if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
        echo "Upgrade cancelled. Your existing data is untouched."
        exit 0
    fi
    echo ""
fi

# ─── Find old install ───────────────────────────────────────────────────

OLD_DIR=""

# Auto-detect from common locations
echo "Looking for your previous ZenithMind OS install..."
CANDIDATES=()

for SEARCH_DIR in "$HOME/Desktop" "$HOME/Downloads" "$HOME/Documents" "$HOME"; do
    while IFS= read -r -d '' DIR; do
        # Skip if it's this folder
        [ "$DIR" = "$NEW_DIR" ] && continue
        # Must have a lesson-1/CLAUDE.md to be a valid ZMOS install
        if [ -f "$DIR/lesson-1/CLAUDE.md" ]; then
            CANDIDATES+=("$DIR")
        fi
    done < <(find "$SEARCH_DIR" -maxdepth 2 -type d -name "ZenithMind*" -print0 2>/dev/null)
done

if [ ${#CANDIDATES[@]} -eq 1 ]; then
    echo "  Found: ${CANDIDATES[0]}"
    OLD_VERSION="$(cat "${CANDIDATES[0]}/VERSION" 2>/dev/null || echo "pre-1.0")"
    echo "  Version: v$OLD_VERSION"
    echo ""
    read -p "Migrate data from this folder? (Y/n): " CONFIRM
    if [ "$CONFIRM" = "n" ] || [ "$CONFIRM" = "N" ]; then
        OLD_DIR=""
    else
        OLD_DIR="${CANDIDATES[0]}"
    fi
elif [ ${#CANDIDATES[@]} -gt 1 ]; then
    echo "  Found multiple ZenithMind installs:"
    for i in "${!CANDIDATES[@]}"; do
        VER="$(cat "${CANDIDATES[$i]}/VERSION" 2>/dev/null || echo "pre-1.0")"
        echo "    $((i+1))) ${CANDIDATES[$i]} (v$VER)"
    done
    echo ""
    read -p "Which one? (1-${#CANDIDATES[@]}, or 0 to enter path manually): " CHOICE
    if [ "$CHOICE" -gt 0 ] 2>/dev/null && [ "$CHOICE" -le ${#CANDIDATES[@]} ]; then
        OLD_DIR="${CANDIDATES[$((CHOICE-1))]}"
    fi
else
    echo "  No previous install found automatically."
fi

# Manual path entry if auto-detect didn't work
if [ -z "$OLD_DIR" ]; then
    echo ""
    echo "Drag your old ZenithMind-OS-Cowork folder here, or type the path:"
    read -p "> " OLD_DIR
    # Strip trailing whitespace and quotes
    OLD_DIR="$(echo "$OLD_DIR" | sed 's/^ *//;s/ *$//;s/^"//;s/"$//')"
fi

# Validate
if [ ! -d "$OLD_DIR" ]; then
    echo "Error: Folder not found: $OLD_DIR"
    exit 1
fi

if [ ! -f "$OLD_DIR/lesson-1/CLAUDE.md" ]; then
    echo "Error: That doesn't look like a ZenithMind OS folder (missing lesson-1/CLAUDE.md)."
    exit 1
fi

OLD_VERSION="$(cat "$OLD_DIR/VERSION" 2>/dev/null || echo "pre-1.0")"

echo ""
echo "Migrating from: $OLD_DIR (v$OLD_VERSION)"
echo ""

# ─── Migrate user data ──────────────────────────────────────────────────

MIGRATED=0

# Root session-progress.md
if [ -f "$OLD_DIR/session-progress.md" ]; then
    cp "$OLD_DIR/session-progress.md" "$NEW_DIR/session-progress.md"
    echo "  ✓ session-progress.md"
    MIGRATED=$((MIGRATED + 1))
fi

# Lesson outputs
for LESSON in 1 2 3 4; do
    OLD_OUTPUTS="$OLD_DIR/lesson-$LESSON/outputs"
    NEW_OUTPUTS="$NEW_DIR/lesson-$LESSON/outputs"

    if [ -d "$OLD_OUTPUTS" ]; then
        FILE_COUNT=$(find "$OLD_OUTPUTS" -type f 2>/dev/null | wc -l | tr -d ' ')
        if [ "$FILE_COUNT" -gt 0 ]; then
            mkdir -p "$NEW_OUTPUTS"
            cp -r "$OLD_OUTPUTS"/* "$NEW_OUTPUTS"/ 2>/dev/null || true
            echo "  ✓ lesson-$LESSON/outputs/ ($FILE_COUNT files)"
            MIGRATED=$((MIGRATED + FILE_COUNT))
        fi
    fi
done

if [ "$MIGRATED" -eq 0 ]; then
    echo "  No user data found to migrate (old folder may be a fresh install)."
fi

echo ""
echo "═══════════════════════════════════════════════════════"
echo "  Upgrade complete! $MIGRATED file(s) migrated."
echo "  Old folder preserved: $OLD_DIR"
echo ""
echo "  Next: Open Cowork, select this folder, and say"
echo "  'Let's continue' — Claude will pick up where you left off."
echo "═══════════════════════════════════════════════════════"
