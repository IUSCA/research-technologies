#!/usr/bin/env python3
"""List REALLMS API models, and optionally smoke-test one with a real completion.

Standard library only. Reads the API key from the REALLMS_API_KEY environment
variable and never prints it.

    reallms_models.py                  # list model IDs
    reallms_models.py --check MODEL    # also send a one-line chat completion

Set REALLMS_BASE_URL to override the base URL from KB0027272.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

BASE_URL = os.environ.get(
    "REALLMS_BASE_URL", "https://reallms.rescloud.iu.edu/direct/v1"
).rstrip("/")


def call(path, key, body=None):
    req = urllib.request.Request(
        BASE_URL + path,
        data=None if body is None else json.dumps(body).encode(),
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as err:
        detail = err.read().decode(errors="replace")[:500]
        sys.exit(f"HTTP {err.code} from {path}: {detail}")
    except urllib.error.URLError as err:
        sys.exit(f"Cannot reach {BASE_URL}: {err.reason}")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", metavar="MODEL", help="send a test completion")
    args = parser.parse_args()

    key = os.environ.get("REALLMS_API_KEY", "").strip()
    if not key:
        sys.exit("REALLMS_API_KEY is unset or empty. Export it first; see SKILL.md.")

    models = call("/models", key).get("data", [])
    for m in sorted(models, key=lambda m: m.get("id", "")):
        print(m.get("id"))

    if args.check:
        reply = call(
            "/chat/completions",
            key,
            {
                "model": args.check,
                "messages": [{"role": "user", "content": "Reply with the word ok."}],
                "max_tokens": 200,
            },
        )
        choice = (reply.get("choices") or [{}])[0]
        text = (choice.get("message") or {}).get("content")
        print(f"\n{args.check}: completion returned {text!r}", file=sys.stderr)


if __name__ == "__main__":
    main()
