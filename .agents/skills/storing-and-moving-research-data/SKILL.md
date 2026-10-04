---
name: storing-and-moving-research-data
description: Store, move, archive, and share research data on IU systems - home directories, Slate, Slate-Project, Slate-Scratch, Geode-Project, and the Scholarly Data Archive (SDA) via HSI, HTAR, SFTP, and Globus. Covers checking quotas and usage on the live system, purge and deletion rules, Lustre good practice, bundling many small files, the IU Globus web app and its collections, Globus guest collections for non-IU collaborators, ACLs, mounting Slate or Geode-Project on a workstation over SMB, and PHI encryption at rest and in transit. Use when deciding where IU research data should live, moving data between IU storage, a workstation, or the SDA, checking why a write failed or files vanished, archiving results, or sharing project data.
---

# Storing and moving research data at IU

Verified 2026-10-01 against the IU Knowledge Base (KB). Each claim names its
KB article; links are in Sources at the end.

Check data classification first. The `iu-research-computing-map` skill has
the approval table and the one-line summary of each system. This skill is the
how-to.

Detail lives in two reference files:

- [references/sda.md](references/sda.md): HSI, HTAR, SFTP, classes of
  service, and archiving many small files.
- [references/workstation-mounts.md](references/workstation-mounts.md): SMB
  mounts of Slate and Geode-Project.

## The live system is the judge

Quotas, paths, and mounts change. Check them on the system before acting on
any number in this file. When the system and this file disagree, believe the
system and update this file.

Run these on a Quartz or Big Red 200 login node:

| Question | Command | Source |
| --- | --- | --- |
| Home, Slate, and SDA usage and quotas | `quota`, after `module load quota` if needed | KB0024053, KB0022605 |
| Slate file count against the inode quota | `lfs quota -h -u $USER /N/slate` | KB0022605, KB0023425 |
| Slate-Scratch file count | `lfs quota -h -u $USER /N/scratch` | KB0025500 |
| Total data in a tree | `du -hc /N/slate/$USER` | KB0023425 |
| What fills the home directory | `cd ..` from home, then `du -h -d 2` and `du -d 2 --inodes` | KB0024053 |
| Interactive size browser | `module load ncdu`, then `ncdu` | KB0024053 |
| Oldest files, at risk of purge | `find . -type f -exec ls -1hltr "{}" +` | KB0025500 |
| Which project spaces you can see | `ls /N/project` | Not in the KB |
| Usage and limit for every space you can use | `quota` | Observed 2026-10-03 on Quartz |
| Mounted size and free space | `df -h /N/slate/$USER`, `df -h /N/project/<project>` | Not in the KB |
| SDA usage and file count | `hsi`, then `du -ka` | KB0026076 |

The KB gives no command for a Slate-Project quota. It offers only `ls -sh`
on one file (KB0022586). **Observed 2026-10-03** on Quartz: `quota`, from the
`quota` module loaded by default, lists home, SDA, Slate, and Slate-Scratch.
It also lists every Slate-Project you belong to, by group, with usage and
limit.

## Choose where data lives

Pick by lifetime and by who needs it. Then confirm the classification in the
`iu-research-computing-map` skill.

- **Scripts, configuration, source code, small inputs:** home directory. It
  has snapshots and monthly backup (KB0025028).
- **One person's working data that must persist:** Slate (KB0022605).
- **A group's working data on the clusters:** Slate-Project (KB0022586).
- **Job intermediates and output in flight:** Slate-Scratch. Move results off
  it quickly (KB0025317).
- **Shared files that need snapshots or campus desktop access:**
  Geode-Project (KB0024967).
- **Anything worth keeping long term:** the SDA (KB0022439, KB0024406).
- **Critical data other than PHI:** nowhere in Research Technologies
  (KB0024406, KB0022478).

Slate, Slate-Project, and Slate-Scratch have no backup of any kind
(KB0022605, KB0022586, KB0025500). Users must archive their own data
(KB0022391, KB0022423). The IU Data Storage Finder at
`https://datastoragefinder.iu.edu` compares options (KB0022439).

## Each space in practice

### Home directory

- Paths are `/N/u/<username>/Quartz` and `/N/u/<username>/BigRed200`
  (KB0025028).
