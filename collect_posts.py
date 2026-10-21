"""Collect candidate r/nba comments and text posts into candidates.csv.

Reddit blocks direct scraping, so this reads the public Arctic Shift archive
(https://arctic-shift.photon-reddit.com). Output columns match labels.csv
(text, label, note) with label and note left blank for you to fill in.

Usage: python collect_posts.py [subreddit] [days] [per_day] [skip_days] [output.csv]
"""
import csv
import re
import sys
import time
from datetime import datetime, timedelta, timezone

import requests

SUB = sys.argv[1] if len(sys.argv) > 1 else "nba"
DAYS = int(sys.argv[2]) if len(sys.argv) > 2 else 10
PER_DAY = int(sys.argv[3]) if len(sys.argv) > 3 else 60
SKIP = int(sys.argv[4]) if len(sys.argv) > 4 else 0  # start this many days further back
OUT = sys.argv[5] if len(sys.argv) > 5 else "candidates.csv"
BASE = "https://arctic-shift.photon-reddit.com/api"
HEADERS = {"User-Agent": "takemeter-class-project/0.1 (educational)"}
MIN_CHARS, MAX_CHARS = 80, 1200
SKIP_AUTHORS = {"AutoModerator", "nba-scores", "[deleted]"}


def fetch(kind, **params):
    for attempt in range(3):
        r = requests.get(f"{BASE}/{kind}/search", params=params, headers=HEADERS, timeout=30)
        time.sleep(1)  # be polite
        if r.ok:
            return r.json()["data"]
    print(f"  skipped {kind} page after 3 failures ({r.status_code})")
    return []


def clean(text):
    text = re.sub(r"https?://\S+", "", text)
    return " ".join(text.split())


def ok(text, author):
    return (
        author not in SKIP_AUTHORS
        and text not in ("[removed]", "[deleted]")
        and MIN_CHARS <= len(text) <= MAX_CHARS
    )


rows, seen = [], set()


def add(text, note):
    text = clean(text)
    key = text.lower()
    if key in seen:
        return
    seen.add(key)
    rows.append((text, "", note))


today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
for d in range(SKIP + 1, SKIP + DAYS + 1):
    start, end = today - timedelta(days=d), today - timedelta(days=d - 1)
    day = start.date().isoformat()
    fmt = "%Y-%m-%dT%H:%M:%S"
    kept, cursor = 0, start.strftime(fmt)
    for _ in range(8):  # page through the day; replies are most of the volume
        page = fetch("comments", subreddit=SUB, after=cursor, before=end.strftime(fmt),
                     limit=100, sort="asc")
        if not page:
            break
        for c in page:
            if kept < PER_DAY and c.get("parent_id", "").startswith("t3_") and ok(c["body"], c["author"]):
                add(c["body"], f"comment {day}")
                kept += 1
        cursor = datetime.fromtimestamp(page[-1]["created_utc"], timezone.utc).strftime(fmt)
        if kept >= PER_DAY or len(page) < 100:
            break
    for p in fetch("posts", subreddit=SUB, after=start.strftime(fmt), before=end.strftime(fmt), limit=100):
        body = p.get("selftext", "")
        if not p["title"].startswith("[Highlight") and ok(body, p["author"]):
            add(f"{p['title']} {body}", f"post {day}")
    print(f"{day}: {len(rows)} candidates so far")

with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["text", "label", "note"])
    w.writerows(rows)
print(f"Wrote {len(rows)} candidates to {OUT}")
