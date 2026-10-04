---
name: using-research-desktop
description: Use IU Research Desktop (RED), the ThinLinc remote desktop on Quartz. Covers access with the ThinLinc client or red.uits.iu.edu, Duo, what RED is and is not for, memory and parallelism limits, launching interactive Quartz jobs, Jupyter and other GUI apps, visible file systems, Google My Drive, data classification, troubleshooting, and support. Use when someone needs a GUI on Quartz, a remote desktop at IU, RStudio, MATLAB, or Jupyter on RED, or when a RED login or session fails.
---

# Using Research Desktop (RED)

Verified 2026-10-03 (KB0023515 and KB0025747 only) against the IU
Knowledge Base (KB). Other sources were verified 2026-10-01. Each claim
names its KB article; links are in Sources at the end.

RED is a graphical desktop for Quartz users, not a place for heavy compute.
Send anything parallel, long, or memory-heavy to a Quartz compute node
(KB0023170). The live system is the judge: check each limit, app, or path on
RED with the command shown, and record any difference here.

Your session runs on one of more than two dozen shared VMs (KB0023167). They
are login nodes that are part of Quartz (KB0023170). You cannot SSH to them
directly (KB0023167). Each user gets one RED session (KB0023170).

## Who can use it

You need two things (KB0023167, KB0023162):

- A Quartz account. All IU students, faculty, staff, and sponsored affiliated
  researchers can request one (KB0022656).
- A device enrolled in IU Two-Step Login (Duo).

Running Slurm jobs from RED also needs an RT Projects allocation and its Slurm
Account Name (KB0025948, KB0025672). See `requesting-accounts-and-allocations`.

## Connect: ThinLinc client or browser

Prefer the ThinLinc client. The browser at `https://red.uits.iu.edu` cannot
use SSH keys, export local drives, or end an existing session (KB0023167,
KB0023170).

Get the client from Cendio for Windows, macOS, or Linux. Set the server to
`red.uits.iu.edu` and log in with your IU username and passphrase. Then enter a
Duo passcode, or `1` for a Push (KB0023162). The SSH port should be 22
(KB0023231). Key login needs the signed "SSH public key authentication to HPS
systems" agreement and a key passphrase (KB0023162).

Disconnecting keeps the session and its applications running; logging out
ends both (KB0023162). Disconnected sessions end after seven days of
inactivity (KB0023170). All sessions end at 7am on maintenance day, the second
Sunday of each month (KB0023170).

## Limits on a shared node

Each user may use at most 100 GB of RAM across the session (KB0023170). Past
that, RED kills one or more of your processes (KB0023170). KB0023167 says it
kills the process using the most RAM. Move anything needing 70 to 80 GB or
more to a compute node (KB0023167).

Fair share throttles heavy CPU users (KB0023170). A parallel test for a few
minutes is fine; hours is not, and may cost login privileges (KB0023170).

**Open item:** KB0023167 asks users to limit parallelism to between 4 and 8
processors. KB0023170 says 5 or fewer. Both still say this on 2026-10-01.
Using 4 or 5 processors satisfies both articles.

**Open item:** KB0023170 calls RED nodes login nodes. KB0022436 kills login
node processes after 20 minutes of CPU time. The KB does not say whether
that rule applies on RED. **Observed 2026-10-03** on a Quartz login node:
`ulimit -t` is `unlimited` and `limits.conf` sets no CPU limit, so the rule is
enforced elsewhere. Comparing `ulimit` output cannot settle it.

Check the node you are on with these commands. They are generic Linux, not
from the KB:

```bash
hostname                                   # which RED node holds your session
nproc; free -g                             # cores and memory on this VM
ps -u "$USER" -o pid,rss,pcpu,etime,comm --sort=-rss | head   # your biggest processes
```

## Launch an interactive Quartz job

The Interactive Job desktop icon requests four hours, eight cores, and 32 GB
on one Quartz compute node (KB0023170). It normally starts in two or three
minutes (KB0023170). For more resources, use `srun` in a Terminal
(KB0023170). This KB0025672 example adds `--x11` for GUI output:

