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

Regenerate this file each quarter with `grep -rn -i "open item"
.agents/skills`. Delete an entry once its skill no longer carries the item.

Every KB article named here was re-read on 2026-10-03. That includes
KB0023515 and KB0025747, which were republished on 2026-10-02. Neither
change settles an item below.

## Summary

The skills carry 47 open-item mentions. They reduce to 38 distinct questions,
because several skills repeat the same question.

| Category | Questions |
| --- | --- |
| Answerable from the KB | 1 |
| Answerable by the system | 7 |
| High Performance Systems (HPS) | 4 |
| Research Desktop (RED) team | 2 |
| RT Projects | 6 |
| REALLMS team | 5 |
| High Performance File Systems (HPFS) | 1 |
| Research Storage | 4 |
| SecureMyResearch | 5 |
| IU Jetstream2 support | 1 |
| KB team | 2 |

## Answerable from the KB

### K1. Who can get Geode-Project access

Skills: `managing-rt-projects/SKILL.md` line 260 and
`storing-and-moving-research-data/SKILL.md` line 318.

The three articles describe two different layers of access. They do not
conflict.

- KB0026680: "Anyone with an active IU account can be given access to the
  Geode-Project allocation's storage space. The RT Project's PI does this by
  adding usernames to either of the Active Directory security groups."
- KB0026680 continues: "Granular file storage access is also managed by the
  project's PI via NFSv4 ACLs [KB0024359] within the Geode-Project."
- KB0025090: "An IU research supercomputer account is not required for
  simple access to an existing Geode-Project space."
- KB0024359 covers only the ACL layer. "You can share access to your
  Geode-Project space data only with other IU research supercomputer users."

**Fix.** Replace each open item with a statement of the two layers. Suggested
text:

> Group access and ACL sharing differ. Anyone with an active IU account can
> join the allocation's Active Directory groups (KB0026680). They can mount
> the space without a supercomputer account (KB0025090). File-level NFSv4 ACL
> sharing reaches only IU research supercomputer users (KB0024359).

## Answerable by the system

Each check needs a person to log in once with their passphrase and Duo. See
`checking-iu-research-access`. Use placeholders such as `<project>` and
`<group>` when recording results in a skill.

### Y1. One Slurm Account Name per project, or one per allocation

Skill: `managing-rt-projects/SKILL.md` line 125. KB0024132 says RT Projects
assigns "each project a Slurm Account Name." KB0023298 says "your
allocation's Slurm Account Name."

Use an account in a project with both a Quartz and a Big Red 200 allocation.
Run on each cluster, then compare with each allocation's "Allocation
Attributes" in RT Projects:

```bash
sacctmgr -n show assoc user=$USER format=Cluster%15,Account%30
```

Matching names settle it as one per project. If the person has only one
compute allocation, ask RT Projects instead.

### Y2. Which account the RED Interactive Job icon charges

Skill: `using-research-desktop/SKILL.md` line 91. The KB does not say which
Slurm account the icon uses, or whether it works without an allocation.

In a RED session, find the launcher and read the command it runs:

```bash
grep -ril "interactive" ~/Desktop /usr/share/applications /etc/xdg 2>/dev/null
grep -i "^Exec" <launcher-file>
```

Read the script that `Exec` names. Look for `-A`, `--account`, or a lookup
of the user's associations.

### Y3. Whether the 20-minute CPU limit applies on RED

Skill: `using-research-desktop/SKILL.md` line 62. KB0023170 says "RED nodes
are login nodes." KB0022436 says login-node processes "that run longer than
20 minutes are terminated automatically."

Compare a RED node with a Quartz login node:

```bash
ulimit -t
grep -ris cpu /etc/security/limits.conf /etc/security/limits.d/
```

If neither host shows a limit, a monitoring daemon may enforce it. Then ask
the RED team, and add it to their ticket below.

### Y4. The HPC LLM module name

