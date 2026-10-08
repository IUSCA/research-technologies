#!/usr/bin/env python3
"""Check every skill in .agents/skills for format, markers, sources, and freshness.

Usage:
    tools/check-skills.py              # offline checks; run before every commit
    tools/check-skills.py --kb         # also look up each cited IU KB article
    tools/check-skills.py --links      # also fetch every cited URL
    tools/check-skills.py --freshness  # the network checks tools/check-skills.toml lists
    tools/check-skills.py --version    # print the version and this file's hash
    tools/check-skills.py --kb-snapshot [KB...]  # record cited KB articles' text

This file is identical in every repository of the IU research skills family
(research-technologies, research-data, research-funding, research-cores).
Everything that differs between them lives in tools/check-skills.toml. Change
this file only in the canonical copy, then copy it to every repository; the
version line it prints lets you compare copies.

Offline checks, per skill:
  - Agent Skills format: frontmatter, name, description, length, file links.
  - A 'Verified YYYY-MM-DD' line; STALE when older than stale_after_days.
  - The skill ends with '## Keep this file current' then '## Sources'.
  - Trust markers: only the repository's markers; **Required** names a source
    matching required_source; **Observed** carries a date.
  - An id cited in the text (KB article, NIH notice) is also in Sources.
  - What stays out: emails not on allowed_emails, internal hostnames.
Offline checks, per repository: every skill has a README row and a trigger
prompt, the top-level and docs/ files pass the what-stays-out checks, and
any Claude plugin manifests in .claude-plugin/ parse, agree on the plugin
name and version, and point at a skills directory that exists.

Network checks:
  --kb      Each KB article cited as [KBnnnnnnn](https://servicenow.iu.edu/kb...)
            is found by KB search and has not changed since it was last read.
            When tools/kb-snapshot.json holds the article, the snapshot is the
            record of that reading: a newer updated date fetches the text, and
            changed text prints STALE (unchanged text prints INFO). Without a
            snapshot entry, a published or updated date after the skill's
            Verified date prints STALE. ServiceNow reports both dates; an edit
            in place changes only the updated date.
  --kb-snapshot [KB...]  Record the version, updated date, and text hash of
            the named KB articles in tools/kb-snapshot.json, or of every
            linked article when none is named. Run it right after re-reading
            those articles, and commit the file with the skill changes. This
            is the per-article record, so a Verified line needs no list of
            partial re-reads for snapshotted articles.
  --links   Each cited URL loads (BROKEN otherwise), with two retries
            10 and 20 seconds apart.
  --freshness runs the [freshness] checks and commands from the config. A
            command that exits non-zero prints CHANGED.

Exit status is 1 on any ERROR, BROKEN, or CHANGED line. STALE and WARN lines
never fail. Standard library only; Python 3.11 or newer.
"""

import datetime
import hashlib
import json
import pathlib
import re
import subprocess
import sys
import time
import tomllib
import urllib.error
import urllib.parse
import urllib.request

VERSION = "1.1.0"

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS = ROOT / ".agents" / "skills"
CONFIG = ROOT / "tools" / "check-skills.toml"
KB_SNAPSHOT = ROOT / "tools" / "kb-snapshot.json"
PLUGIN = ROOT / ".claude-plugin"

ALL_MARKERS = ("Required", "Recommended", "Observed", "External", "Practice", "Open item")
SPEC_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
DEFAULTS = {
    "markers": list(ALL_MARKERS),
    "required_source": r"policy|policies|regulation|law|agreement|terms|notice|\d+ CFR",
    "cited_ids": [r"KB\d{7}"],
    "stale_after_days": 120,
    "allowed_emails": [],
    "internal_hosts": r"[\w.-]*bioloop[\w.-]*\.iu\.edu|[\w.-]+\.sca\.iu\.edu",
    "links": {"user_agent": "research-skills-checker", "skip_403_hosts": [], "skip_urls": []},
    "freshness": {"checks": ["links"], "commands": []},
}

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
VERIFIED_RE = re.compile(r"^Verified (\d{4}-\d{2}-\d{2})", re.M)
# A partial re-read: "Verified D1 (X and Y only) ... Other sources were
# verified D2." X and Y count as checked on D1; everything else on D2.
PARTIAL_RE = re.compile(r"\(([^)]*)\bonly\)")
OTHERS_RE = re.compile(r"Other sources were\s+verified\s+(\d{4}-\d{2}-\d{2})")
DATE_RE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
KB_RE = re.compile(r"\bKB\d{7}\b")
URL_RE = re.compile(r"https?://[^\s)>\]`\"|]+")
EMAIL_RE = re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b")
MARKER_RE = re.compile(r"\*\*(" + "|".join(ALL_MARKERS) + r")\b")
KB_API = "https://servicenow.iu.edu/api/sn_km_api/knowledge/articles"


