---
name: reporting-a-skill-problem
description: Report a problem with one of these IU research computing skills as a GitHub issue on IUSCA/research-technologies - confirming the skill is really at fault, drafting a public-safe report, and filing it only with the person's yes. A short copy of the family skill in IUSCA/iu-research, which covers every IU research skills repository and pull requests in full. Use when a skill's instructions turned out wrong, out of date, or incomplete during a session - an error the skill did not mention, a limit it missed, a command or step that changed, or a gap that cost time - or when someone asks how to suggest a change to these skills.
---

# Reporting a skill problem

Verified 2026-11-03. This skill describes the family's own process; it
cites no KB article.

This is the short copy for research-technologies. The full skill lives in
[iu-research](https://github.com/IUSCA/iu-research/tree/main/.agents/skills/reporting-a-skill-problem).
It works out which repository owns any family skill, and explains attaching
a pull request. When the `iu-research` plugin or a clone of it is
installed, use its skill instead of this one.

**Practice.** When a session finds a problem, finish the person's task
first. Then tell them in one sentence what the skill got wrong, and offer to
draft a report.

## Confirm it is the skill

- Run the failing step again, so the report quotes a real error.
- Check the live system where it can answer, as `CONTRIBUTING.md` says.
  A partition list, quota, or model list comes from a command.
- A one-off outage is not a skill problem. Check the service's status page
  or maintenance window first.

A skill from research-data, research-funding, or research-cores belongs to
that repository, not this one. File it there, or use the iu-research skill.

## Draft and send

**Practice.** The agent drafts the issue. The person reads it and decides
whether to send it. Never send it without their yes.

The issue is public. Leave out data values and file contents; participant,
patient, or sample identifiers; keys, tokens, and passwords; and usernames,
personal paths, project names, and hostnames that are not public. Use
placeholders such as `<user>` and `<project>`.

A good report names the skill and what it said or left out, quotes the
exact error, and says what fixed it and how that was checked, such as
`Observed 2026-11-03 on quartz with sinfo`.

Check for an existing issue first, and comment there if one matches:

```bash
gh issue list -R IUSCA/research-technologies --state open --search "<skill-name>"
gh issue create -R IUSCA/research-technologies \
  --title "<skill-name>: <what was wrong or missing>" \
  --body-file <draft.md>
```

On Quartz, `gh` is the `github_cli` module. The person runs
`gh auth login` themselves; see `versioning-research-code`. Without `gh`,
open `https://github.com/IUSCA/research-technologies/issues/new/choose` and
choose "Skill feedback".

## Keep this file current

Keep this copy short. Change the full skill in iu-research first, then
bring any change to the steps above here. Update this file when the issue
form in `.github/ISSUE_TEMPLATE/` changes.

## Sources

- The full skill in iu-research,
  `https://github.com/IUSCA/iu-research/tree/main/.agents/skills/reporting-a-skill-problem`,
  read 2026-11-03.
- This repository's `CONTRIBUTING.md` and
  `.github/ISSUE_TEMPLATE/skill-feedback.yml`, read 2026-11-03.
- External: [GitHub CLI manual](https://cli.github.com/manual/), read
  2026-10-30.
