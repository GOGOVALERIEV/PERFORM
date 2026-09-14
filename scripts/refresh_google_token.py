"""Re-authenticate Google API and save new token."""
import pickle
import os
import sys
from pathlib import Path
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request

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

# Use Flow (not InstalledAppFlow) so we can control the browser manually
flow = Flow.from_client_secrets_file(
    creds_file,
    SCOPES,
    redirect_uri='urn:ietf:wg:oauth:2.0:oob'  # "Out of band" — shows auth code directly
)

# Generate the URL for the user to open
auth_url, _ = flow.authorization_url(prompt='consent')

print("="*70)
print("GOOGLE AUTH REQUIRED")
print("="*70)
print("\n1. Open this URL in your browser (Ctrl+click or copy-paste):\n")
print(auth_url)
print("\n2. Log in with: gogovaleriev77@gmail.com")
print("3. Click 'Allow' for all permissions")
print("4. You will see a screen that says 'The authentication flow has completed.'")
print("   Copy the CODE from that page (the long string after 'code=')")
print("5. Paste it below and press Enter:\n")

# Wait for user to paste the auth code
auth_code = input("Paste auth code here: ").strip()

# Exchange code for credentials
flow.fetch_token(code=auth_code)
creds = flow.credentials

with open(token_file, 'wb') as f:
    pickle.dump(creds, f)

print(f"\n{'='*70}")
print("✅ Token refreshed and saved!")
print(f"   Location: {token_file}")
print("="*70)
