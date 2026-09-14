"""Re-authenticate Google API and save new token."""
import pickle
import os
import sys
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

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

print(f"Using credentials: {creds_file}")
print(f"Token will be saved to: {token_file}")
print("\nA browser window will open. Please log in and click 'Allow'.")
print("After auth, the token will be saved automatically.\n")

flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
creds = flow.run_local_server(port=0)

with open(token_file, 'wb') as f:
    pickle.dump(creds, f)

print('\n✅ Token refreshed and saved!')
print(f'   Location: {token_file}')
