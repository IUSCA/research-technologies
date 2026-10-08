# Open items across the skills

This file collects every open item in `.agents/skills` as of 2026-10-03. An
open item is a question that neither the live system nor the IU Knowledge
Base (KB) answers. It is also used where KB articles contradict each other.

Use it for step 5 of the full review in `MAINTAINING.md`, "Work the open
items." Work the sections in order:

1. **Answerable from the KB.** Apply each fix to the named skill, and cite
   the article.
2. **Answerable by the system.** Run each read-only command on a cluster.
   Record the result as Observed, with the date, host, and command.
3. **Questions for the owning teams.** Send one ticket per team, with every
   question batched. Close an item only with the ticket number and the date
   of the reply.

As of 2026-10-03 the first two sections are empty. Every remaining item
needs an owning team.

Regenerate this file each quarter with `grep -rn -i "open item"
.agents/skills`. Delete an entry once its skill no longer carries the item.
Entries name skill sections rather than line numbers, which drift.

Every KB article named here was re-read on 2026-10-03. That includes
KB0023515 and KB0025747, which were republished on 2026-10-02. Neither
change settles an item below.

KB0024420 was republished on 2026-10-06 and re-read on 2026-10-07. It now
names NAIRR Pilot allocations as a route to Jetstream2. That settles the
Jetstream2 support question. It still describes Jetstream2 as a gateway
back end, so the HPS question on authentication stands.

### Settled on 2026-10-07

| Item | Settled by | Skill |
| --- | --- | --- |
| Whether ACCESS is the only route to a Jetstream2 allocation | KB0024420, version 2.0: ACCESS or NAIRR Pilot allocations | `jetstream2` |

### Settled on 2026-10-03

These are recorded in their skills and dropped from this file.

| Item | Settled by | Skill |
| --- | --- | --- |
| One Slurm Account Name per project, or per allocation | Observed: `sacctmgr` on both clusters, matched to RT Projects project IDs | `managing-rt-projects` |
| The Geode-Project Globus collection name | Observed: the IU Globus web app | `storing-and-moving-research-data` |
| Who can get Geode-Project access | KB0026680, KB0025090, KB0024359 | `managing-rt-projects`, `storing-and-moving-research-data` |
| Which account the RED Interactive Job icon charges | Observed: its launcher script on Quartz | `using-research-desktop` |
| The HPC LLM module name | Observed: `module spider hpc_llm` on Quartz | `using-reallms` |
| A command for a Slate-Project quota | Observed: `quota` on Quartz | `storing-and-moving-research-data` |
| Slate-Scratch quota units | Observed: `lfs quota -h` on Quartz | `storing-and-moving-research-data` |
| Whether compute nodes reach PyPI and conda-forge | Observed: `curl` in a Quartz `interactive` job | `managing-python-environments` |

## Summary

The skills carry 42 open-item mentions. They reduce to 35 distinct questions,
because several skills repeat the same question.

| Category | Questions |
| --- | --- |
| High Performance Systems (HPS) | 4 |
| Research Desktop (RED) team | 3 |
| Research Applications and Deep Learning (RADL) | 1 |
| RT Projects | 6 |
| REALLMS team | 5 |
| High Performance File Systems (HPFS) | 2 |
| Research Storage | 6 |
| Research Databases (ResDB) | 1 |
| SecureMyResearch | 5 |
| KB team | 2 |

## Questions for the owning teams

Each draft below is ready to send. Do not include PHI, usernames, or project
names. Add any system result from the section above that changes a
question.

### High Performance Systems (HPS)

Queue: `https://projects.rt.iu.edu/help/?queue=hps`

**Subject:** Documentation questions: automated job submission on Quartz and
Big Red 200

Hello HPS team,

We maintain open documentation that helps IU researchers and their tools use
research computing. The KB does not answer the questions below. Your answers
will be cited in the documentation with this ticket number.

1. May a service, such as a research portal, submit Slurm jobs as or on
   behalf of a researcher? If so, what arrangement is needed? From
   `iu-research-computing-map/SKILL.md`, "Submitting on behalf of a group."
   KB0022486 says a passphrase is for its owner only. KB0022656 bars group
   accounts from PHI.
