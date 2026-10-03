---
name: checking-iu-research-access
description: Bootstrap and verify a person's access to IU research computing before doing real work - network reach and SSH login to Quartz and Big Red 200, Duo and the one-time human login an agent needs, Slurm accounts from RT Projects, Slate, Slate-Scratch, Slate-Project, and SDA access, REALLMS API keys, and Jetstream2 credentials. Runs read-only check scripts, says where to go for each missing piece, and surveys the person's Slurm accounts into a private resources file outside the repository. Use at the start of any IU research computing session, when a job, login, or transfer fails for an unclear reason, or when onboarding a new lab member, or to decide which of a person's Slurm accounts or project directories fits the work.
---

# Checking IU research access

Verified 2026-10-01 against the IU Knowledge Base (KB). Each claim names its
KB article; links are in Sources at the end.

Check access before planning work. The checks below are read-only. They tell
you what the person can use today, and where to go for anything missing.

## The person's resources file

What one person can use belongs in a private file, not in this skill or its
repository. The file lives at `$IU_RESEARCH_NOTES` when that is set, and at
`~/.config/iu-research/resources.md` otherwise. The person may point it
anywhere, such as a private notes repository.

Read the file first if it exists. It says which Slurm account and project
directory fit which work, and when each fact was last seen. Re-check a fact
older than a quarter before relying on it. Write what the checks below find
into that file, never into a shared skill. Never write a passphrase, API key,
or keytab into it.

## The agent never handles the passphrase or Duo

Login nodes, SCP, and SFTP need the IU passphrase and Duo (KB0023985). Only
the person may answer those prompts. Never ask for a passphrase, store one, or
try to answer Duo.

An agent works through a connection the person already opened. OpenSSH can
share one authenticated connection with later commands. Suggest this block for
the person's `~/.ssh/config`, with their IU username:

```text
Host quartz.uits.iu.edu bigred200.uits.iu.edu
  User <iu-username>
  ControlMaster auto
  ControlPath ~/.ssh/cm-%C
  ControlPersist 4h
```

The person then logs in once in their own terminal and completes Duo. Later
`ssh` and `scp` commands to that host reuse the connection without a prompt.
Ask before changing the person's SSH configuration.

The KB does not mention connection sharing. It does close SSH connections
idle for 60 minutes (KB0023985). Do not add keepalives to defeat that limit.
When the shared connection drops, ask the person to log in again.

**Observed 2026-10-02**, Quartz: the shared connection worked after one
interactive login with Duo Push. `ssh -O check quartz.uits.iu.edu` reports
whether it is still open. With no shared connection, Quartz refused with
`Permission denied (gssapi-keyex,gssapi-with-mic,password,keyboard-interactive)`.
It did not offer `publickey` for an account with no signed key agreement.

SSH keys are another option. They need the signed "SSH public key
authentication to HPS systems" agreement and a passphrase on the key
(KB0023985). An agent still cannot type that key passphrase.

## Step 1: check from the person's computer

Run [scripts/check-local.sh](scripts/check-local.sh) with the IU username:

```bash
scripts/check-local.sh <iu-username>
```

It checks DNS and port 22 for Quartz and Big Red 200, then tries a login that
cannot prompt. It also checks REALLMS and Jetstream2 credentials if present.
Each line starts with `OK`, `MISSING`, or `SKIP`.

| Result | Meaning | Next step |
| --- | --- | --- |
| Host does not resolve, or port 22 unreachable | Network problem on this side | Check the network. The person may need another network or the IU VPN. |
| `needs an interactive login` | The account may be fine. No shared connection is open. | Ask the person to log in once, as above. Run the check again. |
| `Permission denied` after the person logged in | Wrong username, or no account on that system | Go to Step 3. |
| REALLMS `SKIP` | No key in `REALLMS_API_KEY` | Only needed for LLM work. See the `using-reallms` skill. |

## Step 2: check on the cluster

With a working connection, run
[scripts/check-cluster.sh](scripts/check-cluster.sh) on a login node:

```bash
env -u LC_ALL ssh <iu-username>@quartz.uits.iu.edu 'bash -s' < scripts/check-cluster.sh
```

It reports the person's groups, home, Slate, and Slate-Scratch directories,
and writable Slate-Project directories. It lists the Slurm accounts usable
with `-A`, checks SDA access through HSI, and prints quotas. It is light work
and safe on a login node. Run it on Big Red 200 too if the work goes there.

`env -u LC_ALL` matters when the computer sets `LC_ALL=C.UTF-8` and ssh
forwards `LC_*`. **Observed 2026-10-02:** Quartz lacks that locale, and every
shell then printed a `setlocale` warning.

An SDA account can exist while the HSI check fails. **Observed 2026-10-02**,
Quartz: `quota` listed `sda` with a 48.8T quota. A non-interactive `hsi`
failed with `No credentials cache found` and `Not running interactively &
username not set - PAM authentication failed`. The script now reports this
case separately. HSI needs a keytab or other set-up authentication before an
agent can use it (KB0022463).

A Slurm account is how an RT Projects allocation appears on the cluster.
Every job must name one with `-A` (KB0024132). An empty list means the person
is not on an allocation for that system.

