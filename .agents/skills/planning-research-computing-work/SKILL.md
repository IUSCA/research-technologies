---
name: planning-research-computing-work
description: Turn a researcher's described workflow into a concrete plan across IU research computing systems. Collects data classification (PHI, Restricted), data sizes and file counts, compute shape, interactivity, collaborators, retention, LLM use, and allocation status, then maps each stage to compute (Quartz, Big Red 200, Research Desktop, Jetstream2, REALLMS), storage (home, Slate, Slate-Project, Slate-Scratch, Geode-Project, SDA), data movement (Globus, HSI, HTAR, SFTP), and the accounts and RT Projects allocations still missing. Fills in a plan template with paths, the Slurm account, archive steps, gaps, and the checks to run first. Use when someone describes a new project, pipeline, or dataset and asks how or where to run it at IU, or before writing jobs for a workflow that spans several systems.
---

# Planning research computing work at IU

Verified 2026-10-03 against the IU Knowledge Base (KB). Each claim names its
KB article or the skill that holds the citation; links are in Sources.

This skill ties the other IU skills together. It decides which system holds
each stage of a workflow. The other skills say how to use each system.

Settle data classification before anything else. A fast system is still the
wrong system if it is not approved for the data (KB0023515, KB0025747).

## Start from what the person has

Read the person's private resources file first, if it exists. It lives at
`$IU_RESEARCH_NOTES`, or at `~/.config/iu-research/resources.md`. The
`checking-iu-research-access` skill explains the file and how to fill it.

Prefer accounts, Slurm accounts, and project directories the person already
holds. Re-check any fact in the file older than a quarter. Never copy that
file's contents into a shared repository.

## Collect the facts

Ask for what the description leaves out. Do not guess a classification.

| Ask | Why it matters |
| --- | --- |
| Does the data include PHI? What is its classification? | Rules out systems; see "Classification first" |
| Total size now and at the end, and the file count | Picks storage and quota; many small files change the plan |
| CPU or GPU, memory per task, hours per task | Picks system and partition |
| Many small independent tasks, or few large ones? | Job arrays or PCP versus large parallel jobs |
| GUI, notebook, batch, or an always-on service? | RED, an interactive job, Slurm, or Jetstream2 |
| Who works on it, and are any outside IU? | Accounts, affiliate sponsorship, Globus sharing |
| How long must inputs, intermediates, and results be kept? | Scratch purge, annual renewal, archive |
| Will it call an LLM, and on what data? | REALLMS API or the HPC LLM platform |
| Which RT Project, allocations, and budget exist? | Slurm account, free versus billed storage |

If the person cannot name the classification, send them to the Data
Stewards or SecureMyResearch before planning further (KB0025747, KB0025362).

## Classification first

The `iu-research-computing-map` skill holds the approval table and the full
PHI rules. Apply them from there; do not paraphrase them into the plan.
These consequences shape most plans:

- Critical data other than PHI may not go on any Research Technologies
  system (KB0025747).
- PHI computation goes to Quartz. Big Red 200 is not cleared for PHI
  (KB0023515, KB0026317).
- PHI may live in home, Slate, Slate-Project, Slate-Scratch,
  Geode-Project, and the SDA (KB0023515).
- RED and Jetstream2 are not on the PHI list. Treat both as not approved
  for PHI; the map and `using-research-desktop` record the open items.
- The REALLMS API is approved for PHI (KB0027272). The `using-reallms`
  skill records a conflicting article.
- A PHI workflow needs IRB approval and individual logins, never a group
  account (KB0023407, KB0022656).

## Choose compute

