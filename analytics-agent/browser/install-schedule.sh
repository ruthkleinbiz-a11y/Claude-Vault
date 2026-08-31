#!/bin/bash
# Installs the biweekly browser collection schedule on macOS (launchd).
#
# Runs on the 1st and 15th at 6:00 AM — one hour before the GitHub Actions
# job at 7:00 UTC, so the scraped data is committed and waiting by the time
# the cloud agent builds the report.
#
#   bash browser/install-schedule.sh            # install
#   bash browser/install-schedule.sh --uninstall

set -euo pipefail

LABEL="com.ruthklein.analytics-browser"
PLIST="$HOME/Library/LaunchAgents/${LABEL}.plist"
AGENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="$HOME/.zenithmind/logs"

if [[ "${1:-}" == "--uninstall" ]]; then
  launchctl unload "$PLIST" 2>/dev/null || true
  rm -f "$PLIST"
  echo "Removed the browser collection schedule."
  exit 0
fi

if [[ "$(uname)" != "Darwin" ]]; then
  echo "This installer is macOS-only (launchd)."
  echo "On Linux, use cron:  0 6 1,15 * * cd $AGENT_DIR && python -m browser.run collect"
  exit 1
fi

PYTHON="$(command -v python3 || true)"
if [[ -z "$PYTHON" ]]; then
  echo "python3 not found on PATH."
  exit 1
fi

mkdir -p "$LOG_DIR" "$HOME/Library/LaunchAgents"

cat > "$PLIST" <<PLISTEOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>${LABEL}</string>

  <key>ProgramArguments</key>
  <array>
    <string>${PYTHON}</string>
    <string>-m</string>
    <string>browser.run</string>
    <string>collect</string>
  </array>

  <key>WorkingDirectory</key>
  <string>${AGENT_DIR}</string>

  <!-- 1st and 15th at 6:00 AM, an hour ahead of the cloud report job -->
  <key>StartCalendarInterval</key>
  <array>
    <dict>
      <key>Day</key><integer>1</integer>
      <key>Hour</key><integer>6</integer>
      <key>Minute</key><integer>0</integer>
    </dict>
    <dict>
      <key>Day</key><integer>15</integer>
      <key>Hour</key><integer>6</integer>
      <key>Minute</key><integer>0</integer>
    </dict>
  </array>

  <!-- If the Mac was asleep at 6am, run once it wakes -->
  <key>RunAtLoad</key>
  <false/>

  <key>StandardOutPath</key>
  <string>${LOG_DIR}/browser-collect.log</string>
  <key>StandardErrorPath</key>
  <string>${LOG_DIR}/browser-collect.error.log</string>
</dict>
</plist>
PLISTEOF

launchctl unload "$PLIST" 2>/dev/null || true
launchctl load "$PLIST"

echo "Installed: $LABEL"
echo "  Schedule: 1st and 15th at 6:00 AM"
echo "  Working dir: $AGENT_DIR"
echo "  Logs: $LOG_DIR/browser-collect.log"
echo
echo "Test it now without waiting for the schedule:"
echo "  launchctl start $LABEL && tail -f $LOG_DIR/browser-collect.log"
