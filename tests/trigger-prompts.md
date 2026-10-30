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
| I have a 5 TB imaging dataset and a GPU training pipeline. Plan where each step should run at IU. | `planning-research-computing-work` |
| Check whether I'm set up to use IU research computing. | `checking-iu-research-access` |
| Which of my Slurm accounts should this job use? | `checking-iu-research-access` (read the resources file) |
| Copy 40 TB from Slate-Project to the SDA. | `storing-and-moving-research-data` |
| Share a Slate-Project folder with a collaborator outside IU. | `storing-and-moving-research-data` |
| How do I get a GUI desktop on Quartz? | `using-research-desktop` |
| Call IU's LLM API from Python. | `using-reallms` |
| Run gpt-oss-120b on an H100 for a batch of 10,000 prompts. | `running-llms-on-hpc` |
| Benchmark a local model on Quartz without REALLMS rate limits. | `running-llms-on-hpc` |
| That worked. Make this a skill so I can run it again next month. | `capturing-a-workflow-as-a-skill` |
| Remember how we did this so the agent can do it again. | `capturing-a-workflow-as-a-skill` |
| The REALLMS skill didn't mention this error. Can we report it? | `reporting-a-skill-problem` |
| The skill said this partition exists, but sbatch says it doesn't. How do I tell the maintainers? | `reporting-a-skill-problem` |
| This kb.iu.edu link goes to the KB home page. Find the article. | `searching-the-iu-knowledge-base` |
| How do I keep track of which version of my analysis code produced these results? | `versioning-research-code` |
| Put my analysis scripts on GitHub so my co-author can see them. | `versioning-research-code` |
| My Quartz home directory is full of .conda files. Where should my conda environments go? | `managing-python-environments` |
