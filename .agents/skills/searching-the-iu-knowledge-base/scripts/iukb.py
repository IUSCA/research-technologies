#!/usr/bin/env python3
"""Search and read IU Knowledge Base articles from the command line.

The IU KB runs on ServiceNow and renders in the browser with JavaScript,
so a plain HTTP fetch of an article page returns an empty shell. The
ServiceNow Knowledge API answers anonymous requests and returns the
article body, which is what this tool uses.

Usage:
    iukb.py search <words...>       # number, published date, title
    iukb.py read <KB number|sys_id>  # article text with links kept

Standard library only. No credentials are needed or sent.
"""

import html
import json
import re
import sys
import urllib.parse
import urllib.request

API = "https://servicenow.iu.edu/api/sn_km_api/knowledge/articles"
ARTICLE_URL = "https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article={}"


def _get(url):
    with urllib.request.urlopen(url, timeout=60) as resp:
        return json.load(resp)


def search(query, limit=10):
    params = {"query": query, "limit": limit, "fields": "published"}
    data = _get(API + "?" + urllib.parse.urlencode(params))
    rows = []
    for art in data["result"]["articles"]:
        sys_id = art["id"].split(":", 1)[1]
        published = art.get("fields", {}).get("published", {}).get("value", "")
        rows.append((art["number"], sys_id, published, art["title"]))
    return rows


def _link(match):
    href = html.unescape(match.group(1))
    text = match.group(2)
    if href.startswith("#"):
        return text
    href = href.replace("/kb?id=kb_article_view&sysparm_article=", "")
    return f"{text} [{href}]"


def _to_text(body):
    body = re.sub(r"(?s)<(script|style).*?</\1>", "", body)
    body = re.sub(r'(?is)<a\b[^>]*?href="([^"]+)"[^>]*>(.*?)</a>', _link, body)
    body = re.sub(r"(?i)<br\s*/?>|</(p|div|li|h\d|tr)>", "\n", body)
    body = re.sub(r"(?i)<li[^>]*>", "\n- ", body)
    body = re.sub(r"<[^>]+>", "", body)
    body = html.unescape(body)
    return re.sub(r"\n\s*\n+", "\n\n", body).strip()


def read(ref):
    sys_id = ref
    if ref.upper().startswith("KB"):
        matches = [r for r in search(ref, limit=5) if r[0] == ref.upper()]
        if not matches:
            sys.exit(f"{ref}: not found by search; retired articles are not searchable")
        sys_id = matches[0][1]
    data = _get(f"{API}/{sys_id}")["result"]
    body = "".join(part.get("content", "") for part in data.get("content", []))
    number = data.get("number")
    print(f"# {number} {data.get('short_description')}")
    print(ARTICLE_URL.format(number))
    print()
    print(_to_text(body))


def main(argv):
    if len(argv) < 3 or argv[1] not in ("search", "read"):
        sys.exit(__doc__)
    if argv[1] == "search":
        for number, _sys_id, published, title in search(" ".join(argv[2:])):
            print(f"{number}  {published}  {title}")
    else:
        for ref in argv[2:]:
            read(ref)


if __name__ == "__main__":
    main(sys.argv)