def version_line():
    digest = hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()[:12]
    return f"check-skills.py {VERSION} sha256:{digest}"


def load_config():
    cfg = {k: (dict(v) if isinstance(v, dict) else v) for k, v in DEFAULTS.items()}
    if CONFIG.is_file():
        with CONFIG.open("rb") as f:
            user = tomllib.load(f)
        for key, value in user.items():
            if key not in cfg:
                sys.exit(f"{CONFIG.name}: unknown setting {key!r}")
            if isinstance(cfg[key], dict):
                cfg[key].update(value)
            else:
                cfg[key] = value
    cfg["required_re"] = re.compile(r"\b(" + cfg["required_source"] + r")(?![\w-])", re.I)
    cfg["cited_re"] = [re.compile(r"\b" + p + r"\b") for p in cfg["cited_ids"]]
    cfg["host_re"] = re.compile(r"\b(" + cfg["internal_hosts"] + r")\b", re.I) if cfg["internal_hosts"] else None
    cfg["emails"] = {e.lower() for e in cfg["allowed_emails"]}
    unknown = set(cfg["markers"]) - set(ALL_MARKERS)
    if unknown:
        sys.exit(f"{CONFIG.name}: unknown markers {sorted(unknown)}")
    return cfg


def frontmatter(text):
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end < 0:
        return None, text
    fields = {}
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()
    return fields, text[end + 5:]


def blocks(body):
    """Split Markdown into paragraphs, list items, and table rows. Skip code."""
    out, cur, in_code = [], [], False
    for line in body.splitlines():
        if line.lstrip().startswith("```"):
            in_code = not in_code
            if cur:
                out.append(" ".join(cur))
                cur = []
            continue
        if in_code:
            continue
        starts_item = re.match(r"^\s*([-*]|\d+\.)\s|^\|", line)
        if not line.strip() or starts_item:
            if cur:
                out.append(" ".join(cur))
            cur = [line] if line.strip() else []
            if line.startswith("|"):
                out.append(line)
                cur = []
        else:
            cur.append(line.strip())
    if cur:
        out.append(" ".join(cur))
    return out


def verified_dates(body):
    """Return (date, ids checked on that date, date for every other source)."""
    match = VERIFIED_RE.search(body)
    if not match:
        return None
    para = body[match.start():].split("\n\n", 1)[0]
    partial, others = PARTIAL_RE.search(para), OTHERS_RE.search(para)
    if partial and others:
        return match.group(1), set(KB_RE.findall(partial.group(1))), others.group(1)
    return match.group(1), set(), match.group(1)


def check_content(name, text, cfg):
    """What stays out: personal emails and internal hostnames."""
    problems = []
    for m in EMAIL_RE.finditer(text):
        if m.group(0).lower() not in cfg["emails"]:
            problems.append(("ERROR", f"{name}: email {m.group(0)} is not in allowed_emails"))
    if cfg["host_re"]:
        for m in cfg["host_re"].finditer(text):
            problems.append(("ERROR", f"{name}: internal hostname {m.group(0)}"))
    return problems


def check_markers(name, text, cfg):
    problems = []
    for block in blocks(text):
        snippet = re.sub(r"\s+", " ", block)[:90]
        for marker in sorted(set(MARKER_RE.findall(block)) - set(cfg["markers"])):
            problems.append(("ERROR", f"{name}: **{marker}** is not a marker this repository uses: {snippet}"))
        if "**Required" in block and "Required" in cfg["markers"] and not cfg["required_re"].search(block):
            problems.append(("ERROR", f"{name}: Required statement names no binding source: {snippet}"))
        if "**Observed" in block and not DATE_RE.search(block):
            problems.append(("ERROR", f"{name}: Observed statement has no date: {snippet}"))
    return problems