To learn what the cluster itself offers, run the `describe-cluster.sh` script
from the `submitting-hpc-jobs` skill. Its output outranks any document.

## Step 3: where to go for each missing piece

A job runs only when three things hold (KB0025948). The person has an account
on the system. They belong to an RT Project. They are on that project's
allocation for the system.

| Missing | Where to go | Source |
| --- | --- | --- |
| No IU computing account at all | Create the first IU accounts | KB0022620 |
| No account on Quartz, Big Red 200, or the SDA | Create More Accounts, `https://one.iu.edu/launch-task/iu/account-creation`, then wait for the confirmation email | KB0022647, KB0025948 |
| Eligible but the account is not offered | The campus Support Center | KB0022647 |
| Not eligible, such as an undergraduate for Big Red 200 | A faculty or staff sponsor emails the owning team | KB0022656 |
| Duo not set up | Two-Step Login (Duo) setup | KB0024565 |
| No Slurm account | Join or request an RT Projects allocation at `https://projects.rt.iu.edu` | KB0024132 |
| Slurm account stopped working in July | The RT Project was not renewed | KB0024132 |
| Account disabled | Unused for six months, or not used within 30 days of creation | KB0022486 |
| No Slate-Project directory | The PI requests Slate-Project space in RT Projects | KB0022586 |
| SDA not confirmed | Create an SDA account, or set up HSI authentication | KB0022647, KB0022463 |
| SDA account exists, but `hsi` cannot log in non-interactively | The person sets up a keytab; see `references/sda.md` in `storing-and-moving-research-data` | KB0022463 |

The `requesting-accounts-and-allocations` skill covers eligibility and forms.
The `managing-rt-projects` skill covers allocations and members. The
`getting-help-from-research-technologies` skill names the team to ask.

## When login or SSH misbehaves

- **Practice:** OpenSSH ignores keys and config files that others can write.
  Run `chmod 700 ~/.ssh` and `chmod 600 ~/.ssh/*` on both ends.
- **Practice:** `Too many authentication failures` usually means the client
  offered too many keys before the password prompt. Add `IdentitiesOnly yes`
  to that host's block, or name one key with `IdentityFile`.
- **Practice:** if a login hangs after Duo, the stall is often in the login
  profile, such as a `module restore`, a conda initialization, or a slow file
  system it reads. Skip the profile to tell:

  ```bash
  ssh <host> -- bash --noprofile --norc -c 'echo ok; cat /proc/loadavg'
  ```

  If that answers at once, look in `~/.bashrc`, `~/.bash_profile`, and a
  saved Lmod collection in `~/.lmod.d/`. If it hangs too, the system itself
  is struggling. Check Status.IU and tell HPS.
- **Practice:** while a file system is slow, avoid `df`, `quota`, `ls ~`, and
  `module avail`. Each touches the slow mount and adds another stuck process.
- **Practice:** `lfs` in an Lmod traceback is LuaFileSystem, not Lustre.
  Lmod uses it to walk module directories.

## Step 4: record what the person has

If the resources file does not exist, offer to create it from
[assets/resources-template.md](assets/resources-template.md). Ask before
creating it, and ask where the person wants it.

Then survey the Slurm accounts on each cluster the work will use:

```bash
env -u LC_ALL ssh <iu-username>@quartz.uits.iu.edu 'bash -s' < scripts/survey-allocations.sh
```

It prints Markdown for the file. For each account it gives the member count,
QOS, CPU hours in the last 90 days, the person's fair share and job count, and
`condo_` groups that share members. Slurm does not know which RT Project an
account belongs to; its description is just the account name. **Observed
2026-10-02** on Quartz: shared membership pointed at several groups per
account, because one lab's members span many projects. Treat it as a hint.
The person confirms each account's project and PI in RT Projects, where the
allocation shows its Slurm Account Name (KB0023298). The `managing-rt-projects`
skill shows where.

Add the check output's storage and quota lines to the file with today's date.

## Report back

Tell the person what works, what is missing, and the one next step for each
gap. Quote the check output, not a summary of it. Record the date, since
access changes.

## Keep this file current

Run both scripts whenever this skill is used. Fix a script when a check
misreports, and note what the system actually showed. Re-read KB0023985 and
KB0025948 when login or onboarding steps change. Record any KB statement on
connection sharing if one appears.

## Sources

All IU KB articles, read 2026-10-01. URL form:
`https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=<number>`.

- [KB0022463](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022463) Use HSI to access your SDA account at IU
- [KB0022486](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022486) Policies regarding UITS research systems
- [KB0022586](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022586) About Slate-Project high performance project space at IU
- [KB0022620](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022620) Create your first IU computing accounts (admitted students, faculty, staff, affiliates, and those returning to IU)
- [KB0022647](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022647) Get additional IU computing accounts
- [KB0022656](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022656) Computing accounts at IU
- [KB0023298](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023298) Use Slurm to submit and manage jobs on IU's research computing systems (read 2026-10-02)
- [KB0023985](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023985) About Quartz at IU
- [KB0024132](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024132) Use RT Projects to request and manage access to specialized Research Technologies resources
- [KB0024565](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024565) Get started with Two-Step Login (Duo) at IU
- [KB0025948](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025948) Get started on IU research HPC and storage systems