- One 100 GB allocation is shared across all your supercomputer accounts
  (KB0025028, KB0024053).
- Over quota, running jobs keep running but cannot create or append files
  in home (KB0025028).
- Recover a file from `.snap/@GMT-<date>/` in the same directory. Thirty
  days of snapshots are kept (KB0026290, KB0025028).
- Backups skip `.cache`, `.mozilla`, Trash, and conda or anaconda files
  (KB0025028).
- A path, including the file name, may not exceed 4,096 bytes (KB0025028).
- Ask store-admin@iu.edu for more space (KB0025028).

### Slate

- Path: `/N/slate/<username>` (KB0022605).
- Default quota 800 GiB, raised to 1.6 TiB on request to HPFS. The inode
  limit is 6.4 million (KB0022605).
- A raised quota reverts if usage stays under 800 GiB for six months
  (KB0022605).
- Over quota, your transfers and jobs writing to Slate fail (KB0022605).
- No automated purge. Data is removed 180 days after your account is
  disabled (KB0022391).

### Slate-Scratch

- Path: `/N/scratch/<username>`, created with a supercomputer account
  (KB0025500).
- Limits: 100 TiB and 10 million files and directories (KB0025317).
  **Observed 2026-10-03** on Quartz: `lfs quota -h -u $USER /N/scratch` shows
  a `100T` limit, and `lfs -h` uses binary units. KB0022439's table, "Up to
  100 TB", lags.
- Files not accessed for 30 days are deleted without notice (KB0025317).
- Above 80% capacity, files are deleted oldest first until use falls below
  80% (KB0025317).
- Changing access times to dodge the purge costs you access to Slate-Scratch
  (KB0025317).
- Data is removed 30 days after your account is disabled (KB0025317).
- Copy results off in the job script itself. RADL can help add that step
  (KB0025317).

### Slate-Project

- Path: `/N/project/<project>` (KB0022586).
- Request, resize, and membership are in RT Projects. See the
  `requesting-accounts-and-allocations` skill.
- Members get full access by default, including deleting others' files
  (KB0022423).
- Keep the group ownership HPFS assigned on every file (KB0022423).
  **Observed 2026-10-02** on Quartz: each project's group is named
  `condo_<project>`, and `quota` reports project usage under that name.
- **Practice:** `mv`, `rsync -a`, and unpacking an archive keep each file's
  old group and drop the directory's setgid bit. The files then fall outside
  the project's group, and other members may be locked out. Copy in with
  `cp -r` or `rsync -rlt`, which take the directory's group.
- **Practice:** fix the group on files you own. Only a file's owner can, so
  each member fixes their own; the owner asks HPFS for a bulk reset.

  ```bash
  find <dir> -user $USER ! -group condo_<project> -exec chgrp -h condo_<project> {} +
  find <dir> -user $USER -type d -exec chmod g+rwxs {} +
  find <dir> -user $USER -type f -exec chmod g+rw {} +
  ```

- **Practice:** for data the whole project edits, set `umask 0007` in your
  shell profile so new files are group-writable. Not for PHI, which uses
  `umask 077` (KB0022478).
- ACLs can narrow or widen access per path. They do not show in RT Projects
  (KB0025963).
- Purge: research allocations 180 days after an incomplete annual review.
  Class allocations 30 days after expiry (KB0022423).
- A departed member's data is purged 180 days after they leave IU
  (KB0022423).
- To remove an allocation, delete its data first (KB0026672).

### Geode-Project

- Disk storage replicated at Bloomington and Indianapolis, with daily
  snapshots kept 30 days. It is not backed up (KB0023373).
- Recover files from `.snap` the same way as home (KB0026290).
- Access is through two ADS groups, Admins and Users, plus NFSv4 ACLs
  (KB0026680).
- Read and edit ACLs with `nfs4_getfacl` and `nfs4_setfacl`. **Observed
  2026-10-03** on Quartz: Geode-Project is an NFSv4.1 mount at
  `/geode3/projects`. `nfs4_getfacl` read a project directory's ACL, while
  `mmgetacl` failed with `Function not implemented`. KB0024359 still names
  `mmgetacl` and `mmeditacl`; treat it as lagging.
