# research-technologies

Agent skills for Indiana University research computing infrastructure.
They help a coding agent check a person's access, pick the right IU system,
request access, submit Slurm jobs, store and move data, and reach the right
support team.

## Companion repositories

Four repositories cover research at IU. Skills name a companion's skill by
its repository and skill name, as in "`sharing-research-data` in
research-data," and link the first mention to the skill on GitHub.

- **research-technologies** (this repository) covers clusters, storage, data transfer, and
  allocations.
- [research-data](https://github.com/IUSCA/research-data) covers finding, classifying, managing, and sharing research
  data.
- [research-funding](https://github.com/IUSCA/research-funding) covers planning and preparing grant proposals.
- [research-cores](https://github.com/IUSCA/research-cores) covers core facilities, their instruments, and the data
  they deliver.

This repository covers the computing and storage systems themselves.

## Quickstart

1. Clone this repository.
2. Start your agent in the clone. Claude Code, Codex, OpenCode, and pi all
   find the skills there with no install step.
3. Ask: "Check whether I'm set up to use IU research computing."

The agent will ask you to log in to a cluster once yourself, with your
passphrase and Duo. It then records your own Slurm accounts and storage in a
private file, `~/.config/iu-research/resources.md` or `$IU_RESEARCH_NOTES`.
That file stays outside the repository. To use the skills in another
project, see [Use the skills](#use-the-skills). To have the skills in every
Claude project without a clone, install the
[Claude plugin](#as-a-claude-plugin).

## What the skills trust

Systems at IU retire and get renamed often, so an agent must not trust its
own memory of IU systems. Each skill says where every claim came from.

- **The live system** is the judge of what it can report: partitions, node and
  GPU counts, limits, quotas, paths, and model lists. Hardware changes before
  documentation does. A skill records these facts as **Observed**, with the
  date and host, and tells the agent how to check them again.
- **The IU Knowledge Base (KB)** is the source for policy and process. Each
  KB claim cites its article, and each skill records the date its claims
  were last checked. When a skill and the KB disagree on policy, the KB wins.

A skill also marks three other kinds of statement explicitly:

- **Open item.** Neither the system nor the KB answers the question, or KB
  articles contradict each other. The skill says so instead of guessing.
- **External.** The claim comes from a non-KB source, such as the Jetstream2
  documentation. The source is named.
- **Practice.** Experienced users learned it the hard way, and the KB does
  not say it. It is advice, not IU policy. The skill says how to check it
  where a check exists.

## What stays out

The skills hold what is true for anyone at IU. What one person can use, such
as their Slurm accounts, project directories, and quotas, belongs in that
person's private resources file. It lives at `$IU_RESEARCH_NOTES`, or at
`~/.config/iu-research/resources.md` by default.
`checking-iu-research-access` explains how an agent fills and uses it.

No skill names a person, a ticket, or an internal hostname. Contacts are
office and service addresses. `tools/check-skills.py` fails any address not
listed in `tools/check-skills.toml`.

The KB now lives at `servicenow.iu.edu/kb`. Old `kb.iu.edu/d/<id>` links
redirect to the KB home page and lose the article. The
`searching-the-iu-knowledge-base` skill reads articles from a terminal.

## Skills

| Skill | Use it when |
| --- | --- |
| [checking-iu-research-access](.agents/skills/checking-iu-research-access/SKILL.md) | Starting a session, onboarding someone, or working out why access fails. Start here. |
| [iu-research-computing-map](.agents/skills/iu-research-computing-map/SKILL.md) | Choosing an IU system, or checking which data classifications a system is approved for. |
| [submitting-hpc-jobs](.agents/skills/submitting-hpc-jobs/SKILL.md) | Writing, submitting, or debugging a Slurm job on Quartz or Big Red 200. |
| [requesting-accounts-and-allocations](.agents/skills/requesting-accounts-and-allocations/SKILL.md) | Getting a personal account, an RT Projects allocation, or project storage for the first time. |
| [managing-rt-projects](.agents/skills/managing-rt-projects/SKILL.md) | Running an RT Project: allocations, members, collaborators, renewal, and archiving. |
| [storing-and-moving-research-data](.agents/skills/storing-and-moving-research-data/SKILL.md) | Using Slate, Slate-Project, Slate-Scratch, Geode-Project, or the SDA, or moving data with Globus. |
| [planning-research-computing-work](.agents/skills/planning-research-computing-work/SKILL.md) | Turning a described workflow into a plan: which IU system, storage, transfers, and allocations each stage needs. |
| [managing-python-environments](.agents/skills/managing-python-environments/SKILL.md) | Installing Python or R packages, creating conda or virtual environments, moving caches out of home, or adding a Jupyter kernel on Quartz or Big Red 200. |
| [using-research-desktop](.agents/skills/using-research-desktop/SKILL.md) | Needing a graphical desktop, RStudio, MATLAB, or Jupyter on Quartz. |
| [using-reallms](.agents/skills/using-reallms/SKILL.md) | Calling IU's LLM service from research code, or choosing an IU LLM service for research data. |
| [jetstream2](.agents/skills/jetstream2/SKILL.md) | Considering Jetstream2 cloud for a gateway, a service, or interactive work. |
| [getting-help-from-research-technologies](.agents/skills/getting-help-from-research-technologies/SKILL.md) | Deciding whether to ask for help, which queue to use, and what to send. |
| [searching-the-iu-knowledge-base](.agents/skills/searching-the-iu-knowledge-base/SKILL.md) | Finding, reading, and citing an IU KB article, or settling a KB-versus-system conflict. |

## Use the skills

Each skill is a directory in the open
[Agent Skills](https://agentskills.io/specification) format. A `SKILL.md`
file carries `name` and `description` frontmatter. Scripts use only Python's
standard library or Bash, so any harness that can run a shell can use them.

### As project skills in this repository

Start your agent in a clone of this repository. No install step is needed.

| Harness | Reads project skills from |
| --- | --- |
| Codex | `.agents/skills/` |
| pi | `.agents/skills/` |
| OpenCode | `.agents/skills/` and `.claude/skills/` |
| Claude Code | `.claude/skills/` only, or install the [plugin](#as-a-claude-plugin) |

The skills live in `.agents/skills/`, the shared project location. Claude Code
does not read that directory, so `.claude/skills` is a single committed
symbolic link to it. Nothing outside the repository changes.

### As a Claude plugin

This repository is also a Claude plugin marketplace. Installing the plugin
makes every skill available in all your projects, with no clone and no
copying.

In Claude Code:

```text
/plugin marketplace add IUSCA/research-technologies
/plugin install research-technologies@iusca-research-technologies
```

Claude desktop can add the same marketplace, `IUSCA/research-technologies`,
from its plugin settings.

Plugin skills are namespaced, so `submitting-hpc-jobs` appears as
`research-technologies:submitting-hpc-jobs`. The agent still picks a skill
from its description, so you rarely type the name.

To update, run `/plugin marketplace update iusca-research-technologies`.

The plugin reads the skills from `.agents/skills/`, the directory the other
harnesses use, so no skill is duplicated. The manifests are
`.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`.

### In another project

Pick one of these. None needs a hand-written link per skill.

- **Copy them in.** Copy the skill directories you need into that project's
  `.agents/skills/`. Commit them there, and re-copy to update.
- **Use the `skills` installer.** The open-source
  [`skills` CLI](https://github.com/vercel-labs/skills) installs from a git
  URL or a local path. It writes each harness's directory for you. It needs
  Node.js 22.20 or newer.

  ```bash
  npx skills add <this repository> --list
  npx skills add <this repository> --skill submitting-hpc-jobs --copy
  npx skills update
  ```

  `--copy` writes plain files. Without it, the CLI links each harness to one
  shared copy. Add `-g` to install for your user instead of the project.
- **Claude Code or Claude desktop:** install the
  [plugin](#as-a-claude-plugin). For one session only,
  `claude --add-dir ~/repos/research-technologies` loads this repository's
  `.claude/skills/`.

Sources for these locations, checked 2026-10-01:
[Agent Skills specification](https://agentskills.io/specification),
[Claude Code skills](https://code.claude.com/docs/en/skills),
[Claude Code plugins](https://code.claude.com/docs/en/plugins),
[plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces),
[Codex skills](https://learn.chatgpt.com/docs/build-skills),
[OpenCode skills](https://opencode.ai/docs/skills),
[pi skills](https://pi.dev/docs/latest/skills),
[`skills` CLI](https://github.com/vercel-labs/skills).
**Observed 2026-10-01:** `npx skills add . --list` finds every skill in this
repository's `.agents/skills/`.

## Fork it and run it elsewhere

These skills are meant to be adopted. Fork the repository, keep it current
for your own group, and change what you need. The `MAINTAINING.md` runbook
works the same in a fork.

## Maintaining

- [CONTRIBUTING.md](CONTRIBUTING.md) explains how to verify and write a
  single claim.
- [MAINTAINING.md](MAINTAINING.md) is the runbook for reviewing and updating
  the whole set.
- `tools/check-skills.py` runs the offline checks: format, markers, sources,
  age, and what stays out. `--kb` and `--links` add the network checks, and
  `--freshness` runs every check this repository's weekly workflow runs.
  `tools/check-skills.toml` holds this repository's settings.
- [tests/trigger-prompts.md](tests/trigger-prompts.md) checks that agents
  load the right skill.

## License

Code, meaning scripts and tools, is under the Educational Community License,
Version 2.0; see [LICENSE](LICENSE). Written content, including every
`SKILL.md` and reference file, is under CC BY 4.0; see
[LICENSE-docs](LICENSE-docs). Copyright the Trustees of Indiana University.
