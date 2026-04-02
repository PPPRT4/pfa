#!/usr/bin/env python3

import json
import urllib.request


URL = "http://127.0.0.1:8000/add-note"
PAYLOAD = {
    "content": "Fix login bug on Safari and verify cookie handling.",
}


def main():
    req = urllib.request.Request(
        URL,
        data=json.dumps(PAYLOAD).encode("utf-8"),
        method="POST",
        headers={"Content-Type": "application/json"},
    )

    with urllib.request.urlopen(req, timeout=10) as res:
        raw = res.read().decode("utf-8")

    data = json.loads(raw)
    note = data.get("note", {})

    print("=== FULL RESPONSE ===")
    print(json.dumps(data, indent=2, ensure_ascii=True))
    print("\n=== ANALYZED ===")
    print("topic:", note.get("topic"))
    print("atomic_note:", note.get("atomic_note"))


if __name__ == "__main__":
    main()
