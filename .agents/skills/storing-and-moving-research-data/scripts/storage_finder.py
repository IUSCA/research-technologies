#!/usr/bin/env python3
"""Answer the IU Data Storage Finder's questions from the command line.

The Finder at https://datastoragefinder.iu.edu/dsf/ keeps its logic in a
public file, config.js: each answer lists the storage services it allows.
This script reads that file and the Finder page live on every run, so the
Finder's own maintainers stay the source of its service lists.

    storage_finder.py questions                 # the questions and answer keys
    storage_finder.py match 1.1 2.2 4.4 5.4 6.1 --classification restricted
    storage_finder.py match 1.2 2.1 --classification critical-phi --table
    storage_finder.py table SD SP GS            # comparison rows from the page

Pass at most one answer key per question, as the Finder's radio buttons do.
Leave a question out when its answer is not known; the Finder does the same.

Classification is a separate flag, because the Finder's "Critical" answer
does not separate PHI from other Critical data:

    public, university-internal, restricted   the Finder's answer, unchanged
    critical-phi     the Finder's Critical answer, unchanged
    critical-other   the Finder's Critical answer, then the KB rule below

The KB says Critical data other than PHI is not permitted on Research
Technologies systems. For critical-other the script keeps only the services
in KB_CRITICAL_OTHER_ALLOWED and prints why each other one was removed. That
table is the only data written into this script; each line names its KB
article.

Standard library only. Exits 3 if the Finder's files no longer have the
structure this script expects, so a change is noticed, not misread.
Set DSF_BASE_URL to read another copy of the Finder.
"""
import argparse
import html
import html.parser
import json
import os
import re
import sys
import urllib.error
import urllib.request

BASE_URL = os.environ.get(
    "DSF_BASE_URL", "https://datastoragefinder.iu.edu/dsf/"
).rstrip("/") + "/"
CONFIG_URL = BASE_URL + "config.js"
PAGE_URL = BASE_URL
USER_AGENT = (
    "research-technologies-skills storage_finder.py "
    "(+https://github.com/IUSCA/research-technologies)"
)
KB_URL = "https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article="

# --- The only hardcoded data: the KB rule for Critical data other than PHI.
# Key: the Finder's storage code. The name is checked against config.js so a
# renamed or reused code fails loudly instead of being misapplied.

# Services KB0023604 lists with "Critical" as the most sensitive classification
# allowed (other than PHI). Both must be the Secure Storage form of the service.
KB_CRITICAL_OTHER_ALLOWED = {
    "GS": ("Google Shared Drives", "KB0023604: Paid Google Shared Drives, Critical (other than PHI); request as Google Secure Storage"),
    "MS": ("Microsoft Teams", "KB0023604: Microsoft at IU Secure Storage, Critical (other than PHI); a Teams site requested as Secure Storage (KB0025537)"),
}

# Research Technologies services: Restricted at most, other than PHI.
KB_CRITICAL_OTHER_REMOVED = {
    "SD": ("SDA", "KB0024406, KB0025747, KB0023604: SDA allows Restricted at most (other than PHI)"),
    "HD": ("Home Directories", "KB0023515, KB0025747, KB0023604: research supercomputers allow Restricted at most (other than PHI)"),
    "GP": ("Geode Project", "KB0025747, KB0023604: Geode-Project allows Restricted at most (other than PHI)"),
    "SL": ("Slate", "KB0022478, KB0025747, KB0023604: Slate allows Restricted at most (other than PHI)"),
    "SS": ("Slate Scratch", "KB0022478, KB0025747, KB0023604: Slate-Scratch allows Restricted at most (other than PHI)"),
    "SP": ("Slate Project", "KB0022478, KB0025747, KB0023604: Slate-Project allows Restricted at most (other than PHI)"),
    "RD": ("Research Databases", "KB0022767, KB0025747, KB0023604: ResDB allows Restricted at most (other than PHI)"),
    "DS": ("Scholarly Data Share", "KB0025720: no limit stated; data is stored on the SDA, which allows Restricted at most (KB0024406)"),
}

CRITICAL_OTHER_WARNING = """\
WARNING: Critical data other than PHI is not permitted on Research
Technologies systems (KB0023515, KB0024406, KB0022478, KB0022767).
The Finder's "Critical" answer still lists them. KB0025747 and KB0023604
give them Restricted at most, other than PHI. This result keeps only
services KB0023604 allows for Critical data other than PHI. KB0023604
also excludes payment card, export-controlled, CUI, and advancement data
from those services. Ask securemyresearch@iu.edu before storing it."""