| Workload | System | Source or skill |
| --- | --- | --- |
| CPU batch, any classification up to PHI | Quartz | KB0023985 |
| Large parallel MPI, or A100 GPUs, without PHI | Big Red 200 | KB0026317, KB0022436 |
| GPU work with PHI | Quartz V100 or H100 partitions | KB0022436, KB0023515 |
| Many small independent tasks | Slurm job arrays, or PCP in one job | KB0023513; `submitting-hpc-jobs` |
| GUI applications, light interactive work | RED, then an interactive Quartz job for heavy steps | KB0023170 |
| Notebooks on real data | Jupyter inside an interactive job | KB0025672 |
| Gateway, always-on service, prototype | Jetstream2, sending heavy jobs to HPC | KB0024420; `jetstream2` |
| LLM calls from code, modest volume | REALLMS API | KB0027272; `using-reallms` |
| Batch inference, fine-tuning, or high LLM volume | HPC LLM platform on Quartz or Big Red 200 | KB0027473 |

Run `describe-cluster.sh` before naming a partition or a GPU count. The
system outranks any table, as `submitting-hpc-jobs` explains.

## Choose storage for each stage

| Stage | Default home | Source or skill |
| --- | --- | --- |
| Scripts, configuration, code, environments | Home directory | KB0025028 |
| Inputs for one person | Slate | KB0022605 |
| Inputs or references shared by a group | Slate-Project | KB0022586 |
| Working files and intermediates of running jobs | Slate-Scratch | KB0022439, KB0025317 |
| Results the group keeps using | Slate-Project | KB0022586 |
| Shared files needing snapshots or desktop mounts | Geode-Project | KB0024967 |
| Long-term copy of inputs and results | SDA | KB0022439, KB0024406 |

Slate, Slate-Project, and Slate-Scratch have no backup (KB0022439).
Slate-Scratch deletes files unaccessed for 30 days (KB0025317). Quotas,
inode limits, and paths are in `storing-and-moving-research-data`; check
them live with `quota`.

Size drives some choices. Slate holds 800 GiB by default, up to 1.6 TiB
(KB0022605). A first Slate-Project request is limited to 30 TiB. Up to
120 TiB is free (KB0022586). The SDA starts at 50 TB (KB0024406).

## Choose data movement

| Move | Tool | Source or skill |
| --- | --- | --- |
| Between IU systems, or large transfers from outside | IU Globus web app | KB0025535 |
| Workstation to cluster storage | Globus Connect Personal, or an SMB mount | KB0025535; `storing-and-moving-research-data` |
| Cluster to SDA, scripted | HTAR for bundles, HSI for single large files | KB0023281, KB0022463 |
| PHI anywhere, encrypted first | Globus, SFTP, or SCP | KB0022463 |
| Share with non-IU collaborators | Globus guest collection, 30-day permissions | KB0026500 |

## Access prerequisites

A job runs only with a system account, RT Project membership, and that
project's allocation (KB0025948). Each job names a Slurm account with `-A`
(KB0024132).

| Gap | Skill that closes it |
| --- | --- |
| No account on a system, or not eligible | `requesting-accounts-and-allocations` |
| No RT Project, compute allocation, or Slate-Project or Geode-Project space | `requesting-accounts-and-allocations` |
| A member is missing from a project or allocation | `managing-rt-projects` |
| A non-IU collaborator needs to run jobs | `managing-rt-projects` (affiliate sponsorship, KB0023488) |
| Unclear which Slurm account fits | `checking-iu-research-access` (resources file) |
| HSI cannot log in from a script | `storing-and-moving-research-data` (keytab) |
| No REALLMS key | `using-reallms` |
| No Jetstream2 allocation | `jetstream2` |
| PHI workflow not yet reviewed | `getting-help-from-research-technologies` (SecureMyResearch) |

Choose the Slurm account whose RT Project covers the work. A PHI project
must say so in its RT Project description (KB0024132).

## Rules every plan follows

- Never run job I/O in the home directory (KB0025028). Set each job's
  working directory under Slate-Scratch or Slate-Project.
- Bundle collections of 100 or more files before they reach the SDA
  (KB0025237). Split bundles by how they will be retrieved.
