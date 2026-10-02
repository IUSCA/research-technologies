# Trigger prompts

Use these in a fresh session to check that each skill loads when it should.
Each prompt names the skill that should load first. Others may load too.
Step 7 of `MAINTAINING.md` explains the test.

| Prompt | Expected skill |
| --- | --- |
| Can I put PHI from a clinical study on Big Red 200? | `iu-research-computing-map` |
| Where should a portal that runs genotype imputation send its heavy jobs at IU? | `iu-research-computing-map` |
| Write an sbatch script for one H100 on Quartz. | `submitting-hpc-jobs` |
| My Quartz job says invalid partition "gpu". Why? | `submitting-hpc-jobs` |
| How many GPU nodes does Quartz have right now? | `submitting-hpc-jobs` (run `describe-cluster.sh`) |
| A new grad student joins my lab. What do they need to run jobs on Quartz? | `requesting-accounts-and-allocations` |
| Add a collaborator from another university to my RT Project. | `managing-rt-projects` |
| Our Slurm account stopped working in July. | `managing-rt-projects` |
| Who do I ask about a Slate-Scratch outage? | `getting-help-from-research-technologies` |
| Should our science gateway run on Jetstream2? | `jetstream2` |
| Check whether I'm set up to use IU research computing. | `checking-iu-research-access` |
| Copy 40 TB from Slate-Project to the SDA. | `storing-and-moving-research-data` |
| Share a Slate-Project folder with a collaborator outside IU. | `storing-and-moving-research-data` |
| How do I get a GUI desktop on Quartz? | `using-research-desktop` |
| Call IU's LLM API from Python. | `using-reallms` |
| This kb.iu.edu link goes to the KB home page. Find the article. | `searching-the-iu-knowledge-base` |
