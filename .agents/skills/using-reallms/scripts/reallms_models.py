#!/usr/bin/env python3
"""List REALLMS API models, and optionally smoke-test one with a real completion.

Standard library only. Reads the API key from the REALLMS_API_KEY environment
variable and never prints it.

    reallms_models.py                  # list model IDs
    reallms_models.py --check MODEL    # also send a one-line chat completion
    reallms_models.py --pi             # print a pi models.json for live chat models
    reallms_models.py --pi FILE        # replace the "reallms" provider in FILE
    reallms_models.py --pi FILE --pi-api-key '!cat ~/.config/reallms/api-key'

--pi builds each entry from the service's /model/info and keeps only models
that answer a real chat completion. The first model listed is the suggested
default. The config names the key as $REALLMS_API_KEY, never its value.
--pi-api-key sets that field instead; pi runs a value that starts with "!" as
a command, so the key never has to sit in the agent's environment. Re-run it
whenever the model list changes.

Set REALLMS_BASE_URL to override the base URL from KB0027272.
"""
import argparse
import json
import os
import re
import shutil
import sys
import urllib.error
import urllib.request

BASE_URL = os.environ.get(
    "REALLMS_BASE_URL", "https://reallms.rescloud.iu.edu/direct/v1"
).rstrip("/")

# Coding agents need room for files and tool output. Smaller models are
# document converters, embedders, or speech models, not chat models.
MIN_CONTEXT = 32768


class CallError(Exception):
    pass


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
        raise CallError(f"HTTP {err.code} from {path}: {detail}")
    except urllib.error.URLError as err:
        raise CallError(f"Cannot reach {BASE_URL}: {err.reason}")


def chat_ok(key, model):
    reply = call(
        "/chat/completions",
        key,
        {
            "model": model,
            "messages": [{"role": "user", "content": "Reply with the word ok."}],
            "max_tokens": 200,
        },
    )
    choice = (reply.get("choices") or [{}])[0]
    return (choice.get("message") or {}).get("content")


def pi_provider(key, api_key_field):
    """Build a pi provider block from /model/info, keeping models that chat."""
    models = []
    for m in call("/model/info", key).get("data", []):
        model_id = m.get("model_name")
        info = m.get("model_info") or {}
        meta = info.get("metadata") or ""
        context = info.get("max_input_tokens") or 0
        if not model_id or context < MIN_CONTEXT:
            continue
        modalities = re.search(r"Supported Modalities:\s*([^;]+)", meta)
        modalities = modalities.group(1) if modalities else "Text"
        if "Text" not in modalities:
            continue
        try:
            chat_ok(key, model_id)
        except CallError as err:
            print(f"skipping {model_id}: {err}", file=sys.stderr)
            continue
        entry = {"id": model_id, "_tools": bool(info.get("supports_function_calling"))}
        if re.search(r"Thinking:\s*True", meta):
            entry["reasoning"] = True
        entry["input"] = ["text", "image"] if "Image" in modalities else ["text"]
        entry["contextWindow"] = context
        if info.get("max_output_tokens"):
            entry["maxTokens"] = info["max_output_tokens"]
        models.append(entry)
        print(f"keeping {model_id}", file=sys.stderr)
    # First the models the service says call tools, then the largest context.
    # The first entry is the suggested default.
    models.sort(key=lambda e: (not e["_tools"], -e["contextWindow"], e["id"]))
    for entry in models:
        del entry["_tools"]
    return {
        "name": "IU REALLMS",
        "baseUrl": BASE_URL,
        "api": "openai-completions",
        "apiKey": api_key_field,
        "models": models,
    }


def write_pi_config(key, target, api_key_field):
    provider = pi_provider(key, api_key_field)
    if not provider["models"]:
        sys.exit("No REALLMS model answered a chat completion; nothing written.")
    config = {"$schema": "https://pi.dev/schemas/models.schema.json", "providers": {}}
    if target != "-" and os.path.exists(target):
        with open(target) as f:
            config = json.load(f)
        shutil.copy2(target, target + ".bak")
    config.setdefault("providers", {})["reallms"] = provider
    text = json.dumps(config, indent=2) + "\n"
    if target == "-":
        sys.stdout.write(text)
        return
    os.makedirs(os.path.dirname(os.path.abspath(target)), exist_ok=True)
    with open(target, "w") as f:
        f.write(text)
    print(f"wrote {len(provider['models'])} models to {target}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", metavar="MODEL", help="send a test completion")
    parser.add_argument(
        "--pi",
        metavar="FILE",
        nargs="?",
        const="-",
        help="print a pi models.json, or update the reallms provider in FILE",
    )
    parser.add_argument(
        "--pi-api-key",
        metavar="VALUE",
        default="$REALLMS_API_KEY",
        help='apiKey field for --pi (default "$REALLMS_API_KEY"; "!cmd" runs cmd)',
    )
    args = parser.parse_args()

    key = os.environ.get("REALLMS_API_KEY", "").strip()
    if not key:
        sys.exit("REALLMS_API_KEY is unset or empty. Export it first; see SKILL.md.")

    try:
        if args.pi:
            write_pi_config(key, args.pi, args.pi_api_key)
            return

        models = call("/models", key).get("data", [])
        for m in sorted(models, key=lambda m: m.get("id", "")):
            print(m.get("id"))

        if args.check:
            text = chat_ok(key, args.check)
            print(f"\n{args.check}: completion returned {text!r}", file=sys.stderr)
    except CallError as err:
        sys.exit(str(err))


if __name__ == "__main__":
    main()
