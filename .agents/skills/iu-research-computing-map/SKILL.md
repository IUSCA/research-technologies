---
name: iu-research-computing-map
description: Orientation to Indiana University research computing systems (Quartz, Big Red 200, Research Desktop, Jetstream2, Slate, Slate-Project, Slate-Scratch, Geode-Project, home directories, and the Scholarly Data Archive), what each is for, who can get access, and which data classifications each is approved for, including PHI. Use when choosing where IU research data or computation should go, checking whether a system may hold PHI or Restricted data, or deciding how a portal or service should hand computation to an IU cluster.
---

# IU research computing map

Verified 2026-10-07 (KB0023515, KB0024420, KB0025574, and KB0025747 only)
against the IU Knowledge Base (KB). Other sources were verified 2026-10-01. Each claim
names its KB article; links are in Sources at the end.

Check data classification before anything else. A system that is fast and
available is still the wrong system if it is not approved for the data.

## Current systems at a glance

IU has two current research supercomputers: Quartz and Big Red 200. The
hostname list (KB0025040) and the supercomputer overview (KB0023647) name only
these two. Any other cluster name is retired; see
[references/retired-and-renamed.md](references/retired-and-renamed.md).

| System | What it is | Typical use |
| --- | --- | --- |
| Quartz | High-throughput cluster, `quartz.uits.iu.edu` | Most CPU and GPU batch work, including PHI work |
| Big Red 200 | HPE Cray EX supercomputer, `bigred200.uits.iu.edu` | Large parallel and A100 GPU work without PHI |
| Research Desktop (RED) | Graphical desktop on Quartz-dedicated VMs | GUI applications, Jupyter, light interactive work |
| Jetstream2 | OpenStack cloud allocated through ACCESS or NAIRR Pilot | Gateways, always-on services, prototyping |
| Home directory (Geode) | 100 GB per user, shared across systems | Scripts, configuration, small files |
| Slate | Lustre, persistent, per user | Working data for one person |
| Slate-Project | Lustre, persistent, per project | Shared working data for a group |
| Slate-Scratch | Lustre, purged | Temporary job data |
| Geode-Project | Disk with snapshots, per project | Shared files that need snapshots or campus mounts |
| Scholarly Data Archive (SDA) | Tape archive | Long-term copies of large files |

## Data classification approvals

This table matters most for clinical and biobank data. It combines two KB
articles: the PHI list (KB0023515) and the most-sensitive-classification list
(KB0025747).

| System | PHI allowed | Most sensitive non-PHI classification |
| --- | --- | --- |
| Quartz | Yes (KB0023515, KB0023985) | Restricted (KB0025747) |
| Slate, Slate-Project, Slate-Scratch | Yes (KB0023515) | Restricted (KB0025747) |
| Geode home and Geode-Project | Yes (KB0023515, KB0022668, KB0024967) | Restricted for Geode-Project (KB0025747) |
| SDA | Yes (KB0023515, KB0024406) | Restricted (KB0025747) |
| Research Databases (ResDB) | Yes (KB0023515) | Restricted (KB0025747) |
| IU REDCap | Yes (KB0023515) | Public (KB0025747) |
| Big Red 200 | **No.** "Not currently cleared" for PHI (KB0026317) | Not listed. Open item. |
| Research Desktop (RED) | Not listed. Open item. | Not listed. Open item. |
| Jetstream2 | Not listed by the KB. See below. | Not listed. Open item. |

Read the PHI column with these rules, all from the KB:

- Critical data other than PHI is not permitted on any Research Technologies
  system (KB0025747, KB0023515).
- "Approved for PHI" means the system meets certain HIPAA Security Rule
  requirements. You must still add your own administrative, physical, and
  technical safeguards (KB0023515, KB0023407).
- The PI needs IRB approval before using any IU-owned resource for PHI work
  (KB0023407).
- Everyone working with HIPAA-regulated data needs annual compliance training
  (KB0023407).