PHI_NOTE = """\
NOTE: PHI may go on these services only with the safeguards their KB
articles require (KB0023604, KB0023515). On Research Technologies systems,
encrypt PHI files and keep them in a private directory (KB0022478). Use an
individual login, never a group account (KB0023604). Ask
securemyresearch@iu.edu about HIPAA-regulated research data."""

GOOGLE_DRIVE_NOTE = """\
NOTE: The Finder's answers offer Google Drive above Public, but its own
comparison table says "Public" only. KB0023604 allows University-internal
and some Restricted data in Google at IU My Drive, and no PHI. Confirm in
KB0023604 before using it for anything above Public."""

SECURE_STORAGE_NOTE = """\
NOTE: KB0023604 lists Google Shared Drives and Microsoft Teams for
Restricted, Critical, and PHI data as Secure Storage: Google Secure
Storage, or Microsoft at IU Secure Storage. Request it with the
Institutional storage request form, choosing the data's classification
(KB0023604, KB0025537)."""

SDS_NOTE = """\
NOTE: Scholarly Data Share's KB article (KB0025720) states no data
classification limit. Its data is stored on the SDA (KB0024406)."""

NO_CLASSIFICATION_NOTE = """\
NOTE: No classification was given, so this list includes services that
may not allow the data. Get the classification from the researcher, or
classify it with the classifying-research-data skill in research-data."""

CLASSIFICATIONS = {
    # flag value: words that identify the Finder's choice title
    "public": "public",
    "university-internal": "university internal",
    "restricted": "restricted",
    "critical-phi": "critical",
    "critical-other": "critical",
}


class FinderChanged(Exception):
    """The Finder's files no longer have the structure this script expects."""


class FetchError(Exception):
    pass


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as err:
        raise FetchError(f"HTTP {err.code} from {url}")
    except urllib.error.URLError as err:
        raise FetchError(f"Cannot reach {url}: {err.reason}")


# --- config.js: a JavaScript object literal, converted to JSON by a scanner.

def js_object_to_json(text):
    """Convert one JavaScript object literal to JSON text.

    Handles single- and double-quoted strings, bare identifier keys,
    comments, and trailing commas. Anything else (functions, expressions,
    template strings) raises FinderChanged.
    """
    out = []
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if c in "'\"":
            quote, j, buf = c, i + 1, []
            while j < n and text[j] != quote:
                if text[j] == "\\" and j + 1 < n:
                    buf.append(text[j:j + 2])
                    j += 2
                    continue
                if text[j] == "\n":
                    raise FinderChanged("unterminated string in config.js")
                buf.append(text[j])
                j += 1
            if j >= n:
                raise FinderChanged("unterminated string in config.js")
            raw = "".join(buf)
            if quote == "'":
                # \' is not a JSON escape, and a bare " must become one.
                raw = re.sub(r'\\\'|(?<!\\)"', lambda m: "'" if m.group(0) != '"' else '\\"', raw)
            try:
                value = json.loads('"' + raw + '"')
            except json.JSONDecodeError:
                raise FinderChanged(f"cannot read string {raw[:40]!r} in config.js")
            out.append(json.dumps(value))
            i = j + 1
        elif text.startswith("//", i):
            j = text.find("\n", i)
            i = n if j < 0 else j
        elif text.startswith("/*", i):
            j = text.find("*/", i + 2)
            if j < 0:
                raise FinderChanged("unterminated comment in config.js")
            i = j + 2
        elif c == "`":
            raise FinderChanged("template string in config.js")
        elif c.isalpha() or c in "_$":
            m = re.compile(r"[A-Za-z_$][\w$]*").match(text, i)
            word = m.group(0)
            if word in ("true", "false", "null"):
                out.append(word)
            else:
                rest = text[m.end():].lstrip()
                if not rest.startswith(":"):
                    raise FinderChanged(f"unexpected identifier {word!r} in config.js")
                out.append(json.dumps(word))
            i = m.end()
        elif c == ",":
            rest = re.compile(r"(\s|//[^\n]*|/\*.*?\*/)*", re.S).match(text, i + 1)
            if text[rest.end():rest.end() + 1] not in ("}", "]"):
                out.append(c)
            i += 1
        elif c in "{}[]:" or c.isspace() or c.isdigit() or c in "-.":
            out.append(c)
            i += 1
        else:
            raise FinderChanged(f"unexpected character {c!r} in config.js")
    return "".join(out)