- Group access and ACL sharing differ. Anyone with an active IU account can join
  the allocation's Active Directory groups (KB0026680). They can mount the space
  without a supercomputer account (KB0025090). File-level NFSv4 ACL sharing
  reaches only IU research supercomputer users (KB0024359).
- **Practice:** do not `chmod` in Geode-Project. It rewrites the NFSv4 ACL
  and can drop the entries that grant group access. Change access with
  `nfs4_setfacl` instead.
- Every file must carry the project's group ID. Geode-Project quotas are
  per group (KB0023373).
- No automated purge. A user's data is removed 180 days after their account
  is disabled (KB0023373).
- Geode is down Sundays 7am to 10am and during monthly maintenance
  (KB0023373).

## Lustre good practice

Slate, Slate-Project, and Slate-Scratch are Lustre file systems
(KB0023425). Metadata and data live on different servers, which shapes
these rules:

- Avoid `ls -l` on large directories. It queries every storage server and
  can hang for everyone (KB0025500, KB0023425).
- Add `unalias ls` to your profile if `ls` is aliased to color output
  (KB0025500).
- Check one file with `ls my_file` or `ls -l my_file` (KB0025500).
- Bundle many small files with `tar` or `gzip`. They strain performance and
  the inode quota (KB0025500).
- Set striping with `lfs setstripe -c N` on a file or directory. The default
  is one stripe, and 16 should be the maximum (KB0023425).
- Striping does not change existing files. Inspect it with `lfs getstripe`
  (KB0023425).

## Move data

| From and to | Use | Source |
| --- | --- | --- |
| Between IU research systems, or to and from the SDA | IU Globus web app | KB0025535 |
| Workstation to Slate, Slate-Project, or Scratch | Globus with Globus Connect Personal, or an SMB mount | KB0025535, KB0025689 |
| Workstation to home directory | SFTP to the cluster hostname, with Duo | KB0025028 |
| Google at IU or OneDrive to cluster storage | Globus collections for each | KB0025535 |
| Cluster to SDA, scripted | HSI or HTAR. See [references/sda.md](references/sda.md). | KB0022463, KB0023281 |
| Off campus to the SDA | Globus or SFTP only | KB0024406 |

Inside the clusters, Slate spaces are ordinary mounted paths. Use normal
Linux copy commands (KB0025500).

### IU Globus web app

Log in at `https://globus.iu.edu` as Indiana University, with Duo
(KB0025535). You need an account on any IU system you use as a collection
(KB0025535).

| Storage | Collection | Path to enter | Source |
| --- | --- | --- | --- |
| SDA | `IURT - Scholarly Data Archive` | Opens in your SDA home | KB0025535 |
| Slate | `IURT - Slate` | `/slate/<username>` | KB0025535 |
| Slate-Project | `IURT - Slate` | `/project/<project>` | KB0025535 |
| Slate-Scratch | `IURT - Slate` | `/scratch/<username>` | KB0025535 |
| Home directory | `IURT - Geode Home Directories` | Opens at `/<username>` | KB0025535 |
| Geode-Project | `IURT - Geode Projects` | Opens at `/`; pick your project's folder | KB0025535; Observed 2026-10-03 |
| OneDrive and SharePoint | `IURT - OneDrive` | Follow the SharePoint site first | KB0025535 |

- `IURT - Slate` may say permission denied until you type the path
  (KB0025535).
- **Observed 2026-10-03** in the IU Globus web app: `IURT - Geode Projects`
  is a verified mapped collection on `IURT - RS DTN Endpoint`, owned by
  `iursdtn@iu.edu`. KB0026500's `IURT - Geode Project` lags. A banner says
  the collection is "for all Geode Projects created since January 1st, or
  migrated." Older projects "should continue using the IURT - Geode Projects
  Legacy collection." The KB does not mention the Legacy collection or the
  year meant. If your project folder is missing, try the Legacy collection.
- Encryption is always on for IU Globus transfers (KB0025535).
- Options include sync, delete at destination, preserve times, and skip
  errors. Integrity checking is on unless you disable it (KB0025535).
- Transfers can be scheduled and repeated (KB0025535).
- A personal computer becomes a collection with Globus Connect Personal.
  Name it like `<username>#my_laptop` (KB0025535).
- Geode collections are High Assurance and do not allow bookmarks
  (KB0025535).

