"""
Translates raw all_data + analysis text into a dashboard-data.json
that matches the DASH shape expected by the Weekly Signal artifact.
"""

import json
import re
from datetime import datetime, timezone, timedelta


def _safe(d: dict, *keys, default=None):
    for k in keys:
        if not isinstance(d, dict):
            return default
        d = d.get(k, default)
    return d


def _pct(val) -> float | None:
    if val is None:
        return None
    if isinstance(val, str) and val.endswith("%"):
        try:
            return float(val.rstrip("%"))
        except ValueError:
            return None
    try:
        f = float(val)
        return round(f * 100, 1) if f < 1 else round(f, 1)
    except (TypeError, ValueError):
        return None


def _num(val) -> int | float | None:
    if val is None:
        return None
    try:
        f = float(val)
        return int(f) if f == int(f) else round(f, 2)
    except (TypeError, ValueError):
        return None


def _connector_val(all_data: dict, connector_id: str, metric: str):
    blob = all_data.get(connector_id, {})
    data = blob.get("data") or {}
    if isinstance(data, list):
        # Windsor returns a list of rows; sum the metric across all rows
        total = sum(float(row.get(metric, 0) or 0) for row in data if isinstance(row, dict))
        return total if total else None
    return _num(data.get(metric))


def _platform_entry(all_data: dict, platform_id: str, metrics_map: list[tuple[str, str]]) -> dict:
    """Build a platform object with metric values filled in where available."""
    result = {}
    for display_name, field in metrics_map:
        val = _connector_val(all_data, platform_id, field)
        result[display_name] = val
    return result


