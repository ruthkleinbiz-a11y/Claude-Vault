"""
Search Atlas SEO connector — keyword rankings, competitor analysis,
domain authority, and backlink overview.

Accessed via the Search Atlas REST API (api.searchatlas.com).
Your API key lives under Search Atlas → Account → API Access.
The GoHighLevel integration uses the same key — copy it from
HighLevel → Settings → Integrations → Search Atlas.
"""

import os
from datetime import datetime, timedelta, timezone

import requests


BASE_URL = "https://api.searchatlas.com/v1"


def _headers() -> dict:
    return {
        "Authorization": f"Bearer {os.environ.get('SEARCH_ATLAS_API_KEY', '')}",
        "Accept": "application/json",
    }


def _get(path: str, params: dict = None) -> dict | None:
    try:
        resp = requests.get(f"{BASE_URL}{path}", headers=_headers(), params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except Exception as exc:
        return {"_error": str(exc)}


def _post(path: str, body: dict) -> dict | None:
    try:
        resp = requests.post(f"{BASE_URL}{path}", headers={**_headers(), "Content-Type": "application/json"},
                             json=body, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except Exception as exc:
        return {"_error": str(exc)}


def fetch_rankings(domain: str, tracked_keywords: list[str]) -> dict:
    """
    Current position for each tracked keyword + movement vs previous check.
    Returns list of {keyword, position, prev_position, change, search_volume, url}.
    """
    raw = _get("/rank-tracker/keywords", {"domain": domain, "limit": 200})
    if not isinstance(raw, dict) or "_error" in raw:
        return {"data": None, "error": raw.get("_error") if isinstance(raw, dict) else "API error"}

    keywords = raw.get("data") or raw.get("keywords") or raw.get("results") or []

    # Filter to tracked keywords if supplied, otherwise return all
    if tracked_keywords:
        kw_set = {k.lower() for k in tracked_keywords}
        keywords = [k for k in keywords if (k.get("keyword") or "").lower() in kw_set]

    rankings = []
    for kw in keywords[:50]:  # cap at 50 for report length
        pos      = kw.get("position") or kw.get("rank")
        prev_pos = kw.get("previous_position") or kw.get("prev_rank")
        change   = None
        if pos is not None and prev_pos is not None:
            change = int(prev_pos) - int(pos)  # positive = moved up

        rankings.append({
            "keyword":       kw.get("keyword", ""),
            "position":      pos,
            "prev_position": prev_pos,
            "change":        change,
            "search_volume": kw.get("search_volume") or kw.get("volume"),
            "url":           kw.get("url") or kw.get("landing_page"),
            "difficulty":    kw.get("keyword_difficulty") or kw.get("kd"),
        })

    rankings.sort(key=lambda r: (r["position"] or 999))
    return {"data": rankings, "error": None}


def fetch_domain_overview(domain: str) -> dict:
    """Domain authority, organic traffic estimate, backlinks, referring domains."""
    raw = _get("/domain-overview", {"domain": domain})
    if not isinstance(raw, dict) or "_error" in raw:
        return {"data": None, "error": raw.get("_error") if isinstance(raw, dict) else "API error"}

    data = raw.get("data") or raw
    return {
        "data": {
            "domain_authority":   data.get("domain_authority") or data.get("da"),
            "organic_traffic":    data.get("organic_traffic")  or data.get("est_traffic"),
            "organic_keywords":   data.get("organic_keywords") or data.get("keywords"),
            "backlinks":          data.get("backlinks")        or data.get("total_backlinks"),
            "referring_domains":  data.get("referring_domains"),
        },
        "error": None,
    }


def fetch_competitors(domain: str, competitors: list[str]) -> dict:
    """
    Side-by-side comparison of domain vs competitors on key SEO metrics.
    Each entry: {domain, da, organic_traffic, organic_keywords, backlinks}.
    """
    all_domains = [domain] + (competitors or [])
    rows = []
    for d in all_domains[:6]:  # cap at 6 domains
        raw = _get("/domain-overview", {"domain": d})
        if not isinstance(raw, dict) or "_error" in raw:
            rows.append({"domain": d, "error": True})
            continue
        data = raw.get("data") or raw
        rows.append({
            "domain":           d,
            "is_target":        d == domain,
            "da":               data.get("domain_authority") or data.get("da"),
            "organic_traffic":  data.get("organic_traffic")  or data.get("est_traffic"),
            "organic_keywords": data.get("organic_keywords") or data.get("keywords"),
            "backlinks":        data.get("backlinks")        or data.get("total_backlinks"),
            "referring_domains":data.get("referring_domains"),
        })
    return {"data": rows, "error": None}


def fetch_keyword_opportunities(domain: str, seed_keywords: list[str]) -> dict:
    """
    Keywords the domain could rank for but currently doesn't — quick wins.
    Returns list of {keyword, search_volume, difficulty, opportunity_score}.
    """
    body = {"domain": domain, "seeds": seed_keywords[:20], "limit": 30}
    raw = _post("/keyword-gap", body)
    if not isinstance(raw, dict) or "_error" in raw:
        # Fallback: try keyword suggestions endpoint
        raw = _get("/keyword-suggestions", {"domain": domain, "limit": 30})

    if not isinstance(raw, dict) or "_error" in raw:
        return {"data": None, "error": raw.get("_error") if isinstance(raw, dict) else "API error"}

    items = raw.get("data") or raw.get("keywords") or []
    opps = []
    for kw in items[:20]:
        opps.append({
            "keyword":          kw.get("keyword", ""),
            "search_volume":    kw.get("search_volume") or kw.get("volume"),
            "difficulty":       kw.get("keyword_difficulty") or kw.get("kd"),
            "opportunity_score":kw.get("opportunity_score") or kw.get("score"),
            "intent":           kw.get("intent") or kw.get("search_intent"),
        })
    return {"data": opps, "error": None}


def fetch_all(config: dict) -> dict:
    """Entry point called by agent.py. Pulls all Search Atlas data in one shot."""
    cfg = config.get("search_atlas", {})
    if not cfg.get("enabled"):
        return {}

    domain      = cfg.get("domain", "ruthklein.com")
    competitors = cfg.get("competitors", [])
    keywords    = cfg.get("tracked_keywords", [])
    seeds       = cfg.get("seed_keywords", [])

    print(f"[agent] Fetching Search Atlas for {domain}...")
    results = {}

    results["rankings"]     = fetch_rankings(domain, keywords)
    results["overview"]     = fetch_domain_overview(domain)
    results["competitors"]  = fetch_competitors(domain, competitors)
    results["opportunities"]= fetch_keyword_opportunities(domain, seeds)

    return results
