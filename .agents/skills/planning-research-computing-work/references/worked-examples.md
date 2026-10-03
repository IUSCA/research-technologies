# Worked examples

Verified 2026-10-03. Read the main `SKILL.md` first. These plans are
illustrative. Sizes and counts are invented, and every `<placeholder>` stands
for the person's own value. Confirm partitions, quotas, and paths on the live
system before using a plan.

## 1. GPU model training on a 5 TB dataset

**Facts.** University-internal images, no PHI. 5 TB in about 50,000 files.
Training needs one or two GPUs for about a day per run, a few dozen runs.
Batch only. Collaborators are all at IU.

**Decisions.**

- Compute: Quartz `h100-single`, or Big Red 200 `gpu`, since there is no
  PHI (KB0022436, KB0026317). Pick by which allocation the person holds.
- Input: 5 TB exceeds Slate's 1.6 TiB maximum, so use Slate-Project
  (KB0022605, KB0022586). Copy it in with Globus (KB0025535).
- Working: checkpoints and logs in `/N/scratch/<user>/<model>/<run>`.
  Copy the final checkpoint to Slate-Project in the job script (KB0025317).
- Archive: final weights and the training code version to the SDA. Use
  HSI for a weights file over 68 GB, since HTAR members stop there
  (KB0023281).
- Many-run sweeps use a job array, each task one configuration; see
  `submitting-hpc-jobs`.

**Gaps that often appear.** No Slate-Project space: the PI requests it; see
`requesting-accounts-and-allocations`. No GPU partition access on the chosen
account: check with `check-cluster.sh`.

## 2. Imaging pipeline with PHI

**Facts.** De-identification is not complete, so the images are PHI. 2 TB
in about 10,000 files. CPU preprocessing per subject, then one GPU step.
A researcher wants to view images in a GUI.

**Decisions.**

- Classification first: follow the PHI rules in `iu-research-computing-map`.
  IRB approval and individual logins are prerequisites (KB0023407,
  KB0022656). Consult SecureMyResearch before the first transfer
  (KB0025362).
- Compute: Quartz only, for both CPU and GPU steps (KB0023515, KB0026317).
- Storage: a protected directory on Slate or Slate-Project, set up with the
  PHI steps in `storing-and-moving-research-data` (KB0022478).
- Movement: GPG-encrypted files over Globus or SFTP, not HSI (KB0022463,
  KB0022478).
- GUI viewing: not on RED until SecureMyResearch answers the open item in
  `using-research-desktop`. Ask them which viewing route is approved.
- Archive: encrypted bundles to the SDA through Globus or SFTP
  (KB0023515, KB0022463).
- Paths: no subject identifiers in file or directory names (KB0023985).

**Gaps that often appear.** The RT Project description does not say PHI
will be stored (KB0024132). A group account was planned for automation;
that is not allowed for PHI (KB0022656).

## 3. Many-small-files genomics, archived to the SDA

**Facts.** Restricted data, no PHI. 800 samples, each producing about 5,000
small files. One CPU task per sample, a few hours each. Results kept five
years.

**Decisions.**

- Compute: a job array or PCP on Quartz, one task per sample (KB0023513).
  `describe-cluster.sh` shows the largest array allowed.
- File counts: 800 times 5,000 is 4 million files. That is most of
  Slate's 6.4 million inode limit (KB0022605). Write per-sample output to
  Slate-Scratch, whose limit is 10 million (KB0025317).
- Bundle each sample's output with `tar` at the end of its task. Lustre and
  the inode quota both suffer from many small files (KB0025500).
- Keep summary tables in Slate-Project for the group (KB0022586).
- Archive: HTAR one bundle per sample, or per batch of samples, so single
  samples can be pulled back (KB0025237, KB0023281). Add a README.
- Archive before the 30-day scratch purge, and verify counts first
  (KB0025317, KB0025237).
- Check the SDA file-count quota against the bundle count; the KB articles
  disagree on it, as `storing-and-moving-research-data` records.

**Gaps that often appear.** HSI cannot log in from a batch job without a
keytab; see `storing-and-moving-research-data`.

## Sources

All IU KB articles, read 2026-10-03. URL form:
`https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=<number>`.

- [KB0022436](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022436) Run GPU-accelerated jobs on Quartz or Big Red 200 at IU
- [KB0022463](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022463) Use HSI to access your SDA account at IU
- [KB0022478](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022478) Secure research data containing HIPAA-regulated PHI on high performance file systems at IU
- [KB0022586](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022586) About Slate-Project high performance project space at IU
- [KB0022605](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022605) About Slate high performance storage for research computation at IU
- [KB0022656](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022656) Computing accounts at IU
- [KB0023281](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023281) Use HTAR with your SDA account
- [KB0023407](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023407) Your legal responsibilities for protecting data containing PHI when using UITS Research Technologies systems and services
- [KB0023513](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023513) Use PCP to bundle multiple serial jobs to run in parallel on IU research supercomputers
- [KB0023515](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023515) UITS Research Technologies systems and services for researchers working with data containing HIPAA-regulated PHI
- [KB0023985](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023985) About Quartz at IU
- [KB0024132](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024132) Use RT Projects to request and manage access to specialized Research Technologies resources
- [KB0025237](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025237) Best uses for an IU SDA account
- [KB0025317](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025317) Slate-Scratch high performance file system: Terms of service
- [KB0025362](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025362) About SecureMyResearch
- [KB0025500](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025500) About the Slate-Scratch high performance file system for research computation at IU
- [KB0025535](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025535) Use the IU Globus Web App to transfer data to and from your accounts on IU's research computing and storage systems
- [KB0026317](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0026317) About Big Red 200 at IU
