---
name: submitting-hpc-jobs
description: Submit, monitor, and cancel Slurm jobs on IU's Quartz and Big Red 200 supercomputers. Covers the Slurm Account Name from RT Projects, partitions including the GPU partitions, a batch script skeleton, interactive jobs, job arrays and PCP, Lmod modules, Python and Apptainer, where job data should live, and the limits that kill jobs. Use when writing or debugging an sbatch script, choosing a partition, or working out why an IU job did not run.
---

# Submitting HPC jobs at IU

Verified 2026-10-01 against the IU Knowledge Base (KB). Each claim names its
KB article; links are in Sources at the end.

Quartz and Big Red 200 both use Slurm and Lmod (KB0023298, KB0023985,
KB0026317). The commands below work on both unless a section says otherwise.
Check data classification first: Big Red 200 is not cleared for PHI
(KB0026317). See the `iu-research-computing-map` skill.

## Three things must be true before a job runs

A job runs only when all three hold (KB0025948):

1. You have an account on that system.
2. You are a member of an RT Project.
3. You are added to that project's allocation for that system.

Every job must name the allocation's Slurm Account Name with `-A`
(KB0024132, KB0023298). Find it on the RT Projects home page under
"Submitting Slurm Jobs with your Project's Account" (KB0023298). See the
`requesting-accounts-and-allocations` skill to get one.

## Log in

```bash
ssh <username>@quartz.uits.iu.edu
ssh <username>@bigred200.uits.iu.edu
```

Login needs your IU passphrase and Duo (KB0025948). SSH keys need the signed
"SSH public key authentication to HPS systems" agreement (KB0023985). Idle SSH
sessions close after 60 minutes (KB0023985).

Do not compute on login nodes. Processes there are killed after 20 minutes of
CPU time, without warning (KB0022436).

## Batch job skeleton

This is the serial-job example from KB0023298, with the account added.

```bash
#!/bin/bash
#SBATCH -J job_name
#SBATCH -p general
#SBATCH -o filename_%j.txt
#SBATCH -e filename_%j.err
#SBATCH --mail-type=ALL
#SBATCH --mail-user=username@iu.edu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=02:00:00
#SBATCH --mem=16G
#SBATCH -A slurm-account-name

module load modulename
srun ./my_program my_program_arguments
```

`%j` becomes the job ID (KB0023298). `--mail-type=ALL` sends a resource
summary when the job ends, which helps size `--mem` (KB0022436).

A minimal runnable script is in
[scripts/quartz-minimal.sbatch](scripts/quartz-minimal.sbatch). Its directives
match KB0023298. It has not been run as written.
Run it once and record the result as Observed.

Submit it and note the job ID:

```bash
sbatch quartz-minimal.sbatch
```

### Parallel options

- For threads on one node, add `--cpus-per-task=N` and set
  `OMP_NUM_THREADS` to the same N (KB0023298).
- For MPI across nodes, set `--nodes` and `--ntasks-per-node`. Request more
  than one node only if the program communicates across nodes (KB0023298).
- Use `--begin=YYYY-MM-DDTHH:MM:SS` to defer a job (KB0023298).
- Use `--no-requeue` for a job that must not restart after an interruption
  (KB0023298).

## Partitions

Run `sinfo` on the system for the current list. Each system shows different
partitions (KB0023298). These names appear in the KB:

| System | Partition | Purpose | Source |
| --- | --- | --- | --- |
| Quartz | `general` | Default CPU partition. Sample output shows a 4-day limit. | KB0023298 |
| Quartz | `debug` | Short test jobs. Sample output shows a 4-hour limit. | KB0023298 |
| Quartz | `interactive` | Interactive jobs, including from RED | KB0025672, KB0023170 |
| Quartz | `h100-debug` | Short GPU tests | KB0025672 |
| Quartz | `v100` | 24 nodes, 4 V100 each | KB0022436 |
| Quartz | `h100-single` | 50 nodes, 4 H100 each, a quarter node per job | KB0022436 |
| Quartz | `h100-multi` | 12 nodes, 4 H100 each | KB0022436 |
| Big Red 200 | `gpu` | 64 nodes, 4 A100 each. Sample output shows a 2-day limit. | KB0022436 |