- Copy results off Slate-Scratch inside the job script (KB0025317).
- **Practice:** archive results as soon as they are final, not near the
  purge. Verify the archive copy before deleting the source.
- Keep sensitive data out of file names and paths (KB0023985).

## Checks to run first

Run these before writing jobs. Each comes from another skill.

1. `check-local.sh` from `checking-iu-research-access`, on the workstation.
2. `check-cluster.sh` from `checking-iu-research-access`, on each cluster
   the plan uses.
3. `describe-cluster.sh` from `submitting-hpc-jobs`, for partitions and
   limits.
4. `quota` on a login node, for each storage space the plan uses.

The agent cannot answer Duo. The person logs in once first; see
`checking-iu-research-access`.

## The plan

Fill in [references/plan-template.md](references/plan-template.md). Save the
filled plan with the person's project, such as in its repository. Keep
usernames, project names, and paths out of shared skills.

[references/worked-examples.md](references/worked-examples.md) has three
illustrative plans: GPU training, PHI imaging, and many-small-files genomics.

## Open items

- Whether RED may hold PHI is unanswered; see `using-research-desktop`.
- How a Jetstream2 service authenticates to Quartz is unanswered; see
  `jetstream2`.

## Keep this file current

This skill should hold decisions, not system detail. When a fact here
changes, fix it in the skill that owns it first, then here. Re-read the
articles in Sources when the map's approval table changes. Add a worked
example when a common workflow does not fit the three given.

## Sources

All IU KB articles. Read 2026-10-03 unless noted. URL form:
`https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=<number>`.

- [KB0022436](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022436) Run GPU-accelerated jobs on Quartz or Big Red 200 at IU
- [KB0022439](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022439) Available access to allocated and short-term storage capacity on IU's research systems
- [KB0022463](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022463) Use HSI to access your SDA account at IU
- [KB0022586](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022586) About Slate-Project high performance project space at IU
- [KB0022605](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022605) About Slate high performance storage for research computation at IU
- [KB0022656](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022656) Computing accounts at IU
- [KB0023170](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023170) Research Desktop (RED) usage policies and interface features
- [KB0023281](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023281) Use HTAR with your SDA account
- [KB0023407](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023407) Your legal responsibilities for protecting data containing PHI when using UITS Research Technologies systems and services
- [KB0023488](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023488) Sponsor a computing account for an IU affiliate
- [KB0023513](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023513) Use PCP to bundle multiple serial jobs to run in parallel on IU research supercomputers
- [KB0023515](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023515) UITS Research Technologies systems and services for researchers working with data containing HIPAA-regulated PHI
- [KB0023985](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023985) About Quartz at IU
- [KB0024132](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024132) Use RT Projects to request and manage access to specialized Research Technologies resources
- [KB0024406](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024406) About the Scholarly Data Archive (SDA) at Indiana University
- [KB0024420](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024420) About Jetstream2
- [KB0024967](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024967) Request a project space allocation on Geode-Project
- [KB0025028](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025028) About home directory space on IU research supercomputers
- [KB0025237](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025237) Best uses for an IU SDA account
- [KB0025317](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025317) Slate-Scratch high performance file system: Terms of service
- [KB0025362](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025362) About SecureMyResearch
- [KB0025535](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025535) Use the IU Globus Web App to transfer data to and from your accounts on IU's research computing and storage systems
- [KB0025672](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025672) Use Jupyter Notebook on Quartz
- [KB0025747](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025747) Types of sensitive institutional data appropriate for UITS Research Technologies services
- [KB0025948](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025948) Get started on IU research HPC and storage systems
- [KB0026317](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0026317) About Big Red 200 at IU
- [KB0026500](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0026500) Share Geode-Project or Slate-Project data with non-IU collaborators
- [KB0027272](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0027272) About the Research and Academic LLM Services (REALLMS) API at IU
- [KB0027473](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0027473) Common LLM workflows on IU's research supercomputers
