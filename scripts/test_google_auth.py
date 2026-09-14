#!/usr/bin/env python3
"""Test Google Calendar auth with PERFORM paths."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from google_helper import get_calendar

try:
    cal = get_calendar()
    # Try to list calendars
    result = cal.calendarList().list(maxResults=1).execute()
    print("✅ Google Calendar auth WORKS")
    print(f"   Found calendars: {len(result.get('items', []))}")
    for c in result.get('items', []):
        print(f"   - {c.get('summary')}")
except Exception as e:
    print(f"❌ Google Calendar auth FAILED: {e}")
    print("   Token may be expired. Need to re-auth.")
