"""
NOW — the machine's single source of truth for time.
Usage:  py scripts/now.py

Prints:
  1. Local PC clock time
  2. Web time (timeapi.io, Europe/Sofia) — cross-check
  3. DRIFT WARNING if local clock is off by more than 2 minutes
Exit code 0 always (never breaks the routine); JSON flag --json for machine use.

Tony Stark pipeline rule: morning routine and any manual scheduling
MUST run this first. Never trust memory; never trust wake time.
"""
import json
import sys
import datetime
import urllib.request

WEB_TIMEOUT = 8  # seconds
DRIFT_TOLERANCE = 120  # seconds


def local_now():
    return datetime.datetime.now().astimezone()


def web_now():
    """Fetch authoritative local time (Europe/Sofia) from timeapi.io. Returns dict or None."""
    try:
        url = "https://timeapi.io/api/Time/current/zone?timeZone=Europe/Sofia"
        with urllib.request.urlopen(url, timeout=WEB_TIMEOUT) as r:
            d = json.loads(r.read().decode())
        return d
    except Exception:
        return None


def main():
    ln = local_now()
    local_str = ln.strftime("%A %d.%m.%Y %H:%M:%S")
    print(f"🖥️  PC CLOCK:  {local_str} (local tz: {ln.tzname()})")

    web = web_now()
    if web:
        web_dt = datetime.datetime(
            web["year"], web["month"], web["day"],
            web["hour"], web["minute"], web.get("seconds", 0),
        ).astimezone()
        drift = abs((ln.replace(microsecond=0) - web_dt.replace(microsecond=0)).total_seconds())
        print(f"🌐 WEB TIME:  {web['dayOfWeek']} {web['day']:02d}.{web['month']:02d}.{web['year']} "
              f"{web['time']} ({web['timeZone']}, DST={web.get('dstActive')})")
        if drift <= DRIFT_TOLERANCE:
            print(f"✅ SYNC OK — drift {drift:.0f}s (tolerance {DRIFT_TOLERANCE}s). Use PC clock.")
        else:
            print(f"⚠️ DRIFT {drift:.0f}s — PC CLOCK IS WRONG. Machine uses WEB time until fixed.")
            sys.exit(2)
    else:
        print("⚠️ WEB TIME UNREACHABLE — falling back to PC clock (offline mode). Verify clock manually.")

    if "--json" in sys.argv:
        print(json.dumps({
            "local": local_str,
            "date": ln.strftime("%Y-%m-%d"),
            "time": ln.strftime("%H:%M"),
            "weekday": ln.strftime("%A"),
            "web_ok": web is not None,
            "drift_s": drift if web else None,
        }, ensure_ascii=False))


if __name__ == "__main__":
    main()
