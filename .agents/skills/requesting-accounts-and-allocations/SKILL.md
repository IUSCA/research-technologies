---
name: requesting-accounts-and-allocations
description: Get access to IU research computing - personal accounts on Quartz, Big Red 200, Slate, and the Scholarly Data Archive; RT Projects projects and their compute allocations and Slurm Account Names; Slate-Project and Geode-Project storage; group accounts; and Jetstream2 through ACCESS. Covers eligibility, PI and sponsor rules, what the forms ask (including PHI), renewal deadlines, and stated turnaround. Use when someone needs access to an IU research system, is adding lab members, or is planning storage for a project.
---

# Requesting accounts and allocations at IU

Verified 2026-10-01 against the IU Knowledge Base (KB). Each claim names its
KB article; links are in Sources at the end.

Access has two layers. A personal account lets you log in. An RT Projects
allocation lets you run jobs and holds project storage. You need both before a
job will run (KB0025948).

## Order of steps

1. Each person creates the system account at "Create More Accounts"
   (KB0022647). Wait for the confirmation email (KB0025948).
2. The PI creates an RT Project at `https://projects.rt.iu.edu` (KB0024132).
3. The PI requests allocations inside the project: compute, Slate-Project, or
   Geode-Project (KB0024132).
4. The PI adds members to the project, then to each allocation (KB0024132).
   The `managing-rt-projects` skill covers membership.
5. Members create any storage account the allocation needs, such as a
   Slate-Project account (KB0026672). Slate-Project lets a member be added
   first; they show as "Eligible" until the account exists (KB0026672).
6. Members submit jobs with the project's Slurm Account Name (KB0023298).

KB0024132 says a user must hold the system account before being added to an
allocation that needs it. KB0026672 allows the reverse order for
Slate-Project. **Open item:** confirm the order for compute allocations.

## Personal accounts

Request research system accounts at "Create More Accounts" (KB0022647).

| Account | Who can request it directly | Source |
| --- | --- | --- |
| Quartz | All IU students, faculty, staff, and sponsored affiliated researchers | KB0022656 |
| Slate | All IU students, faculty, staff, and sponsored affiliated researchers | KB0022656 |
| Big Red 200 | Graduate students, faculty, and staff | KB0022656, KB0026317 |
| ResDB | Graduate students, faculty, and staff | KB0022656 |
| SDA | Graduate students, faculty, and staff | KB0022656 |

Undergraduates and sponsored affiliates need a sponsor for Big Red 200, ResDB,
and the SDA. The sponsor emails the owning team with the person's IU username
and a short justification (KB0022656):

- Big Red 200: the High Performance Systems (HPS) team.
- ResDB: resdb@iu.edu.
- SDA: store-admin@iu.edu.

The research supercomputer form asks for citizenship and discipline. It asks
whether you will store PHI. It also asks you to send a yearly citation list to
researchtechnologies@iu.edu (KB0025574).

Slate-Scratch space and a 100 GB home directory come automatically with a
supercomputer account (KB0022439).

Accounts not logged into within 30 days of creation are disabled. Accounts
unused for six months are disabled (KB0022486).

## RT Projects

RT Projects is the portal for allocations on Quartz, Big Red 200,
Slate-Project, Posit Connect, Geode-Project, and the REALLMS API
(KB0024132, KB0025604). It runs on ColdFront (KB0025604).

### Who can be PI

The PI must be IU faculty or staff. The PI must log in to RT Projects once
before anyone can create a project naming them (KB0024132). Students may
request a project but need a faculty or staff PI (KB0024132).

A student without a faculty or staff sponsor can ask to join the "HPC for
Students" project. Search RT Projects for it; KB0025604 names its PI.

A PI gets one research project and one class project by default. Several
research efforts go into one project as multiple abstracts. Contact Research
Technologies if you need more projects (KB0024132).

### What the project form asks

The description should cover (KB0024132):

- The applications or workflows you intend to use.
- How you intend to use the system.
- **Whether PHI will be stored.**
- Your research area and department.
- Approximate class size, for class projects.

Project titles and PIs are searchable by anyone. Descriptions and allocation
requests are visible only to Research Technologies staff (KB0024132).

### Turnaround

RT Projects says you will hear about a new request within two business days
(KB0024132). The KB states no turnaround for system accounts.

### After the project exists

