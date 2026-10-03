#!/usr/bin/env python3
"""Check every skill in .agents/skills for format and staleness.

Usage:
    tools/check-skills.py          # format checks only, no network
    tools/check-skills.py --kb     # also check each cited KB article

Format checks follow the Agent Skills specification and CONTRIBUTING.md.
The --kb check flags a cited article that was published after the skill's
Verified date, or that KB search no longer finds (often a retired article).

Exits 1 when any skill has an ERROR. STALE and WARN lines do not fail.
Standard library only.
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS = ROOT / ".agents" / "skills"
sys.path.insert(0, str(SKILLS / "searching-the-iu-knowledge-base" / "scripts"))

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
VERIFIED_RE = re.compile(r"^Verified (\d{4}-\d{2}-\d{2})", re.M)
# A partial check reads "Verified D1 (KB... only) ... Other sources were
# verified D2". The named articles count as checked on D1, the rest on D2.
PARTIAL_RE = re.compile(r"\(([^)]*\bKB\d{7}[^)]*)\bonly\)")
OTHERS_RE = re.compile(r"Other sources were\s+verified\s+(\d{4}-\d{2}-\d{2})")
KB_RE = re.compile(r"\bKB\d{7}\b")
SOURCE_RE = re.compile(r"\[(KB\d{7})\]\(https://servicenow\.iu\.edu/kb")


def frontmatter(text):
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end < 0:
        return None, text
    fields = {}
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith(" "):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()
    return fields, text[end + 5:]


def check_format(skill_dir):
    problems = []
    path = skill_dir / "SKILL.md"
    if not path.is_file():
        return [("ERROR", "no SKILL.md")], None, set()
    text = path.read_text()
    fields, body = frontmatter(text)
    if fields is None:
        return [("ERROR", "no YAML frontmatter")], None, set()

    name = fields.get("name", "")
    desc = fields.get("description", "")
    if name != skill_dir.name:
        problems.append(("ERROR", f"name '{name}' differs from directory"))
    if not NAME_RE.match(name) or len(name) > 64:
        problems.append(("ERROR", "name breaks the spec's naming rules"))
    if not 1 <= len(desc) <= 1024:
        problems.append(("ERROR", f"description is {len(desc)} chars; spec allows 1-1024"))
    for key in fields:
        if key not in ("name", "description", "license", "compatibility",
                       "metadata", "allowed-tools"):
            problems.append(("WARN", f"frontmatter field '{key}' is not in the spec"))

    lines = body.count("\n")
    if lines > 500:
        problems.append(("WARN", f"body is {lines} lines; spec suggests under 500"))
    match = VERIFIED_RE.search(body)
    if not match:
        problems.append(("ERROR", "no 'Verified YYYY-MM-DD' line"))
    for heading in ("## Keep this file current", "## Sources"):
        if heading not in body:
            problems.append(("ERROR", f"missing '{heading}' section"))

    for ref in re.findall(r"\]\(((?:references|scripts|assets)/[^)#]+)\)", body):
        if not (skill_dir / ref).exists():
            problems.append(("ERROR", f"link to missing file {ref}"))

    mentioned, cited = set(), set()
    for md in skill_dir.rglob("*.md"):
        md_text = md.read_text()
        mentioned |= set(KB_RE.findall(md_text))
        cited |= set(SOURCE_RE.findall(md_text))
    for number in sorted(mentioned - cited):
        problems.append(("WARN", f"{number} is mentioned but not in a Sources list"))
    verified = None
    if match:
        para = body[match.start():].split("\n\n", 1)[0]
        partial, others = PARTIAL_RE.search(para), OTHERS_RE.search(para)
        if partial and others:
            verified = (match.group(1), set(KB_RE.findall(partial.group(1))), others.group(1))
        else:
            verified = (match.group(1), set(), match.group(1))
    return problems, verified, cited


def check_kb(cited, verified, cache):
    import iukb

    problems = []
    for number in sorted(cited):
        if number not in cache:
            rows = [r for r in iukb.search(number, limit=5) if r[0] == number]
            cache[number] = rows[0] if rows else None
        row = cache[number]
        if row is None:
            problems.append(("STALE", f"{number} not found by KB search; retired or renumbered?"))
        elif verified:
            date = verified[0] if number in verified[1] else verified[2]
            if row[2] > date:
                problems.append(("STALE", f"{number} published {row[2]}, after Verified {date}: {row[3]}"))
    return problems


def main(argv):
    with_kb = "--kb" in argv
    cache = {}
    failed = False
    for skill_dir in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        problems, verified, cited = check_format(skill_dir)
        if with_kb:
            problems += check_kb(cited, verified, cache)
        status = "ok" if not problems else ""
        shown = verified and (verified[0] if verified[0] == verified[2] else f"{verified[0]} (partial; others {verified[2]})")
        print(f"{skill_dir.name}: verified {shown}, {len(cited)} KB articles {status}")
        for level, message in problems:
            print(f"  {level:5} {message}")
            failed |= level == "ERROR"
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
