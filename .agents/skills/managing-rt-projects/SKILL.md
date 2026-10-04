---
name: managing-rt-projects
description: Run an IU RT Projects (projects.rt.iu.edu, ColdFront) project day to day as a PI, Manager, or member. Covers creating a project, requesting Quartz, Big Red 200, Slate-Project, Geode-Project, Posit Connect, and REALLMS API allocations, adding and removing members and allocation members, Manager and User roles, non-IU collaborators through sponsored affiliate accounts and Globus sharing, finding and checking the Slurm Account Name, the June renewal and annual review, research updates and citations, quota changes, archiving, and what breaks when a step is missed. Use when a lab member cannot run jobs or reach project storage, when onboarding or offboarding people, before the renewal window, or when changing or retiring an allocation.
---

# Managing an RT Project

Verified 2026-10-03 (KB0024668, KB0025016, and KB0025574 only) against the IU
Knowledge Base (KB). Other sources were verified 2026-10-01. Each claim
names its KB article; links are in Sources at the end.

An RT Project owns allocations, members, and renewal. RT Projects runs on
ColdFront (KB0025604). For first-time accounts, see the
`requesting-accounts-and-allocations` skill.

## Check the live system before trusting this file

The portal and the clusters are the authority on current state. Check with
these before acting on anything below:

- Slurm accounts: on a login node, check with
  `sacctmgr show assoc user=$USER format=Account%30,Partition,QOS%40`.
  This is standard Slurm, not a KB instruction.
- A whole person's access: check with the `checking-iu-research-access`
  skill's scripts.
- Slate-Project usage: check with `quota` (KB0022586).
- A REALLMS key: check with a GET of `/models` (KB0027272); see the
  `using-reallms` skill.
- Members, allocation statuses, and renewal status: check the project's page
  in RT Projects.

Record command output here only as observed, with the date.

## Resources RT Projects allocates

RT Projects lists six resources, and more will be phased in (KB0024132,
KB0025604, KB0025948):

| Resource | Kind | Detail |
| --- | --- | --- |
| Quartz | Compute | Members need a Quartz account (KB0024132, KB0025948) |
| Big Red 200 | Compute | Members need a Big Red 200 account (KB0024132, KB0025948) |
| Slate-Project | Storage | Several per project allowed (KB0026672) |
| Geode-Project | Storage | One per PI per project; needs an MOU (KB0026680, KB0024967) |
| Posit Connect | Service | Requested as a project allocation (KB0025370) |
| REALLMS API | Service | Each member makes a personal API key (KB0027272) |

Check the "Request New Allocation" page for the current list.

## Roles

The PI owns the project and all its allocations (KB0024132). The PI controls
access to compute and storage for everyone in the project (KB0024132).

- **Manager.** The requester and PI get it. Managers change membership,
  request allocations, and help renew (KB0024132).
- **User.** The default for new members. Use the "Role" drop-down to promote
  one to Manager (KB0024132).
- **PI only.** Only the PI can change an existing Slate-Project or
  Geode-Project allocation (KB0026672, KB0026680).
- **Owner only.** Only storage owners can request external Globus sharing
  (KB0026500).

The PI must be IU faculty or staff (KB0024132). A PI has one research and one
class project by default (KB0024132). Put several research efforts in one
project as multiple abstracts (KB0024132). Ask for more projects through the
`projects-incoming` help queue (KB0024132).

**Open item:** KB0022423 allows ACNP Slate-Project owners. KB0024132 says the
PI "must be IU faculty or staff".

## Create a project

The PI must log in once first (KB0024132). Then select Add a Project, and give a title,
description, PI username, and type (KB0024132). Add members by IU username,
or skip and add them later (KB0024132). Make one Class project per class
(KB0024132). The `requesting-accounts-and-allocations` skill lists what the
description must cover.

## Request an allocation

Select Request Resource Allocation, pick the resource, and answer its
questions (KB0024132). The page notes any system account it depends on
(KB0024132). You are added by default; add other members in the "Users"
field (KB0024132). Expect a reply within two business days (KB0024132).

For Quartz and Big Red 200, members need an account on that system before
they can be added (KB0024132).

### Slate-Project

Request it under "Storages" at the bottom of the resource list (KB0026672).
The project owner owns the allocation (KB0026672). It mounts at
`/N/project/<project_name>`, with initial requests up to 30 TiB (KB0022586).

### Geode-Project

Request it under "Storages" too. The form asks for a secondary contact and
two Active Directory security groups, Admins and Users (KB0026680). The
groups are fixed at creation; only their membership changes (KB0026680).
Your department manages them (KB0024967). An MOU and a Research Storage
consultation follow (KB0024967).

### Posit Connect