def parse_config(js):
    m = re.search(r"\bconfig_data\s*=\s*", js)
    if not m:
        raise FinderChanged("config.js no longer assigns config_data")
    body = js[m.end():].strip()
    body = re.sub(r";\s*$", "", body)
    try:
        data = json.loads(js_object_to_json(body))
    except json.JSONDecodeError as err:
        raise FinderChanged(f"config_data is not a plain object literal: {err}")
    validate_config(data)
    return data


def validate_config(data):
    def need(cond, msg):
        if not cond:
            raise FinderChanged(msg)

    need(isinstance(data, dict), "config_data is not an object")
    for field in ("storagekeys", "encryption_required", "questions"):
        need(field in data, f"config_data has no {field!r}")
    keys = data["storagekeys"]
    need(isinstance(keys, dict) and keys, "storagekeys is not a non-empty object")
    need(all(isinstance(k, str) and isinstance(v, str) for k, v in keys.items()),
         "storagekeys does not map codes to names")
    need(isinstance(data["encryption_required"], list), "encryption_required is not a list")
    for code in data["encryption_required"]:
        need(code in keys, f"encryption_required names unknown code {code!r}")
    questions = data["questions"]
    need(isinstance(questions, list) and questions, "questions is not a non-empty list")
    seen = set()
    for q in questions:
        need(isinstance(q, dict) and "question_key" in q and "title" in q and "choices" in q,
             "a question lacks question_key, title, or choices")
        need(isinstance(q["choices"], list) and q["choices"], f"question {q['question_key']} has no choices")
        for ch in q["choices"]:
            need(isinstance(ch, dict) and {"key", "title", "storages"} <= ch.keys(),
                 f"a choice in question {q['question_key']} lacks key, title, or storages")
            need(str(ch["key"]).split(".")[0] == str(q["question_key"]),
                 f"choice {ch['key']} is not under question {q['question_key']}")
            need(ch["key"] not in seen, f"choice key {ch['key']} repeats")
            seen.add(ch["key"])
            for code in ch["storages"]:
                need(code in keys, f"choice {ch['key']} names unknown code {code!r}")
    # The KB override must still point at the services it was written for.
    for table in (KB_CRITICAL_OTHER_ALLOWED, KB_CRITICAL_OTHER_REMOVED):
        for code, (name, _) in table.items():
            need(code in keys, f"KB override code {code!r} is gone from storagekeys")
            need(keys[code] == name,
                 f"KB override expects {code} = {name!r}, config.js says {keys[code]!r}")
    classification_question(data)


def classification_question(data):
    """Return the question whose choices are the four DM-01 classifications."""
    for q in data["questions"]:
        titles = {norm(ch["title"]) for ch in q["choices"]}
        if "classification" in q["title"].lower():
            missing = set(CLASSIFICATIONS.values()) - titles
            if missing:
                raise FinderChanged(
                    f"classification question lacks {sorted(missing)}; it has {sorted(titles)}")
            return q
    raise FinderChanged("no question about classification in config.js")


def norm(title):
    return re.sub(r"[\s-]+", " ", title).strip().lower()


# --- The Finder page: the comparison table.

