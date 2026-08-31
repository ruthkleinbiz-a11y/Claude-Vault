"""
Shared extraction helpers for dashboard scraping.

Analytics dashboards rewrite their markup often, so nothing here depends on
a single brittle CSS path. The general strategy is to find a *label* the
product shows the user ("Followers", "Page views") and read the nearest
number to it. Labels survive redesigns far better than class names do.

Every helper returns None rather than raising — one platform's redesign
must never abort the whole run.
"""

import re


# "1,234" · "12.3K" · "1.2M" · "45%" · "1:23" (duration)
_NUM_RE = re.compile(r"(\d[\d,]*\.?\d*)\s*([KMB%]?)", re.IGNORECASE)

_MULTIPLIER = {"K": 1_000, "M": 1_000_000, "B": 1_000_000_000}


def parse_number(text: str | None):
    """
    Pull the first number out of a blob of dashboard text.

    Returns an int for counts, a float for rates/decimals, or None.
    '12.3K' -> 12300 · '45%' -> 0.45 · '1,234' -> 1234
    """
    if not text:
        return None
    match = _NUM_RE.search(text.replace(" ", " "))
    if not match:
        return None

    raw, suffix = match.group(1), (match.group(2) or "").upper()
    try:
        value = float(raw.replace(",", ""))
    except ValueError:
        return None

    if suffix == "%":
        return round(value / 100, 4)
    if suffix in _MULTIPLIER:
        value *= _MULTIPLIER[suffix]

    return int(value) if value == int(value) else round(value, 2)


def metric_near_label(page, label_pattern: str, search_chars: int = 120):
    """
    Find text matching `label_pattern` and return the first number that
    appears near it — checking the element itself, then its parent, then
    the following sibling. That ordering covers the three layouts these
    dashboards actually use (number inside the tile, number beside the
    label, number stacked under it).
    """
    try:
        locator = page.locator(f"text=/{label_pattern}/i").first
        if locator.count() == 0:
            return None

        # 1. the labelled element itself
        own = locator.inner_text(timeout=3000)
        value = parse_number(_strip_label(own, label_pattern))
        if value is not None:
            return value

        # 2. its container
        parent = locator.locator("xpath=..")
        value = parse_number(_strip_label(parent.inner_text(timeout=3000)[:search_chars],
                                          label_pattern))
        if value is not None:
            return value

        # 3. the element right after it
        sibling = locator.locator("xpath=following-sibling::*[1]")
        if sibling.count():
            return parse_number(sibling.inner_text(timeout=3000)[:search_chars])
    except Exception:
        return None
    return None


def _strip_label(text: str, label_pattern: str) -> str:
    """Remove the label itself so we don't parse digits out of it."""
    if not text:
        return ""
    return re.sub(label_pattern, " ", text, flags=re.IGNORECASE)


def collect_metrics(page, spec: dict) -> dict:
    """
    Run a {output_key: label_regex} spec against a page.
    Missing metrics come back as None rather than being dropped, so the
    report can distinguish "zero" from "couldn't read it".
    """
    out = {}
    for key, pattern in spec.items():
        out[key] = metric_near_label(page, pattern)
    return out


def goto(page, url: str, wait_selector: str | None = None, timeout: int = 45000) -> bool:
    """Navigate and give client-rendered dashboards a chance to populate."""
    try:
        page.goto(url, timeout=timeout, wait_until="domcontentloaded")
    except Exception:
        return False

    if wait_selector:
        try:
            page.wait_for_selector(wait_selector, timeout=15000)
        except Exception:
            pass  # keep going — partial data beats none

    try:
        page.wait_for_timeout(2500)  # let async metric tiles settle
    except Exception:
        pass
    return True


def result(data: dict, error: str | None = None) -> dict:
    """Match the shape the API connectors return, so agent.py can merge them."""
    has_data = any(v is not None for v in (data or {}).values())
    return {
        "data": data if has_data else None,
        "error": error or (None if has_data else "No metrics could be read from the page"),
        "via": "browser",
    }