It serves R and Python apps at `connect.posit.iu.edu` (KB0025370). Apps are
limited to 100 MB, nothing is backed up, and Critical or Restricted data is
not allowed (KB0025370).

### REALLMS API

After approval, create an API key on the allocation's page (KB0027272).
Keys are personal, so add each teammate to the allocation to make their own
(KB0027272). The beta service is approved for Critical data and PHI
(KB0027272).

## Find the Slurm Account Name

Look on the RT Projects Home page under "Submitting Slurm Jobs with your
Project's Account" (KB0023298). Or open the allocation and read "Allocation
Attributes" (KB0023298). Pass it to every job with `-A` (KB0023298).

Then check with the `sacctmgr show assoc` command above that Slurm lists
you on that account. Ask HPS if it does not; the KB states no sync delay.

KB0024132 says RT Projects assigns "each project a Slurm Account Name".
KB0023298 calls it "your allocation's Slurm Account Name". **Observed
2026-10-03** with `sacctmgr show assoc` on Quartz and Big Red 200, compared
with the RT Projects project list: the name is `r` plus the project ID,
padded to five digits. Project 1234 is `r01234`. Its Quartz and Big Red 200
allocations share that one name.

## Add and remove members

Membership has two levels. A person joins the project first, then each
allocation (KB0024132, KB0026672).

- **Add.** On the project page, select Add Users under "Users" (KB0024132).
  The same page adds them to allocations (KB0024132).
- **Remove.** Select Remove Users under "Users" (KB0024132). That page also
  removes people from allocations (KB0024132).
- **Join request.** A person finds the project by PI search and selects
  Request Access; the PI gets an email (KB0024132).
- **Slate-Project access.** Add project members from the allocation's
  "Detail" screen, as read-write or read-only (KB0026672). Non-members do
  not appear in the list (KB0026672).
- **Geode-Project access.** The PI adds usernames to the Admins or Users
  group (KB0026680). Finer access uses NFSv4 ACLs (KB0026680, KB0024359).

Changes made on the RT Projects site can take up to an hour (KB0026672).
Members must log out and back in to pick up Slate-Project access
(KB0026672).

A Slate-Project detail page shows Active, Eligible, Disabled, or Retired (KB0026672).
"Eligible" means the person must still create a Slate-Project account.
"Retired" means they are inactive and likely should be removed (KB0026672).

**Open item:** KB0024132 says users need a system account before being added
to an allocation. KB0026672 lets members be added first and shown as
"Eligible". The KB does not list which resources need the account first.

**Open item:** The KB does not say whether removing someone from a project
also removes them from its allocations.

## Non-IU collaborators

A non-IU person needs an IU account before joining a project. RT Projects
adds members only by IU username (KB0024132).

### Sponsor an affiliate account

A full-time IU faculty or staff member sponsors the account (KB0023488).
Request it at "Manage your affiliates" in One.IU (KB0023488). The sponsor
gets a reply within two business days (KB0023488).

- Have name, birth date, external email, campus, department, dates, and
  reason ready (KB0023488).
- Access starts on the start date and lasts up to one year (KB0023488).
- Renew it annually at the same page (KB0023488).
- Sign a written affiliation agreement first (KB0023488).

Do not use an affiliate account for someone about to join IU (KB0023488).
IU Health collaborators of School of Medicine researchers go through HTS at
hts@iu.edu instead (KB0024639).

Affiliates can then request Quartz and Slate accounts themselves (KB0022656,
KB0025016). Big Red 200 and the SDA need the sponsor to email the owning
team (KB0022656). Then add the affiliate's username to the project and
allocation.

**Open item:** No KB article read says whether affiliates may use Posit
Connect or the REALLMS API. KB0027412 says only "IU-affiliated person".

### Share data without an account

Storage owners can share through Globus guest collections, to named Globus
users only (KB0026500). Shares last at most 30 days (KB0026500). The
`storing-and-moving-research-data` skill has the steps.

## Renewal and annual review

Research projects renew every year (KB0024132). The window opens June 1, and
projects expire June 30 (KB0024132). The requester and PI get an email 30
days before expiry (KB0024132).

Select "Needs Review - click to review" on the project (KB0024132). Confirm
the description, verify active users, and pick allocations to renew
(KB0024132). Fill in "Project Updates", acknowledge, and submit (KB0024132).

Reviews take up to two business days (KB0024132). Allocations expire with
their project (KB0024132). Geode-Project and Slate-Project storage also need
the annual review (KB0026680, KB0022423). Class projects expire at semester
end and cannot be renewed (KB0024132).

### Reporting research output

"Project Updates" records research progress that RT resources made possible
(KB0024132). Supercomputer account holders also agree to email a yearly
citation list to researchtechnologies@iu.edu (KB0025574). Papers should include
the acknowledgment text in KB0024668.

**Open item:** The KB does not describe ColdFront publication or grant
records in RT Projects.

