# Plan template

Verified 2026-10-03. Read the main `SKILL.md` first. Copy this template, fill
every field, and write "unknown" rather than guess. Each choice names the
skill or KB article behind it.

Save the filled plan with the person's project, not in a shared skill.

```markdown
# Computing plan: <workflow name>

Date: <YYYY-MM-DD>. Re-check access and quotas if this plan is older than a quarter.

## Facts

| Question | Answer |
| --- | --- |
| Classification, PHI or not | <Public / University-internal / Restricted / PHI> |
| IRB approval (PHI only) | <yes, protocol on file / not yet / n.a.> |
| Data size now, at end; file count | <e.g. 5 TB, 12 TB; 40,000 files> |
| Compute shape | <CPU or GPU; memory per task; hours per task; task count> |
| Interactivity | <batch / notebook / GUI / service> |
| Collaborators | <IU only / non-IU: names not recorded here> |
| Retention | <inputs: ...; intermediates: ...; results: ...> |
| LLM use | <none / REALLMS API / HPC LLM platform> |
| RT Project and allocations | <from the resources file, or "none yet"> |

## Stages

| Stage | System | Path pattern | Moves in by | Leaves by |
| --- | --- | --- | --- | --- |
| Input | <e.g. Slate-Project> | `/N/project/<project>/<workflow>/input` | <Globus> | stays |
| Working | Slate-Scratch | `/N/scratch/<user>/<workflow>/<run>` | job copies in | job copies results out |
| Intermediate | <Slate-Scratch or Slate-Project> | `...` | job | <deleted / kept> |
| Results | <Slate-Project> | `/N/project/<project>/<workflow>/results` | job script | archive step |
| Archive | SDA | `<workflow>/<YYYY-MM>/<bundle>.tar` | <HTAR / HSI / Globus> | kept |
| Code and environment | Home | `~/<workflow>` | git | n.a. |

## Compute

- System and partition: <e.g. Quartz, `h100-single`>, confirmed with `describe-cluster.sh` on <date>.
- Slurm account (`-A`): <account>, because <its RT Project covers this work>.
- Job pattern: <single job / job array of N / PCP / interactive>.
- Working directory: `--chdir` under Slate-Scratch, never home.

## Data movement

1. <Source> to <destination> with <tool>.
2. Results off Slate-Scratch inside the job script.

## Archive

- What: <results, inputs that cannot be re-fetched, the code version>.
- How: <HTAR bundles split by retrieval unit; HSI for single files over 68 GB>.
- Verify: <file counts and sizes, or HSI checksums> before deleting the source.
- README in the archive: dates, origin, method, people, and grant numbers.

## Gaps

| Gap | Fix | Skill |
| --- | --- | --- |
| <e.g. no Slate-Project space> | <PI requests it in RT Projects> | `requesting-accounts-and-allocations` |

## Checks before the first job

- [ ] `check-local.sh` on the workstation
- [ ] `check-cluster.sh` on each cluster
- [ ] `describe-cluster.sh` on each cluster
- [ ] `quota` for each storage space
- [ ] One small test job, with its working directory checked by `squeue -o "%Z"`
```

Notes on filling it in:

- Path patterns come from `storing-and-moving-research-data`. Confirm each
  on the system before writing it.
- The HTAR 68 GB member limit is in KB0023281. Files above it go to the SDA
  with HSI or Globus instead.
- A PHI plan follows the PHI rules in `iu-research-computing-map` and the
  storage steps in `storing-and-moving-research-data`. Name both in the plan.

## Sources

- [KB0023281](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023281) Use HTAR with your SDA account, read 2026-10-03
