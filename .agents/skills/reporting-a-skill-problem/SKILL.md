---
name: reporting-a-skill-problem
description: Report a problem with one of these IU research computing skills as a GitHub issue on IUSCA/research-technologies, with a pull request if the person wants - confirming the skill is really at fault, checking for an existing issue, drafting a public-safe report with the exact error and how the fix was checked, and letting the person decide whether to send it. Use when a skill's instructions turned out wrong, out of date, or incomplete during a session - an error the skill did not mention, a limit it missed, a command or step that changed, or a gap that cost time - or when someone asks how to suggest a change to these skills.
---

# Reporting a skill problem

Verified 2026-10-30. This skill describes this repository's own process; it
cites no KB article.

A session can show that a skill here was wrong, out of date, or silent.
Report it, so the next researcher at IU does not hit the same problem. The
maintainers check each report, cite a source, and update the skill.

**Practice.** When a session finds such a problem, finish the person's task
first. Then tell them in one sentence what the skill got wrong, and offer to
draft a report.

## Confirm it is the skill

Report the skill only when it, not the session, was wrong.

- Run the failing step again, so the report quotes a real error.
- Check the live system where it can answer, as `CONTRIBUTING.md` says.
  A partition list, quota, or model list comes from a command.
- A one-off outage is not a skill problem. Check the service's status page
  or maintenance window first.

## Check for an existing issue

```bash
gh issue list -R IUSCA/research-technologies --state open --search "<skill-name>"
```

Add a comment to a matching issue instead of opening a new one. Without
`gh`, search at `https://github.com/IUSCA/research-technologies/issues`.

## Draft the report

**Practice.** The agent drafts the issue. The person reads it and decides
whether to send it. Never send it without their yes.

The issue is public. Leave out:

- Data values, file contents, and model outputs about the data.
- Participant, patient, or sample identifiers.
- Keys, tokens, and passwords.
- Usernames, personal paths, project names, and hostnames that are not
  public. Use placeholders such as `<user>` and `<project>`.

A good report has:

- The skill name, and what it said or left out.
- What happened, with the exact error text.
- What fixed it, and how that was checked: the command, the host, and the
  date, such as `Observed 2026-10-30 on quartz with sinfo`.
- A KB article number if one backs the fix.

The repository's skill feedback form asks for these.

## Send it

With `gh` signed in to GitHub.com:

```bash
gh issue create -R IUSCA/research-technologies \
  --title "<skill-name>: <what was wrong or missing>" \
  --body-file <draft.md>
```

On Quartz, `gh` is the `github_cli` module. The person runs
`gh auth login` themselves; see `versioning-research-code`.

Without `gh`, open `https://github.com/IUSCA/research-technologies/issues/new/choose`,
choose "Skill feedback", and paste the draft.

## Attach a pull request, if wanted

An issue alone is enough. A person comfortable with GitHub can attach the
fix:

1. Fork and clone: `gh repo fork IUSCA/research-technologies --clone`.
2. Make a branch, and edit the skill. `CONTRIBUTING.md` says how to mark
   and cite each claim.
3. Run `tools/check-skills.py`. It must print `OK`.
4. Open the pull request with `Closes #<issue>` in its description.

A maintainer reviews it before anything merges.

## Keep this file current

Update this file when the issue form in `.github/ISSUE_TEMPLATE/` or the
review process in `MAINTAINING.md` changes.

## Sources

This repository's `CONTRIBUTING.md`, `MAINTAINING.md`, and
`.github/ISSUE_TEMPLATE/skill-feedback.yml`, read 2026-10-30.

External: [GitHub CLI manual](https://cli.github.com/manual/), read
2026-10-30.
