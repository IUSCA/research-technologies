# research-technologies

Agent skills for Indiana University research computing infrastructure.
They help a coding agent pick the right IU system, request access, submit
Slurm jobs, and reach the right support team.

## The IU Knowledge Base is the source of truth

Every factual claim in a skill cites an IU Knowledge Base (KB) article. Each
skill records the date its claims were last checked. Systems at IU retire and
get renamed often, so an agent must not trust its own memory of IU systems.
When a skill and the KB disagree, the KB wins and the skill is stale.

A skill marks two other kinds of statement explicitly:

- **Open item.** The KB is silent or contradicts itself. The skill says so
  instead of guessing.
- **External.** The claim comes from a non-KB source, such as the Jetstream2
  documentation. The source is named.

The KB now lives at `servicenow.iu.edu/kb`. Old `kb.iu.edu/d/<id>` links
redirect to the KB home page and lose the article. Cite articles by KB number
and the `sysparm_article` URL instead. `CONTRIBUTING.md` explains how to fetch
an article from the command line.

## Skills

| Skill | Use it when |
| --- | --- |
| [iu-research-computing-map](skills/iu-research-computing-map/SKILL.md) | Choosing an IU system, or checking which data classifications a system is approved for. |
| [submitting-hpc-jobs](skills/submitting-hpc-jobs/SKILL.md) | Writing, submitting, or debugging a Slurm job on Quartz or Big Red 200. |
| [requesting-accounts-and-allocations](skills/requesting-accounts-and-allocations/SKILL.md) | Getting a personal account, an RT Projects allocation, or project storage. |
| [getting-help-from-research-technologies](skills/getting-help-from-research-technologies/SKILL.md) | Deciding whether to ask for help, which queue to use, and what to send. |
| [jetstream2](skills/jetstream2/SKILL.md) | Considering Jetstream2 cloud for a gateway, a service, or interactive work. |

## Install

Each skill is a directory under `skills/` in the open Agent Skills format. A
`SKILL.md` file carries `name` and `description` frontmatter. Clone the
repository once, then link the skills into each harness's skills directory.

```bash
git clone <this repository> ~/repos/research-technologies
cd ~/repos/research-technologies
```

Claude Code reads `~/.claude/skills/`, or `.claude/skills/` inside a project.

```bash
mkdir -p ~/.claude/skills
for d in skills/*/; do ln -s "$PWD/$d" ~/.claude/skills/; done
```

OpenCode reads `~/.config/opencode/skills/`. It also reads `~/.claude/skills/`
and `~/.agents/skills/`, so the Claude Code links work for OpenCode too.

pi reads `~/.agents/skills/`, or `.agents/skills/` inside a project. Older pi
releases documented `~/.pi/agent/skills/` instead.

```bash
mkdir -p ~/.agents/skills
for d in skills/*/; do ln -s "$PWD/$d" ~/.agents/skills/; done
```

A skill becomes available in the next session after it is linked. Run
`git pull` in the clone to update every linked skill at once.

Sources for these locations, checked 2026-10-01:
[Claude Code skills](https://code.claude.com/docs/en/skills),
[OpenCode skills](https://opencode.ai/docs/skills),
[pi skills](https://pi.dev/docs/latest/skills).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to verify and update a skill.
