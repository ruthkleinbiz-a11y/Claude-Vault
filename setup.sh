#!/bin/bash
# ZenithMind OS — Setup & Upgrade
# Handles fresh installs AND upgrades from previous versions.
# Run once per version. After this, say "zenithmind" in any Claude session to start.
set -e

ZMOS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$HOME/.zenithmind"
BIN_DIR="$HOME/.local/bin"
LAUNCHER="$BIN_DIR/zenithmind"
NEW_VERSION="$(cat "$ZMOS_DIR/VERSION" 2>/dev/null || echo "unknown")"

# ─── Detect install state ───────────────────────────────────────────────

MODE="fresh"
OLD_DIR=""
OLD_VERSION=""

if [ -f "$CONFIG_FILE" ]; then
    OLD_DIR="$(cat "$CONFIG_FILE" 2>/dev/null)"

    if [ "$OLD_DIR" = "$ZMOS_DIR" ]; then
        # Case C: Re-run in same folder — just refresh
        MODE="refresh"
    elif [ -n "$OLD_DIR" ] && [ -d "$OLD_DIR" ]; then
        OLD_VERSION="$(cat "$OLD_DIR/VERSION" 2>/dev/null || echo "pre-1.0")"
        if [ "$OLD_VERSION" = "$NEW_VERSION" ]; then
            # Same version in a different folder — still migrate data
            MODE="upgrade"
        else
            # Different version — upgrade
            MODE="upgrade"
        fi
    else
        # Case D: Pointer exists but old folder is gone
        MODE="fresh"
    fi
fi

# ─── Cowork detection (no ~/.zenithmind exists for Cowork users) ─────
# If still fresh, scan common locations for a Cowork folder with user data
if [ "$MODE" = "fresh" ]; then
    COWORK_SEARCH_DIRS=("$HOME/Desktop" "$HOME/Documents" "$HOME/Downloads")
    COWORK_NAMES=("ZenithMind-OS-Cowork" "ZenithMind-OS-Cowork-1")

    for SEARCH_DIR in "${COWORK_SEARCH_DIRS[@]}"; do
        for CNAME in "${COWORK_NAMES[@]}"; do
            CANDIDATE="$SEARCH_DIR/$CNAME"
            if [ -d "$CANDIDATE" ] && [ "$CANDIDATE" != "$ZMOS_DIR" ]; then
                # Check if it has actual user data (any output files)
                HAS_DATA=false
                for LESSON in 1 2 3 4; do
                    if [ -d "$CANDIDATE/lesson-$LESSON/outputs" ]; then
                        FC=$(find "$CANDIDATE/lesson-$LESSON/outputs" -type f 2>/dev/null | wc -l | tr -d ' ')
                        if [ "$FC" -gt 0 ]; then
                            HAS_DATA=true
                            break
                        fi
                    fi
                done

                if [ "$HAS_DATA" = true ]; then
                    OLD_DIR="$CANDIDATE"
                    OLD_VERSION="$(cat "$CANDIDATE/VERSION" 2>/dev/null || echo "cowork")"
                    MODE="upgrade"
                    break 2
                fi
            fi
        done
    done
fi

# ─── Execute based on mode ──────────────────────────────────────────────

if [ "$MODE" = "refresh" ]; then
    echo "ZenithMind OS v$NEW_VERSION — already set up in this folder."
    echo "Refreshing launcher..."

