"""Compare agents/*.md with the live routine prompts.

Usage: python tools/check_routines.py <dump.json>
The dump is the JSON body of a `RemoteTrigger list` call. Exits 1 on any mismatch.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def main() -> int:
    text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
    live = {r["id"]: r for r in json.loads(text[text.index("{"):])["data"]}
    manifest = json.loads((ROOT / "agents" / "routines.json").read_text(encoding="utf-8"))
    bad = 0
    for entry in manifest["routines"]:
        routine = live.get(entry["trigger_id"])
        if routine is None:
            print(f"MISSING {entry['file']}: {entry['trigger_id']} not live")
            bad += 1
            continue
        prompt = routine["derived_state"]["prompt"].strip()
        local = (ROOT / entry["file"]).read_text(encoding="utf-8").strip()
        if prompt != local:
            print(f"DIFF    {entry['file']}")
            bad += 1
        else:
            print(f"OK      {entry['file']}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