The Quartz partitions `gpu` and `hopper` were renamed on 2026-08-09. Jobs
naming the old partitions are rejected (KB0022436).

Check the per-job and per-user limits with this command (KB0023298):

```bash
sacctmgr show qos allocated format=Name%15,MaxTres%20,MaxSubmitPU
```

**Open item:** the KB does not name Big Red 200's CPU partitions. Run `sinfo`
on Big Red 200 and record what you find here.

## GPU jobs

Add three things to a GPU job (KB0022436):

- `-p` with a GPU partition name.
- `--gpus-per-node`, up to 4.
- `-A` with your Slurm Account Name.

```bash
# One H100 on Quartz, interactive
srun -p h100-single -A slurm-account-name --gpus-per-node h100:1 --pty bash

# One A100 on Big Red 200, interactive
srun -p gpu -A slurm-account-name --gpus-per-node 1 --pty bash
```

The `python/gpu` modules bundle TensorFlow, Torch, scikit-learn, and similar
tools (KB0022436). List them with `module spider python/gpu`.

## Interactive jobs

Use `srun --pty` for a shell on a compute node (KB0023298):

```bash
srun -p general -A slurm-account-name --time=01:00:00 --pty bash
srun -p debug -A slurm-account-name --time=01:00:00 --pty bash
```

Add `--x11` for graphical programs (KB0023298). Type `exit` to release the
node.

A shell from `srun --pty` cannot run further `srun` steps. Use `salloc`
instead when you need several steps (KB0023298):

```bash
salloc -A slurm-account-name --nodes=1 --ntasks-per-node=24 --time=2:00:00 --mem=128G
srun -n 24 python my_program.py
exit
```

From RED, the Interactive Job icon starts a 4-hour, 8-core, 32 GB job on a
Quartz compute node (KB0023170).

## Many small jobs: arrays and PCP

The KB mentions job arrays only as an alternative to PCP (KB0023513). It does
not document IU-specific array limits. Standard Slurm syntax is
`#SBATCH --array=1-100` with `$SLURM_ARRAY_TASK_ID` in the script.
**Open item:** confirm array size limits on each system with HPS or with
`scontrol show config`.

PCP runs a list of serial commands across the cores of one job (KB0023513).
Load it with `module load pcp`. Put one command per line in a text file. It
suits parameter sweeps and Monte Carlo runs. It can use cores more
efficiently than many separate jobs (KB0023513).

## Monitor and cancel

| Task | Command | Source |
| --- | --- | --- |
| Your jobs | `squeue -u <username>` | KB0023298 |
| Your pending jobs in a partition | `squeue -u <username> -p general -t PENDING` | KB0023298 |
| One job, all fields | `squeue -j <jobid> -o %all` | KB0023298 |
| Cancel one job | `scancel <jobid>` | KB0023298 |
| Cancel by name | `scancel -n <job_name>` | KB0023298 |
| Cancel all your jobs | `scancel -u <username>` | KB0023298 |
| Partitions and limits | `sinfo`, or `sinfo -No "%10P %8N %4c %7m %10l %.6t"` | KB0023298 |

## Software: modules, Python, containers

- `module avail` lists what can load now. `module spider <word>` searches
  every module (KB0023985).
- Load a Python module before running Python. The operating system's own
  Python is not supported (KB0024539).
- You may install software in your home directory or Slate space. Only you can
  use it there. A package installed in Slate-Project space is usable by the
  whole project (KB0022486).
- A faculty member or PI requests shared software with an HPC Software
  Request. Students' advisors request it for them (KB0022486).
