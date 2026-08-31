"""
Per-platform browser collectors.

Each function takes a Playwright page and returns the same
{"data": {...}, "error": ..., "via": "browser"} shape the API connectors
use, so agent.py can merge either source without special-casing.

Metric keys deliberately match the API connectors' keys — that way the
report, the summary table, and the dashboard extractor need no changes
regardless of which path supplied the number.
"""

from .common import collect_metrics, goto, metric_near_label, result


def hotjar(page, lookback_days: int = 14) -> dict:
    """Hotjar — the one with no workable API key. Visitor behavior + feedback."""
    if not goto(page, "https://insights.hotjar.com/", "text=/dashboard|sites/i"):
        return result({}, "Could not open Hotjar")

    data = collect_metrics(page, {
        "sessions":         r"sessions?",
        "pageviews":        r"page ?views?",
        "visitors":         r"(unique )?(visitors|users)",
        "recordings_total": r"recordings?",
    })

    # Heatmaps and feedback live on their own tabs
    if goto(page, "https://insights.hotjar.com/heatmaps"):
        data["heatmaps_active"] = metric_near_label(page, r"active|heatmaps?")

    if goto(page, "https://insights.hotjar.com/feedback"):
        data["nps_score"] = metric_near_label(page, r"nps|net promoter")
        data["feedback_rating"] = metric_near_label(page, r"average|rating")
        data["feedback_count"] = metric_near_label(page, r"responses?|submissions?")

    return result(data)


def medium(page, lookback_days: int = 14) -> dict:
    """Medium — replaces the manual CSV drop."""
    if not goto(page, "https://medium.com/me/stats", "text=/views|reads/i"):
        return result({}, "Could not open Medium stats")

    data = collect_metrics(page, {
        "views":     r"views",
        "reads":     r"reads",
        "followers": r"followers",
        "claps":     r"claps|fans",
    })

    if data.get("views") and data.get("reads"):
        try:
            data["read_ratio"] = round(data["reads"] / data["views"], 4)
        except ZeroDivisionError:
            data["read_ratio"] = None

    return result(data)


def substack(page, lookback_days: int = 14) -> dict:
    """Substack — The Sacred Energy of Time. Replaces the manual CSV drop."""
    base = "https://thesacredenergyoftime.substack.com/publish/stats"
    if not goto(page, base, "text=/subscribers|opens/i"):
        return result({}, "Could not open Substack stats")

    data = collect_metrics(page, {
        "total_subscribers": r"total subscribers|all subscribers|subscribers",
        "new_subscribers":   r"new subscribers|net new",
        "open_rate":         r"open rate",
        "views":             r"views",
    })

    if goto(page, base + "/subscribers"):
        data["paid_subscribers"] = metric_near_label(page, r"paid")
        data["free_subscribers"] = metric_near_label(page, r"free")

    return result(data)


def highlevel(page, lookback_days: int = 14) -> dict:
    """
    HighLevel email stats. Windsor already covers this via the gohighlevel
    connector — this is the fallback for when that connector has no data.
    """
    if not goto(page, "https://app.gohighlevel.com/", "text=/dashboard|marketing/i"):
        return result({}, "Could not open HighLevel")

    data = collect_metrics(page, {
        "emails_sent":  r"sent|delivered",
        "open_rate":    r"open rate|opened",
        "click_rate":   r"click(-| )?(through )?rate|clicked",
        "unsubscribes": r"unsubscribes?|opt(-| )?outs?",
    })
    return result(data)


def search_atlas(page, lookback_days: int = 14) -> dict:
    """
    Search Atlas SEO, reached through the HighLevel integration.
    Returns the same sub-structure the API connector produces so the
    report's SEO section works identically either way.
    """
    if not goto(page, "https://dashboard.searchatlas.com/", "text=/keywords?|rankings?/i"):
        return {"overview": result({}, "Could not open Search Atlas"),
                "rankings": {"data": None, "error": "Not collected", "via": "browser"}}

    overview = collect_metrics(page, {
        "domain_authority":  r"domain authority|(^|\s)da(\s|$)",
        "organic_traffic":   r"organic traffic|est\.? traffic",
        "organic_keywords":  r"(organic )?keywords",
        "backlinks":         r"backlinks",
        "referring_domains": r"referring domains",
    })

    rankings = []
    if goto(page, "https://dashboard.searchatlas.com/rank-tracker"):
        try:
            rows = page.locator("table tbody tr")
            for i in range(min(rows.count(), 25)):
                cells = rows.nth(i).locator("td")
                if cells.count() < 2:
                    continue
                from .common import parse_number
                rankings.append({
                    "keyword":  cells.nth(0).inner_text(timeout=2000).strip(),
                    "position": parse_number(cells.nth(1).inner_text(timeout=2000)),
                })
        except Exception:
            pass

    return {
        "overview": result(overview),
        "rankings": {"data": rankings or None,
                     "error": None if rankings else "No ranking rows found",
                     "via": "browser"},
        "competitors":   {"data": None, "error": "Not available via browser", "via": "browser"},
        "opportunities": {"data": None, "error": "Not available via browser", "via": "browser"},
    }


def instagram(page, lookback_days: int = 14) -> dict:
    """
    Instagram professional dashboard.

    Note: Meta actively fingerprints automation. This is the least reliable
    collector here and Windsor should stay the primary source — it exists
    as a cross-check when Windsor numbers look wrong.
    """
    if not goto(page, "https://www.instagram.com/accounts/professional_dashboard/",
                "text=/accounts reached|insights/i"):
        return result({}, "Could not open Instagram dashboard")

    data = collect_metrics(page, {
        "reach":         r"accounts reached|reach",
        "impressions":   r"impressions|views",
        "profile_views": r"profile visits|profile views",
        "followers":     r"followers",
    })
    return result(data)


def facebook(page, lookback_days: int = 14) -> dict:
    """Facebook Page insights via Meta Business Suite."""
    if not goto(page, "https://business.facebook.com/latest/insights/overview",
                "text=/reach|insights/i"):
        return result({}, "Could not open Facebook insights")

    data = collect_metrics(page, {
        "reach":            r"reach",
        "impressions":      r"impressions|views",
        "post_engagements": r"engagements?|interactions",
        "page_fans":        r"followers|likes",
    })
    return result(data)


def tiktok(page, lookback_days: int = 14) -> dict:
    """TikTok Studio analytics."""
    if not goto(page, "https://www.tiktok.com/tiktokstudio/analytics",
                "text=/video views|followers/i"):
        return result({}, "Could not open TikTok analytics")

    data = collect_metrics(page, {
        "video_views":   r"video views",
        "profile_views": r"profile views",
        "followers":     r"followers",
        "likes":         r"likes",
    })
    return result(data)


def pinterest(page, lookback_days: int = 14) -> dict:
    """Pinterest analytics overview."""
    if not goto(page, "https://analytics.pinterest.com/", "text=/impressions|saves/i"):
        return result({}, "Could not open Pinterest analytics")

    data = collect_metrics(page, {
        "impressions":     r"impressions",
        "saves":           r"saves",
        "outbound_clicks": r"outbound clicks",
        "pin_clicks":      r"pin clicks",
    })
    return result(data)


# Keys match connectors/config so browser data merges cleanly with API data
COLLECTORS = {
    "hotjar":         hotjar,
    "medium":         medium,
    "substack":       substack,
    "gohighlevel":    highlevel,
    "search_atlas":   search_atlas,
    "instagram":      instagram,
    "facebook":       facebook,
    "tiktok_organic": tiktok,
    "pinterest":      pinterest,
}
