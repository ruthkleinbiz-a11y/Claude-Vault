# Browser-Based Collection

Pulls analytics from platforms by reading their dashboards in a real,
signed-in Chrome — no API keys needed.

## Why this runs on the Mac

GitHub Actions runs on a fresh Linux container with no cookies, so it hits
a login wall on every platform. Only a machine with a signed-in browser can
do this, which means the Mac.

The setup is therefore split in two halves:

| | Runs where | Schedule | Covers |
|---|---|---|---|
| **Browser collection** | Ruth's Mac (launchd) | 1st & 15th, 6:00 AM local | Hotjar, Medium, Substack, Search Atlas, socials |
| **Report generation** | GitHub Actions | 1st & 15th, 7:00 UTC | Windsor APIs, GA4, Claude analysis, PDF → Drive |

The Mac run commits `browser-data/latest.json` to the repo; the cloud run
reads it an hour later. That file is the handoff between the two halves.

**API data always wins.** Browser numbers only fill gaps — platforms with no
working API key, or connectors that returned nothing. Scraped values come
off a rendered page and are the more fragile of the two sources.

## Setup

```bash
cd analytics-agent
pip install -r requirements.txt
python -m playwright install chromium

# Sign in once — opens a visible Chrome for each platform
python -m browser.run login

# Confirm it works
python -m browser.run collect --no-commit

# Install the biweekly schedule
bash browser/install-schedule.sh
```

Sign-in is one-time. Cookies live in a dedicated Chrome profile at
`~/.zenithmind/browser-profile` — separate from everyday browsing, so this
never disturbs normal Chrome and never needs Chrome quit before a run.

## Commands

```bash
python -m browser.run login                    # sign in to everything
python -m browser.run login --only hotjar      # re-auth one platform
python -m browser.run check                    # which sessions are still valid
python -m browser.run collect                  # scrape, commit, push
python -m browser.run collect --no-commit      # scrape only
python -m browser.run collect --show           # visible browser (debugging)
python -m browser.run collect --screenshot     # save what each page looked like
```

## When a platform stops returning data

Sessions expire — that's the normal failure, and it's expected every few
weeks. Diagnose in this order:

```bash
python -m browser.run check                          # 1. expired session?
python -m browser.run login --only <platform>        # 2. if so, re-auth
python -m browser.run collect --only <platform> --show --screenshot
```

`--show` puts a real browser on screen so you can watch what happens;
`--screenshot` saves each page to `browser-data/screenshots/`. If the page
loads fine but numbers come back empty, the dashboard was redesigned and
the label patterns in `collectors/platforms.py` need updating.

## Reliability, honestly

These collectors read rendered dashboards, so they are inherently more
fragile than the API path:

- **Hotjar, Medium, Substack, Search Atlas** — the main reason this exists.
  Straightforward dashboards, no API key needed. Most reliable of the set.
- **Instagram and Facebook** — Meta actively fingerprints automation, and
  these may fail or require re-login often. Windsor stays the primary
  source; treat these as a cross-check, not a replacement.
- **TikTok, Pinterest** — usually fine, occasional layout churn.

A platform failing never aborts the run. It returns no data, gets logged,
and the report notes it as pending.

## Requirements

The Mac must be awake at the scheduled time. launchd will run the job when
the machine next wakes if it was asleep, but a Mac that is off entirely
misses the window — the cloud half still runs and produces the report with
whatever the APIs supplied.