class TableParser(html.parser.HTMLParser):
    """Collect the storage comparison table: headers and one row per code."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_table = False
        self.headers = []
        self.rows = {}
        self.row = None
        self.cell = None
        self.href = None
        self.section = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "table" and a.get("id") == "storage-table":
            self.in_table = True
        if not self.in_table:
            return
        if tag in ("thead", "tbody"):
            self.section = tag
        elif tag == "tr" and self.section == "tbody":
            m = re.fullmatch(r"storage-entry-(\w+)", a.get("id") or "")
            self.row = {"code": m.group(1) if m else None, "cells": [], "link": None}
        elif tag in ("th", "td"):
            self.cell = []
        elif tag == "a" and self.row is not None and self.cell is not None and a.get("href"):
            self.row["link"] = self.row["link"] or a["href"]

    def handle_endtag(self, tag):
        if not self.in_table:
            return
        if tag in ("th", "td") and self.cell is not None:
            text = re.sub(r"\s+", " ", "".join(self.cell)).strip()
            if self.section == "thead":
                self.headers.append(text)
            elif self.row is not None:
                self.row["cells"].append(text)
            self.cell = None
        elif tag == "tr" and self.row is not None:
            if self.row["code"]:
                self.rows[self.row["code"]] = self.row
            self.row = None
        elif tag == "table":
            self.in_table = False

    def handle_data(self, data):
        if self.in_table and self.cell is not None:
            self.cell.append(data)


def parse_table(page, config):
    p = TableParser()
    p.feed(page)
    if not p.headers or not p.rows:
        raise FinderChanged("the Finder page has no storage-table with rows")
    if p.headers[0].lower() != "storage":
        raise FinderChanged(f"the table's first column is {p.headers[0]!r}, not 'Storage'")
    table = {}
    for code, row in p.rows.items():
        if len(row["cells"]) != len(p.headers):
            raise FinderChanged(
                f"row {code} has {len(row['cells'])} cells for {len(p.headers)} headers")
        table[code] = {
            "fields": dict(zip(p.headers, row["cells"])),
            "link": html.unescape(row["link"]) if row["link"] else None,
        }
    missing = set(config["storagekeys"]) - set(table)
    if missing:
        raise FinderChanged(f"the page's table has no row for {sorted(missing)}")
    return p.headers, table


def kb_number(link):
    m = re.search(r"sysparm_article=(KB\d{7})", link or "")
    return m.group(1) if m else None


# --- Commands

def load(want_table):
    config = parse_config(fetch(CONFIG_URL))
    headers, table = (None, None)
    if want_table:
        headers, table = parse_table(fetch(PAGE_URL), config)
    return config, headers, table


def cmd_questions(args):
    config, _, _ = load(False)
    if args.json:
        print(json.dumps(config["questions"], indent=2))
        return 0
    print(f"Source: {CONFIG_URL}")
    for q in config["questions"]:
        print(f"\n{q['question_key']}. {q['title']}")
        for ch in q["choices"]:
            print(f"   {ch['key']:5} {ch['title']}")
    cq = classification_question(config)
    print(f"\nFor question {cq['question_key']}, pass --classification instead of a key:")
    print("   " + ", ".join(CLASSIFICATIONS))
    print("critical-phi and critical-other both answer the Finder's Critical;")
    print("critical-other then applies the KB rule for Critical data other than PHI.")
    return 0


def resolve_answers(config, keys, classification):
    choices = {ch["key"]: (q, ch) for q in config["questions"] for ch in q["choices"]}
    cq = classification_question(config)
    by_question = {}
    for key in keys:
        if key not in choices:
            raise SystemExit(f"error: unknown answer key {key!r}; run 'questions' to list them")
        q, _ = choices[key]
        if q["question_key"] in by_question:
            raise SystemExit(
                f"error: {by_question[q['question_key']]} and {key} both answer question "
                f"{q['question_key']}; the Finder takes one answer per question")
        by_question[q["question_key"]] = key
    given = by_question.get(cq["question_key"])
    if classification:
        word = CLASSIFICATIONS[classification]
        wanted = next(ch["key"] for ch in cq["choices"] if norm(ch["title"]) == word)
        if given and given != wanted:
            raise SystemExit(f"error: answer {given} contradicts --classification {classification}")
        by_question[cq["question_key"]] = wanted
    elif given:
        title = norm(choices[given][1]["title"])
        if title == "critical":
            raise SystemExit(
                f"error: {given} (Critical) does not separate PHI from other Critical data. "
                "Use --classification critical-phi or --classification critical-other.")
        classification = next(k for k, v in CLASSIFICATIONS.items() if v == title)
    return [by_question[k] for k in sorted(by_question, key=str)], classification, choices


def cmd_match(args):
    config, headers, table = load(True)
    names = config["storagekeys"]
    answers, classification, choices = resolve_answers(config, args.keys, args.classification)

    allowed = list(names)  # the Finder's order
    for key in answers:
        allowed = [c for c in allowed if c in choices[key][1]["storages"]]

    removed = []
    if classification == "critical-other":
        removed = [(c, KB_CRITICAL_OTHER_REMOVED.get(c, (None, "not listed in KB0023604 for Critical data other than PHI"))[1])
                   for c in allowed if c not in KB_CRITICAL_OTHER_ALLOWED]
        allowed = [c for c in allowed if c in KB_CRITICAL_OTHER_ALLOWED]

    critical = classification in ("critical-phi", "critical-other")
    encrypt = set(config["encryption_required"]) if critical else set()
    unanswered = [q for q in config["questions"]
                  if not any(str(k).split(".")[0] == str(q["question_key"]) for k in answers)]

    notes = []
    if classification == "critical-other":
        notes.append(CRITICAL_OTHER_WARNING)
    if classification == "critical-phi":
        notes.append(PHI_NOTE)
    if classification is None:
        notes.append(NO_CLASSIFICATION_NOTE)
    if "GD" in allowed and classification != "public" and \
            "public" == norm(table["GD"]["fields"].get("Data Allowed", "")):
        notes.append(GOOGLE_DRIVE_NOTE)
    if {"GS", "MS"} & set(allowed) and classification in ("restricted", "critical-phi", "critical-other"):
        notes.append(SECURE_STORAGE_NOTE)
    if "DS" in allowed and classification in ("restricted", "critical-phi"):
        notes.append(SDS_NOTE)

    result = {
        "source": CONFIG_URL,
        "answers": [{"key": k, "question": choices[k][0]["title"], "answer": choices[k][1]["title"]}
                    for k in answers],
        "classification": classification,
        "unanswered": [q["title"] for q in unanswered],
        "services": [{"code": c, "name": names[c], "encryption_required": c in encrypt,
                      "finder_link": table[c]["link"], "kb": kb_number(table[c]["link"])}
                     for c in allowed],
        "removed_by_kb_rule": [{"code": c, "name": names[c], "reason": r} for c, r in removed],
        "notes": notes,
    }
    if args.json:
        if args.table:
            result["table"] = {c: table[c]["fields"] for c in allowed}
        print(json.dumps(result, indent=2))
        return 0

    print(f"Source: {CONFIG_URL} (read live)")
    print("Answers:")
    for a in result["answers"]:
        print(f"   {a['key']:5} {a['question']} -> {a['answer']}")
    if classification:
        print(f"   classification flag: {classification}")
    for t in result["unanswered"]:
        print(f"   (not answered) {t}")
    print()
    if allowed:
        print(f"{len(allowed)} service(s) match:")
        for s in result["services"]:
            enc = "  [encryption required]" if s["encryption_required"] else ""
            kb = f"  {s['kb']}" if s["kb"] else (f"  {s['finder_link']}" if s["finder_link"] else "")
            print(f"   {s['code']}  {s['name']}{enc}{kb}")
    else:
        print("No service matches these answers. The Finder asks you to contact its")
        print(f"maintainers for a consultation (the contact link on {PAGE_URL}).")
    if removed:
        print("\nRemoved by the KB rule for Critical data other than PHI:")
        for r in result["removed_by_kb_rule"]:
            print(f"   {r['code']}  {r['name']}: {r['reason']}")
    for note in notes:
        print()
        print(note)
    if args.table and allowed:
        print()
        print_table(headers, table, allowed, names)
    print("\nThe Finder is guidance. Each service's KB article governs what it allows.")
    return 0


def print_table(headers, table, codes, names):
    for code in codes:
        row = table[code]
        print(f"== {code}  {row['fields'][headers[0]] or names[code]}")
        if row["link"]:
            print(f"   {'Link':22} {row['link']}")
        for h in headers[1:]:
            print(f"   {h + ':':22} {row['fields'][h]}")


def cmd_table(args):
    config, headers, table = load(True)
    names = config["storagekeys"]
    codes = [c.upper() for c in args.codes] or list(names)
    unknown = [c for c in codes if c not in table]
    if unknown:
        raise SystemExit(f"error: unknown storage code(s) {unknown}; known: {', '.join(names)}")
    if args.json:
        print(json.dumps({c: dict(table[c]["fields"], link=table[c]["link"]) for c in codes}, indent=2))
        return 0
    print(f"Source: {PAGE_URL} (read live)\n")
    print_table(headers, table, codes, names)
    return 0


def main():
    ap = argparse.ArgumentParser(
        description=__doc__.split("\n\n")[0],
        epilog="Run 'questions' first to see the answer keys.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("questions", help="list the Finder's questions and answer keys")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_questions)

    p = sub.add_parser("match", help="list the services allowed by a set of answers")
    p.add_argument("keys", nargs="*", help="answer keys such as 1.1 2.2 4.4")
    p.add_argument("--classification", choices=list(CLASSIFICATIONS),
                   help="highest data classification; required to answer Critical")
    p.add_argument("--table", action="store_true", help="also print the comparison rows")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_match)

    p = sub.add_parser("table", help="print the Finder page's comparison rows")
    p.add_argument("codes", nargs="*", help="storage codes such as SD GS; all if none")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_table)

    args = ap.parse_args()
    try:
        return args.func(args)
    except FetchError as err:
        print(f"error: {err}", file=sys.stderr)
        return 2
    except FinderChanged as err:
        print(f"error: the Data Storage Finder changed and this script no longer reads it: {err}",
              file=sys.stderr)
        print("Do not guess the answer. Use the Finder in a browser, and report the change:",
              file=sys.stderr)
        print("https://github.com/IUSCA/research-technologies/issues/new/choose", file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