## Share data

### With IU users

- **Slate, Slate-Scratch, or a PHI directory:** POSIX ACLs with `setfacl`.
  See the PHI section (KB0022478). The same steps work for other data: `x`
  on each parent, the ACL on the directory, a default ACL with `-d`, and a
  fresh `setfacl -R -m` after moving files in (KB0022478).
- **Practice:** if `getfacl` shows `#effective:---` beside a granted user,
  the ACL mask blocks it. Set the mask, as in `setfacl -m m::rx <path>`.
- **Never share by a hidden path.** Do not give "other" users `x` on a
  parent and send someone the name (**Practice**). It opens the path to every
  cluster account. Paths leak through job scripts, history, and `ps`. You
  cannot revoke one person. For PHI it also breaks "no access at all" for
  other users (KB0022478). Check with `getfacl` that no `other::` entry grants
  access.
- **Slate-Project:** add members in RT Projects with read-write or read-only
  access. Changes take up to an hour (KB0026672).
- **Geode-Project:** add usernames to the project's ADS groups, then refine
  with NFSv4 ACLs (KB0026680, KB0024359).

### With non-IU collaborators

Use a Globus guest collection (KB0026500).

- Only the project owner can request and manage external sharing
  (KB0026500).
- Slate-Project needs external sharing enabled by HPFS first. It is
  read-only (KB0026500).
- Geode-Project guest collections may grant write access (KB0026500).
- Collaborators need a Globus or federated login. Anonymous sharing is not
  allowed (KB0026500).
- Each permission lasts at most 30 days, then is removed automatically
  (KB0026500).

Steps, from KB0026500: in the Globus web app, open Collections and clear all
filters. Search `IURT`, pick the collection, and choose Add Guest
Collection. Browse to the directory and name it. On Permissions, choose Add
Permissions - Share With, then a user or Globus group and an expiration.

The owner answers for every person given PHI through a guest collection.
The owner is also responsible if re-sharing is enabled (KB0026500,
KB0022423).

For one-off files of Critical data, Secure Share at
`https://secureshare.iu.edu` deletes uploads after 30 days (KB0024193,
KB0023434).

## PHI in storage and transit

Read the map skill's PHI rules first. These are the storage steps.

1. Encrypt PHI files with GPG before they move to storage (KB0022478,
   KB0023296).
2. Move PHI with SFTP, SCP, or Globus (KB0022439). Even the HSI article
   points PHI there (KB0022463).
3. Keep PHI in a directory such as `/N/slate/<username>/protected`. Set it
   with `chmod 700` (KB0022478).
4. Consider `umask 077` in your shell profile (KB0022478).
5. Never grant group permissions on that directory (KB0022478).
6. Share with `setfacl -m u:<user>:rx` on each parent and on the directory
   (KB0022478).
7. Add a default ACL with `setfacl -d -m u:<user>:rx` (KB0022478).
8. Re-run `setfacl -R -m` after moving files in. Moved files do not inherit
   default ACLs (KB0022478).
9. Revoke with `setfacl -R -x` and `setfacl -R -d -x`. Never use
   `setfacl -b` (KB0022478).
10. Decrypt only the files a job needs. Delete plaintext copies afterward
    (KB0022478).

More PHI rules for storage and transfer:

- Share Geode-Project PHI only with individual accounts, never a group
  account (KB0024359).
- A file leaves a full-disk-encrypted laptop decrypted. Encrypt the file
  itself first (KB0022478).
- Keep sensitive data out of file names and paths (KB0022439).

## Open items

- **SDA file count.** KB0022439 says "A maximum file limit of 25,000 files
  is enforced for new accounts." KB0024406, KB0025237, and KB0023604 say new
  accounts "begin at 5,000 files but may be increased to 25,000." Check with
  `du -ka` in HSI.
- **Slate-Project free limit units.** KB0022439 says "Up to 120 TB."
  KB0022586 and KB0022423 say "120 TiB."
- **Slate-Project owner.** KB0022586 says faculty or staff. KB0022423 also
  allows Academic Non-Paid (ACNP).
- **Geode-Project fee.** KB0022439 lists it under fee-based storage.
  KB0023604 says "No fee (up to 10 TB)."