Roles, adding members and collaborators, the yearly June renewal, and
archiving are in the `managing-rt-projects` skill. Research projects renew
every year between June 1 and June 30 (KB0024132). Missing renewal
deactivates the project's Slurm accounts after July 31 (KB0024132).

## Project storage

### Slate-Project

Only faculty or staff who are already RT Project PIs may request Slate-Project
space (KB0022586). **Open item:** KB0022423 also allows Academic Non-Paid
(ACNP) appointees to own Slate-Project space. Request it from the project's "Request Resource
Allocation" page, under "Storages" (KB0026672).

- Initial requests are limited to 30 TiB (KB0022586).
- Up to 120 TiB is available without a fee (KB0022586).
- Larger allocations are a direct-bill service (KB0022439).
- Only the PI can change an existing allocation (KB0026672).
- Members get read-write or read-only access (KB0026672).
- Research allocations are purged 180 days after an incomplete annual review
  (KB0022423).
- A departed user's data is purged 180 days after they leave IU (KB0022423).

**Open item:** KB0022439 states the free limit as "120 TB". KB0022586 and
KB0022423 state it as "120 TiB".

### Geode-Project

Geode-Project needs a memo of understanding (MOU) with Research Technologies
(KB0024967, KB0022439). The steps are (KB0024967):

1. Request a Geode-Project allocation in RT Projects.
2. Consult a Research Storage administrator about use, quota, access, and
   permissions.
3. Create ADS security groups that your department manages.
4. Assign roles and set up subdirectories and permissions.

Capacity depends on the MOU (KB0022439). The KB lists Geode-Project under
fee-based storage.

### SDA

Request a personal SDA account at "Create More Accounts" (KB0022439). A group
account uses the SDA Group Account Request form (KB0022439). The default quota
is 50 TB. Increases come in 50 TB steps with a data management plan, up to
200 TB before a charge (KB0024406).

## Group accounts

A faculty or staff member can request a group account for a course, project,
or team (KB0022645). A group account can then request research system
accounts (KB0022647, KB0022656).

- The owner must be active faculty or staff. Hourly employees, ACNP employees,
  and affiliates cannot own one (KB0022645).
- The account is disabled if the owner leaves or becomes ineligible
  (KB0022656).
- Do not share group access with people who lack an official IU affiliation
  (KB0022645).
- **A group account may not be used for PHI** (KB0022656, KB0022645).

## Jetstream2

Jetstream2 is not in RT Projects. It needs an ACCESS allocation
(KB0024420). See the `jetstream2` skill.

## PHI prerequisites

Before any request for PHI work, the PI needs IRB approval (KB0023407). Each
person needs annual HIPAA training (KB0023407). Say "PHI will be stored" in the
RT Project description (KB0024132). Choose only systems on the PHI list; see
the `iu-research-computing-map` skill.

## Keep this file current

Re-read KB0024132 every spring, before the June renewal window. RT Projects
adds resources over time, so check its resource list. Record actual
turnaround you observe, dated and marked as observed. Remove an open item only
with a citation that settles it.

## Sources

All IU KB articles, read 2026-10-01. URL form:
`https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=<number>`.

- [KB0022423](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022423) Slate-Project high performance storage system: Terms of service
- [KB0022439](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022439) Available access to allocated and short-term storage capacity on IU's research systems
- [KB0022486](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022486) Policies regarding UITS research systems
- [KB0022586](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022586) About Slate-Project high performance project space at IU
- [KB0022645](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022645) About group and departmental accounts
- [KB0022647](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022647) Get additional IU computing accounts
- [KB0022656](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022656) Computing accounts at IU
- [KB0023298](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023298) Use Slurm to submit and manage jobs on IU's research computing systems
- [KB0023407](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023407) Your legal responsibilities for protecting data containing PHI when using UITS Research Technologies systems and services
- [KB0024132](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024132) Use RT Projects to request and manage access to specialized Research Technologies resources
- [KB0024406](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024406) About the Scholarly Data Archive (SDA) at Indiana University
- [KB0024420](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024420) About Jetstream2
- [KB0024967](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024967) Request a project space allocation on Geode-Project
- [KB0025574](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025574) Questions you'll need to answer when requesting research computing accounts
- [KB0025604](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025604) About RT Projects at IU
- [KB0025948](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025948) Get started on IU research HPC and storage systems
- [KB0026317](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0026317) About Big Red 200 at IU
- [KB0026672](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0026672) Manage your Slate-Project allocations within your RT Project