2. May users run `scrontab` or `cron` entries on the login nodes? From
   `iu-research-computing-map/SKILL.md`. KB0022486 says unattended
   listening services are terminated, but it does not mention scheduled
   jobs.
3. Does a Slurm REST endpoint, such as `slurmrestd`, exist for IU clusters?
   From `iu-research-computing-map/SKILL.md`.
4. How should a service running on Jetstream2 authenticate to Quartz or Big
   Red 200 to submit jobs? From `jetstream2/SKILL.md`, "Gateways."
   KB0024420 describes Jetstream2 as a gateway back end, and KB0023985
   requires Duo or a signed SSH key agreement.

Thank you for your help.

### Research Desktop (RED) team

Queue: `https://projects.rt.iu.edu/help/?queue=red`

**Subject:** Documentation questions: RED parallelism, CPU-time limit, and
support queue

Hello RED team,

We maintain open documentation that helps IU researchers use Research
Desktop. The KB does not answer the questions below, or its articles
disagree. We would like to cite your answer.

1. What parallelism limit applies on RED nodes? From
   `using-research-desktop/SKILL.md` and `iu-research-computing-map/SKILL.md`.
   KB0023167 says to "limit the parallelism of programs run on the nodes to
   between 4 and 8 processors." KB0023170 says to "Limit the parallelism the
   applications use to 5 or fewer."
2. Which queue should RED users use? From `using-research-desktop/SKILL.md`
   and `getting-help-from-research-technologies/SKILL.md`. Most RED articles
   link to `?queue=red`. KB0023170, KB0023231, and KB0023162 link specific
   problems to `?queue=radl`, labeled as the RED development team.
3. Does the 20-minute CPU-time limit for login nodes apply on RED nodes? From
   `using-research-desktop/SKILL.md`. KB0023170 says "RED nodes are login
   nodes." KB0022436 says login-node processes "that run longer than 20
   minutes are terminated automatically." On a Quartz login node,
   `ulimit -t` reports `unlimited`, so we cannot tell from the shell.

Thank you for your help.

### Research Applications and Deep Learning (RADL)

Queue: `https://projects.rt.iu.edu/help/?queue=radl`

**Subject:** Documentation question: Anaconda channels on IU clusters

Hello RADL team,

We maintain open documentation that helps IU researchers set up Python
environments on Quartz and Big Red 200.

1. May IU research use Anaconda's `defaults` channel without a commercial
   license, or should researchers keep to `conda-forge`? From
   `managing-python-environments/SKILL.md`, "Anaconda licensing." KB0023231
   recommends the conda module over installing Anaconda or Miniconda. The
   module's own configuration uses only `conda-forge`.

Thank you for your help.

### RT Projects

Queue: `https://projects.rt.iu.edu/help/?queue=projects-incoming`

**Subject:** Documentation questions: RT Projects membership, archiving, and
PI changes

Hello RT Projects team,

We maintain open documentation that helps IU researchers run RT Projects.
The KB does not answer the questions below, or its articles disagree. Your
answers will be cited with this ticket number.

1. May an Academic Non-Paid (ACNP) appointee own Slate-Project space? From
   `managing-rt-projects/SKILL.md`,
   `requesting-accounts-and-allocations/SKILL.md`, and
   `storing-and-moving-research-data/SKILL.md`. KB0022423 says an owner
   "must be IU Faculty, Staff, or Academic Non-Paid (ACNP) and the Principal
   Investigator of a corresponding RT Project." KB0024132 says "The PI must
   be IU faculty or staff." KB0022586 limits requests to "individuals with
   faculty or staff status."
2. Which resources need the system account before a member is added to the
   allocation? Does this include Quartz and Big Red 200? From
   `managing-rt-projects/SKILL.md` and
   `requesting-accounts-and-allocations/SKILL.md`, which asks for the order
   of steps for compute allocations. KB0024132 says users
   "will not be able to be added to the allocation without an account on the
   system." KB0026672 lets Slate-Project members be added first, shown as
   "Eligible."