- PHI files must be encrypted at rest and in transit (KB0023515). Use GPG for
  files at rest on the supercomputers (KB0022478).
- A group or departmental account may not be used for PHI. Each person uses an
  individual login (KB0023515, KB0022656).
- Keep PHI in a directory only you can read, and share it with ACLs, never
  with group permissions (KB0022478).
- Do not put sensitive data in a file name or path (KB0023985, KB0026317).
- PHI is allowed only for research, not for active patient treatment
  (KB0023407).
- Software you deploy or administer on these systems is not automatically
  HIPAA-aligned (KB0023407, KB0025574).

Jetstream2 is outside the KB's lists. **External:** the Jetstream2 acceptable
use policy bars HIPAA-protected data unless the responsible University
administrator authorizes it. It says the system does not meet those
requirements by default. Treat Jetstream2 as not approved for PHI unless
SecureMyResearch says otherwise. See the `jetstream2` skill.

Ask SecureMyResearch (securemyresearch@iu.edu) before any new PHI workflow.
It offers no-fee consulting on which system fits and how to secure it
(KB0025362).

## Compute

### Quartz

Quartz is IU's high-throughput cluster (KB0023985). It has 92 CPU nodes. Each
has two 64-core AMD EPYC 7742 CPUs and 512 GB of RAM. Quartz also has GPU
partitions with V100 and H100 GPUs (KB0022436). Quartz runs Red Hat Enterprise
Linux 8 and uses Lmod and Slurm (KB0023985).

Who can get access: all IU students, faculty, staff, and sponsored affiliated
researchers can request an account (KB0022656). Running jobs also needs an RT
Projects allocation (KB0025948).

Use Quartz for PHI computation. It is the only research supercomputer on the
PHI list (KB0023515).

### Big Red 200

Big Red 200 is an HPE Cray EX supercomputer (KB0026317). It has 640 CPU nodes
with 256 GB of memory and two 64-core EPYC 7742 CPUs each. It also has 64 GPU
nodes with four NVIDIA A100 GPUs each. It runs SUSE Linux Enterprise Server 15.

Who can get access: IU graduate students, faculty, and staff can request an
account. Undergraduates and affiliates need a full-time faculty or staff
sponsor (KB0026317, KB0022656).

Do not use Big Red 200 for PHI (KB0026317).

### GPU resources

All current IU GPU nodes are in Quartz or Big Red 200 (KB0022436).

| System | Partition | Nodes | GPUs per node | Memory per GPU |
| --- | --- | --- | --- | --- |
| Quartz | `v100` | 24 | 4 V100 | 32 GB |
| Quartz | `h100-single` | 50 | 4 H100 | 80 GB |
| Quartz | `h100-multi` | 12 | 4 H100 | 80 GB |
| Big Red 200 | `gpu` | 64 | 4 A100 | 40 GB |

A job in `h100-single` gets at most one quarter of a node (KB0022436). Quartz
renamed `gpu` to `v100` and `hopper` to `h100-multi` on 2026-08-09. Jobs that
use the old names are rejected (KB0022436).

KB0023985 says Quartz has 88 GPU nodes, but KB0022436's partition table sums
to 86. The system settles counts like this. Run `describe-cluster.sh` from the
`submitting-hpc-jobs` skill, and trust its output over either article.

### Research Desktop (RED)

RED is a graphical desktop for people with Quartz accounts (KB0023167). It
runs on more than two dozen shared VMs. Reach it with the ThinLinc client or
at `https://red.uits.iu.edu`. It needs a Quartz account and Duo.

RED nodes are login nodes. Run compute-heavy or memory-heavy work on Quartz
compute nodes instead (KB0023170). Each user may use at most 100 GB of RAM in a
session. Past that limit, RED terminates the largest process (KB0023167) or one or
more processes (KB0023170). See the `using-research-desktop` skill.

**Open item:** KB0023167 asks users to limit parallelism to 4 to 8 processors.
KB0023170 says to limit it to 5 or fewer.

### Jetstream2

