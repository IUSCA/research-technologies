---
name: getting-help-from-research-technologies
description: Decide when to self-serve and when to contact IU Research Technologies, and pick the right channel - HPS for supercomputers, RADL for software and programming, HPFS for Slate storage, Research Storage for the SDA and Geode, SecureMyResearch for PHI and data classification, plus ResDB, REDCap, RED, BHRS, Jetstream2, and the HPC Slack. Covers what to put in a request. Use when an IU research computing question cannot be answered from the KB, or before drafting a ticket or email to an IU support team.
---

# Getting help from Research Technologies

Verified 2026-10-01 against the IU Knowledge Base (KB). Each claim names its
KB article; links are in Sources at the end.

Search the KB first, then ask the team that owns the system. Most questions
about limits, paths, and commands have a KB answer. Questions about policy
exceptions, PHI workflows, and automation do not, and need a person.

## Self-serve first

Answer these from the KB or the system itself before opening a request:

- Partitions and wall-time limits: run `sinfo` (KB0023298).
- Per-job and per-user limits: run
  `sacctmgr show qos allocated format=Name%15,MaxTres%20,MaxSubmitPU`
  (KB0023298).
- Available software: run `module spider <word>` (KB0023985).
- Quotas: run `quota` (KB0023985).
- Your Slurm Account Name: the RT Projects home page (KB0023298).
- Which systems may hold PHI: KB0023515 and KB0025747.

`tools/iukb.py` in this repository searches and reads KB articles from a
terminal. See `CONTRIBUTING.md`.

## Ask a person when

- The work involves PHI, a data use agreement, or an unclear data
  classification.
- You want a policy exception, such as a queue change (KB0023298).
- A portal or service needs to submit jobs or hold credentials. The KB does
  not cover this case.
- Something that worked has stopped and the KB explains nothing.
- You need software installed for a whole group (KB0022486).

## Who to contact

| Topic | Team | Channel | Source |
| --- | --- | --- | --- |
| Quartz or Big Red 200 system issues, accounts, queues, colocation nodes | High Performance Systems (HPS) | `https://projects.rt.iu.edu/help/?queue=hps` | KB0023697, KB0024661 |
| Compilers, libraries, debuggers, scientific software, programming help, containers | Research Applications and Deep Learning (RADL) | `https://projects.rt.iu.edu/help/?queue=radl` | KB0023697, KB0025214 |
| Research Desktop (RED) | RED development team, part of RADL | `https://projects.rt.iu.edu/help/?queue=red` | KB0023697 |
| Slate, Slate-Project, Slate-Scratch | High Performance File Systems (HPFS) | `https://projects.rt.iu.edu/help/?queue=hpfs` | KB0023697 |
| SDA, home directories, Geode-Project, HSI, HTAR | Research Storage | store-admin@iu.edu | KB0023697 |
| PHI, HIPAA, data classification, grant or DUA security terms | SecureMyResearch | securemyresearch@iu.edu | KB0025362 |
| Biomedical computing, data management, life-science workflows | Biomedical and Health Research Services (BHRS) | bhrs@iu.edu | KB0023420 |
| Research Databases (ResDB) | ResDB Administration | resdb@iu.edu | KB0023697 |
| IU REDCap | IU REDCap Support | redcap@iu.edu | KB0025747 |
| Visualization and the AVL | Advanced Visualization Lab | vishelp@iu.edu | KB0023697 |
| Shared software installation | Faculty or PI files an HPC Software Request | `https://projects.rt.iu.edu/request_forms/software-request` | KB0022486 |
| Jetstream2 allocation requests | IU Jetstream2 support | `https://jetstream-cloud.org/contact/index.html` | KB0024420 |
| Cannot create an account you are eligible for | Campus Support Center | See KB0022647 | KB0022647 |
| A retired KB article | KB team | kb@iu.edu | KB0024722 |
| Anything else in Research Technologies | Research Technologies | `https://uits.iu.edu/services/technology-for-research/support/index.html` | KB0025948 |

**Open items:**

- KB0023170 points RED questions to the RADL queue. KB0023697 points them to
  a separate `red` queue. Either appears to reach the RED team.
