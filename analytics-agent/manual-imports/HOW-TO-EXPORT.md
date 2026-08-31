# Manual Exports — Medium & Substack

Drop your CSV files in THIS folder before each run. The agent picks up the most recently modified file matching each pattern.

---

## Medium

1. Go to medium.com → click your profile → **Stats**
2. Click **Export** (top right)
3. Download the CSV
4. Rename it: `medium_stats_YYYY-MM-DD.csv`
5. Drop it in this folder

**Metrics captured:** views, reads, read ratio, claps, fans

---

## Substack

1. Go to your Substack dashboard
2. **Settings → Exports → Download subscriber data** (for subscriber counts)
3. For email stats: **Dashboard → Email analytics → Export**
4. Rename it: `substack_YYYY-MM-DD.csv`
5. Drop it in this folder

**Metrics captured:** emails sent, open rate, paid subscribers, free subscribers, new subscribers

---

## Timing

Export these the same day the agent runs (every 2 weeks on Monday). The agent runs at 7 AM UTC — so drop your files Sunday night or Monday morning before that.

If no file is found, the agent will note it in the report as "data unavailable" and continue with everything else.
