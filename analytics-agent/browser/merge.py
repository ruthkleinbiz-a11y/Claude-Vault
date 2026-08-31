"""
Merges browser-collected data into the API-collected data.

The hybrid split means a platform can arrive from either side. The rule is
simple and deliberate: an API value always wins, because Windsor's numbers
come from the platforms' own reporting APIs, while a scraped number is read
off a rendered dashboard and is the more fragile of the two. The browser
fills the gaps — platforms with no API key, and platforms whose connector
returned nothing this period.

`agent.py` calls this after collect_all_data().
"""

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path


BROWSER_DATA = Path(__file__).resolve().parent.parent / "browser-data" / "latest.json"

# Past this age the scraped file is stale enough that reporting it as
# current would be misleading — the biweekly cycle is 14 days.
MAX_AGE_DAYS = 16


def _has_data(blob) -> bool:
    if not isinstance(blob, dict):
        return False
    if "data" in blob:
        return blob.get("data") is not None
    # nested shape (search_atlas)
    return any(isinstance(v, dict) and v.get("data") for v in blob.values())


def load_browser_data() -> tuple[dict, str | None]:
    """Return (platforms, note). An unusable file yields ({}, reason)."""
    if not BROWSER_DATA.exists():
        return {}, "No browser data file — run `python -m browser.run collect` on the Mac."

    try:
        with open(BROWSER_DATA) as f:
            payload = json.load(f)
    except Exception as exc:
        return {}, f"Browser data unreadable: {exc}"

    collected_at = payload.get("collected_at")
    if collected_at:
        try:
            when = datetime.fromisoformat(collected_at)
            age = datetime.now(tz=timezone.utc) - when
            if age > timedelta(days=MAX_AGE_DAYS):
                return {}, (f"Browser data is {age.days} days old "
                            f"(cutoff {MAX_AGE_DAYS}) — ignoring it as stale.")
        except ValueError:
            pass

    return payload.get("platforms", {}), None


def merge(all_data: dict) -> dict:
    """Fill gaps in all_data from the browser payload. API values win."""
    browser, note = load_browser_data()
    if note:
        print(f"[browser] {note}")
        return all_data
    if not browser:
        print("[browser] No browser platforms present.")
        return all_data

    filled, skipped = [], []
    for key, blob in browser.items():
        if not _has_data(blob):
            continue
        if _has_data(all_data.get(key)):
            skipped.append(key)   # API already supplied it
        else:
            all_data[key] = blob
            filled.append(key)

    if filled:
        print(f"[browser] Filled from browser: {', '.join(filled)}")
    if skipped:
        print(f"[browser] API data preferred over browser for: {', '.join(skipped)}")

    return all_data
