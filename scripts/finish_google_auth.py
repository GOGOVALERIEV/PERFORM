"""Finish Google auth with the provided code."""
import pickle
import os
import sys
from pathlib import Path
from google_auth_oauthlib.flow import Flow

# Auto-detect project root
BASE = Path(__file__).resolve().parent.parent
config_dir = str(BASE / 'config')
creds_file = os.path.join(config_dir, 'google-credentials.json')
token_file = os.path.join(config_dir, 'google-token.pickle')

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/calendar',
    'https://mail.google.com/',
    'https://www.googleapis.com/auth/gmail.settings.basic',
]

AUTH_CODE = "4/1ATsMZqBZAaW3NC6YeSnClKO7kA2qgwJ7WHam8XE-UBnbgrzvu6xl8rHu-fA"

print("Finishing Google auth with provided code...")

flow = Flow.from_client_secrets_file(
    creds_file,
    SCOPES,
    redirect_uri='urn:ietf:wg:oauth:2.0:oob'
)

try:
    flow.fetch_token(code=AUTH_CODE)
    creds = flow.credentials

    with open(token_file, 'wb') as f:
        pickle.dump(creds, f)

    print(f"\n✅ Token saved to: {token_file}")
    print("Google Calendar, Drive, Docs, and Gmail are now authenticated.")
except Exception as e:
    print(f"❌ Auth failed: {e}")
    print("The code may have expired (codes expire after a few minutes).")
    print("Generate a new code and try again.")
