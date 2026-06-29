#!/usr/bin/env python3
"""
Ruth Klein — Biweekly Analytics Review Agent
Run manually: python agent.py
Scheduled via GitHub Actions every 2 weeks.
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml
from dotenv import load_dotenv

# Load .env (local runs). GitHub Actions uses repo secrets instead.
load_dotenv(Path(__file__).parent / ".env")

from connectors import windsor, twitter as twitter_connector, manual_import
from report import generator
from sheets import writer as sheets_writer
from email import sender as email_sender


REPORTS_DIR = Path(__file__).parent / "reports"
HISTORY_FILE = Path(__file__).parent / "reports" / "history.json"


def load_config() -> dict:
    with open(Path(__file__).parent / "config.yml") as f:
        return yaml.safe_load(f)


def load_previous_data() -> dict | None:
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE) as f:
            history = json.load(f)
        if history:
            return history[-1].get("data")
    return None


def save_to_history(all_data: dict):
    REPORTS_DIR.mkdir(exist_ok=True)
    history = []
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE) as f:
            history = json.load(f)
    history.append({
        "run_at": datetime.now(tz=timezone.utc).isoformat(),
        "data": all_data,
    })
    # Keep last 12 runs (6 months of biweekly data)
    history = history[-12:]
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2, default=str)


def collect_all_data(config: dict) -> dict:
    all_data = {}

    print("[agent] Fetching Windsor.ai platforms...")
    windsor_data = windsor.fetch_all(config)
    all_data.update(windsor_data)

    if config.get("twitter", {}).get("enabled"):
        username = config["twitter"]["username"] or os.environ.get("TWITTER_USERNAME", "")
        if username:
            print(f"[agent] Fetching Twitter/X for @{username}...")
            all_data["twitter"] = twitter_connector.fetch(
                username, config["report"]["lookback_days"]
            )
        else:
            print("[agent] Twitter: TWITTER_USERNAME not set — skipping.")

    manual_cfg = config.get("manual_imports", {})

    if manual_cfg.get("medium", {}).get("enabled"):
        print("[agent] Loading Medium CSV...")
        all_data["medium"] = manual_import.fetch_medium(
            manual_cfg["medium"].get("metrics", [])
        )

    if manual_cfg.get("substack", {}).get("enabled"):
        print("[agent] Loading Substack CSV...")
        all_data["substack"] = manual_import.fetch_substack(
            manual_cfg["substack"].get("metrics", [])
        )

    return all_data


def main():
    print("=" * 60)
    print("Ruth Klein Analytics Agent")
    print(f"Run: {datetime.now(tz=timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print("=" * 60)

    config = load_config()
    previous_data = load_previous_data()

    # 1. Collect data from all platforms
    all_data = collect_all_data(config)

    # 2. Write to Google Sheets
    print("[agent] Writing to Google Sheets...")
    try:
        sheets_writer.append_row(all_data)
    except Exception as exc:
        print(f"[sheets] WARNING: {exc}")

    # 3. Generate Claude analysis + PDF
    print("[agent] Analyzing with Claude...")
    analysis = generator.analyze_with_claude(all_data, previous_data, config)

    REPORTS_DIR.mkdir(exist_ok=True)
    run_date = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
    pdf_path = str(REPORTS_DIR / f"analytics-report-{run_date}.pdf")

    print("[agent] Generating PDF...")
    generator.generate_pdf(analysis, all_data, config, pdf_path)

    # 4. Email the report
    print("[agent] Emailing report...")
    try:
        email_sender.send_report(pdf_path, config)
    except Exception as exc:
        print(f"[email] WARNING: {exc}")

    # 5. Save data snapshot for next period comparison
    save_to_history(all_data)

    print("=" * 60)
    print(f"Done. Report saved to: {pdf_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