- A general RT Projects contact address is not in the KB. Ask HPS about RT
  Projects problems until one is found.
- The KB names no support channel for Posit Connect or REALLMS in the articles
  read. Search the KB for each before asking.

### Data classification questions

Use the Data Sharing and Handling (DSH) tool or ask the relevant Data Stewards
about a classification (KB0022478, KB0025747). Ask SecureMyResearch which
system fits a classified dataset (KB0025362).

### Community help

The "IU HPC and AI User Community" Slack is at
`https://iu-hpc-ai-users.slack.com` (KB0024086). It has channels for each
supercomputer, storage systems, and REALLMS. Staff are often there, but
response times are not guaranteed (KB0024086). Use a support queue for
anything that matters. Never use the IU passphrase as the Slack password
(KB0024086).

## Cost of consulting

Consulting from RADL and AVL is a no-charge baseline service. Work longer
than 20 hours needs a signed agreement between the researcher and UITS
(KB0023697). SecureMyResearch is offered at no fee (KB0025362).

## What to put in a request

The KB states content requirements only for sponsorship requests: the
person's IU username and a short justification (KB0022656). The SDA account
form asks for department, phone, and space needed now and at 6 and 12 months.
It also asks for file count, duration, average file size, and a project
description (KB0025574).

For other requests, include these. This list is house practice, not KB
policy:

- The system and hostname, such as `quartz.uits.iu.edu`.
- Your IU username and the RT Project or Slurm Account Name.
- The job ID, the exact command, and the full error text.
- The time it happened, with timezone.
- What you expected, and what you have already tried.
- For storage, the full path and the quota output.
- For PHI work, the IRB status and which systems hold the data.

Do not put PHI or other sensitive data in a request. Describe data by type,
count, or size. The KB already bars sensitive data in file names and paths
(KB0023985), so quoting a path is safe only if that rule was followed.

## Planned downtime

Check the date before reporting an outage:

- IU HPC systems have maintenance on the second Sunday of each month, 7am to
  7pm (KB0023985).
- The SDA is offline every Sunday, 7am to 10am (KB0024406).
- **External:** Jetstream2 GPU resources have maintenance on the first
  Tuesday of each month, 7am to 7pm Eastern. See the Jetstream2 policies page.

## Keep this file current

When a channel bounces or redirects, find the current one in KB0023697 and
fix this table. Note a team rename the same way as a system rename. Record
response times you observe, dated and marked as observed. Close an open item
only with a citation.

## Sources

All IU KB articles, read 2026-10-01. URL form:
`https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=<number>`.

- [KB0022478](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022478) Secure research data containing HIPAA-regulated PHI on high performance file systems at IU
- [KB0022486](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022486) Policies regarding UITS research systems
- [KB0022647](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022647) Get additional IU computing accounts
- [KB0022656](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022656) Computing accounts at IU
- [KB0023170](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023170) Research Desktop (RED) usage policies and interface features
- [KB0023298](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023298) Use Slurm to submit and manage jobs on IU's research computing systems
- [KB0023420](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023420) Get computing help for biomedical research
- [KB0023515](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023515) UITS Research Technologies systems and services for researchers working with data containing HIPAA-regulated PHI
- [KB0023697](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023697) Research computing support at IU
- [KB0023985](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023985) About Quartz at IU
- [KB0024086](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024086) About the IU HPC and AI User Community Slack
- [KB0024406](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024406) About the Scholarly Data Archive (SDA) at Indiana University
- [KB0024420](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024420) About Jetstream2
- [KB0024661](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024661) Research computing services at IU
- [KB0024722](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024722) About archived content in the IU Knowledge Base
- [KB0025214](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025214) Use Apptainer on Quartz or Big Red 200 at IU
- [KB0025362](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025362) About SecureMyResearch
- [KB0025574](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025574) Questions you'll need to answer when requesting research computing accounts
- [KB0025747](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025747) Types of sensitive institutional data appropriate for UITS Research Technologies services
- [KB0025948](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025948) Get started on IU research HPC and storage systems

External, read 2026-10-01:

- [Jetstream2 acceptable use policies](https://docs.jetstream-cloud.org/general/policies/)
