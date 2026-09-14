"""
Upload docs/industry-terms-cheatsheet.md to Google Drive as a Google Doc.

How it works:
1. google_helper gives us an authenticated Drive connection (it loads the
   saved token pickle from config/, so no login needed).
2. We upload the markdown FILE but tell Drive the target type is a Google Doc.
   Drive converts markdown -> Doc automatically: # becomes Heading 1,
   ## becomes Heading 2, | tables | become real tables, **bold** stays bold.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / 'scripts'))
from google_helper import get_drive

from googleapiclient.http import MediaFileUpload

MD_PATH = 'C:/Users/User/Desktop/PERFORM/docs/industry-terms-cheatsheet.md'

drive = get_drive()

# media_body = the file content we're sending (and what format it's in)
media = MediaFileUpload(MD_PATH, mimetype='text/markdown')

# body = what the file should BE on Drive (name + Google Doc type)
created = drive.files().create(
    body={
        'name': 'Meta + Ecom + DR Terms Cheatsheet',
        'mimeType': 'application/vnd.google-apps.document',
    },
    media_body=media,
    fields='id, webViewLink',
).execute()

print('Created Google Doc!')
print('ID:  ' + created['id'])
print('Link: ' + created['webViewLink'])
