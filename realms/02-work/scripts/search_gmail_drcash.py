import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / 'scripts'))
from google_helper import get_gmail

service = get_gmail()

# Search for dr.cash password emails
results = service.users().messages().list(
    userId='me',
    q='dr.cash password',
    maxResults=10
).execute()

messages = results.get('messages', [])

if not messages:
    print("No emails found matching 'dr.cash password'")
else:
    print(f"Found {len(messages)} email(s)\n")
    for msg in messages:
        full = service.users().messages().get(
            userId='me',
            id=msg['id'],
            format='full'
        ).execute()

        headers = full['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No subject')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
        date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown')

        print(f"From:    {sender}")
        print(f"Date:    {date}")
        print(f"Subject: {subject}")
        print("-" * 60)

        # Get body
        def get_body(payload):
            if 'parts' in payload:
                for part in payload['parts']:
                    text = get_body(part)
                    if text:
                        return text
            elif payload.get('mimeType') == 'text/plain':
                data = payload['body'].get('data', '')
                if data:
                    return base64.urlsafe_b64decode(data).decode('utf-8', errors='replace')
            return None

        body = get_body(full['payload'])
        if body:
            print(body[:2000])
        else:
            print("(no plain text body)")
        print("=" * 60)