- Apptainer runs containers on both systems: `module load apptainer`
  (KB0025214). Ask RADL first whether the application can be installed
  natively (KB0025214).

## Where job data goes

| Location | Use it for | Rule |
| --- | --- | --- |
| Home, `/N/u/<user>/Quartz` | Scripts, configuration, builds | 100 GB. Slow I/O. Not for large data (KB0022439). |
| Slate-Scratch, `/N/scratch/<user>` | Job input and output while running | Purged after 30 days without access. Not backed up (KB0022439). |
| Node `/tmp` on Quartz | Per-job temporary files | 1.7 TB. Deleted after 10 days (KB0022439). |
| Slate, `/N/slate/<user>` | Personal working data that must persist | Not backed up (KB0022439). |
| Slate-Project, `/N/project/<project>` | Shared project data | Not backed up. Needs an allocation (KB0022439). |
| SDA | Anything worth keeping | Tape archive, two copies (KB0024406). |

Check quotas with `quota`, after `module load quota` if needed (KB0023985).

For PHI, keep files in a `chmod 700` directory, encrypt them with GPG at rest,
and share with ACLs only (KB0022478).

## Common causes of failure

Each row names a KB rule. The KB does not quote Slurm's error text, so match
on the cause, not the message.

| Symptom | Likely cause | Source |
| --- | --- | --- |
| Job rejected for an unknown partition | Old Quartz names `gpu` or `hopper` | KB0022436 |
| Job rejected or never eligible | Missing or wrong `-A`, or you are not on the allocation | KB0025948, KB0024132 |
| All jobs stopped working in July | The RT Project was not renewed; Slurm accounts deactivate after the renewal window | KB0024132 |
| A process on the login node vanished | It exceeded 20 minutes of CPU time | KB0022436 |
| A RED process vanished | The session exceeded 100 GB of RAM | KB0023170 |
| SSH session dropped | Idle for 60 minutes | KB0023985 |
| Files missing from scratch | Not accessed for 30 days, so purged | KB0022439 |
| Everything down on a Sunday | Monthly maintenance, second Sunday, 7am to 7pm | KB0023985 |
| SDA unreachable on a Sunday morning | Weekly SDA maintenance, 7am to 10am | KB0024406 |
| Account disabled | Not used for six months | KB0022486 |

## Keep this file current

Run `sinfo` and `sacctmgr show qos allocated` when you are on a system. Record
any partition or limit that differs from this file, with the date. Re-read
KB0023298 and KB0022436 before changing the skeleton or the GPU section. Add
real Slurm error text to the failure table once you have seen it, and say it
was observed rather than read in the KB.

## Sources

All IU KB articles, read 2026-10-01. URL form:
`https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=<number>`.

- [KB0022436](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022436) Run GPU-accelerated jobs on Quartz or Big Red 200 at IU
- [KB0022439](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022439) Available access to allocated and short-term storage capacity on IU's research systems
- [KB0022478](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022478) Secure research data containing HIPAA-regulated PHI on high performance file systems at IU
- [KB0022486](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022486) Policies regarding UITS research systems
- [KB0023170](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023170) Research Desktop (RED) usage policies and interface features
- [KB0023298](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023298) Use Slurm to submit and manage jobs on IU's research computing systems
- [KB0023513](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023513) Use PCP to bundle multiple serial jobs to run in parallel on IU research supercomputers
- [KB0023985](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023985) About Quartz at IU
- [KB0024132](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024132) Use RT Projects to request and manage access to specialized Research Technologies resources
- [KB0024406](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024406) About the Scholarly Data Archive (SDA) at Indiana University
- [KB0024539](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024539) Use Python on IU research supercomputers
- [KB0025214](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025214) Use Apptainer on Quartz or Big Red 200 at IU
- [KB0025672](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025672) Use Jupyter Notebook on Quartz
- [KB0025948](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025948) Get started on IU research HPC and storage systems
- [KB0026317](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0026317) About Big Red 200 at IU
