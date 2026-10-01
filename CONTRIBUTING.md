# Verifying and updating a skill

A skill is only as good as its last check against the IU Knowledge Base (KB).
Update a skill whenever an agent finds a claim that no longer matches the KB.

## Fetch the KB article, not a memory of it

The KB runs on ServiceNow and builds each page with JavaScript. A plain fetch
of an article URL returns an empty page shell. Old `kb.iu.edu/d/<id>` links
redirect to the KB home page and drop the article id.

The ServiceNow Knowledge API answers anonymous requests. `tools/iukb.py` wraps
it and needs only the Python standard library.

```bash
tools/iukb.py search Quartz        # KB number, published date, title
tools/iukb.py read KB0023985       # article text, links shown in brackets
```

A bracketed `[KB0012345]` in the output is a link to another article. Follow
it with another `read`.

Retired articles drop out of KB search. The KB says so in "About archived
content in the IU Knowledge Base" (KB0024722). Ask the KB team at kb@iu.edu
when a retired article matters.

## Cite each claim

Cite the KB article by number with a link of this form:

```text
https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023985
```

Each skill keeps its citations in a Sources list at the end. Inline text names
the KB number next to the claim it supports. Mark a claim from a non-KB source as
**External** and name it.

## Record what is unknown

Write an open item when the KB is silent or contradicts itself. Name the
articles that disagree and quote the numbers that differ. Do not resolve a
contradiction by picking the more plausible value.

Record a retired system as retired. An agent that does not see a system
listed may assume it still exists.

## Update the verified date

Each skill carries a `Verified <date>` line near the top. Change it only after
re-reading every article in that skill's Sources list. A partial check updates
the line for the claims checked, as in `Verified 2026-10-01 (partitions only)`.

## Style

- One idea per sentence, under 25 words, with the serial comma.
- Lead each section with its claim, then support it.
- Keep skills harness-neutral. Do not name a harness's tools.
- Keep `name` in the frontmatter equal to the directory name, in kebab-case.
- End every skill with a "Keep this file current" section.

## Commits

Make one focused commit per skill change. Say in the message which KB articles
were re-read.