def check_skill(skill_dir, cfg, today):
    problems = []
    path = skill_dir / "SKILL.md"
    if not path.is_file():
        return [("ERROR", "no SKILL.md")]
    text = path.read_text()
    fields, body = frontmatter(text)
    if fields is None:
        return [("ERROR", "no YAML frontmatter")]

    name, desc = fields.get("name", ""), fields.get("description", "")
    if name != skill_dir.name:
        problems.append(("ERROR", f"name {name!r} does not match directory"))
    if not NAME_RE.match(name) or len(name) > 64:
        problems.append(("ERROR", "name must be kebab-case, at most 64 characters"))
    if not desc or len(desc) > 1024:
        problems.append(("ERROR", f"description is {len(desc)} characters; spec allows 1-1024"))
    elif "Use when" not in desc:
        problems.append(("WARN", "description does not say 'Use when'"))
    extra = set(fields) - SPEC_FIELDS
    if extra:
        problems.append(("ERROR", f"unknown frontmatter fields: {sorted(extra)}"))
    if len(text.splitlines()) > 500:
        problems.append(("ERROR", "SKILL.md over 500 lines; move detail to references/"))

    dates = verified_dates(body)
    if not dates:
        problems.append(("ERROR", "no 'Verified YYYY-MM-DD' line"))
    else:
        oldest = datetime.date.fromisoformat(min(dates[0], dates[2]))
        newest = datetime.date.fromisoformat(max(dates[0], dates[2]))
        age = (today - oldest).days
        if newest > today:
            problems.append(("ERROR", f"Verified {newest} is in the future"))
        if cfg["stale_after_days"] and age > cfg["stale_after_days"]:
            problems.append(("STALE", f"Verified {oldest} is {age} days old; re-read its Sources"))

    headings = re.findall(r"^## (.+)$", body, re.M)
    if headings[-2:] != ["Keep this file current", "Sources"]:
        problems.append(("ERROR", "must end with '## Keep this file current' then '## Sources'"))

    main_text, _, sources = body.partition("\n## Sources")
    for cited_re in cfg["cited_re"]:
        for cid in sorted(set(cited_re.findall(main_text)) - set(cited_re.findall(sources))):
            problems.append(("WARN", f"{cid} cited in text but not in Sources"))

    for ref in re.findall(r"\]\(((?:references|scripts|assets)/[^)#]+)\)", body):
        if not (skill_dir / ref).exists():
            problems.append(("ERROR", f"link to missing file {ref}"))

    # "Keep this file current" tells maintainers how to use the markers; it
    # mentions them without making claims, so it is not marker-checked.
    problems += check_markers("SKILL.md", main_text.partition("\n## Keep this file current")[0], cfg)
    for f in [path, *sorted(skill_dir.glob("references/*.md"))]:
        f_text = f.read_text()
        problems += check_content(f.name, f_text, cfg)
        if f != path:
            problems += check_markers(f.name, f_text, cfg)
        for link in re.findall(r"\]\((\.\./[^)]*)\)", f_text):
            problems.append(("ERROR", f"{f.name} links outside the skill: {link}"))
    for script in sorted(p for p in skill_dir.glob("scripts/*") if p.is_file()):
        try:
            script_text = script.read_text()
        except UnicodeDecodeError:
            continue
        if cfg["host_re"]:
            for m in cfg["host_re"].finditer(script_text):
                problems.append(("ERROR", f"{script.name}: internal hostname {m.group(0)}"))
    return problems


def check_repo(names, cfg):
    """Every skill has a README row and a trigger prompt; top-level docs stay clean."""
    problems = []
    readme_path, prompts_path = ROOT / "README.md", ROOT / "tests" / "trigger-prompts.md"
    readme = readme_path.read_text() if readme_path.is_file() else ""
    prompts = prompts_path.read_text() if prompts_path.is_file() else ""
    for name in names:
        if f"(.agents/skills/{name}/SKILL.md)" not in readme:
            problems.append(("ERROR", f"{name} has no row in the README skills table"))
        if f"`{name}`" not in prompts:
            problems.append(("ERROR", f"{name} has no trigger prompt in tests/trigger-prompts.md"))
    others = [ROOT / n for n in ("README.md", "CONTRIBUTING.md", "MAINTAINING.md")]
    others += [prompts_path, *sorted((ROOT / "docs").glob("*.md"))]
    for f in others:
        if f.is_file():
            problems += check_content(str(f.relative_to(ROOT)), f.read_text(), cfg)
    return problems


def kb_get(url):
    """GET a KB API URL as JSON, backing off on 429 and 503."""
    for attempt in range(5):
        try:
            with urllib.request.urlopen(url, timeout=60) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as err:
            if err.code not in (429, 503) or attempt == 4:
                raise
            wait = err.headers.get("Retry-After", "")
            time.sleep(min(int(wait) if wait.isdigit() else 5 * 2 ** attempt, 120))


