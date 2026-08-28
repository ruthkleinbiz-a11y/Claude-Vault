"""Uploads the PDF report to the Analytics Reports folder in Google Drive."""

import os
from datetime import datetime, timezone

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Folder ID: Ruth Klein | Every Task → Deliverables → Marketing → Analytics Reports
DRIVE_FOLDER_ID = "1CgmapQrheoH2SmSOJU3egoX2C9scLo6v"

SCOPES = ["https://www.googleapis.com/auth/drive.file"]


def _get_service():
    creds_path = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not creds_path:
        raise RuntimeError("GOOGLE_SERVICE_ACCOUNT_JSON env var not set")
    creds = service_account.Credentials.from_service_account_file(creds_path, scopes=SCOPES)
    return build("drive", "v3", credentials=creds)


def upload_report(pdf_path: str) -> str:
    """Upload pdf_path to Drive and return the file URL."""
    service = _get_service()

    month_year = datetime.now(tz=timezone.utc).strftime("%B %Y")
    file_name = f"Marketing Analytics Report - {month_year}.pdf"

    file_metadata = {
        "name": file_name,
        "parents": [DRIVE_FOLDER_ID],
    }
    media = MediaFileUpload(pdf_path, mimetype="application/pdf", resumable=True)

    uploaded = (
        service.files()
        .create(body=file_metadata, media_body=media, fields="id,webViewLink")
        .execute()
    )

    url = uploaded.get("webViewLink", "")
    print(f"[drive] Uploaded: {file_name} → {url}")
    return url
