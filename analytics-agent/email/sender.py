"""Sends the PDF report via SendGrid."""

import base64
import os
from datetime import datetime

import sendgrid
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName, FileType, Disposition
)


def send_report(pdf_path: str, config: dict):
    sg = sendgrid.SendGridAPIClient(api_key=os.environ["SENDGRID_API_KEY"])

    run_date = datetime.utcnow().strftime("%B %d, %Y")
    subject = f"Analytics Report — {run_date}"

    with open(pdf_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    attachment = Attachment(
        FileContent(encoded),
        FileName(os.path.basename(pdf_path)),
        FileType("application/pdf"),
        Disposition("attachment"),
    )

    html_body = f"""
    <div style="font-family: Georgia, serif; max-width: 600px; margin: 0 auto; color: #333;">
      <div style="background: #2D4A8A; padding: 24px; border-radius: 8px 8px 0 0;">
        <h1 style="color: white; margin: 0; font-size: 20px;">Ruth Klein — Biweekly Analytics Report</h1>
        <p style="color: #c5d5f5; margin: 6px 0 0; font-size: 14px;">{run_date}</p>
      </div>
      <div style="background: #f9f9f9; padding: 24px; border-radius: 0 0 8px 8px; border: 1px solid #e0e0e0;">
        <p>Your analytics report for the past {config["report"]["lookback_days"]} days is attached.</p>
        <p>It covers: Instagram, Facebook, YouTube, TikTok, Pinterest, Twitter/X, HighLevel Emails,
        Website (GA4), Medium, and Substack.</p>
        <p style="color: #666; font-size: 13px;">This report was generated automatically. The next one arrives in ~14 days.</p>
      </div>
    </div>
    """

    message = Mail(
        from_email=os.environ.get("REPORT_FROM_EMAIL", "analytics@ruthklein.com"),
        to_emails=os.environ.get("REPORT_TO_EMAIL", config["report"]["to_email"]),
        subject=subject,
        html_content=html_body,
    )
    message.attachment = attachment

    try:
        response = sg.send(message)
        print(f"[email] Sent to {config['report']['to_email']} — status {response.status_code}")
    except Exception as exc:
        print(f"[email] FAILED: {exc}")
        raise