Jetstream2 is an OpenStack research cloud whose primary system is at IU
(KB0024420). It is not an HPC or high-throughput environment. It is meant for
interactive and smaller-scale work, and for science gateways. A gateway may
compute on Jetstream2 or route jobs to HPC systems (KB0024420).

Access comes through ACCESS or NAIRR Pilot allocations (KB0024420). See the
`jetstream2` skill.

## Storage

This table is the overview. The `storing-and-moving-research-data` skill has
paths, quota checks, transfers, sharing, and the PHI procedure. Check live
quotas with `quota` on a login node rather than trusting a size here.

| Storage | Path | Default size | Backup | When data is removed |
| --- | --- | --- | --- | --- |
| Home directory | `/N/u/<user>/Quartz`, `/N/u/<user>/BigRed200` | 100 GB, shared across all your supercomputer accounts (KB0025028) | Monthly backup and daily snapshots in `.snap` (KB0023379) | 180 days after the account is disabled (KB0023379) |
| Slate | `/N/slate/<user>` | 800 GiB, up to 1.6 TiB on request (KB0022439) | None (KB0022439) | 180 days after the account is disabled (KB0022391) |
| Slate-Project | `/N/project/<project>` | Up to 120 TiB without fee (KB0022586) | None (KB0022439) | 180 days after an incomplete annual review; class allocations 30 days after expiry (KB0022423) |
| Slate-Scratch | `/N/scratch/<user>` | Up to 100 TiB (KB0025317) | None (KB0022439) | Files unaccessed for 30 days; oldest first when the system passes 80% full (KB0025317) |
| Quartz local scratch | `/tmp` on a node | 1.7 TB (KB0022439) | None | Files older than 10 days (KB0022439) |
| Geode-Project | Mounted on clusters and campus | Set by agreement (KB0022439) | Not backed up; replicated to two data centers, with daily snapshots (KB0023373) | 180 days after the account is disabled (KB0023373) |
| SDA | HSI, HTAR, SFTP, Globus | 50 TB (KB0024406) | Two tape copies at two sites (KB0024406) | Never while the owner's account is valid (KB0024406). Deletions are permanent (KB0024366). |

Points that change a design:

- Slate, Slate-Project, and Slate-Scratch are working storage, not backed up
  (KB0023515, KB0022439). Archive anything worth keeping to the SDA
  (KB0022439).
- Slate-Project needs an RT Projects allocation. Allocations above 120 TB are
  direct-billed (KB0022439).
- The SDA is offline every Sunday 7am to 10am. It suits large files; many
  small files perform badly (KB0024406).

KB articles disagree on several storage numbers, such as SDA file-count limits
and TB versus TiB. The `storing-and-moving-research-data` skill lists them as
open items.

## Platform services hand computation to a cluster

A portal, notebook container, or other platform service should not run heavy
computation itself. Computation that needs real resources is submitted to an
IU cluster. The KB supports this split in several places:

- Login-node processes are killed after 20 minutes of CPU time (KB0022436).
- RED nodes are login nodes. Heavy work belongs on compute nodes (KB0023170).
- RADL recommends Python scripts over notebooks on compute nodes, because
  interactive notebooks waste node time (KB0025672).
- Jetstream2 is meant as a gateway back end that can route jobs to HPC
  (KB0024420).

### Submitting on behalf of a group or from a service account

The KB does not document service accounts, a Slurm REST API, or remote job
submission for portals. Treat automated submission as needing a special
arrangement with the High Performance Systems (HPS) team. These KB rules
constrain any design:

- A passphrase is for its owner only. Do not share it (KB0022486).
- Login nodes and SCP or SFTP need Duo. SSH keys need a signed "SSH public key
  authentication to HPS systems" agreement and a passphrase on the key
  (KB0023985).
- Unattended listening services, such as a program waiting on a socket, are
  terminated (KB0022486).
- Group accounts exist and can request research system accounts (KB0022656,
  KB0022647). A group account needs an active faculty or staff owner
  (KB0022656).
