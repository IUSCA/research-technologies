# Verifying and updating a skill

A skill is only as good as its last check. Update a skill whenever an agent
finds a claim that no longer matches the live system or the IU Knowledge Base
(KB). [MAINTAINING.md](MAINTAINING.md) is the runbook for reviewing the whole
set.

## Let the system answer what it can

The live system is the judge of facts it can report. Check these with a
command, not a document:

| Fact | Check with |
| --- | --- |
| Partitions, node and GPU counts, time limits, QOS and array limits | `submitting-hpc-jobs/scripts/describe-cluster.sh` on a login node |
| A person's Slurm accounts, storage, and SDA access | `checking-iu-research-access/scripts/check-cluster.sh` |
| Quotas | `quota` on a login node |
| Installed software | `module spider <word>` |
| REALLMS models | the API's `/models` endpoint; see `using-reallms` |

Record such a fact as **Observed**, with the date, the host, and the command,
as in `Observed 2026-10-01 on quartz with sinfo`. When the KB states a
different number, keep the observed one. Note the KB figure as lagging, not as
an open item.

An agent cannot log in without a person. Login needs the IU passphrase and
Duo. `checking-iu-research-access` explains how a person shares one login with
an agent.

## Fetch the KB article, not a memory of it

The KB is the source for policy and process: eligibility, data
classification, PHI rules, renewals, forms, and support channels.

The KB runs on ServiceNow and builds each page with JavaScript. A plain fetch
of an article URL returns an empty page shell. Old `kb.iu.edu/d/<id>` links
redirect to the KB home page and drop the article id.

The ServiceNow Knowledge API answers anonymous requests. The
`searching-the-iu-knowledge-base` skill wraps it in a script that needs only
the Python standard library.

```bash
k=.agents/skills/searching-the-iu-knowledge-base/scripts/iukb.py
$k search Quartz        # KB number, published date, title
$k read KB0023985       # article text, links shown in brackets
```

A bracketed KB number in the output links to another article. Follow it with
another `read`.

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
Mark a claim from running a command as **Observed**.

## Record what is unknown

Write an open item when neither the system nor the KB answers a question.
Also write one when KB articles contradict each other on policy. Name the
articles that disagree and quote the numbers that differ. Do not resolve a
contradiction by picking the more plausible value.

Record a retired system as retired. An agent that does not see a system
listed may assume it still exists.

## Update the verified date

Each skill carries a `Verified <date>` line near the top. Change it only after
re-reading every article in that skill's Sources list. A partial check updates
the line for the claims checked, as in `Verified 2026-10-01 (partitions only)`.
Observed values carry their own dates.

## Format and style

- Follow the [Agent Skills specification](https://agentskills.io/specification).
  Keep `name` equal to the directory name, in kebab-case. Keep `description`
  under 1024 characters, and say what the skill does and when to use it.
- Use only `name` and `description` in frontmatter unless a spec field is
  needed.
- Keep `SKILL.md` under 500 lines. Move detail to `references/`.
- Put runnable helpers in `scripts/`. Use Bash or the Python standard library.
  A script must not prompt for a passphrase or answer Duo.
- Keep skills harness-neutral. Do not name a harness's tools.
- Refer to another skill by its name in backticks. Do not link across skill
  directories, because a skill may be installed alone.
- One idea per sentence, under 25 words, with the serial comma.
- Lead each section with its claim, then support it.
- End every skill with a "Keep this file current" section, then Sources.
- Nothing specific to one person or team, such as usernames, project numbers,
  keys, or internal hostnames.

Run `tools/check-skills.py` before committing. It must exit cleanly.

## Commits

Make one focused commit per skill change. Say in the message which KB articles
were re-read and which systems were observed.
