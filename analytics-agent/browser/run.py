#!/usr/bin/env python3
"""
Browser-based analytics collection. Runs on Ruth's Mac, not in CI.

  python -m browser.run login      # sign in once (opens a visible Chrome)
  python -m browser.run check      # which sessions are still valid?
  python -m browser.run collect    # scrape everything (what the schedule runs)
  python -m browser.run collect --show --only hotjar,medium   # debug a platform

`collect` writes browser-data/latest.json and, unless --no-commit is passed,
commits and pushes it. The cloud agent picks that file up on its next run —
that handoff is what makes the hybrid setup work: this machine has the
logged-in browser, GitHub Actions has the schedule and the API keys.
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

from browser import session
from browser.collectors.platforms import COLLECTORS


AGENT_DIR = Path(__file__).resolve().parent.parent
OUT_DIR = AGENT_DIR / "browser-data"
OUT_FILE = OUT_DIR / "latest.json"
SHOTS_DIR = OUT_DIR / "screenshots"


def _lookback() -> int:
    try:
        with open(AGENT_DIR / "config.yml") as f:
            return yaml.safe_load(f)["report"]["lookback_days"]
    except Exception:
        return 14


def collect(only: list[str] | None = None, headless: bool = True,
            screenshot: bool = False) -> dict:
    targets = {k: v for k, v in COLLECTORS.items() if not only or k in only}
    lookback = _lookback()

    print("=" * 64)
    print("ZenithMind — browser collection")
    print(f"Run: {datetime.now(tz=timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"Platforms: {', '.join(targets)}")
    print("=" * 64)

    if not session.profile_exists():
        print("\nNo browser profile yet. Run this first:\n"
              "    python -m browser.run login\n")
        sys.exit(1)

    if screenshot:
        SHOTS_DIR.mkdir(parents=True, exist_ok=True)

    ctx = session.open_context(headless=headless)
    collected, failed = {}, []

    try:
        for key, fn in targets.items():
            page = ctx.new_page()
            try:
                print(f"[browser] {key}...", end=" ", flush=True)
                blob = fn(page, lookback)

                # search_atlas returns a nested structure, the rest are flat
                ok = (blob.get("data") is not None if "data" in blob
                      else any((v or {}).get("data") for v in blob.values()))

                collected[key] = blob
                if ok:
                    print("ok")
                else:
                    err = blob.get("error") if "data" in blob else "no data"
                    print(f"no data ({err})")
                    failed.append(key)

                if screenshot:
                    page.screenshot(path=str(SHOTS_DIR / f"{key}.png"), full_page=True)
            except Exception as exc:
                print(f"failed: {exc}")
                collected[key] = {"data": None, "error": str(exc), "via": "browser"}
                failed.append(key)
            finally:
                page.close()
    finally:
        session.close_context(ctx)

    payload = {
        "collected_at": datetime.now(tz=timezone.utc).isoformat(),
        "lookback_days": lookback,
        "platforms": collected,
        "failed": failed,
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_FILE, "w") as f:
        json.dump(payload, f, indent=2, default=str)

    print("=" * 64)
    print(f"Saved: {OUT_FILE}")
    if failed:
        print(f"No data from: {', '.join(failed)}")
        print("If these should be working, a session may have expired:")
        print("    python -m browser.run check")
    print("=" * 64)
    return payload


def commit_and_push():
    """Hand the scraped data to the cloud agent through the repo."""
    try:
        subprocess.run(["git", "add", str(OUT_FILE)], cwd=AGENT_DIR, check=True)
        status = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=AGENT_DIR)
        if status.returncode == 0:
            print("[git] browser data unchanged — nothing to push.")
            return

        stamp = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        subprocess.run(
            ["git", "commit", "-m", f"Browser analytics data — {stamp}"],
            cwd=AGENT_DIR, check=True,
        )
        branch = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=AGENT_DIR, capture_output=True, text=True, check=True,
        ).stdout.strip()
        subprocess.run(["git", "push", "origin", branch], cwd=AGENT_DIR, check=True)
        print(f"[git] pushed browser data to {branch}.")
    except subprocess.CalledProcessError as exc:
        print(f"[git] WARNING: could not push browser data: {exc}")


def main():
    ap = argparse.ArgumentParser(description="Browser-based analytics collection")
    ap.add_argument("command", choices=["login", "check", "collect"])
    ap.add_argument("--only", help="comma-separated platform keys")
    ap.add_argument("--show", action="store_true",
                    help="run with a visible browser (debugging)")
    ap.add_argument("--screenshot", action="store_true",
                    help="save a full-page screenshot per platform")
    ap.add_argument("--no-commit", action="store_true",
                    help="write the JSON but don't commit or push it")
    args = ap.parse_args()

    only = [s.strip() for s in args.only.split(",")] if args.only else None

    if args.command == "login":
        session.interactive_login(only)
    elif args.command == "check":
        print("Checking saved sessions...\n")
        for key, ok in session.check_sessions().items():
            label = session.PLATFORMS[key]["label"]
            print(f"  {'OK       ' if ok else 'SIGNED OUT'} {label}")
        print("\nRe-authorize any signed-out platform with:\n"
              "    python -m browser.run login --only <key>")
    else:
        collect(only=only, headless=not args.show, screenshot=args.screenshot)
        if not args.no_commit:
            commit_and_push()


if __name__ == "__main__":
    main()