def kb_lookup(number):
    """Return a dict for a KB article from KB search, or None if not found."""
    params = urllib.parse.urlencode(
        {"query": number, "limit": 5, "fields": "published,sys_updated_on,version"})
    data = kb_get(f"{KB_API}?{params}")
    for art in data["result"]["articles"]:
        if art["number"] == number:
            fields = art.get("fields", {})
            return {
                "number": number,
                "title": art["title"],
                "sys_id": art["id"].split(":")[-1],
                "published": fields.get("published", {}).get("value", ""),
                "updated": fields.get("sys_updated_on", {}).get("value", "")[:10],
                "version": fields.get("version", {}).get("display_value", ""),
            }
    return None


def kb_text_hash(sys_id):
    """sha256 of an article's text, with tags and whitespace runs removed."""
    data = kb_get(f"{KB_API}/{sys_id}")["result"]
    body = "".join(part.get("content", "") for part in data.get("content", []))
    text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body)).strip()
    return hashlib.sha256(text.encode()).hexdigest()


def load_kb_snapshot():
    try:
        return json.loads(KB_SNAPSHOT.read_text())
    except FileNotFoundError:
        return {}


def linked_kb(skill_dir):
    """KB numbers a skill links to. An article KB search cannot find is named
    without a link, with the date it went missing, so it is not checked."""
    cited = set()
    for md in skill_dir.rglob("*.md"):
        cited |= set(re.findall(r"\[(KB\d{7})\]\(https://servicenow\.iu\.edu/kb", md.read_text()))
    return cited


def check_kb(skill_dir, cache, snapshot):
    """STALE when a cited KB article is gone, or changed after Verified."""
    path = skill_dir / "SKILL.md"
    if not path.is_file():
        return []
    dates = verified_dates(frontmatter(path.read_text())[1])
    problems = []
    for number in sorted(linked_kb(skill_dir)):
        if number not in cache:
            cache[number] = kb_lookup(number)
        row = cache[number]
        if row is None:
            problems.append(("STALE", f"{number} not found by KB search; retired or renumbered?"))
            continue
        if not dates:
            continue
        snap = snapshot.get(number)
        what = f"published {row['published']}, updated {row['updated']}, version {row['version']}"
        if snap:
            if max(row["published"], row["updated"]) <= max(snap.get("published", ""), snap.get("updated", "")):
                continue
            if "hash" not in row:
                row["hash"] = kb_text_hash(row["sys_id"])
            if row["hash"] == snap.get("sha256"):
                problems.append(("INFO", f"{number} {what}; text unchanged since snapshot {snap.get('taken')}"))
            else:
                problems.append(("STALE", f"{number} {what}; text changed since snapshot {snap.get('taken')}: {row['title']}"))
            continue
        verified = dates[0] if number in dates[1] else dates[2]
        if max(row["published"], row["updated"]) > verified:
            problems.append(("STALE", f"{number} {what}, after Verified {verified}: {row['title']}"))
    return problems


def write_kb_snapshot(names, today, only):
    """Record version, updated date, and text hash for linked articles; with
    `only`, refresh just those and keep the other entries."""
    snapshot = load_kb_snapshot() if only else {}
    linked = set().union(*(linked_kb(SKILLS / name) for name in names))
    for number in sorted(linked):
        if only and number not in only:
            continue
        row = kb_lookup(number)
        if row is None:
            print(f"STALE  {number}: not found by KB search; not recorded")
            continue
        snapshot[number] = {
            "title": row["title"], "version": row["version"],
            "published": row["published"], "updated": row["updated"],
            "sha256": kb_text_hash(row["sys_id"]), "taken": today.isoformat(),
        }
    for number in only - linked:
        print(f"WARN   {number}: no skill links to it; not recorded")
    snapshot = {k: v for k, v in snapshot.items() if k in linked}
    KB_SNAPSHOT.write_text(json.dumps(dict(sorted(snapshot.items())), indent=2) + "\n")
    print(f"Wrote {len(snapshot)} KB articles to {KB_SNAPSHOT.relative_to(ROOT)}")