- **A group account may not touch PHI** (KB0022656, KB0023515). A portal that
  runs PHI jobs under one shared account breaks this rule. PHI jobs must run
  under the researcher's own login.
- Accounts unused for six months are disabled (KB0022486).
- Each job charges an RT Projects Slurm Account Name, and the PI controls who
  may use it (KB0024132).

Departments can buy Quartz-compatible nodes that UITS hosts and manages for
their sole use (KB0024661). Ask HPS about this colocation service when a
service needs dedicated capacity.

**Open items.** The KB does not answer these. Ask HPS before designing
around any of them.

- May a service submit jobs as, or on behalf of, a researcher?
- May `scrontab` or cron run on login nodes?
- Does a Slurm REST endpoint exist for IU clusters?

## Keep this file current

When a claim here disagrees with the KB, the KB is right. Fix the claim, cite
the article, and update the Verified line. Record a newly retired system in
`references/retired-and-renamed.md` rather than deleting it. Add an open item
when the KB is silent. Remove an open item only when the KB or the owning
team answers it, and cite that answer.

## Sources

All IU KB articles, read 2026-10-01. KB0023515, KB0024420, KB0025574, and
KB0025747 re-read 2026-10-07. URL form:
`https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=<number>`.

- [KB0022391](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022391) Slate high performance storage system: Terms of service
- [KB0022423](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022423) Slate-Project high performance storage system: Terms of service
- [KB0022436](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022436) Run GPU-accelerated jobs on Quartz or Big Red 200 at IU
- [KB0022439](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022439) Available access to allocated and short-term storage capacity on IU's research systems
- [KB0022478](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022478) Secure research data containing HIPAA-regulated PHI on high performance file systems at IU
- [KB0022486](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022486) Policies regarding UITS research systems
- [KB0022586](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022586) About Slate-Project high performance project space at IU
- [KB0022647](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022647) Get additional IU computing accounts
- [KB0022656](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022656) Computing accounts at IU
- [KB0022668](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022668) About Geode at Indiana University
- [KB0023167](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023167) About Research Desktop (RED) at IU
- [KB0023170](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023170) Research Desktop (RED) usage policies and interface features
- [KB0023238](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023238) Research and high performance computing
- [KB0023373](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023373) Geode-Project: Terms of service
- [KB0023379](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023379) Geode home directory file system: Terms of service
- [KB0023407](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023407) Your legal responsibilities for protecting data containing PHI when using UITS Research Technologies systems and services
- [KB0023515](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023515) UITS Research Technologies systems and services for researchers working with data containing HIPAA-regulated PHI
- [KB0023647](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023647) Supercomputers for academic research at IU
- [KB0023985](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023985) About Quartz at IU
- [KB0024132](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024132) Use RT Projects to request and manage access to specialized Research Technologies resources
- [KB0024366](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024366) About accidentally deleted SDA files
- [KB0024406](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024406) About the Scholarly Data Archive (SDA) at Indiana University
- [KB0024420](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024420) About Jetstream2
- [KB0024661](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024661) Research computing services at IU
- [KB0024967](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024967) Request a project space allocation on Geode-Project
- [KB0025028](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025028) About home directory space on IU research supercomputers
- [KB0025040](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025040) Hostnames of IU research supercomputers
- [KB0025317](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025317) Slate-Scratch high performance file system: Terms of service
- [KB0025362](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025362) About SecureMyResearch
- [KB0025574](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025574) Questions you'll need to answer when requesting research computing accounts
- [KB0025672](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025672) Use Jupyter Notebook on Quartz
- [KB0025747](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025747) Types of sensitive institutional data appropriate for UITS Research Technologies services
- [KB0025948](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025948) Get started on IU research HPC and storage systems
- [KB0026317](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0026317) About Big Red 200 at IU

External, read 2026-10-01:

- [Jetstream2 acceptable use policies](https://docs.jetstream-cloud.org/general/policies/)
