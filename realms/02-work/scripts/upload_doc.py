"""
Generic uploader: any markdown file -> Google Doc (with formatting).

Usage:
    python scripts/upload_doc.py <path-to-md-file> "<Doc Title>" [share-email]

Same trick as upload_terms_doc.py, but reusable: Drive converts markdown
into a real Doc (headings, tables, bold). Optionally shares with an email
(so it opens no matter which Google account the browser is logged into).
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / 'scripts'))
from google_helper import get_drive

from googleapiclient.http import MediaFileUpload

md_path = sys.argv[1]
title = sys.argv[2]
share_email = sys.argv[3] if len(sys.argv) > 3 else None

drive = get_drive()

created = drive.files().create(
    body={'name': title, 'mimeType': 'application/vnd.google-apps.document'},
    media_body=MediaFileUpload(md_path, mimetype='text/markdown'),
    fields='id, webViewLink',
).execute()

if share_email:
    drive.permissions().create(
        fileId=created['id'],
        body={'type': 'user', 'role': 'writer', 'emailAddress': share_email},
        sendNotificationEmail=False,
    ).execute()
    print(f'Shared with {share_email}')

print('Created: ' + created['webViewLink'])
