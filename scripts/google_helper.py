"""
Google API Helper — reusable functions for all Google operations.
Import this in any script or use from Claude Code inline.

Usage:
    from google_helper import get_creds, get_docs, get_drive, get_sheets, get_gmail
"""

import pickle
import sys
import io
import os
from pathlib import Path

# Fix Windows terminal encoding — prevents Unicode crash.
# Only wrap if not already UTF-8: wrapping twice closes the stream underneath
# and crashes with "I/O operation on closed file".
# Under pythonw.exe (windowless) the streams are None — skip wrapping entirely.
if sys.stdout is not None and (getattr(sys.stdout, 'encoding', '') or '').lower().replace('-', '') != 'utf8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if sys.stderr is not None and (getattr(sys.stderr, 'encoding', '') or '').lower().replace('-', '') != 'utf8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Paths — auto-detect project root from this file's location
_BASE = Path(__file__).resolve().parent.parent
CONFIG_DIR = str(_BASE / 'config')
TOKEN_PATH = str(_BASE / 'config' / 'google-token.pickle')
CREDS_PATH = str(_BASE / 'config' / 'google-credentials.json')


def get_creds():
    """Load Google OAuth credentials from pickle token."""
    with open(TOKEN_PATH, 'rb') as f:
        return pickle.load(f)


def get_docs():
    """Return Google Docs API service."""
    from googleapiclient.discovery import build
    return build('docs', 'v1', credentials=get_creds())


def get_drive():
    """Return Google Drive API service."""
    from googleapiclient.discovery import build
    return build('drive', 'v3', credentials=get_creds())


def get_sheets():
    """Return Google Sheets API service."""
    from googleapiclient.discovery import build
    return build('sheets', 'v4', credentials=get_creds())


def get_gmail():
    """Return Gmail API service."""
    from googleapiclient.discovery import build
    return build('gmail', 'v1', credentials=get_creds())


def get_calendar():
    """Return Google Calendar API service."""
    from googleapiclient.discovery import build
    return build('calendar', 'v3', credentials=get_creds())


# --- Google Docs Tab Helpers ---

def create_tab(doc_id, title):
    """Create a new tab in a Google Doc. Returns the new tab ID."""
    docs = get_docs()
    result = docs.documents().batchUpdate(
        documentId=doc_id,
        body={'requests': [{'addDocumentTab': {'tabProperties': {'title': title}}}]}
    ).execute()
    tab_props = result['replies'][0]['addDocumentTab']['tabProperties']
    print(f"Created tab '{tab_props['title']}' (ID: {tab_props['tabId']}, index: {tab_props['index']})")
    return tab_props['tabId']


def rename_tab(doc_id, tab_id, new_title):
    """Rename an existing tab."""
    docs = get_docs()
    docs.documents().batchUpdate(
        documentId=doc_id,
        body={'requests': [{
            'updateDocumentTabProperties': {
                'tabProperties': {'tabId': tab_id, 'title': new_title},
                'fields': 'title'
            }
        }]}
    ).execute()
    print(f"Renamed tab {tab_id} to '{new_title}'")


def move_tab(doc_id, tab_id, new_index):
    """Move a tab to a new position (0-based index)."""
    docs = get_docs()
    docs.documents().batchUpdate(
        documentId=doc_id,
        body={'requests': [{
            'updateDocumentTabProperties': {
                'tabProperties': {'tabId': tab_id, 'index': new_index},
                'fields': 'index'
            }
        }]}
    ).execute()
    print(f"Moved tab {tab_id} to index {new_index}")


def delete_tab(doc_id, tab_id):
    """Delete a tab from a Google Doc."""
    docs = get_docs()
    docs.documents().batchUpdate(
        documentId=doc_id,
        body={'requests': [{'deleteTab': {'tabId': tab_id}}]}
    ).execute()
    print(f"Deleted tab {tab_id}")


def list_tabs(doc_id):
    """List all tabs in a Google Doc. Returns list of {id, title, index, chars}."""
    docs = get_docs()
    doc = docs.documents().get(documentId=doc_id, includeTabsContent=True).execute()
    tabs = []
    for tab in doc.get('tabs', []):
        props = tab.get('tabProperties', {})
        body = tab.get('documentTab', {}).get('body', {})
        content = body.get('content', [])
        end_idx = content[-1].get('endIndex', 0) if content else 0
        tabs.append({
            'id': props.get('tabId'),
            'title': props.get('title'),
            'index': props.get('index'),
            'chars': end_idx
        })
        print(f"Tab {props.get('index')}: {props.get('title')} ({end_idx} chars) [ID: {props.get('tabId')}]")
    return tabs


def insert_text_in_tab(doc_id, tab_id, text, index=1):
    """Insert plain text into a tab at given index."""
    docs = get_docs()
    docs.documents().batchUpdate(
        documentId=doc_id,
        body={'requests': [{
            'insertText': {
                'text': text,
                'location': {'index': index, 'tabId': tab_id}
            }
        }]}
    ).execute()
    print(f"Inserted {len(text)} chars into tab {tab_id}")


def insert_structured_content(doc_id, tab_id, sections):
    """
    Insert text with headings into a tab.

    sections: list of (style, text) tuples
        style: 'HEADING_1', 'HEADING_2', 'HEADING_3', or 'NORMAL_TEXT'
        text: the text content (include \\n at end)
    """
    docs = get_docs()

    all_text = ''
    style_ranges = []

    for style, text in sections:
        start = len(all_text) + 1
        all_text += text
        end = len(all_text) + 1
        if style != 'NORMAL_TEXT':
            style_ranges.append({
                'start': start,
                'end': start + len(text),
                'style': style
            })

    requests = [{
        'insertText': {
            'text': all_text,
            'location': {'index': 1, 'tabId': tab_id}
        }
    }]

    for sr in style_ranges:
        requests.append({
            'updateParagraphStyle': {
                'range': {
                    'startIndex': sr['start'],
                    'endIndex': sr['end'],
                    'tabId': tab_id
                },
                'paragraphStyle': {'namedStyleType': sr['style']},
                'fields': 'namedStyleType'
            }
        })

    docs.documents().batchUpdate(
        documentId=doc_id,
        body={'requests': requests}
    ).execute()
    print(f"Inserted {len(all_text)} chars with {len(style_ranges)} styled headings into tab {tab_id}")


# --- Drive Helpers ---

def read_drive_file(file_id):
    """Download a text file from Drive and return its content as string."""
    drive = get_drive()
    content = drive.files().get_media(fileId=file_id).execute()
    return content.decode('utf-8')


def list_folder(folder_id):
    """List files in a Drive folder. Returns list of {id, name, mimeType}."""
    drive = get_drive()
    results = drive.files().list(
        q=f"'{folder_id}' in parents",
        fields='files(id, name, mimeType)',
        pageSize=100
    ).execute()
    files = results.get('files', [])
    for f in files:
        print(f"{f['name']} | {f['id']} | {f['mimeType']}")
    return files


def rename_file(file_id, new_name):
    """Rename a file on Google Drive."""
    drive = get_drive()
    drive.files().update(fileId=file_id, body={'name': new_name}).execute()
    print(f"Renamed to: {new_name}")


if __name__ == '__main__':
    print("Google Helper loaded. Available: get_creds, get_docs, get_drive, get_sheets, get_gmail")
    print(f"Token: {TOKEN_PATH}")
    print(f"Creds: {CREDS_PATH}")
