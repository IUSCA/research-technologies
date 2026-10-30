# Start here: an AI agent on Quartz

This sets up the [pi](https://pi.dev) coding agent on Quartz, with IU's REALLMS models and the skills in this repository. You need a Quartz account; if you have none, request one under Create More Accounts at `https://one.iu.edu/launch-task/iu/account-creation` (KB0022647).

## 1. Log in to Quartz and get this repository

```bash
ssh <your-iu-username>@quartz.uits.iu.edu
git clone https://github.com/IUSCA/research-technologies.git
```

Log in with your passphrase and Duo.

## 2. Get your REALLMS API key

Each person makes their own key in RT Projects (KB0027272):

1. Log in at `https://projects.rt.iu.edu` and open your lab's project.
2. Open its "REALLMS API" allocation, and create a key on that page (KB0027272).

No project, or no REALLMS API allocation? Your PI requests one there with Request New Allocation, and adds you to it. Approval can take two business days (KB0024132).

## 3. Run the setup script

```bash
research-technologies/tools/setup-pi.sh
```

Paste your key when it asks. The script saves it in `~/.config/reallms/api-key`, readable only by you. It then installs pi and offers to start it. Your first question can be:

> Check whether I'm set up to use IU research computing.

Next time, just run `pi`, in any directory.

## Good to know

- **Use only the REALLMS models with IU data.** REALLMS is approved for Restricted and Critical data, including PHI (KB0026817, KB0027272). Personal AI accounts are not approved for any institutional data (KB0026507), so skip pi's `/login`.
- **pi acts without asking.** It runs commands and edits files without asking first (External: pi quickstart). Keep important work in git; ask pi to "keep this code in git" and the `versioning-research-code` skill does the rest.
- **Heavy work belongs in jobs.** Login-node processes are killed after 20 minutes of CPU time (KB0022436). Ask pi to submit a Slurm job instead.
- **Models change often.** When one disappears, run the setup script again. It refreshes the model list, updates pi, and keeps your key. `/model` switches models inside pi.
- **To update the skills,** run `git -C research-technologies pull`.

## Details

The script never asks for your passphrase and never edits your shell startup files. It writes only these paths; delete them to remove everything.

| Path | What it is |
| --- | --- |
| `~/.local/share/pi-npm/` | pi itself |
| `~/.local/bin/pi` | A launcher that adds Node.js |
| `~/.config/reallms/api-key` | Your REALLMS key. pi reads it per request, so commands pi runs never see it. |
| `~/.pi/agent/models.json` | The REALLMS models, read from the live service |
| `~/.pi/agent/settings.json` | The default model, and where these skills live |

If your key leaks, delete it on the allocation's page, make a new one, put it in `~/.config/reallms/api-key`, and run the script again.

**Observed 2026-10-22** on Quartz: the script installed pi 1.4.0 using the default `nodejs` module, version 25.2.1. It found three REALLMS chat models and chose `qwen3.8-27b` as the default. Big Red 200 had no Node.js, which pi needs, so use Quartz.

## Sources

IU KB articles, read 2026-10-01. URL form: `https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=<number>`.

- KB0022436 Run GPU-accelerated jobs on Quartz or Big Red 200 at IU
- KB0022647 Get additional IU computing accounts
- KB0024132 Use RT Projects to request and manage access to specialized Research Technologies resources
- KB0026507 Generative AI tools at IU
- KB0026817 Acceptable use of AI tools with IU research data
- KB0027272 About the Research and Academic LLM Services (REALLMS) API at IU

External: [pi documentation](https://pi.dev/docs/latest), read 2026-10-22.