Skill: `using-reallms/SKILL.md` line 163. KB0027473 writes `hpc_llm/gpu/`
and `hpc-llm/gpu`. KB0026530 writes `hpc_llm/gpu`.

```bash
module spider hpc_llm
module spider hpc-llm
```

Run on Quartz and Big Red 200. Record the name that resolves.

### Y5. A command for a Slate-Project quota

Skill: `storing-and-moving-research-data/SKILL.md` line 43 and its last open
item. The KB offers only `ls -sh` on one file (KB0022586).

```bash
df -h /N/project/<project>
ls -ld /N/project/<project>                  # shows the owning group
lfs quota -h -g <group> /N/project
lfs project -d /N/project/<project>          # shows a project ID, if set
lfs quota -h -p <project-id> /N/project
```

Record whichever command reports the allocation's limit.

### Y6. Slate-Scratch quota units

Skill: `storing-and-moving-research-data/SKILL.md`, "Slate-Scratch units."
KB0022439's table says "Up to 100 TB." Its text and KB0025317 say "100 TiB."

```bash
lfs quota -h -u $USER /N/scratch
```

`lfs -h` prints binary units, so a `100T` limit is 100 TiB. Record it as
Observed, and note KB0022439's table as lagging.

### Y7. The Geode-Project Globus collection name

Skill: `storing-and-moving-research-data/SKILL.md`, "Geode-Project
collection name." KB0025535 says `IURT - Geode Projects`. KB0026500 says
`IURT - Geode Project`.

Search for `IURT - Geode` in the IU Globus web app, or with the Globus CLI:

```bash
globus endpoint search "IURT - Geode"
```

Record the exact display name, and note the other article as lagging.

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

**Subject:** Documentation questions: RED parallelism limit and support
queue

Hello RED team,

We maintain open documentation that helps IU researchers use Research
Desktop. Two KB points conflict, and we would like to cite your answer.

1. What parallelism limit applies on RED nodes? From
   `using-research-desktop/SKILL.md` and `iu-research-computing-map/SKILL.md`.
   KB0023167 says to "limit the parallelism of programs run on the nodes to
   between 4 and 8 processors." KB0023170 says to "Limit the parallelism the
   applications use to 5 or fewer."
2. Which queue should RED users use? From `using-research-desktop/SKILL.md`
   and `getting-help-from-research-technologies/SKILL.md`. Most RED articles
   link to `?queue=red`. KB0023170, KB0023231, and KB0023162 link specific
   problems to `?queue=radl`, labeled as the RED development team.

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
   `requesting-accounts-and-allocations/SKILL.md`. KB0024132 says users
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

**Subject:** Documentation question: Slate-Project free limit units

Hello HPFS team,

We maintain open documentation that helps IU researchers plan storage. Two
KB articles state the free Slate-Project limit in different units.

1. Is the free Slate-Project limit 120 TB or 120 TiB? From
   `requesting-accounts-and-allocations/SKILL.md` and
   `storing-and-moving-research-data/SKILL.md`. KB0022439 says "Requests for
   up to 120 TB may be granted without fee." KB0022586 says "Slate-Project
   allows up to 120 TiB." KB0022423 defines it as "120 tebibytes (TiB)."

Thank you for your help.

### Research Storage

Email: `store-admin@iu.edu`

**Subject:** Documentation questions: SDA file limits, Geode-Project fees,
and HSI clients

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

### IU Jetstream2 support

Contact: `https://jetstream-cloud.org/contact/index.html`

**Subject:** Documentation question: routes to a Jetstream2 allocation

Hello Jetstream2 support,

We maintain open documentation that helps IU researchers plan Jetstream2
use.

1. Is ACCESS the only route to a Jetstream2 allocation for IU researchers?
   From `jetstream2/SKILL.md`. KB0024420 says "Access to Jetstream2 is
   available only through" ACCESS allocations. The Jetstream2 documentation
   also describes allocations through NAIRR.

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
