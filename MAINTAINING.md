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
| An open issue labeled `freshness` | Step 1's reading list: steps 2 and 3 for the lines it lists |

GitHub Actions runs two checks for you. On every pull request and push to
`main`, `check-skills.yml` runs `tools/check-skills.py` and fails on any
`ERROR`. Every Monday, `freshness.yml` runs `tools/check-skills.py
--freshness`, which here means `--kb` and `--links`. When it finds `STALE`,
`BROKEN`, or `ERROR` lines, it opens an issue labeled `freshness`, or
comments on the one already open. Close that issue once the lines are
worked.

## Full review

Work on a branch. Make one commit per skill, as `CONTRIBUTING.md` asks.

### 1. Lint and find stale sources

```bash
tools/check-skills.py --freshness
```

It checks each skill against the Agent Skills specification and the house
rules. It then lists every cited KB article published after the skill's
Verified date, and any article that KB search no longer finds. Last, it
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