```bash
srun -A slurm-account-name -p interactive --nodes=1 --cpus-per-task=8 \
     --time=1:00:00 --mem=20G --x11 --pty bash
```

KB0025672 also names `debug` and `h100-debug`. Check limits with
`sinfo -p interactive` and `sacctmgr show qos allocated` (KB0023298). See
`submitting-hpc-jobs` for partitions and `salloc`.

**Observed 2026-10-03** on Quartz, reading
`/N/soft/rhel8/red/bin/slurm_job_submit_interactive.sh`: the Interactive Job
icon picks an account from `sacctmgr show association user=$USER`. It prefers
`staff`, then an `r` account, then a `c` account, then `student` or
`workshop`. It runs `srun -p interactive -A <account> --cpus-per-task=8
--mem=32G --time=4:00:00 --x11 --pty bash`. With no such account it stops and
points to RT Projects. To charge a different account, run the `srun` line
yourself with that account.

## Applications

The Applications menu lists installed software by category (KB0023170):

- Analytics: Jupyter Notebook, Mathematica, MATLAB, RStudio, SAS, SPSS, Stata.
- Coding and Editing: Emacs, Spyder, VS Code, and others.
- Compute jobs: Interactive job, Quartz Job Manager, Slurm Info.
- Visualization: ParaView, QGIS, VMD, Fiji, and others.

The menu drifts from the KB. KB0026422 puts Forge under Coding and Editing,
but KB0023170 omits it. Check the live menu, and `module spider <word>`
(KB0023985).

### Jupyter

Jupyter Notebook is in the Applications menu. For Jupyter Lab, run
`module load jupyter`, then `jupyter lab` (KB0025672). For real computation,
start an interactive job and run Jupyter on the compute node (KB0025672).
RADL prefers Python scripts over notebooks there; convert with
`jupyter nbconvert --to python` (KB0025672). Jupyter cannot browse above home,
so `cd` to Slate first or symlink it into home (KB0025672).

RED also supports Posit Connect publishing (KB0025370) and the HPC LLM
platform (KB0027473).

## File systems visible from RED

The KB says RED sees these (KB0023167, KB0023170, KB0025948):

| Space | Path | Note |
| --- | --- | --- |
| Quartz home | `/N/u/<user>/Quartz` | Home icon. Trash counts toward quota (KB0023170). |
| Big Red 200 home | `/N/u/<user>/BigRed200` | Named in KB0025948 |
| Slate | `/N/slate/<user>` | Type the path in the file browser (KB0023170) |
| Slate-Project | `/N/project/<project>` | KB0025672 |
| Slate-Scratch | `/N/scratch/<user>` | Desktop icon (KB0023170) |
| SDA | Not mounted | FileZilla (SFTP) or Globus from the Storage menu (KB0023170) |
| Your computer | `thindrives` | ThinLinc client only (KB0023162) |

Check with `df -h /N/u/$USER/Quartz /N/slate/$USER /N/scratch/$USER`,
`ls /N/project`, and `quota` (KB0023231). Do not drag multi-gigabyte files
through `thindrives`; new exports appear only in a new session (KB0023162).

## Google at IU My Drive

Globus is the preferred route, especially above 1 GB (KB0025397). RED offers
three others (KB0025397):

- Firefox on RED, at `google.iu.edu`.
- `module load rclone`, then `rclone config create googlemydrive drive`.
- Caja through GNOME Online Accounts, for transfers of 1 GB or less.

Avoid `rclone mount` (KB0025397). It exists only on your RED node, so jobs
cannot see it. Its I/O is at least 10 times slower than Slate-Scratch. A
killed mount may stay locked until maintenance reboots (KB0025397).

## Data classification

**Open item:** RED is absent from both approval lists. KB0023515 lists Quartz,
but not RED, for PHI. KB0025747 lists Quartz as Restricted, but not RED. RED
runs on nodes that are part of Quartz (KB0023170). The KB does not say whether
Quartz's approval covers RED.

Until SecureMyResearch answers in writing, do not open PHI in RED. Ask at
securemyresearch@iu.edu (KB0023515). This is this skill's advice, not KB
policy. Files with PHI must be encrypted at rest and in transit anywhere
(KB0023515). Other Critical data is barred from all Research Technologies
systems (KB0025747).

