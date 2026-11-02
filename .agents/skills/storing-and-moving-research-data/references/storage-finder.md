# Choosing storage from a researcher's documents

Verified 2026-11-02 against the IU Knowledge Base (KB) and the IU Data Storage Finder. Read the main `SKILL.md` first. This file is the workflow for `scripts/storage_finder.py`.

The IU Data Storage Finder at `https://datastoragefinder.iu.edu/dsf/` asks six questions and shows the IU storage services that fit (KB0022439). A researcher should not have to click through it. Point the agent at a solicitation, a data management and sharing (DMS) plan, a data use agreement, or a description of the project. The agent derives each answer, shows where it came from, and runs the script.

## What the script reads

The script reads the Finder live on every run and keeps no copy of it.

- **Observed 2026-11-02:** the Finder's logic is a public file, `https://datastoragefinder.iu.edu/dsf/config.js`. It lists 13 storage codes, the codes that need encryption for Critical data, and six questions. Each answer lists the codes it allows.
- **Observed 2026-11-02:** the Finder page carries a comparison table with each service's description, example usage, cost, capacity, data allowed, and data loss prevention, and a link to its KB article.
- The Finder takes one answer per question and shows the services every answer allows. The script does the same.

The script exits with status 3 and says so when either file changes shape. Then use the Finder in a browser, and report the change; see `reporting-a-skill-problem`.

```bash
f=.agents/skills/storing-and-moving-research-data/scripts/storage_finder.py
$f questions                       # the six questions and their answer keys
$f match 1.1 2.2 4.4 5.4 6.1 --classification restricted
$f match 1.2 2.1 --classification critical-phi --table
$f table SP SD                     # comparison rows for chosen services
```

Add `--json` to any command for machine-readable output.

## The Finder and the KB disagree on non-PHI Critical data

The Finder's "Critical" answer does not separate PHI from other Critical data. It allows Research Technologies systems for both. The KB does not.

- Critical data other than PHI is not permitted on Research Technologies systems (KB0023515, KB0024406, KB0022478, KB0022767).
- KB0025747 and KB0023604 list Restricted, other than PHI, as the most sensitive data allowed on Slate, Slate-Project, Slate-Scratch, Geode-Project, the SDA, ResDB, and the research supercomputers.
- KB0023604 allows Critical data other than PHI in Paid Google Shared Drives and Microsoft at IU Secure Storage. Microsoft Secure Storage is a Teams site requested as Secure Storage (KB0025537).
- Scholarly Data Share's article states no classification limit. Its data is stored on the SDA (KB0025720).

So the script takes classification as a flag, `--classification`, not as an answer key. `critical-phi` and `critical-other` both answer the Finder's Critical. `critical-other` then keeps only the services KB0023604 allows, lists what it removed with the KB article for each, and prints a warning. That KB rule is the only data written into the script.

The script also flags a second mismatch. The Finder's answers offer Google Drive for Restricted data. Its own table says Public only. KB0023604 says University-internal and some Restricted, and no PHI.

**Open item.** The research-data repository's open items record both mismatches as a correction request for the Finder's maintainers. Until the Finder changes, trust the KB. When it changes, check the script's KB rule against the new Finder and update this file.

## Steps

1. **Read what the researcher provides.** A solicitation, DMS plan, data use agreement, IRB protocol, or project description. Ask for whichever one the answers are likely in.
2. **Derive each answer you can.** For each question, quote the sentence the answer came from, and say how you read it. Show the researcher this list before running anything. A question the document does not answer stays unanswered; ask the researcher or leave it out.
3. **Never guess the classification.** Take it from the researcher. If they do not know, hand off to [`classifying-research-data`](https://github.com/IUSCA/research-data/tree/main/.agents/skills/classifying-research-data) in research-data. A data use agreement or a mention of PHI is evidence to show them, not a classification. Critical data needs one more answer: is it PHI, or other Critical data?
4. **Split the project by stage when needs differ.** The Finder answers one storage need at a time. Analysis on Quartz and a long-term archive are two runs: one with HPC and computational analysis, one without HPC and archival.
5. **Run `match`** with the derived keys and `--classification`. Add `--table` to show the comparison rows.
6. **Present the options.** For each service, give the KB article the script prints. Then point to this skill's section on that service for quotas, purge rules, and access. Pass on every warning and note the script prints.
7. **Say the Finder is guidance.** Each service's KB article governs what it allows. Where they disagree, the KB wins.

### Reading the six questions from a document

| Question | Evidence that answers it | Ask when |
| --- | --- | --- |
| 1. High performance computing | Alignment, imaging pipelines, simulation, model training, Slurm, Quartz, Big Red 200 | The document names analysis but not where it runs |
| 2. Collaborators outside IU | Subawards, multi-site teams, named external co-investigators, a consortium | Collaborators are named but their access to the data is not |
| 3. Classification | Never derive it. Show the evidence: PHI, a data use agreement, de-identification, controlled access | Always |
| 4. Kind of data | Archiving and retention language means archival; pipelines mean computational; shared team folders mean collaborative | The document covers several stages; see step 4 |
| 5. Size over three years | Data volumes in the DMS plan or budget justification, sample counts times file size | No volume is stated; ask for an estimate |
| 6. Largest file over 10 GB | Whole-genome BAM or CRAM files, raw imaging stacks, video | File types are not named |

A DMS plan's "data types," "preservation," and "access" sections usually answer questions 2, 4, and 5. A data use agreement usually limits where data may be stored and who may see it. Quote those limits too; they may rule out services the Finder allows.

## When to ask a person

- **Sensitive data storage:** SecureMyResearch at securemyresearch@iu.edu, for PHI and other regulated data (KB0023604, KB0025747).
- **The Finder itself, or no service matches:** the Finder page's "contact us" link offers a consultation with its maintainers.
- **A service's quota, access, or allocation:** the queues in `getting-help-from-research-technologies`.

## Sources

URL form: `https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=<number>`. KB0022439, KB0022478, KB0022767, KB0023515, KB0023604, KB0024406, KB0025537, KB0025720, KB0025747, all read 2026-11-02 except KB0022439 (read 2026-10-01). Titles are in the main `SKILL.md` Sources list.

External: the IU Data Storage Finder, `https://datastoragefinder.iu.edu/dsf/` and its `config.js`, read live by the script; observed 2026-11-02.
