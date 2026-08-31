"""Hotjar analytics — visitor behavior, heatmaps, and session recordings."""

import os
from datetime import datetime, timedelta, timezone

import requests


BASE_URL = "https://api.hotjar.com"


def _headers() -> dict:
    token = os.environ.get("HOTJAR_API_KEY", "")
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }


def _date_range(lookback_days: int) -> tuple[str, str]:
    end = datetime.now(tz=timezone.utc).date()
    start = end - timedelta(days=lookback_days)
    return str(start), str(end)


def _get(path: str, params: dict = None) -> dict | list | None:
    try:
        resp = requests.get(f"{BASE_URL}{path}", headers=_headers(), params=params, timeout=20)
        resp.raise_for_status()
        return resp.json()
    except Exception as exc:
        return {"_error": str(exc)}


def fetch(site_id: str, lookback_days: int = 14) -> dict:
    """
    Pull visitor behavior data for a Hotjar site.

    site_id: your numeric Hotjar site ID (Settings → Sites → Site ID).
    Returns keys:
      visitors, sessions, pageviews,
      recordings_total, recordings_new,
      heatmaps_active,
      rage_click_pages, u_turn_pages,
      nps_score, nps_responses,
      feedback_rating, feedback_count
    """
    date_from, date_to = _date_range(lookback_days)

    # ---- Site-level daily stats ----
    stats_raw = _get(f"/v1/sites/{site_id}/daily_page_views", {
        "date_from": date_from,
        "date_to": date_to,
    })

    visitors, sessions, pageviews = None, None, None
    if isinstance(stats_raw, dict) and "data" in stats_raw:
        rows = stats_raw["data"]
        if isinstance(rows, list):
            visitors   = sum(int(r.get("visitors",  0) or 0) for r in rows)
            sessions   = sum(int(r.get("sessions",  0) or 0) for r in rows)
            pageviews  = sum(int(r.get("pageviews", 0) or 0) for r in rows)

    # ---- Recordings ----
    rec_raw = _get(f"/v1/sites/{site_id}/recordings", {
        "date_from": date_from,
        "date_to": date_to,
        "limit": 1,
    })
    recordings_total = None
    if isinstance(rec_raw, dict):
        recordings_total = rec_raw.get("total") or rec_raw.get("count")

    # ---- Heatmaps ----
    hm_raw = _get(f"/v1/sites/{site_id}/heatmaps", {"limit": 100})
    heatmaps_active = None
    if isinstance(hm_raw, dict) and "data" in hm_raw:
        active = [h for h in (hm_raw["data"] or []) if h.get("status") == "active"]
        heatmaps_active = len(active)

    # ---- NPS / Polls ----
    nps_score, nps_responses, feedback_rating, feedback_count = None, None, None, None
    polls_raw = _get(f"/v1/sites/{site_id}/polls")
    if isinstance(polls_raw, dict) and "data" in polls_raw:
        for poll in (polls_raw["data"] or []):
            ptype = (poll.get("type") or "").lower()
            if "nps" in ptype:
                nps_score = poll.get("nps_score") or poll.get("average")
                nps_responses = poll.get("responses_count")
            elif "rating" in ptype or "satisfaction" in ptype:
                feedback_rating = poll.get("average")
                feedback_count  = poll.get("responses_count")

    # ---- Rage / U-turn signals (from recordings filters) ----
    rage_click_pages, u_turn_pages = None, None
    signals_raw = _get(f"/v1/sites/{site_id}/recordings/summary", {
        "date_from": date_from,
        "date_to": date_to,
    })
    if isinstance(signals_raw, dict):
        rage_click_pages = signals_raw.get("rage_click_count") or signals_raw.get("rage_clicks")
        u_turn_pages     = signals_raw.get("u_turn_count")     or signals_raw.get("u_turns")

    data = {
        "visitors":          visitors,
        "sessions":          sessions,
        "pageviews":         pageviews,
        "recordings_total":  recordings_total,
        "heatmaps_active":   heatmaps_active,
        "rage_click_pages":  rage_click_pages,
        "u_turn_pages":      u_turn_pages,
        "nps_score":         nps_score,
        "nps_responses":     nps_responses,
        "feedback_rating":   feedback_rating,
        "feedback_count":    feedback_count,
    }

    has_data = any(v is not None for k, v in data.items() if not k.startswith("_"))
    return {
        "data":  data if has_data else None,
        "error": None if has_data else "No Hotjar data returned — check HOTJAR_API_KEY and HOTJAR_SITE_ID.",
    }
