#!/bin/bash
# Double-click this file to migrate data from an older ZenithMind OS install.
cd "$(dirname "$0")"
bash upgrade.sh
echo ""
echo "You can close this window."
read -p "Press Enter to exit..."