elif [ "$MODE" = "upgrade" ]; then
    echo "═══════════════════════════════════════════════════════"
    echo "  ZenithMind OS — Upgrading"
    echo "  From: v$OLD_VERSION ($OLD_DIR)"
    echo "  To:   v$NEW_VERSION ($ZMOS_DIR)"
    echo "═══════════════════════════════════════════════════════"
    echo ""

    # Step 1: Backup old install
    BACKUP_DIR="$HOME/.zenithmind-backup-$(date +%Y%m%d-%H%M%S)"
    echo "Creating backup of old install..."
    cp -r "$OLD_DIR" "$BACKUP_DIR"
    echo "  Backup saved: $BACKUP_DIR"
    echo ""

    # Step 2: Migrate user data
    echo "Migrating your data..."
    MIGRATED=0

    # Root session-progress.md
    if [ -f "$OLD_DIR/session-progress.md" ]; then
        cp "$OLD_DIR/session-progress.md" "$ZMOS_DIR/session-progress.md"
        echo "  ✓ session-progress.md"
        MIGRATED=$((MIGRATED + 1))
    fi

    # Lesson outputs
    for LESSON in 1 2 3 4; do
        OLD_OUTPUTS="$OLD_DIR/lesson-$LESSON/outputs"
        NEW_OUTPUTS="$ZMOS_DIR/lesson-$LESSON/outputs"

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
        echo "  No user data found to migrate (fresh install in old folder)."
    fi

    echo ""
    echo "Migration complete. $MIGRATED file(s) transferred."
    echo "  Old folder preserved: $OLD_DIR"
    echo "  Backup: $BACKUP_DIR"
    echo ""

else
    echo "Setting up ZenithMind OS v$NEW_VERSION..."
    echo ""
fi

# ─── Register launcher + CLI command (all modes) ────────────────────────

# Save install path
echo "$ZMOS_DIR" > "$CONFIG_FILE"

# Create launcher command
mkdir -p "$BIN_DIR"
cat > "$LAUNCHER" << 'EOF'
#!/bin/bash
ZMOS_DIR=$(cat "$HOME/.zenithmind" 2>/dev/null)
if [ -z "$ZMOS_DIR" ] || [ ! -d "$ZMOS_DIR" ]; then
    echo "ZenithMind OS folder not found."
    echo "Open Claude Code from your ZenithMind-OS folder to re-run setup."
    exit 1
fi
cd "$ZMOS_DIR" && exec claude "$@"
EOF
chmod +x "$LAUNCHER"

# Ensure ~/.local/bin is in PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    if [ -f "$HOME/.zshrc" ]; then
        SHELL_RC="$HOME/.zshrc"
    elif [ -f "$HOME/.bashrc" ]; then
        SHELL_RC="$HOME/.bashrc"
    else
        SHELL_RC="$HOME/.profile"
    fi

    if ! grep -q '\.local/bin' "$SHELL_RC" 2>/dev/null; then
        echo '' >> "$SHELL_RC"
        echo '# ZenithMind OS' >> "$SHELL_RC"
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_RC"
    fi
fi

# Register ZenithMind as a global trigger in Claude Code
CLAUDE_MD="$HOME/.claude/CLAUDE.md"
MARKER="## ZenithMind OS"

if ! grep -q "$MARKER" "$CLAUDE_MD" 2>/dev/null; then
    mkdir -p "$HOME/.claude"
    cat >> "$CLAUDE_MD" << TRIGGER

$MARKER

**Trigger:** "zenithmind", "let's do zenithmind", "start zenithmind", "continue zenithmind", "let's continue zenithmind", "pick up zenithmind", "zenith mind"

When ANY of these triggers appear in the user's message:

1. Read \`~/.zenithmind\` to get the install path
2. \`cd\` into that folder
3. Read the \`CLAUDE.md\` at that path
4. Follow the **Session Start — Loading Protocol** in that CLAUDE.md
5. If the user said "continue" or "pick up" — check \`session-progress.md\` and resume where they left off
6. If the user said "start" or "let's do" — check progress and either start fresh or resume

**This works from ANY Claude Code session, ANY folder, ANY terminal.** The trigger phrase is the only thing needed.
TRIGGER
    echo "Registered ZenithMind as a global trigger in Claude Code."
else
    echo "ZenithMind trigger already registered in Claude Code."
fi

echo ""
echo "Setup complete!"
echo "  • Say 'zenithmind' in any Claude session to start or continue"
echo "  • Or type 'zenithmind' in any terminal"