## Troubleshooting

| Symptom | Likely cause or fix | Source |
| --- | --- | --- |
| "Wrong username or password" or a timeout | Wrong credentials, no Quartz account, account not yet active, or maintenance day | KB0023231 |
| "You are not allowed to use ThinLinc" | RED may be offline for maintenance | KB0023231 |
| "Perhaps this server doesn't run a ThinLinc server?" | Server field is not `red.uits.iu.edu` | KB0023231 |
| "Server refused the connection" | Five failed logins block you for one hour | KB0023231 |
| Immediate timeout | SSH port not set to 22 | KB0023231 |
| "SSH connection succeeded, but the ThinLinc server connection failed", or a session bus error | `.bashrc` prepends to `PATH`, often from `conda init` | KB0023231, KB0022379 |
| Blank blue screen or stuck at "step X of Y" | Restart client, choose Advanced, End existing session | KB0023231 |
| `.ICEauthority` error, missing icons, crashes | Home quota full; empty Trash, run `quota` | KB0023231 |
| Full screen hides controls | Press F8, deselect Full screen | KB0023231 |
| `thindrives` empty | Run `tl-mount-verbose.sh`, or log out and back in | KB0023231 |
| A process vanished | Session passed 100 GB of RAM | KB0023170 |

Append to `PATH`, use the `conda` module, and never run `conda init`
(KB0023231, KB0022379). If RED will not start, fix `.bashrc` or quota over SSH
to `quartz.uits.iu.edu` (KB0023231).

## Support

Send RED questions to the RED development team, part of RADL, at
`https://projects.rt.iu.edu/help/?queue=red` (KB0023167, KB0023697).

**Open item:** some specific problems still point to the RADL queue,
`?queue=radl`. These are Interactive Job failures (KB0023170), login lockouts
and web-client session resets (KB0023231), and RSA key help (KB0023162). Each
link is labeled as the RED team. Either queue appears to reach them.

Jupyter software questions go to RADL (KB0025672). Inside RED, the Feedback
and Questions icon also reaches the team (KB0023170).

## Keep this file current

Re-read KB0023167, KB0023170, and KB0023231 before changing limits or the
troubleshooting table. On RED, compare the Applications menu, `df -h`, and
`sinfo -p interactive` with this file. Record each difference with the date and
mark it as observed. Close an open item only with a KB citation or a written
answer from the owning team.

## Sources

All IU KB articles, read 2026-10-01. KB0023515 and KB0025747 re-read
2026-10-03. URL form:
`https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=<number>`.

- [KB0022379](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022379) Install packages in a conda environment on IU's high performance computers
- [KB0022436](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022436) Run GPU-accelerated jobs on Quartz or Big Red 200 at IU
- [KB0022656](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022656) Computing accounts at IU
- [KB0023162](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023162) Download, install, and configure ThinLinc Client to use Research Desktop (RED) at IU
- [KB0023167](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023167) About Research Desktop (RED) at IU
- [KB0023170](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023170) Research Desktop (RED) usage policies and interface features
- [KB0023231](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023231) Troubleshoot Research Desktop
- [KB0023298](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023298) Use Slurm to submit and manage jobs on IU's research computing systems
- [KB0023515](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023515) UITS Research Technologies systems and services for researchers working with data containing HIPAA-regulated PHI
- [KB0023697](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023697) Research computing support at IU
- [KB0023985](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023985) About Quartz at IU
- [KB0025370](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025370) About Posit Connect at IU
- [KB0025397](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025397) Access Google at IU My Drive from Research Desktop (RED)
- [KB0025672](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025672) Use Jupyter Notebook on Quartz
- [KB0025747](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025747) Types of sensitive institutional data appropriate for UITS Research Technologies services
- [KB0025948](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025948) Get started on IU research HPC and storage systems
- [KB0026422](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0026422) Use Linaro Forge to profile resource utilization and debug your programs on IU research computers
- [KB0027473](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0027473) Common LLM workflows on IU's research supercomputers
