#!/usr/bin/env python3
"""Test Clockify auth."""
import sys, os, json, urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
env = {}
with open(BASE / "config" / ".env", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k] = v

API_KEY = env.get("CLOCKIFY_API_KEY", "")
WORKSPACE = env.get("CLOCKIFY_WORKSPACE_ID", "")

req = urllib.request.Request(
    f"https://api.clockify.me/api/v1/workspaces/{WORKSPACE}/projects",
    headers={"X-Api-Key": API_KEY}
)
try:
    with urllib.request.urlopen(req) as r:
        data = json.loads(r.read().decode())
        print(f"✅ Clockify auth WORKS")
        print(f"   Workspace: {WORKSPACE}")
        print(f"   Projects found: {len(data)}")
        for p in data[:3]:
            print(f"   - {p.get('name')} (ID: {p.get('id')[:8]}...)")
except Exception as e:
    print(f"❌ Clockify auth FAILED: {e}")
