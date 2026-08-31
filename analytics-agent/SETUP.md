# Analytics Agent — Setup Guide

One-time setup. After this, the agent runs automatically every 2 weeks and emails the report to claudia@every-task.com.

---

## Step 1 — Connect Platforms in Windsor.ai

Log in to your Windsor.ai account and connect each of these (takes ~5 min each):

| Platform | Windsor Connector Name |
|---|---|
| Instagram | Instagram (Organic) |
| Facebook | Facebook (Organic) |
| YouTube | YouTube |
| TikTok | TikTok Organic |
| Pinterest | Pinterest |
| Google Analytics 4 | Google Analytics 4 |
| GoHighLevel | GoHighLevel |
| Google Sheets | Google Sheets |

For each one: click **Add Connector → [Platform Name] → Connect Account → authorize with your login**.

> Instagram is already connected. Start from Facebook.

---

## Step 2 — Get Your Windsor API Key

1. In Windsor.ai, go to **Settings → API**
2. Copy your API key
3. You'll need this in Step 5

---

## Step 3 — Set Up Twitter/X API Access

1. Go to [developer.x.com](https://developer.x.com)
2. Create a free developer account (or log in)
3. Create a new App
4. Go to **Keys and Tokens → Bearer Token** → copy it
5. Add your Twitter handle to `config.yml` under `twitter.username` (without the @)

---

## Step 4 — Google Sheets + Service Account

The agent needs permission to write to Google Sheets automatically.

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a new project (or use existing)
3. Enable **Google Sheets API** and **Google Drive API**
4. Go to **IAM & Admin → Service Accounts → Create Service Account**
5. Name it `analytics-agent`, click Create
6. Click the service account → **Keys → Add Key → JSON** → download the file
7. Rename it `google-service-account.json`
8. Create a new Google Sheet named `RK Analytics`
9. Share that Sheet with the service account email (it looks like `analytics-agent@your-project.iam.gserviceaccount.com`) — give it **Editor** access
10. Copy the Sheet ID from the URL: `docs.google.com/spreadsheets/d/THIS_PART_HERE/edit`

---

## Step 5 — Set Up SendGrid (Email Delivery)

1. Create a free SendGrid account at [sendgrid.com](https://sendgrid.com) (100 emails/day free)
2. Go to **Settings → API Keys → Create API Key** → Full Access
3. Copy the key
4. Verify your sender email (analytics@ruthklein.com or similar) under **Sender Authentication**

---

## Step 6 — Add GitHub Secrets

This is what lets GitHub Actions run the agent securely with your credentials.

Go to your GitHub repo → **Settings → Secrets and variables → Actions → New repository secret**

Add each of these:

| Secret Name | Value |
|---|---|
| `WINDSOR_API_KEY` | Your Windsor.ai API key |
| `WINDSOR_ACCOUNT_ID` | Your Windsor.ai account ID |
| `TWITTER_BEARER_TOKEN` | Your X API bearer token |
| `TWITTER_USERNAME` | Your Twitter handle (no @) |
| `ANTHROPIC_API_KEY` | Your Anthropic API key |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | Paste the entire contents of your google-service-account.json file |
| `GOOGLE_SHEET_ID` | Your Google Sheet ID |
| `SENDGRID_API_KEY` | Your SendGrid API key |
| `REPORT_FROM_EMAIL` | The verified sender email (e.g. analytics@ruthklein.com) |

---

## Step 7 — Test It

After all secrets are added:

1. Go to GitHub repo → **Actions → Biweekly Analytics Report**
2. Click **Run workflow → Run workflow**
3. Watch the logs — it should collect data, write to Sheets, generate the PDF, and email it

If anything fails, the error will show in the Action logs with a clear message.

---

## Schedule

The agent runs automatically on the **1st and 15th of every month at 7 AM UTC** (that's 3 AM ET / midnight PT).

To change the schedule, edit `.github/workflows/analytics-review.yml` and update the cron line.

---

## Medium & Substack (Manual, Takes 60 Seconds)

See `manual-imports/HOW-TO-EXPORT.md` for instructions. Drop the CSV files the night before or morning of each run.

---

## What You Get

Every 2 weeks, claudia@every-task.com receives a PDF with:

- At-a-glance summary table of all platforms
- Executive summary (top 5 things to know)
- Top performers this period
- Platforms to watch (what's declining)
- Platform-by-platform breakdown with vs-prior-period comparisons
- Content & engagement insights across platforms
- 5-7 specific recommendations for the next 2 weeks
- Anomalies and things to investigate

All raw numbers also go into your Google Sheet automatically for your own tracking and trend analysis.
