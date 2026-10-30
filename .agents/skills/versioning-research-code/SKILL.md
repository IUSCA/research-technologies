---
name: versioning-research-code
description: Keep research analysis code in git on IU's Quartz and Big Red 200 so every result points back to the exact code that made it, for researchers who know why version control matters but not how to use git. The agent does the git work - starting a repository with a .gitignore that keeps data and secrets out, committing each working change with a note of the AI tool used, stamping the commit into Slurm job output, tagging the version behind a paper, and pushing to GitHub:IU or GitHub.com with the gh CLI module or forwarded SSH keys - and explains it in plain words. Includes a read-only check for uncommitted changes and tracked data, secret, or large files. Use when writing or changing analysis code, before a job whose results will be reported, when asked how to track code versions or share code, or when someone asks which version of the code produced a result.
---

# Versioning research code at IU

Verified 2026-10-30 against the IU Knowledge Base (KB). Each claim names its
KB article; links are in Sources.

A result is reproducible only when you can say which code produced it. Git
records that. Many researchers know this and have never used git. In this
skill the agent does the git work and explains it in plain words. The person
decides what to keep, what to share, and with whom.

## Plain words for the person

Use these words with someone new to git. Give the git term once, in
parentheses.

| Say | Git term | What it gives the person |
| --- | --- | --- |
| Save point | commit | A named version of the code they can return to |
| History | log | Every save point, with who made it and why |
| Label | tag | A fixed name for the version behind a paper or report |
| Copy elsewhere | push to a remote | A backup off the cluster, and a way to share |

Do not teach branches, rebasing, or merging unless the person asks. One line
of history is enough for one analyst.

## What the agent does by default

**Practice.** Follow these without being asked, and say what you did:

1. Before editing code in a directory that is not a repository, offer to
   start one. Explain it in one sentence.
2. Commit after each change that runs, with a message that says why.
3. Before a job whose results may be reported, run `scripts/check-repo.sh`.
   Commit first if the tree is not clean.
4. Write the commit into every job's output; see "Tie each result to a
   commit".
5. When results go into a paper, poster, or report, offer to tag the commit.
6. Never commit data, outputs, keys, or passwords. Never push without the
   person's yes.

## Start a repository

Keep code in its own directory, apart from data. The data stays where its
classification allows; see `storing-and-moving-research-data`.

```bash
cd ~/<workflow>
git init -b main
git config --global user.name "<Full Name>"      # once per cluster
git config --global user.email "<user>@iu.edu"   # once per cluster
```

**Observed 2026-10-30** on Quartz: `git init` without `-b` names the first
branch `master`. Use `-b main` to match GitHub's default.

Write a `.gitignore` before the first commit. It keeps data and secrets out
even when someone runs `git add -A`. **Practice:** start from this one and
add the project's own data extensions.

```text
# Data and outputs stay out of git; record where they live in README.md
data/
results/
outputs/
*.csv
*.tsv
*.parquet
*.h5
*.rds
*.RData
*.xlsx
*.zip
*.gz
# Secrets
.env
*.key
*.pem
# Job and tool clutter
slurm-*.out
*.err
__pycache__/
.ipynb_checkpoints/
```

A small public example file the tests need may be committed. Add it with
`git add -f <file>` and say why in the commit message.

Commit the environment file with the code: `environment.yml`,
`requirements.txt`, `uv.lock`, or R's `renv.lock`. The
`managing-python-environments` skill says how to make one.

## Commit as you go

Commit each change that runs. A message says what changed and why, in a
sentence the person would understand a year later.

```bash
git add <files>
git commit -m "Exclude samples below 20x coverage before calling variants" \
  -m "Assisted-by: <agent> (<model>)"
```

**Practice:** add an `Assisted-by:` line naming the agent and model when an
AI wrote or changed the code. IU asks researchers to plan how they will
document their use of AI (KB0027312). The trailer does that in each commit,
and `git log --grep=Assisted-by` lists them. The person remains accountable
for the code and must review it (KB0027312).

## Tie each result to a commit

Write the commit into the output of every job. Then any result file points
back to its code. **Practice:** add this to the batch script after the
`#SBATCH` lines. The `submitting-hpc-jobs` skill has the rest of the script.

```bash
CODE=~/<workflow>            # the repository
OUT=/N/scratch/<user>/<run>  # where this job writes results
mkdir -p "$OUT"
git -C "$CODE" describe --always --dirty > "$OUT/code-version.txt"
git -C "$CODE" status --short >> "$OUT/code-version.txt"
```

A version ending in `-dirty` means the code had uncommitted changes. That
result cannot be traced to a commit. Commit, then run it again before
reporting it.

To find the code behind a result later:

```bash
git -C ~/<workflow> show --stat <version-from-code-version.txt>
```

## Label what you publish

Tag the commit behind each paper, poster, or report. A tag never moves.

```bash
git tag -a paper-2026-<short-name> -m "Code for figures 2-4 of <title>"
git push origin paper-2026-<short-name>
```

**Practice:** name the tag in the methods section or the data availability
statement.

## Put a copy elsewhere

A repository only in a home directory has one copy. Push it to a remote for
a backup and for sharing. Ask the person before every first push, and say
where it will go and who will see it.

| Remote | Use it when | Limits |
| --- | --- | --- |
| GitHub:IU, `github.iu.edu` | IU people and IU affiliates work on it | Public and University-Internal material only; no passwords (KB0024764) |
| GitHub.com | Code to publish, or outside collaborators without affiliate accounts | Check the repository is private until the person chooses to publish |

