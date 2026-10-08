# Runbook: reviewing and updating the skill set

This runbook keeps the skills true to IU as it is now. It covers a full
review, the checks that drive it, and when to run it. `CONTRIBUTING.md`
covers how to write and verify a single claim.

## Who decides what is true

- **The live system** wins for anything it can report: partitions, node and
  GPU counts, time limits, QOS and array limits, quotas, paths, installed
  modules, and service endpoints. Hardware changes before the KB does.
- **The IU Knowledge Base (KB)** wins for policy and process: eligibility, data
  classification, PHI rules, renewals, forms, and support channels.
- **The owning team** settles what neither one answers. Record its answer with
  the date and the ticket or email it came from.

A skill records a system fact as **Observed**, with the date, host, and
command. When an Observed value and the KB disagree, keep the Observed value
and note the KB's figure as lagging. Do not open an item for it.

## When to review

| Trigger | Scope |
| --- | --- |
| Any agent finds a wrong claim during real work | That claim, right away, in its own commit |
| The day after monthly HPC maintenance (second Sunday) | Step 3, system facts, on Quartz and Big Red 200 |
| Every quarter (January, April, July, October) | The full review below |
| Each May, before RT Projects renewal opens on June 1 | `managing-rt-projects` and `requesting-accounts-and-allocations` |
| A system or service is announced, renamed, or retired | Every skill that names it, plus `references/retired-and-renamed.md` |
| An open issue labeled `freshness` | [Working a freshness issue](#working-a-freshness-issue) |

GitHub Actions runs two checks for you. On every pull request and push to
`main`, `check-skills.yml` runs `tools/check-skills.py` and fails on any
`ERROR`. Every Monday, `freshness.yml` runs `tools/check-skills.py
--freshness`, which here means `--kb` and `--links`. When it finds `STALE`,
`BROKEN`, or `ERROR` lines, it opens an issue labeled `freshness`, or
comments on the one already open. Close that issue once the lines are
worked.

## Working a freshness issue

A person or their agent works each `freshness` issue by hand. Nothing
edits a skill on its own, because every fixed claim needs someone to read
its source. An agent can do all of this; give it this section and the
issue. A person reviews and merges the pull request.

1. Make a branch from `main`. Run `tools/check-skills.py --freshness`
   again. The issue may be days old, and some lines may have cleared.
2. Work each line by kind:
   - **STALE, KB article changed.** Read the whole article with
     `iukb.py read KB0123456` (in research-technologies'
     `searching-the-iu-knowledge-base` skill). Find every claim citing it,
     in each skill the line names and in that skill's `references/`.
     Fix what changed. Then record the reading with
     `tools/check-skills.py --kb-snapshot KB0123456`.
   - **INFO, text unchanged.** The article was touched but its text was
     not. Record it with `--kb-snapshot KB0123456`. No skill changes.
   - **STALE, not found by KB search.** The article was retired or
     renumbered. Search for its replacement. If there is none, name the
     article without a link, with the date it went missing.
   - **STALE, Verified date too old.** Re-read every source the skill
     cites, then update its Verified line.
   - **BROKEN.** Run `--links` again; a single failure is often transient.
     If it still fails, find the page's new address. If the page is gone,
     find another source or make the claim an open item.
   - **CHANGED.** Run the snapshot script named in the line. Update the
     catalog or directory file it compares against, and every skill that
     names what changed.
3. A claim the new source no longer supports is fixed, cut, or turned into
   an open item in `docs/open-items.md`. A question the source now settles
   leaves the open items.
4. Update the Verified line of each skill you edited. For an article with
   a snapshot entry, `--kb-snapshot` is the record, so the Verified line
   does not need to list it as a partial re-read.
5. Run `tools/check-skills.py --freshness` until no STALE, BROKEN, or
   CHANGED line remains. Commit one skill per commit, with the snapshot
   change in the same commit as the skill it supports.
6. Open a pull request that says `Closes #<issue>`. List each line and
   what you did with it: fixed, unchanged, or opened as an item.

## Full review

Work on a branch. Make one commit per skill, as `CONTRIBUTING.md` asks.

### 1. Lint and find stale sources

```bash
tools/check-skills.py --freshness
```

It checks each skill against the Agent Skills specification and the house
rules. It then lists every cited KB article changed since it was last
read, and any article that KB search no longer finds. An article in
`tools/kb-snapshot.json` is compared with its snapshot: a newer update
with the same text prints INFO, changed text prints STALE. Other articles
are compared with the skill's Verified date. Last, it
fetches every cited URL. The KB check takes about a minute.

- `ERROR` lines must be fixed before merging.
- `STALE` lines are the reading list for step 2. A skill whose Verified
  date is over 120 days old also prints `STALE`.
- `BROKEN` lines usually mean a page moved. Find the new page. A URL that
  cannot load from a script on purpose, such as an API endpoint, goes in
  `skip_urls` in `tools/check-skills.toml`.
- `WARN` lines usually mean a KB number appears in the text but not in
  Sources.

### 2. Re-read stale articles and fix the claims

For each `STALE` article:

```bash
.agents/skills/searching-the-iu-knowledge-base/scripts/iukb.py read KB0023985
grep -rn KB0023985 .agents/skills
```

Compare each claim that cites the article with the new text. Fix what
changed. An article that search no longer finds may be retired. Search for
its replacement, and record a retired system in
`.agents/skills/iu-research-computing-map/references/retired-and-renamed.md`.

Update a skill's Verified line only after re-reading every article in its
Sources list. Otherwise use the partial form in `CONTRIBUTING.md`, which names the
articles re-read and keeps the older date for the rest.

### 3. Let the systems report their own facts

A person must log in once to each cluster, with their passphrase and Duo. The
`checking-iu-research-access` skill shows how to share that login with an
agent. Then run:

```bash
s=.agents/skills/submitting-hpc-jobs/scripts/describe-cluster.sh
ssh <user>@quartz.uits.iu.edu 'bash -s' < $s > /tmp/quartz.txt
ssh <user>@bigred200.uits.iu.edu 'bash -s' < $s > /tmp/bigred200.txt
```

Compare the output with every Observed value in the skills:

```bash
grep -rn "Observed" .agents/skills
```

Update a changed value with the new date. Add newly visible partitions or
limits. Remove a partition that no longer exists, and note the removal in
`references/retired-and-renamed.md`.

### 4. Test the access checks

Run both scripts from `checking-iu-research-access` with a real account.

```bash
.agents/skills/checking-iu-research-access/scripts/check-local.sh <user>
env -u LC_ALL ssh <user>@quartz.uits.iu.edu 'bash -s' < .agents/skills/checking-iu-research-access/scripts/check-cluster.sh
```

Every line should match what you know of that account. Fix a script that
misreports, and say in the commit what the system actually showed.

### 5. Work the open items

```bash
grep -rn -i "open item" .agents/skills
```

For each item, try in this order:

1. Can the system answer it? Run the command, and record the answer as
   Observed.
2. Has the KB changed? Search for it again.
3. Otherwise collect the item for its owning team. Send one ticket per team
   with every question batched. The `getting-help-from-research-technologies`
   skill names the queues.

Close an item only with its source: a command and date, a KB number, or a
ticket number.

### 6. Look for gaps

New services appear in the KB before anyone writes a skill for them.

```bash
k=.agents/skills/searching-the-iu-knowledge-base/scripts/iukb.py
$k search research computing
$k search RT Projects
$k search research storage
```

Look for recently published articles about a service that no skill covers.
Also check the resource list in RT Projects. Add a skill when a service needs
more than a line in the map. Otherwise add the line to
`iu-research-computing-map`.

### 7. Test that agents find the right skill

Start a fresh session in this repository in each harness you support. Try the
prompts in [tests/trigger-prompts.md](tests/trigger-prompts.md). Check that
the expected skill loads and that the answer cites it. Fix a description that
fails to trigger. Note which harness and version you tested in the review
commit.

### 8. Finish

```bash
tools/check-skills.py
```

It must exit cleanly. Open a pull request that lists the articles re-read,
the systems observed, and the open items closed or opened.

## Adding a skill

1. Create `.agents/skills/<name>/SKILL.md`. Keep `name` equal to the
   directory name.
2. Follow `CONTRIBUTING.md` for sources, markers, and style.
3. Add a row to the skills table in `README.md`.
4. Add trigger prompts to `tests/trigger-prompts.md`. The checker fails a
   skill with no README row or trigger prompt.
5. Run `tools/check-skills.py --kb`.

## Retiring a skill

Delete the directory and its README row in one commit. Say why in the
message. If the service itself retired, record it in
`references/retired-and-renamed.md` first.
