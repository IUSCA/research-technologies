---
name: capturing-a-workflow-as-a-skill
description: Turn a research computing session that worked into a reusable Agent Skill, so the next session repeats the workflow without re-explaining it - deciding whether it is worth a skill, choosing a personal, lab, or shared home, writing SKILL.md and scripts from what actually ran, keeping data, identifiers, and keys out, testing that the skill loads, and keeping it in git. Use when a session that worked is ending, when someone says "make this a skill" or "remember how we did this", or when the same steps are being explained to an agent again.
---

# Capturing a workflow as a skill

Verified 2026-10-30 against the IU Knowledge Base (KB) and the pi
documentation. Each claim names its source; links are in Sources.

A session that worked holds steps, commands, and fixes that took effort to
find. A skill keeps them. The next session loads it and starts where this one
ended. Write the skill before the session closes, while the agent still has
the whole history.

A session can also show that a skill in this repository was wrong or
missing something. That goes back to this repository as an issue; see
`reporting-a-skill-problem`.

## Is it worth a skill?

**Practice.** Write one when any of these hold:

- The person will run the workflow again, on new data or a new month.
- It took several tries to get right, and the fixes are not obvious.
- Someone else in the lab will run it.
- The person has explained the same steps to an agent before.

A one-off analysis does not need a skill. Its commit history is enough; see
`versioning-research-code`.

## Choose where it lives

| Audience | Where | Notes |
| --- | --- | --- |
| Only the person | `~/.agents/skills/<name>/` | Found in every directory |
| One project | `<repo>/.agents/skills/<name>/` | Travels with that project's code |
| The lab | A lab repository on GitHub:IU | Public and University-Internal material only (KB0024764) |
| Anyone at IU | This repository | Send an issue; see `reporting-a-skill-problem` |

**External:** pi reads skills from `~/.agents/skills/` and from
`.agents/skills/` in the working directory and its parents, up to the
repository root (pi documentation, version 1.4.0). Other agents that follow
the Agent Skills specification read `.agents/skills/` too; see the README of
this repository.

**Practice:** keep a lab's skills in a GitHub:IU organization, not one
person's account. GitHub:IU removes content a year after its owner leaves
IU (KB0024764). Organizations are free (KB0023547).

## Write it from what actually ran

Draft the skill from the session history, not from memory of it.

1. Name it as a gerund phrase in kebab-case, such as
   `calling-variants-on-new-runs`. The directory name must match `name`.
2. Write the `description` first. Say what the skill does and when to use
   it, with the words the person would type. An agent loads a skill by its
   description alone (pi documentation).
3. List the steps in the order they ran. Keep the commands that worked.
   Drop the dead ends.
4. Keep each failure that cost time, as a symptom and its fix. Quote the
   exact error text, so a later agent recognizes it.
5. Put commands that run every time into `scripts/`, and call them from
   `SKILL.md`.
6. Replace anything that changes per run with a placeholder, such as
   `<run-id>` or `<input-dir>`.
7. Name what the person must do themselves, such as a Duo login or a
   decision about data.

Start from this layout:

```markdown
---
name: <skill-name>
description: <What it does>. Use when <the situations and words that should load it>.
---

# <Title>

<One paragraph: what the workflow produces and when to run it.>

## Before you start
<Accounts, modules, environments, and inputs it needs.>

## Steps
1. <Step, with the command that worked.>

## When it goes wrong
| Symptom | Fix |
| --- | --- |
| `<exact error text>` | <what fixed it> |

## Keep this file current
<What to re-check, and when.>
```

**Practice:** keep `SKILL.md` under 500 lines. Move long detail to
`references/`. The Agent Skills specification recommends the same limit.

## Keep data, identifiers, and keys out

A skill is read by every session that loads it and copied wherever it is
shared. **Practice.** Leave out:

- Data values, sample rows, file contents, and model outputs about the data.
- Participant, patient, or sample identifiers, even in an example.
- API keys, tokens, passwords, and key file contents. Name the file or
  variable that holds a secret, never its value.
- For a lab or shared skill: usernames, personal paths, and project names.
  Use placeholders such as `<user>` and `<project>`.

A path to where data lives is fine in a personal skill. The data itself is
not.

The session itself keeps the full history. **External:** pi saves each
session as a `.jsonl` file under `~/.pi/agent/sessions/` (pi
documentation). Never copy a session file into a skill, a repository, or an
issue.

Run [scripts/check-skill.sh](scripts/check-skill.sh) before sharing. It
checks the frontmatter and length. It flags strings that look like keys,
email addresses, cluster paths, and long numeric identifiers. It changes
nothing. A clean result is not proof; read the skill too.

```bash
bash scripts/check-skill.sh ~/.agents/skills/<name>
```

## Test that it loads

Start a new session and ask for the task in the person's own words. The
skill should load without being named. **External:** in pi, `/skill:<name>`
loads a skill by name, and `/reload` picks up edits during a session (pi
documentation).

If it does not load, rewrite the description with the words the person
used. Then test again.

## Keep it in git

Keep personal skills in a repository too: `~/.agents/skills` can be one.
Commit each change with a message that says what the session taught. The
`versioning-research-code` skill does the git work.

## Send improvements back

When the session showed that one of this repository's skills was wrong or
incomplete, offer to report it. The `reporting-a-skill-problem` skill drafts
the issue, and a pull request if the person wants one.

## Keep this file current

Re-read the pi skills and sessions documentation when pi updates, and update
the version named above. Re-read the KB articles in Sources. Run
`scripts/check-skill.sh` on a test skill after changing it.

If a session finds this file wrong or missing something, offer to report it
at `https://github.com/IUSCA/research-technologies/issues/new/choose`; see
`reporting-a-skill-problem`.

## Sources

IU KB articles, read 2026-10-30. URL form:
`https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=<number>`.

- [KB0023547](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023547) About organizations in IU GitHub
- [KB0024764](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024764) About GitHub at IU

External, read 2026-10-30:

- [Agent Skills specification](https://agentskills.io/specification).
- pi documentation, version 1.4.0, `docs/skills.md` and `docs/sessions.md`
  in the installed package, also at [pi.dev](https://pi.dev).
