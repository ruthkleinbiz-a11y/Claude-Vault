"""
Persistent Chrome session for browser-based analytics collection.

Runs on Ruth's Mac, not in CI — it needs a real, logged-in browser.

We keep a dedicated Chrome profile at ~/.zenithmind/browser-profile rather
than touching the everyday browsing profile. Chrome locks a profile while
it is open, so reusing the default one would mean quitting Chrome before
every scheduled run. A dedicated profile also means this automation can
never disturb normal browsing state.

Sign in once per platform (`python -m browser.run login`); the cookies
persist in that profile and later scheduled runs reuse them headlessly.
"""

import os
from pathlib import Path

from playwright.sync_api import sync_playwright


PROFILE_DIR = Path(os.environ.get(
    "ZENITHMIND_BROWSER_PROFILE",
    Path.home() / ".zenithmind" / "browser-profile",
))

# Where each platform's analytics live, and a selector that only renders
# for a signed-in user. The probe is how we tell "logged in" from
# "bounced to a login wall" without guessing from the URL alone.
PLATFORMS = {
    "hotjar": {
        "label": "Hotjar",
        "url": "https://insights.hotjar.com/",
        "logged_in_probe": "text=/dashboard|sites|recordings/i",
    },
    "medium": {
        "label": "Medium",
        "url": "https://medium.com/me/stats",
        "logged_in_probe": "text=/views|reads|stories/i",
    },
    "substack": {
        "label": "Substack",
        "url": "https://thesacredenergyoftime.substack.com/publish/stats",
        "logged_in_probe": "text=/subscribers|opens|posts/i",
    },
    "highlevel": {
        "label": "HighLevel (email + Search Atlas)",
        "url": "https://app.gohighlevel.com/",
        "logged_in_probe": "text=/dashboard|conversations|marketing/i",
    },
    "instagram": {
        "label": "Instagram",
        "url": "https://www.instagram.com/accounts/login/",
        "logged_in_probe": "svg[aria-label='Home'], a[href='/']",
    },
    "facebook": {
        "label": "Facebook Page",
        "url": "https://business.facebook.com/latest/insights/overview",
        "logged_in_probe": "text=/insights|reach|overview/i",
    },
    "tiktok": {
        "label": "TikTok",
        "url": "https://www.tiktok.com/tiktokstudio/analytics",
        "logged_in_probe": "text=/analytics|video views|followers/i",
    },
    "pinterest": {
        "label": "Pinterest",
        "url": "https://analytics.pinterest.com/",
        "logged_in_probe": "text=/impressions|saves|analytics/i",
    },
}


def profile_exists() -> bool:
    return PROFILE_DIR.exists() and any(PROFILE_DIR.iterdir())


def _launch(p, headless: bool):
    """
    Open the dedicated profile. channel="chrome" uses the real Chrome
    install rather than Playwright's bundled Chromium — some of these
    dashboards behave differently (or block outright) on vanilla Chromium.
    """
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    return p.chromium.launch_persistent_context(
        user_data_dir=str(PROFILE_DIR),
        channel="chrome",
        headless=headless,
        viewport={"width": 1440, "height": 900},
        args=["--disable-blink-features=AutomationControlled"],
    )


def open_context(headless: bool = True):
    """Context manager yielding a logged-in browser context."""
    p = sync_playwright().start()
    try:
        ctx = _launch(p, headless)
    except Exception:
        p.stop()
        raise
    ctx._playwright = p  # keep a handle so close_context can stop it
    return ctx


def close_context(ctx):
    pw = getattr(ctx, "_playwright", None)
    try:
        ctx.close()
    finally:
        if pw:
            pw.stop()


def is_logged_in(page, platform_key: str, timeout_ms: int = 8000) -> bool:
    cfg = PLATFORMS.get(platform_key, {})
    probe = cfg.get("logged_in_probe")
    if not probe:
        return True
    try:
        page.wait_for_selector(probe, timeout=timeout_ms)
        return True
    except Exception:
        return False


def interactive_login(only: list[str] | None = None):
    """
    Open each platform in a visible window and wait for a manual sign-in.

    Run this once up front, and again whenever a session expires — the
    scheduled job reports which platforms bounced, so you know when.
    """
    targets = [k for k in PLATFORMS if not only or k in only]

    print("=" * 64)
    print("ZenithMind — browser sign-in")
    print("=" * 64)
    print(f"Profile: {PROFILE_DIR}")
    print(f"Signing in to {len(targets)} platform(s).")
    print("A Chrome window will open for each. Sign in, then press Enter here.")
    print("Press Enter without signing in to skip a platform.\n")

    ctx = open_context(headless=False)
    results = {}
    try:
        for key in targets:
            cfg = PLATFORMS[key]
            page = ctx.new_page()
            print(f"\n[{cfg['label']}] opening {cfg['url']}")
            try:
                page.goto(cfg["url"], timeout=60000, wait_until="domcontentloaded")
            except Exception as exc:
                print(f"  could not open the page: {exc}")

            if is_logged_in(page, key, timeout_ms=5000):
                print("  already signed in — nothing to do.")
                results[key] = True
            else:
                input(f"  sign in to {cfg['label']} in the browser, then press Enter... ")
                ok = is_logged_in(page, key, timeout_ms=10000)
                results[key] = ok
                print("  signed in." if ok else "  still not detected as signed in — skipping.")
            page.close()
    finally:
        close_context(ctx)

    print("\n" + "=" * 64)
    for key, ok in results.items():
        print(f"  {'OK     ' if ok else 'MISSING'} {PLATFORMS[key]['label']}")
    print("=" * 64)
    print("Cookies are saved in the profile. Scheduled runs will reuse them.")
    return results


def check_sessions() -> dict:
    """Report which platforms still have a valid session, without scraping."""
    ctx = open_context(headless=True)
    status = {}
    try:
        for key, cfg in PLATFORMS.items():
            page = ctx.new_page()
            try:
                page.goto(cfg["url"], timeout=45000, wait_until="domcontentloaded")
                status[key] = is_logged_in(page, key)
            except Exception:
                status[key] = False
            page.close()
    finally:
        close_context(ctx)
    return status
