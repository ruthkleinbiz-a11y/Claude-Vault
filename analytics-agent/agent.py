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

from connectors import windsor, twitter as twitter_connector, manual_import, hotjar, search_atlas
from report import generator
from sheets import writer as sheets_writer
from drive import uploader as drive_uploader
from dashboard import extractor as dash_extractor
from browser import merge as browser_merge


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

    hj_cfg = config.get("hotjar", {})
    if hj_cfg.get("enabled"):
        site_id = hj_cfg.get("site_id") or os.environ.get("HOTJAR_SITE_ID", "")
        if site_id:
            print(f"[agent] Fetching Hotjar for site {site_id}...")
            all_data["hotjar"] = hotjar.fetch(site_id, config["report"]["lookback_days"])
        else:
            print("[agent] Hotjar: HOTJAR_SITE_ID not set — skipping.")

    sa_data = search_atlas.fetch_all(config)
    if sa_data:
        all_data["search_atlas"] = sa_data

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

    # Fill any remaining gaps from the Mac's browser collection run.
    # API values always win; this only covers what the APIs couldn't supply.
    print("[agent] Merging browser-collected data...")
    all_data = browser_merge.merge(all_data)

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

    # 4. Upload PDF to Google Drive
    print("[agent] Uploading PDF to Google Drive...")
    try:
        drive_url = drive_uploader.upload_report(pdf_path)
        print(f"[agent] Drive link: {drive_url}")
    except Exception as exc:
        print(f"[drive] WARNING: {exc}")

    # 5. Write dashboard data JSON for artifact auto-update
    print("[agent] Writing dashboard data...")
    dash_data = dash_extractor.build_dash_data(all_data, analysis, config)
    dash_extractor.save_dash_data(dash_data, str(REPORTS_DIR / "dashboard-data.json"))

    # 6. Save data snapshot for next period comparison
    save_to_history(all_data)

    print("=" * 60)
    print(f"Done. Report saved to: {pdf_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
