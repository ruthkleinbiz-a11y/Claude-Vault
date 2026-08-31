"""Windsor.ai data fetcher — pulls organic analytics for all connected platforms."""

import os
import requests
from datetime import datetime, timedelta


BASE_URL = "https://api.windsor.ai/v1"


def _headers():
    return {"Authorization": f"Bearer {os.environ['WINDSOR_API_KEY']}"}


def _date_range(lookback_days: int) -> tuple[str, str]:
    end = datetime.utcnow().date()
    start = end - timedelta(days=lookback_days)
    return str(start), str(end)


def fetch_connector(connector_id: str, metrics: list[str], lookback_days: int = 14) -> dict:
    """Return aggregated metric totals for the given connector over the lookback window."""
    api_key = os.environ.get("WINDSOR_API_KEY")
    if not api_key:
        return {"connector": connector_id, "data": None, "error": "WINDSOR_API_KEY not set"}

    date_from, date_to = _date_range(lookback_days)
    params = {
        "api_key": api_key,
        "date_from": date_from,
        "date_to": date_to,
        "connector": connector_id,
        "fields": ",".join(metrics),
        "account_id": os.environ.get("WINDSOR_ACCOUNT_ID", ""),
    }
    try:
        resp = requests.get(f"{BASE_URL}/data", params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return {"connector": connector_id, "data": data, "error": None}
    except Exception as exc:
        return {"connector": connector_id, "data": None, "error": str(exc)}


def fetch_ga4_by_page_group(page_groups: dict, metrics: list[str], lookback_days: int = 14) -> dict:
    """Fetch GA4 data broken down by page group (blogs, quiz, lead magnets, other)."""
    api_key = os.environ.get("WINDSOR_API_KEY")
    date_from, date_to = _date_range(lookback_days)
    results = {}
    for group_name, path_pattern in page_groups.items():
        if not api_key:
            results[group_name] = {"data": None, "pattern": path_pattern,
                                   "error": "WINDSOR_API_KEY not set"}
            continue
        params = {
            "api_key": api_key,
            "date_from": date_from,
            "date_to": date_to,
            "connector": "googleanalytics4",
            "fields": ",".join(metrics) + ",page_path",
            "account_id": os.environ.get("WINDSOR_ACCOUNT_ID", ""),
        }
        try:
            resp = requests.get(f"{BASE_URL}/data", params=params, timeout=30)
            resp.raise_for_status()
            results[group_name] = {"data": resp.json(), "pattern": path_pattern, "error": None}
        except Exception as exc:
            results[group_name] = {"data": None, "pattern": path_pattern, "error": str(exc)}
    return results


def fetch_all(config: dict) -> dict:
    """Fetch data for all enabled Windsor connectors defined in config."""
    results = {}
    lookback = config["report"]["lookback_days"]

    for connector in config.get("windsor_connectors", []):
        if not connector.get("enabled"):
            continue
        cid = connector["id"]
        if cid == "googleanalytics4":
            results[cid] = fetch_ga4_by_page_group(
                connector.get("page_groups", {}),
                connector["metrics"],
                lookback,
            )
        else:
            results[cid] = fetch_connector(cid, connector["metrics"], lookback)

    return results