GitHub:IU details from KB0024764:

- Log in with an IU username and passphrase.
- Outside collaborators need an IU affiliate account.
- Content of people no longer active at IU is removed after a year.
  **Practice:** keep a lab's repositories in a GitHub:IU organization, not a
  student's personal account. Organizations are free (KB0023547).
- The service is down for maintenance Sundays 8 am to noon.

A repository moves from GitHub:IU to GitHub.com with the steps in KB0025590.
Faculty and staff can ask IU's GitHub support team at githelp@iu.edu
(KB0024764).

### The gh command on the clusters

`gh` creates the remote repository and pushes in one step. It is a module on
Quartz.

```bash
module load github_cli
gh auth login --hostname github.iu.edu   # or github.com; the person does this once
gh repo create <org>/<name> --private --source . --push
```

The person runs `gh auth login` themselves. It opens a browser or asks for a
token, which the agent must not handle. **Observed 2026-10-30** on Quartz
with `module load github_cli`: `gh version 2.43.1`. Big Red 200 has no `gh`
module.

### Or forward the SSH keys from your own computer

A person whose laptop key is already on GitHub can skip `gh auth login`.
`ssh -A` forwards the laptop's SSH agent to the login node, so `git push`
over SSH uses the laptop key. No key or token is stored on the cluster.

```bash
ssh -A <user>@quartz.uits.iu.edu        # or set ForwardAgent yes for the host
ssh-add -l                               # on the cluster: lists the laptop's keys
ssh -T git@github.iu.edu                 # or git@github.com
git remote add origin git@github.iu.edu:<org>/<name>.git
```

Create the empty repository first in the web interface; plain `git` cannot
create it. **Practice:** forward the agent only to hosts you trust. While
you are connected, anyone with root on the login node can use your keys.
The agent is not forwarded into Slurm jobs, so push from the login node.

With a shared connection (ControlMaster, see `checking-iu-research-access`),
only the first login decides forwarding. Log in with `-A` for that one.
**Observed 2026-10-30** on Quartz and Big Red 200: `ssh -A` through a shared
connection opened without `-A` forwarded no agent.

## Data and secrets never go in git

A file pushed to a remote is a copy outside the cluster. Deleting it in a
later commit leaves it in the history.

- Run `scripts/check-repo.sh` before every push. It lists tracked files that
  look like data, secrets, or files over 10 MB.
- If a key or password was committed, revoke it and make a new one first.
  The `using-reallms` skill covers REALLMS keys. Then remove the file from
  the repository.
- If Restricted or Critical data, or PHI, reached a remote, stop pushing.
  Report it to the University Information Policy Office and University
  Information Security Office (KB0025260).

Large data belongs in Slate-Project, Geode-Project, or the SDA. Record the
path and the date of the data version in `README.md`.

## Check a repository

[scripts/check-repo.sh](scripts/check-repo.sh) changes nothing. It reports
the current commit, uncommitted changes, tracked files that look like data,
secrets, or large files, and where each remote points.

```bash
bash scripts/check-repo.sh ~/<workflow>
```

It exits 0 when nothing needs attention, 1 when something does, and 2
outside a repository. **Observed 2026-10-30** on Quartz: in a test
repository it flagged a tracked `.csv`, a `.env`, an 11 MB file, a missing
`.gitignore`, an unset `user.email`, and a GitHub:IU remote.

## Git on the clusters

**Observed 2026-10-30** with `git --version`, `module avail`, and
`git ls-remote`:

| | Quartz | Big Red 200 |
| --- | --- | --- |
| `git` | `/usr/bin/git` 2.43.7 | `/usr/bin/git` 2.43.0 |
| `git lfs` | installed, 3.4.1 | `module load git-lfs`, 3.7.0 |
| `gh` | `module load github_cli`, 2.43.1 | none |
| HTTPS clone from GitHub.com | worked | worked |

No module is needed for `git`. Big Red 200 also has a `git/2.9.5` module;
do not load it, because it is older than the system `git`. Prefer research
storage for data over Git LFS. `github.iu.edu` answered from Quartz over
HTTPS and SSH, and asked for credentials.

**Practice:** commit and push on a login node. These are light commands.

## Open items

- `gh auth login --hostname github.iu.edu` from a cluster login node has not
  been tested end to end.
- Agent forwarding on a fresh `ssh -A` login has not been observed. The test
  through a shared connection forwarded nothing; see "Or forward the SSH
  keys from your own computer".

## Keep this file current

Re-run the commands under "Git on the clusters" on each cluster and update
the observed lines. Re-run `scripts/check-repo.sh` on a test repository.
Re-read the KB articles in Sources. Date every observation.

## Sources

All IU KB articles, read 2026-10-30. URL form:
`https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=<number>`.

- [KB0023547](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023547) About organizations in IU GitHub
- [KB0024764](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024764) About GitHub at IU
- [KB0025260](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025260) Report a suspected information or information technology (IT) security issue at IU
- [KB0025590](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025590) Move a repository from GitHub:IU to GitHub.com
- [KB0027312](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0027312) Researcher responsibilities for using AI tools with research data at IU

External: [Pro Git](https://git-scm.com/book/en/v2), and the
[GitHub CLI manual](https://cli.github.com/manual/), read 2026-10-30.