## Change quotas, remove storage, and archive

- **Change a quota.** Select the allocation's folder icon, then request a
  change (KB0026672, KB0026680). You cannot shrink below current usage
  (KB0026672).
- **Geode-Project increases.** Show a demonstrated need (KB0026680).
- **Remove Slate-Project storage.** Delete all its data first, then select
  Removal (KB0026672).
- **Archive a project.** On the "Detail" page, select Archive project
  (KB0024132).

Archiving ends access to every allocation at once and cannot be undone
(KB0024132). Archived projects get no renewal email and leave the project
limit (KB0024132).

**Open item:** The KB does not say what archiving does to storage data.

## What breaks when a step is missed

| Missed step | Result | Source |
| --- | --- | --- |
| PI never logged in | The project cannot be created | KB0024132 |
| Member lacks the system account | Cannot be added to that allocation | KB0024132 |
| Member in project, not allocation | Jobs will not run | KB0025948 |
| No Slate-Project account | Status stays "Eligible"; no access | KB0026672 |
| No logout after a change | Open terminals lack the new access | KB0026672 |
| Renewal missed past July 31 | Slurm accounts deactivated; new project needed | KB0024132 |
| Slate-Project review incomplete | Allocation purged after 180 days | KB0022423 |
| Class project ends | Slurm accounts deactivated; Slate-Project data purged in 30 days | KB0024132, KB0022423 |
| Member leaves IU | Slate-Project data purged 180 days after separation | KB0022423 |
| Member account disabled | Geode-Project data removed after 180 days | KB0023373 |
| Geode PI leaves, no successor | Access stops until an owner is named | KB0023373 |
| Wrong group on Geode files | Group changed by admins; owner notified | KB0023373 |
| Affiliate not renewed | Account ends within one year | KB0023488 |
| REALLMS key shared | Keys are personal; each member makes one | KB0027272 |

**Open item:** The KB does not say how to move an RT Project to a new PI. A
storage owner change needs a new service agreement (KB0022423, KB0023373).

**Geode-Project access.** Group access and ACL sharing differ. Anyone with an active IU account can join
the allocation's Active Directory groups (KB0026680). They can mount the space
without a supercomputer account (KB0025090). File-level NFSv4 ACL sharing
reaches only IU research supercomputer users (KB0024359).

## Where to ask

Use queue `projects-incoming` for RT Projects itself (KB0024132). Use `racs`
for Posit Connect and REALLMS (KB0025370, KB0027272). Use `hpfs` for
Slate-Project (KB0026500). Queue URLs take the form
`https://projects.rt.iu.edu/help/?queue=<name>`. Email store-admin@iu.edu
for Geode-Project (KB0026500).

## Keep this file current

Re-read KB0024132 every May, before the June renewal window. Compare the
resource table with the "Request New Allocation" page. Close an open item
only with a citation that settles it.

## Sources

All IU KB articles, read 2026-10-01. KB0024668, KB0025016, and KB0025574 re-read
2026-10-03. URL form:
`https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=<number>`.

- [KB0022423](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022423) Slate-Project high performance storage system: Terms of service
- [KB0022586](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022586) About Slate-Project high performance project space at IU
- [KB0022656](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022656) Computing accounts at IU
- [KB0023298](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023298) Use Slurm to submit and manage jobs on IU's research computing systems
- [KB0023373](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023373) Geode-Project: Terms of service
- [KB0023488](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023488) Sponsor a computing account for an IU affiliate
- [KB0024132](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024132) Use RT Projects to request and manage access to specialized Research Technologies resources
- [KB0024359](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024359) Share access to your Geode-Project space with other IU research supercomputer users
- [KB0024639](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024639) Eligibility for IU computing accounts at the School of Medicine
- [KB0024668](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024668) Sources of funding to acknowledge in published work if you use IU's research cyberinfrastructure
- [KB0024967](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024967) Request a project space allocation on Geode-Project
- [KB0025016](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025016) IU account types and eligibility
- [KB0025090](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025090) Map or mount a drive to your Geode-Project space
- [KB0025370](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025370) About Posit Connect at IU
- [KB0025574](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025574) Questions you'll need to answer when requesting research computing accounts
- [KB0025604](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025604) About RT Projects at IU
- [KB0025948](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025948) Get started on IU research HPC and storage systems
- [KB0026500](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0026500) Share Geode-Project or Slate-Project data with non-IU collaborators
- [KB0026672](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0026672) Manage your Slate-Project allocations within your RT Project
- [KB0026680](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0026680) Manage your Geode-Project allocation within your RT Project
- [KB0027272](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0027272) About the Research and Academic LLM Services (REALLMS) API at IU
- [KB0027412](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0027412) Research and Academic LLM Services (REALLMS): Terms of service
