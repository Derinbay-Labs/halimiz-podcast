"""Copy the metrics routine's drop file into panel/data/metrics.json when it is newer.

The metrics routine runs bound to kobe (it needs Chrome), and kobe-bound routines cannot push.
It writes the finished file to .panel-drop/metrics.json in kobe's checkout instead, and
.github/workflows/panel-metrics.yml runs this on a kobe runner to land it on master.

Usage: python tools/panel_drop.py DROP TARGET
Prints the drop's date (YYYY-MM-DD) when TARGET was replaced, nothing otherwise.
"""
import json
import sys
from datetime import datetime
from pathlib import Path

KEYS = {"updated", "goal", "daily", "followers", "episodes", "ads", "agents", "suggestions"}


def updated(data):
    return datetime.fromisoformat(data["updated"])


def main(drop, target):
    drop, target = Path(drop), Path(target)
    if not drop.exists():
        print(f"panel_drop: no drop file at {drop}", file=sys.stderr)
        return
    raw = drop.read_bytes()
    new = json.loads(raw)
    missing = KEYS - new.keys()
    if missing:
        sys.exit(f"panel_drop: drop file lacks {sorted(missing)}")
    old = json.loads(target.read_bytes())
    if updated(new) <= updated(old):
        print(f"panel_drop: drop {new['updated']} is not newer than {old['updated']}", file=sys.stderr)
        return
    target.write_bytes(raw)
    print(new["updated"][:10])


if __name__ == "__main__":
    main(*sys.argv[1:3])