3. Does removing someone from a project also remove them from its
   allocations? From `managing-rt-projects/SKILL.md`.
4. Does RT Projects keep publication or grant records, as ColdFront can? From
   `managing-rt-projects/SKILL.md`. KB0024132 describes only "Project
   Updates."
5. What happens to Slate-Project and Geode-Project data when a project is
   archived? From `managing-rt-projects/SKILL.md`. KB0024132 says archiving
   "will immediately terminate access to any allocations."
6. How is an RT Project moved to a new PI? From
   `managing-rt-projects/SKILL.md`. KB0022423 and KB0023373 say a storage
   owner change needs a new service agreement.

Thank you for your help.

### REALLMS team

Queue: `https://projects.rt.iu.edu/help/?queue=racs`

**Subject:** Documentation questions: REALLMS eligibility, limits, and
supported model

Hello REALLMS team,

We maintain open documentation that helps IU researchers use REALLMS and
Posit Connect. The KB does not answer the questions below. Your answers will
be cited with this ticket number.

1. May sponsored affiliates use the REALLMS API or Posit Connect? From
   `managing-rt-projects/SKILL.md`. KB0027412 defines a REALLMS User only as
   "An IU-affiliated person."
2. May a student who is a member of a PI's RT Project get a REALLMS API
   key? From `using-reallms/SKILL.md`. KB0024132 requires a faculty or staff
   PI for the project.
3. Which model is currently labeled long-term supported? From
   `using-reallms/SKILL.md`. KB0027412 says the Service Provider "will label
   one general purpose model as a long-term supported model."
4. What are the API rate limits, and do API keys expire? From
   `using-reallms/SKILL.md`. KB0027272 says only that heavy usage "may
   result in your requests being rate-limited."
5. Where should questions about the HPC LLM platform go? From
   `using-reallms/SKILL.md`. KB0027473 and KB0026530 send them to the RADL
   queue. The REALLMS articles use `racs`.

Thank you for your help.

### High Performance File Systems (HPFS)

Queue: `https://projects.rt.iu.edu/help/?queue=hpfs`

**Subject:** Documentation questions: Slate-Project free limit units and
Slate sponsorship

Hello HPFS team,

We maintain open documentation that helps IU researchers plan storage. The
KB articles below disagree, and we would like to cite your answer.

1. Is the free Slate-Project limit 120 TB or 120 TiB? From
   `requesting-accounts-and-allocations/SKILL.md` and
   `storing-and-moving-research-data/SKILL.md`. KB0022439 says "Requests for
   up to 120 TB may be granted without fee." KB0022586 says "Slate-Project
   allows up to 120 TiB." KB0022423 defines it as "120 tebibytes (TiB)."
2. Do part-time employees need faculty sponsorship for a Slate account? From
   `requesting-accounts-and-allocations/SKILL.md`. KB0025016 marks Slate for
   part-time employees "Faculty sponsorship required." KB0022656 says all
   IU staff can request Slate directly.

Thank you for your help.

### Research Storage

Email: `store-admin@iu.edu`

**Subject:** Documentation questions: SDA file limits and eligibility,
Geode-Project fees and Globus collections, and HSI clients

Hello Research Storage team,

We maintain open documentation that helps IU researchers store and archive
data. These KB articles disagree, and we would like to cite your answer.

1. What is the file limit for a new SDA account? From
   `storing-and-moving-research-data/SKILL.md`. KB0022439 says "A maximum
   file limit of 25,000 files is enforced for new accounts." KB0024406,
   KB0025237, and KB0023604 say it "begins at 5,000 files but may be
   increased to 25,000 files upon request." Can a user see their own file
   limit from HSI?
2. Does Geode-Project carry a fee? From
   `storing-and-moving-research-data/SKILL.md`. KB0022439 sends Geode-Project
   to "Fee-based research storage." KB0023604 says "No fee (up to 10 TB)."
