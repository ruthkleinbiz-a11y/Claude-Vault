"""Appends a timestamped analytics snapshot row to Google Sheets."""

import json
import os
from datetime import datetime, timezone

import gspread
from google.oauth2.service_account import Credentials


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

SHEET_HEADERS = [
    "Run Date",
    # Instagram
    "IG Followers", "IG Impressions", "IG Reach", "IG Profile Views",
    # Facebook
    "FB Page Fans", "FB Impressions", "FB Reach", "FB Engagements",
    # YouTube
    "YT Views", "YT Subscribers", "YT Watch Time (min)", "YT CTR",
    # TikTok
    "TT Video Views", "TT Followers", "TT Likes",
    # Pinterest
    "PIN Impressions", "PIN Saves", "PIN Outbound Clicks",
    # Twitter
    "TW Impressions", "TW Likes", "TW Retweets", "TW Followers",
    # GA4 Website
    "WEB Blog Sessions", "WEB Quiz Sessions", "WEB Lead Magnet Sessions", "WEB Other Sessions",
    # HighLevel Email
    "HL Open Rate", "HL Click Rate", "HL Emails Sent",
    # Medium
    "MED Views", "MED Reads", "MED Claps",
    # Substack
    "SUB Emails Sent", "SUB Open Rate", "SUB Free Subscribers", "SUB Paid Subscribers",
]


def _get_client() -> gspread.Client:
    key_path = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "secrets/google-service-account.json")
    creds = Credentials.from_service_account_file(key_path, scopes=SCOPES)
    return gspread.authorize(creds)


def _ensure_headers(sheet: gspread.Worksheet):
    existing = sheet.row_values(1)
    if not existing:
        sheet.append_row(SHEET_HEADERS, value_input_option="RAW")


def append_row(all_data: dict):
    gc = _get_client()
    sheet_id = os.environ["GOOGLE_SHEET_ID"]
    sh = gc.open_by_key(sheet_id)

    try:
        ws = sh.worksheet("Analytics")
    except gspread.WorksheetNotFound:
        ws = sh.add_worksheet(title="Analytics", rows=1000, cols=50)

    _ensure_headers(ws)

    def g(source, *keys, default=0):
        """Safely drill into nested data dicts."""
        node = all_data.get(source, {})
        for k in keys:
            if isinstance(node, dict):
                node = node.get(k, default)
            else:
                return default
        return node if node is not None else default

    run_date = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    row = [
        run_date,
        g("instagram", "data", "followers"),
        g("instagram", "data", "impressions"),
        g("instagram", "data", "reach"),
        g("instagram", "data", "profile_views"),
        g("facebook", "data", "page_fans"),
        g("facebook", "data", "impressions"),
        g("facebook", "data", "reach"),
        g("facebook", "data", "post_engagements"),
        g("youtube", "data", "views"),
        g("youtube", "data", "subscribers"),
        g("youtube", "data", "watch_time_minutes"),
        g("youtube", "data", "click_through_rate"),
        g("tiktok_organic", "data", "video_views"),
        g("tiktok_organic", "data", "followers"),
        g("tiktok_organic", "data", "likes"),
        g("pinterest", "data", "impressions"),
        g("pinterest", "data", "saves"),
        g("pinterest", "data", "outbound_clicks"),
        g("twitter", "data", "impressions"),
        g("twitter", "data", "likes"),
        g("twitter", "data", "retweets"),
        g("twitter", "data", "followers"),
        g("googleanalytics4", "blogs", "data", "sessions"),
        g("googleanalytics4", "quiz", "data", "sessions"),
        g("googleanalytics4", "lead_magnets", "data", "sessions"),
        g("googleanalytics4", "other", "data", "sessions"),
        g("gohighlevel", "data", "open_rate"),
        g("gohighlevel", "data", "click_rate"),
        g("gohighlevel", "data", "emails_sent"),
        g("medium", "data", "views"),
        g("medium", "data", "reads"),
        g("medium", "data", "claps"),
        g("substack", "data", "emails_sent"),
        g("substack", "data", "open_rate"),
        g("substack", "data", "free_subscribers"),
        g("substack", "data", "paid_subscribers"),
    ]

    ws.append_row(row, value_input_option="USER_ENTERED")
    print(f"[sheets] Row appended: {run_date}")