def check_plugin(names):
    """Claude plugin manifests, when present, parse and agree with each other."""
    problems = []
    if not PLUGIN.is_dir():
        return problems
    manifests = {}
    for fname in ("plugin.json", "marketplace.json"):
        f = PLUGIN / fname
        if not f.is_file():
            problems.append(("ERROR", f".claude-plugin/{fname} is missing"))
            continue
        try:
            manifests[fname] = json.loads(f.read_text())
        except json.JSONDecodeError as err:
            problems.append(("ERROR", f".claude-plugin/{fname} is not valid JSON: {err}"))
    plugin, market = manifests.get("plugin.json"), manifests.get("marketplace.json")
    if plugin:
        skills = plugin.get("skills")
        for rel in [skills] if isinstance(skills, str) else (skills or []):
            if not (ROOT / rel).is_dir():
                problems.append(("ERROR", f"plugin.json skills path {rel} does not exist"))
    if plugin and market:
        entries = {e.get("name"): e for e in market.get("plugins", [])}
        entry = entries.get(plugin.get("name"))
        if entry is None:
            problems.append(("ERROR", f"marketplace.json lists no plugin named {plugin.get('name')}"))
        elif entry.get("version") and entry.get("version") != plugin.get("version"):
            problems.append(("WARN", f"plugin version {plugin.get('version')} in plugin.json, {entry.get('version')} in marketplace.json"))
    return problems


def check_links(cfg):
    lc = cfg["links"]
    urls = {}
    for f in [*SKILLS.rglob("*.md"), *(ROOT / "docs").glob("*.md"), ROOT / "README.md"]:
        if not f.is_file():
            continue
        for url in URL_RE.findall(f.read_text()):
            url = url.rstrip(".,;:")
            if "<" in url or "example" in url:
                continue
            urls.setdefault(url, f.relative_to(ROOT))
    broken = 0
    for url, where in sorted(urls.items()):
        if url in lc["skip_urls"]:
            print(f"SKIP    {url}  (skip_urls)")
            continue
        req = urllib.request.Request(url, headers={"User-Agent": f"Mozilla/5.0 {lc['user_agent']}"})
        for attempt in range(3):  # two retries, for transient errors
            try:
                with urllib.request.urlopen(req, timeout=45) as resp:
                    status = resp.status
            except urllib.error.HTTPError as e:
                status = e.code
            except Exception as e:  # network errors are reported, not fatal
                status = type(e).__name__
            if status == 200 or (isinstance(status, int) and status < 429):
                break
            if attempt < 2:
                time.sleep(10 * (attempt + 1))
        if status == 200:
            continue
        host = urllib.parse.urlparse(url).hostname or ""
        if status in (202, 403) and host in lc["skip_403_hosts"]:
            print(f"SKIP    {url}  ({status}; host refuses scripted requests)")
            continue
        print(f"BROKEN  {url}  ({status}) in {where}")
        broken += 1
        time.sleep(0.5)
    print(f"{len(urls)} URLs checked, {broken} broken.")
    return broken


def run_commands(cfg):
    changed = 0
    for cmd in cfg["freshness"]["commands"]:
        print(f"== {cmd['name']}: {cmd['run']}")
        result = subprocess.run(cmd["run"], shell=True, cwd=ROOT, capture_output=True, text=True)
        print((result.stdout + result.stderr).rstrip())
        if result.returncode:
            print(f"CHANGED  {cmd['name']}: exit {result.returncode}; see {cmd.get('step', 'MAINTAINING.md')}")
            changed += 1
    return changed


def main(argv):
    if "--version" in argv:
        print(version_line())
        return 0
    cfg = load_config()
    print(version_line())
    today = datetime.date.today()
    if "--kb-snapshot" in argv:
        only = {a.upper() for a in argv if re.fullmatch(r"(?i)KB\d{7}", a)}
        write_kb_snapshot(sorted(p.name for p in SKILLS.iterdir() if p.is_dir()), today, only)
        return 0
    checks = set(a.lstrip("-") for a in argv if a in ("--kb", "--links"))
    if "--freshness" in argv:
        checks |= set(cfg["freshness"]["checks"])
    failed = False
    cache = {}
    snapshot = load_kb_snapshot() if "kb" in checks else {}
    names = sorted(p.name for p in SKILLS.iterdir() if p.is_dir())
    for name in names:
        problems = check_skill(SKILLS / name, cfg, today)
        if "kb" in checks:
            problems += check_kb(SKILLS / name, cache, snapshot)
        for level, msg in problems:
            print(f"{level:5}  {name}: {msg}")
            failed |= level == "ERROR"
    for level, msg in check_repo(names, cfg) + check_plugin(names):
        print(f"{level:5}  repository: {msg}")
        failed |= level == "ERROR"
    if "kb" in checks:
        print(f"{len(cache)} KB articles checked.")
    if "links" in checks and check_links(cfg):
        failed = True
    if "--freshness" in argv and run_commands(cfg):
        failed = True
    if not failed:
        print(f"OK: {len(names)} skills")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
