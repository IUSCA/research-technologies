---
name: searching-the-iu-knowledge-base
description: Search and read Indiana University Knowledge Base (KB) articles from a terminal, cite them correctly, and decide whether the KB or the live system is right when they disagree. Includes a standard-library script for the ServiceNow Knowledge API, since KB pages render with JavaScript and old kb.iu.edu links lose the article. Use when a question about IU systems, policies, accounts, or services needs an authoritative answer, when checking a claim in another IU skill, or when a kb.iu.edu link does not open the article.
---

# Searching the IU Knowledge Base

Verified 2026-10-01 against the IU Knowledge Base (KB) and its public API.

Answer IU questions from the KB, not from memory. IU systems retire and get
renamed often, so remembered facts go stale.

## Search and read from a terminal

The KB runs on ServiceNow and builds each page with JavaScript. A plain fetch
of an article page returns an empty shell. **Observed 2026-10-01:** old
`kb.iu.edu/d/<id>` links redirect to the KB home page and lose the article.

[scripts/iukb.py](scripts/iukb.py) uses the ServiceNow Knowledge API instead.
That API answers anonymous requests. The script needs only Python 3.

```bash
scripts/iukb.py search Quartz GPU    # KB number, published date, title
scripts/iukb.py read KB0024722       # article text, links in brackets
```

A bracketed number such as `[KB0024722]` in the output links to another
article. Read it with another `read`. A bracketed URL is a link outside the
KB.

Search terms match titles and bodies. Try the system name, the task, and any
old name. The published date shows how recently an article changed.

## Retired articles disappear

Retired articles drop out of KB search (KB0024722). `read` then reports the
number as not found. Treat that as a sign the system or process may be gone.
Ask the KB team at kb@iu.edu when a retired article matters (KB0024722).

## Cite what you used

Cite an article by number, with a link of this form:

```text
https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024722
```

Name the KB number next to each claim it supports. Say when you read it.

## The KB or the system: which one wins

The live system wins for facts it can report. These include node and GPU
counts, partitions, time limits, quotas, array limits, and installed modules.
Hardware gets upgraded before articles do. Check with a command on the
system, and say the answer was observed, with the date and host. The
`submitting-hpc-jobs` skill has a script that reports these facts.

The KB wins for policy and process. These include eligibility, data
classification, PHI rules, renewal dates, and who to contact. A system cannot
report these facts.

When two KB articles disagree and the system cannot settle it, quote both
numbers. Do not pick the more plausible one. Ask the owning team; see the
`getting-help-from-research-technologies` skill.

## Keep this file current

Run `scripts/iukb.py search Quartz` after any KB platform change. If it fails,
fix the script before relying on any IU skill. Re-read KB0024722 if retired
articles start to behave differently.

## Sources

IU KB article, read 2026-10-01:

- [KB0024722](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024722) About archived content in the IU Knowledge Base

External: the ServiceNow Knowledge API at
`https://servicenow.iu.edu/api/sn_km_api/knowledge/articles`, used 2026-10-01.
