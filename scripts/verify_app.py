"""Verify a running Patchamomma API extracts non-empty results for every fixture transcript.

Usage:
    python scripts/verify_app.py                    # local backend, all fixtures
    python scripts/verify_app.py --limit 2          # quick check, first 2 fixtures
    python scripts/verify_app.py --url https://...  # deployed backend
"""

import argparse
import glob
import json
import os
import sys
from collections import Counter

import requests

FIXTURES = os.path.join(os.path.dirname(__file__), "..", "tests", "fixtures", "sample_transcripts", "*.json")


def load_transcript(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    lines = [f"[{s['timestamp']}] {s['speaker_name']}: {s['text']}" for s in data["segments"]]
    return data["meeting_id"], "\n".join(lines)


def check_health(url):
    r = requests.get(f"{url}/health", timeout=15)
    r.raise_for_status()
    print(f"[OK] health: {r.json()}")


def analyze(url, meeting_id, text):
    r = requests.post(f"{url}/analyze", json={"transcript_text": text}, timeout=300)
    if r.status_code != 200:
        print(f"[FAIL] {meeting_id}: HTTP {r.status_code} {r.text[:200]}")
        return None
    return r.json()


def report(meeting_id, data):
    decisions = data["decisions"]
    actions = data["action_items"]
    deps = data["dependencies"]
    stats = data["stats"]
    validation = data["validation"]
    conflicts = data["conflicts"]
    conflict_types = Counter(c["type"] for c in conflicts["conflicts"])

    print(f"\n=== {meeting_id} ===")
    print(
        f"  decisions={len(decisions)}  actions={len(actions)}  dependencies={len(deps)}  "
        f"owners={stats['owner_count']}  high_priority={stats['high_priority_count']}  "
        f"validation_issues(dec/act)={validation['decisions']['issue_count']}/{validation['actions']['issue_count']}  "
        f"conflicts={conflicts['conflict_count']} {dict(conflict_types) if conflict_types else ''}"
    )
    for d in decisions[:2]:
        print(f"  D: {d['text'][:90]}  (conf={d['confidence']}, speaker={d.get('evidence_speaker')})")
    for a in actions[:2]:
        print(f"  A: {a['text'][:70]}  owner={a.get('owner')} deadline={a.get('deadline')} priority={a.get('priority')}")
    for dep in deps[:2]:
        print(f"  R: {dep['source_id']} --{dep['relationship']}--> {dep['target_id']} (conf={dep['confidence']})")

    problems = []
    if not decisions:
        problems.append("0 decisions")
    if not actions:
        problems.append("0 actions")
    if not deps:
        problems.append("0 dependencies")
    if problems:
        print(f"  [FAIL] {', '.join(problems)}")
    return not problems


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://localhost:8000")
    parser.add_argument("--limit", type=int, default=0, help="only test the first N fixtures (0 = all)")
    args = parser.parse_args()
    url = args.url.rstrip("/")
    print(f"[TEST] target={url}")

    check_health(url)

    files = sorted(glob.glob(FIXTURES))
    if args.limit:
        files = files[: args.limit]
    if not files:
        print("[FAIL] no fixture transcripts found")
        sys.exit(1)

    passed = 0
    for path in files:
        meeting_id, text = load_transcript(path)
        data = analyze(url, meeting_id, text)
        if data and report(meeting_id, data):
            passed += 1

    print(f"\n[RESULT] {passed}/{len(files)} transcripts passed")
    if passed != len(files):
        print("[FAIL]")
        sys.exit(1)
    print("[SUCCESS] all transcripts produced decisions, actions and dependencies")


if __name__ == "__main__":
    main()