def build_dash_data(all_data: dict, analysis: str, config: dict) -> dict:
    now = datetime.now(tz=timezone.utc)
    lookback = config["report"]["lookback_days"]
    period_end = now.date()
    period_start = period_end - timedelta(days=lookback)

    def platform(pid, metrics_map):
        vals = {}
        for k, field in metrics_map:
            vals[k] = _connector_val(all_data, pid, field)
        return vals

    # ---- per-platform metrics ----
    ig = platform("instagram", [
        ("Followers", "followers"), ("Accounts reached", "reach"),
        ("Profile visits", "profile_views"), ("Interactions", "impressions"),
    ])
    fb = platform("facebook", [
        ("Page followers", "page_fans"), ("Reach", "reach"),
        ("Post engagements", "post_engagements"), ("Posts published", "posts_count"),
    ])
    yt = platform("youtube", [
        ("Subscribers", "subscribers"), ("Views", "views"),
        ("Watch time (hrs)", "watch_time_minutes"), ("Videos published", "video_count"),
    ])
    if yt.get("Watch time (hrs)") is not None:
        yt["Watch time (hrs)"] = round(yt["Watch time (hrs)"] / 60, 1)

    tt = platform("tiktok_organic", [
        ("Followers", "followers"), ("Video views", "video_views"),
        ("Profile views", "profile_views"), ("Likes", "likes"),
    ])
    pin = platform("pinterest", [
        ("Impressions", "impressions"), ("Saves", "saves"),
        ("Outbound clicks", "outbound_clicks"), ("Pin clicks", "pin_clicks"),
    ])

    # GA4 — aggregate across all page groups
    ga4_sessions, ga4_users, ga4_new_users = 0, 0, 0
    for group in ["blogs", "quiz", "lead_magnets", "other"]:
        ga4_sessions += _connector_val(all_data, "googleanalytics4", "sessions") or 0
        ga4_users    += _connector_val(all_data, "googleanalytics4", "users") or 0

    ghl = platform("gohighlevel", [
        ("Emails sent", "emails_sent"), ("Open rate", "open_rate"),
        ("Click rate", "click_rate"), ("Unsubscribes", "unsubscribes"),
    ])
    if ghl.get("Open rate") is not None:
        ghl["Open rate"] = _pct(ghl["Open rate"])

    # twitter
    tw_blob = all_data.get("twitter", {})
    tw_data = tw_blob.get("data") or {}
    tw = {
        "Followers": _num(tw_data.get("followers")),
        "Impressions": _num(tw_data.get("impressions")),
        "Engagements": _num(tw_data.get("engagements")),
        "Posts": _num(tw_data.get("posts")),
    }

    # manual imports
    med_blob = all_data.get("medium", {})
    med_data = med_blob.get("data") or {}
    med = {
        "Followers": _num(med_data.get("followers")),
        "Views": _num(med_data.get("views")),
        "Reads": _num(med_data.get("reads")),
        "Read ratio": _pct(med_data.get("read_ratio")),
    }
    sub_blob = all_data.get("substack", {})
    sub_data = sub_blob.get("data") or {}
    sub = {
        "Total subscribers": _num(sub_data.get("total_subscribers")),
        "New subscribers": _num(sub_data.get("new_subscribers")),
        "Open rate": _pct(sub_data.get("open_rate")),
        "Post views": _num(sub_data.get("views")),
    }

    def status(vals: dict) -> str:
        return "ok" if any(v is not None for v in vals.values()) else "pending"

    def metrics_list(vals: dict) -> list:
        return [{"k": k, "v": v} for k, v in vals.items()]

    def glance_total(*fields_and_connectors) -> int | None:
        total = 0
        found = False
        for connector_id, field in fields_and_connectors:
            v = _connector_val(all_data, connector_id, field)
            if v is not None:
                total += v
                found = True
        return int(total) if found else None

    total_audience = glance_total(
        ("instagram", "followers"), ("facebook", "page_fans"),
        ("youtube", "subscribers"), ("tiktok_organic", "followers"),
    )

    total_engagement = glance_total(
        ("facebook", "post_engagements"), ("tiktok_organic", "likes"),
    )

    # ---- email stats ----
    email_stats = []
    if ghl.get("Emails sent") is not None:
        email_stats.append({"k": "Emails sent", "v": ghl["Emails sent"], "color": "var(--orange)"})
    if ghl.get("Open rate") is not None:
        email_stats.append({"k": "Open rate", "v": ghl["Open rate"], "unit": "%", "deltaUnit": "pp", "color": "var(--pink)"})
    if ghl.get("Click rate") is not None:
        email_stats.append({"k": "Click rate", "v": ghl["Click rate"], "unit": "%", "deltaUnit": "pp", "color": "var(--blue)"})

    # ---- GA4 website stats ----
    website_stats = []
    if ga4_sessions:
        website_stats.append({"k": "Sessions", "v": int(ga4_sessions), "color": "var(--lime)"})
    if ga4_users:
        website_stats.append({"k": "Active users", "v": int(ga4_users), "color": "var(--teal)"})

    return {
        "generated": now.strftime("%d %b %Y, %H:%M UTC"),
        "periodStart": str(period_start),
        "periodEnd": str(period_end),
        "periodLabel": f"Period {period_start.strftime('%-d')}–{period_end.strftime('%-d %b %Y')}",
        "firstRun": None,
        "runNote": None,

        "glance": [
            {"label": "Total audience",      "value": total_audience,  "unit": "", "fill": "var(--pink)",   "onFill": "#fff",    "foot": "Followers + subscribers across all channels"},
            {"label": "Biweekly engagement", "value": total_engagement,"unit": "", "fill": "var(--blue)",   "onFill": "#fff",    "foot": "Reactions, comments, shares, claps and replies"},
            {"label": "Website sessions",    "value": int(ga4_sessions) if ga4_sessions else None, "unit": "", "fill": "var(--teal)", "onFill": "#04322E", "foot": "ruthklein.com via Google Analytics 4"},
            {"label": "Biggest mover",       "value": None,            "unit": "", "fill": "var(--yellow)", "onFill": "#3D2A00", "foot": "Channel with the largest period-over-period swing"},
        ],

        "platforms": [
            {"id": "facebook",  "name": "Facebook Page",    "handle": "/ruthklein",          "chip": "var(--blue)",   "url": "https://www.facebook.com/ruthklein",                    "analytics": "Windsor.ai → facebook",        "analyticsUrl": "https://app.windsor.ai/", "status": status(fb),  "metrics": metrics_list(fb)},
            {"id": "instagram", "name": "Instagram",        "handle": "@ruth.klein",          "chip": "var(--pink)",   "url": "https://www.instagram.com/ruth.klein/",                 "analytics": "Windsor.ai → instagram",       "analyticsUrl": "https://app.windsor.ai/", "status": status(ig),  "metrics": metrics_list(ig)},
            {"id": "x",         "name": "X / Twitter",      "handle": "@RuthKlein",           "chip": "var(--violet)", "url": "https://x.com/RuthKlein",                               "analytics": "Tweepy API",                   "analyticsUrl": "https://analytics.x.com/","status": status(tw),  "metrics": metrics_list(tw)},
            {"id": "youtube",   "name": "YouTube",          "handle": "@RuthKleinBiz",        "chip": "var(--red)",    "url": "https://www.youtube.com/user/RuthKleinBiz",             "analytics": "Windsor.ai → youtube",         "analyticsUrl": "https://app.windsor.ai/", "status": status(yt),  "metrics": metrics_list(yt)},
            {"id": "tiktok",    "name": "TikTok",           "handle": "@ruthklein",           "chip": "var(--lime)",   "url": "https://www.tiktok.com/@ruthklein",                     "analytics": "Windsor.ai → tiktok_organic",  "analyticsUrl": "https://app.windsor.ai/", "status": status(tt),  "metrics": metrics_list(tt)},
            {"id": "pinterest", "name": "Pinterest",        "handle": "@ruthklein",           "chip": "var(--red)",    "url": "https://www.pinterest.com/ruthklein/",                  "analytics": "Windsor.ai → pinterest",       "analyticsUrl": "https://app.windsor.ai/", "status": status(pin), "metrics": metrics_list(pin)},
            {"id": "substack",  "name": "Substack",         "handle": "Sacred Energy of Time","chip": "var(--orange)", "url": "https://thesacredenergyoftime.substack.com/",           "analytics": "Manual CSV → Substack Stats",  "analyticsUrl": "https://thesacredenergyoftime.substack.com/publish/stats", "status": status(sub), "metrics": metrics_list(sub)},
            {"id": "medium",    "name": "Medium",           "handle": "@ruthkleinbiz",        "chip": "var(--lime)",   "url": "https://ruthkleinbiz.medium.com/",                      "analytics": "Manual CSV → Medium Stats",    "analyticsUrl": "https://medium.com/me/stats", "status": status(med), "metrics": metrics_list(med)},
            {"id": "ga4",       "name": "ruthklein.com",    "handle": "Google Analytics 4",   "chip": "var(--teal)",   "url": "https://analytics.google.com/analytics/web/#/a15364784p361216511/reports/intelligenthome", "analytics": "Windsor.ai → googleanalytics4", "analyticsUrl": "https://app.windsor.ai/", "status": "ok" if ga4_sessions else "pending", "metrics": [{"k": "Sessions", "v": int(ga4_sessions) if ga4_sessions else None}, {"k": "Active users", "v": int(ga4_users) if ga4_users else None}, {"k": "New users", "v": None}, {"k": "Engagement rate", "v": None}]},
        ],

        "topPosts": [],

        "resonance": {"themes": [], "formats": [], "timing": [], "takeaways": []},

        "email": {
            "stats": email_stats,
            "campaigns": [],
            "lists": [],
            "takeaways": [],
            "sources": [
                {"name": "GoHighLevel — email campaigns (primary)", "handle": "Ruth Klein account", "url": "https://app.gohighlevel.com/", "analytics": "Windsor.ai → gohighlevel", "analyticsUrl": "https://app.windsor.ai/", "status": status(ghl), "note": "Opens, clicks, delivered, unsubscribes via Windsor.ai connector."},
                {"name": "Substack — The Sacred Energy of Time", "handle": "thesacredenergyoftime.substack.com", "url": "https://thesacredenergyoftime.substack.com/", "analytics": "Manual CSV import", "analyticsUrl": "https://thesacredenergyoftime.substack.com/publish/stats/emails", "status": status(sub), "note": "Drop a CSV export in analytics-agent/manual-imports/ before each run."},
            ],
        },

        "website": {
            "stats": website_stats,
            "pages": [],
            "channels": [],
            "countries": [],
        },

        "history": {},
    }


def save_dash_data(dash: dict, path: str):
    with open(path, "w") as f:
        json.dump(dash, f, indent=2, default=str)
    print(f"[dashboard] Saved dashboard data: {path}")