- **HSI and HTAR workstation clients.** KB0022463 offers version 10.3 for
  64-bit Linux only. KB0023281 offers bundles for RHEL 5 and 6, Ubuntu,
  macOS, and Windows by email.
- **HSI encryption.** The KB never says whether HSI or HTAR traffic is
  encrypted. It sends PHI to SFTP, SCP, or Globus instead (KB0022463).
- **GPG key size.** KB0023296 tells you to choose a 1024-bit key with GnuPG
  2.0.14. Ask SecureMyResearch whether that still meets IU standards.

## Keep this file current

Run the commands in the first section whenever you are on a cluster. Record
any limit that differs from this file, with the date and "observed." Re-read
KB0022439 and KB0025535 before changing the choice list or the Globus
table. Close an open item only with a citation that settles it.

## Sources

All IU KB articles, read 2026-10-01. URL form:
`https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=<number>`.

- [KB0022391](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022391) Slate high performance storage system: Terms of service
- [KB0022423](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022423) Slate-Project high performance storage system: Terms of service
- [KB0022439](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022439) Available access to allocated and short-term storage capacity on IU's research systems
- [KB0022463](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022463) Use HSI to access your SDA account at IU
- [KB0022478](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022478) Secure research data containing HIPAA-regulated PHI on high performance file systems at IU
- [KB0022483](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022483) Stage your SDA files to be available when you want them
- [KB0022499](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022499) Use SFTP or SCP to access your SDA account at IU
- [KB0022586](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022586) About Slate-Project high performance project space at IU
- [KB0022605](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022605) About Slate high performance storage for research computation at IU
- [KB0023281](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023281) Use HTAR with your SDA account
- [KB0023296](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023296) Use GPG to encrypt files on IU's research supercomputers
- [KB0023364](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023364) Enable HSI/HTAR transfers from IU's Scholarly Data Archive when your system is protected by a firewall
- [KB0023373](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023373) Geode-Project: Terms of service
- [KB0023425](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023425) Lustre file systems at IU
- [KB0023434](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023434) Recommended tools for encrypting data containing HIPAA-regulated PHI
- [KB0023604](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023604) About dedicated file storage services and IT services with storage components appropriate for sensitive institutional data, including research data containing protected health information
- [KB0023774](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023774) Use HSI to create and manage checksums
- [KB0024053](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024053) Check your home directory quota on the IU research supercomputers
- [KB0024193](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024193) About Secure Share
- [KB0024359](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024359) Share access to your Geode-Project space with other IU research supercomputer users
- [KB0024366](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024366) About accidentally deleted SDA files
- [KB0024368](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024368) Access the SDA at IU
- [KB0024387](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024387) Use keytabs to automate authentication of scripts accessing the IU SDA
- [KB0024406](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024406) About the Scholarly Data Archive (SDA) at Indiana University
- [KB0024967](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024967) Request a project space allocation on Geode-Project
- [KB0024976](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024976) Use classes of service on the Scholarly Data Archive at IU
- [KB0024997](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024997) If you can't connect to the SDA at IU
- [KB0025028](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025028) About home directory space on IU research supercomputers
- [KB0025030](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025030) If you're unable to move a file to the SDA using HSI
- [KB0025090](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025090) Map or mount a drive to your Geode-Project space
- [KB0025237](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025237) Best uses for an IU SDA account
- [KB0025317](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025317) Slate-Scratch high performance file system: Terms of service
- [KB0025500](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025500) About the Slate-Scratch high performance file system for research computation at IU
- [KB0025535](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025535) Use the IU Globus Web App to transfer data to and from your accounts on IU's research computing and storage systems
- [KB0025689](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025689) Map or mount a Slate file system on your personal workstation
- [KB0025838](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025838) Archive directories of many small files to the SDA
- [KB0025963](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025963) Use ACLs to provide additional access to Slate-Project files and directories
- [KB0026076](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0026076) Check storage space on your SDA account
- [KB0026290](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0026290) Recover deleted or corrupt files from your home directory or Geode-Project space on the IU research supercomputers
- [KB0026500](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0026500) Share Geode-Project or Slate-Project data with non-IU collaborators
- [KB0026672](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0026672) Manage your Slate-Project allocations within your RT Project
- [KB0026680](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0026680) Manage your Geode-Project allocation within your RT Project