3. Which HSI and HTAR clients are offered for workstations? From
   `storing-and-moving-research-data/SKILL.md`. KB0022463 offers version 10.3
   for "64-bit Linux distributions only." KB0023281 offers bundles "for Red
   Hat Enterprise Linux 5 and 6, Ubuntu Linux, macOS, and Windows."
4. Is HSI and HTAR traffic to the SDA encrypted in transit? From
   `storing-and-moving-research-data/SKILL.md`. KB0022463 calls HSI a way of
   "securely transferring files." It still sends PHI to SFTP, SCP, or Globus.
5. Do part-time employees need faculty sponsorship for an SDA account? From
   `requesting-accounts-and-allocations/SKILL.md`. KB0025016 marks the SDA
   for part-time employees "Faculty sponsorship required." KB0022656 says
   staff can request the SDA directly.
6. Which Geode-Project spaces belong in the `IURT - Geode Projects Legacy`
   Globus collection, and when will they migrate? From
   `storing-and-moving-research-data/SKILL.md`. In the Globus web app,
   `IURT - Geode Projects` says it is "for all Geode Projects created since
   January 1st, or migrated," without a year. No KB article names the
   Legacy collection.

Thank you for your help.

### Research Databases (ResDB)

Email: `resdb@iu.edu`

**Subject:** Documentation question: ResDB account eligibility for staff

Hello ResDB team,

We maintain open documentation that helps IU researchers request accounts.

1. Do staff need faculty sponsorship for a ResDB account? From
   `requesting-accounts-and-allocations/SKILL.md`. KB0025016 marks ResDB for
   staff "Faculty sponsorship required." KB0022656 says graduate students,
   faculty, and staff can request ResDB directly.

Thank you for your help.

### SecureMyResearch

Email: `securemyresearch@iu.edu`

**Subject:** Documentation questions: data classification for RED, Big Red
200, Jetstream2, and REALLMS

Hello SecureMyResearch team,

We maintain open documentation that helps IU researchers choose systems for
sensitive data. The KB does not answer the questions below, or its articles
disagree. Your answers will be cited with this ticket number.

1. May PHI or Restricted data be used in Research Desktop (RED)? From
   `using-research-desktop/SKILL.md` and `iu-research-computing-map/SKILL.md`.
   KB0023515 and KB0025747 list Quartz but not RED. KB0023170 says RED runs
   on nodes that are part of Quartz.
2. What is the most sensitive non-PHI classification allowed on Big Red 200?
   From `iu-research-computing-map/SKILL.md`. KB0026317 says Big Red 200 "is
   not currently cleared" for PHI. KB0025747 does not list it.
3. Which classifications, if any, may IU researchers place on Jetstream2?
   From `iu-research-computing-map/SKILL.md`. Neither KB0023515 nor
   KB0025747 lists Jetstream2.
4. Does REALLMS exclude research data with contractual, regulatory, or legal
   constraints? From `using-reallms/SKILL.md`. KB0026507 approves REALLMS for
   Critical data and PHI "with the exception of research data with
   contractual, regulatory, or legal constraints." KB0026817, KB0027272, and
   KB0027412 state the approval without that exception.
5. Does a 1024-bit GPG key still meet IU standards? From
   `storing-and-moving-research-data/SKILL.md`. KB0023296 says "Enter 1024"
   at the keysize prompt, using GnuPG 2.0.14.

Thank you for your help.

### KB team

Email: `kb@iu.edu`

**Subject:** Documentation questions: archived articles and the support
overview

Hello KB team,

We maintain open documentation that cites the IU Knowledge Base for research
computing.

1. Can retirement dates for research systems be recovered from archived
   articles? From `iu-research-computing-map/references/retired-and-renamed.md`.
   KB0024722 says retired articles drop out of search.
2. Could the research computing support overview, KB0023697, list the `racs`
   and `projects-incoming` queues? From
   `getting-help-from-research-technologies/SKILL.md`. KB0026671, KB0027272,
   and KB0024132 name those queues, but KB0023697 does not.

Thank you for your help.
