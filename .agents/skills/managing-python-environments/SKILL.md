---
name: managing-python-environments
description: Set up and use Python and R software environments on IU's Quartz and Big Red 200 - the python and conda modules, venv and virtualenv, pip, uv, mamba, self-installed Miniforge, R package libraries, Jupyter kernels, and Apptainer as an alternative. Covers where environments and package caches should live (home, Slate, Slate-Project, not Slate-Scratch), moving pip, conda, uv, and R caches out of the home directory, building environments in an interactive job instead of on a login node, activating environments in batch jobs, why not to run conda init, environment files for reproducibility, and a read-only check of where caches point. Use when installing Python or R packages on an IU cluster, creating a conda environment or virtualenv, sharing an environment with a lab, fixing a home directory full of .conda or .cache files, adding a Jupyter kernel, or debugging an import or activation failure in a job.
---

# Managing Python and R environments at IU

Verified 2026-10-03 against the IU Knowledge Base (KB). Each claim names its
KB article; links are in Sources at the end.

The same rules hold on Quartz and Big Red 200. Only Quartz was observed for
this file. The `submitting-hpc-jobs` skill covers jobs and partitions. The
`storing-and-moving-research-data` skill covers quotas and storage spaces.

## Start from the modules

Load a module before running Python. The operating system's Python is not
supported (KB0024539). **Observed 2026-10-03** on Quartz with
`which python3; python3 --version`: with no module loaded, `python3` is
`/usr/bin/python3`, version 3.6.8.

The modules already hold many packages. Check them before you install
anything (KB0022379, KB0022631).

| Need | Load | Source |
| --- | --- | --- |
| Python with common science packages | `module load python` or `python/<version>` | KB0024539 |
| GPU Python: Torch, TensorFlow, JAX | `module load python/gpu` | KB0022631, KB0022436 |
| conda, with `mamba` | `module unload python; module load conda` | KB0022379; Observed |
| R | `module load r` | KB0024479 |
| Jupyter Notebook and Lab | `module load jupyter`, on RED or a compute node | KB0025672 |
| Containers | `module load apptainer` | KB0025214 |

List a module's packages with `pip list` or `pip freeze` after loading it
(KB0022631). Ask RADL to add a package many researchers need as a site
package (KB0024539, KB0024479).

**Observed 2026-10-03** on Quartz with `module -t avail`, `module spider`,
and `module show`:

- Python 3.12.4, 3.13.5, and 3.14.5; the default is 3.13.5, not the newest.
- `python/gpu` 3.10.10, 3.11.5, and 3.12.5.
- One `conda/26.3.2` module, which includes `mamba`. It is in the python
  Lmod family, so load one or the other.
- No `miniforge`, `anaconda`, `mamba`, or `uv` module.
- R 4.4.1, 4.5.1, and 4.6.1; the default is 4.5.1.
- `python/3.13.5` has pip, virtualenv, and ipykernel. It sets `PYTHONPATH`.

## Choose a tool

- **venv on a python module** suits most Python work. It is much smaller than
  a conda environment (KB0025217). Create it with
  `python -m venv <dir>` (KB0025217).
- **conda** suits non-Python dependencies, since conda installs those too.
  Its environments take much more disk space (KB0025217, KB0022379).
- **Apptainer** suits a stack that will not build natively. Ask RADL first
  whether it can be installed natively (KB0025214).
- **uv** is not a module (Observed above). **Practice:** install it with
  `pip install --user uv` on a python module. It resolves faster than pip.
- **Your own Miniforge or Miniconda** is a last resort. The KB recommends the
  conda module instead of installing Anaconda or Miniconda (KB0023231).

`python -m venv --system-site-packages <dir>` lets the venv see the module's
packages, so you install only what is missing (KB0025217). Loaded modules,
`PYTHONPATH`, and `LD_LIBRARY_PATH` all affect a venv (KB0025217).

**Practice:** a venv is bound to the interpreter it was built from. Load the
same `python/<version>` module every time you use it. Name the version in
job scripts, because the default changes.

## Where environments live

The home directory is the wrong place for large environments. It is 100 GB
with a file-count limit, shared across all your cluster accounts
(KB0025028). It is for low-capacity, low-performance use (KB0025028). Conda
environments are large (KB0022379).

| Location | Use it for | Source |
| --- | --- | --- |
| Home, `/N/u/<user>/Quartz` | A small venv, kernel specs, config files | KB0025217, KB0025028 |
| Slate, `/N/slate/<user>` | Your conda environments and larger venvs | KB0022379, KB0025217 |
| Slate-Project, `/N/project/<project>` | One environment the whole lab uses | KB0022486 |
| Slate-Scratch | Not for environments | KB0025317 |
| An Apptainer image on Slate | A large or fragile stack | KB0025214 |

- The KB names both home and Slate as good venv locations. Home is backed
  up; Slate is optimized for access from compute nodes (KB0025217).
- Build conda environments with `-p` on Slate, not with `-n`, which writes
  under `~/.conda` (KB0022379).
- Software in home or Slate is usable only by you. Software in Slate-Project
  is usable by the whole project (KB0022486).
- Slate-Scratch deletes files not accessed for 30 days (KB0025317). An
  environment there loses files it rarely reads and breaks at random.
- Home backups skip `.conda`, `.anaconda`, and `.cache` (KB0025028). Keep the
  environment file in a backed-up place, not the environment.
- Environments built on Quartz and Big Red 200 are not interchangeable. Keep
  them in separate directories, such as `envs/quartz` and `envs/br200`
  (KB0022379, KB0022631).

**Observed 2026-10-03** on Quartz with `stat -f -c %T` and `df -hT`: home
is NFS; `/N/slate`, `/N/project`, and `/N/scratch` are Lustre.

Lustre handles metadata and data separately, which makes metadata-heavy
work slow (KB0023425). **Practice:** an environment is many small files, and
Python opens many of them at each `import`. Expect slow imports from Slate,
worse when many jobs start at once. Two fixes help:

- Pack a large environment into one Apptainer image on Slate. Opening one
  file replaces many metadata lookups.
- For many-node runs, unpack an archived environment to node-local `/tmp`
  at job start. Quartz nodes have `/tmp` (KB0022439). **External:**
  `conda-pack` makes a relocatable archive of a conda environment
  (conda-pack documentation).

**Practice:** for a shared lab environment on Slate-Project, let one person
build and update it. Others use it read-only. Set group permissions as the
`storing-and-moving-research-data` skill describes. Keep the environment
file in the lab's git repository.

Count an environment's files before choosing where it goes:
`du -s --inodes <env-dir>`. Compare the total with `quota` (KB0025028).

## Keep caches out of home

Package managers cache downloads in home by default. These caches grow
quietly and count against the home quota and file limit (KB0022379,
KB0025028).

**Observed 2026-10-03** on Quartz with `conda config --show-sources`,
`conda config --show pkgs_dirs envs_dirs`, and `pip cache dir`:

- The conda module's own `.condarc` sets `channels: conda-forge` only.
- `pkgs_dirs` lists the module's package directory, then `~/.conda/pkgs`.
- `envs_dirs` lists `~/.conda/envs` first, so `-n` lands in home.
- pip's cache is `~/.cache/pip`.

Set these once per system. Each cluster has its own home subdirectory, so
each needs its own settings (KB0022379, KB0025028).

```bash
module load conda
conda config --add pkgs_dirs /N/slate/<user>/conda/pkgs/quartz
conda config --add envs_dirs /N/slate/<user>/conda/envs/quartz
```

The KB recommends a per-system package directory on Slate in `~/.condarc`
(KB0022379). `conda config --add` writes that file and puts the new entry
first. **External:** conda also reads `CONDA_PKGS_DIRS` and
`CONDA_ENVS_PATH` (conda documentation, "Using custom locations for
environment and package cache").

**Practice:** for pip, uv, and Apptainer, set cache variables in
`~/.bashrc`. Setting a variable is safe there; prepending to `PATH` is not
(KB0023231). **External:** each tool documents its variable (pip, uv, and
Apptainer user guides).

```bash
export PIP_CACHE_DIR=/N/slate/<user>/cache/pip
export UV_CACHE_DIR=/N/slate/<user>/cache/uv
export APPTAINER_CACHEDIR=/N/slate/<user>/cache/apptainer
```

**External:** `XDG_CACHE_HOME` moves `~/.cache` as a whole, for every tool
that follows the XDG convention (freedesktop.org XDG Base Directory spec).
**External:** uv links files from its cache when both are on one file
system, and copies them otherwise (uv documentation, "Caching"). Keep the uv
cache and its venvs on the same file system.

`pip install --no-cache-dir` skips the cache for a one-off install. Clear
conda's cache with `conda clean -a` (KB0022379). Clear pip's with
`pip cache purge`.

[scripts/check-env-locations.sh](scripts/check-env-locations.sh) shows where
each cache and environment directory points, and flags any under home. It
also flags `conda initialize` blocks and activations in start-up files.

```bash
ssh <user>@quartz.uits.iu.edu 'bash -l -s' < scripts/check-env-locations.sh
```

It is read-only and light. Add `--sizes` to count files in `~/.conda`,
`~/.cache`, and similar trees. It has not yet been run on a cluster. Run it
once and record the result as Observed.

## R libraries and Jupyter kernels

R installs packages into home by default (KB0024479). Move a large library
to Slate with `R_LIBS_USER` in `~/.Renviron`. Jupyter runs on RED or a
compute node, not a login node (KB0025672). Register an environment as a
kernel with `ipykernel`. Details, commands, and Observed values are in
[references/r-and-jupyter.md](references/r-and-jupyter.md).

## Build environments in a job, not on a login node

Login-node processes are killed after 20 minutes of CPU time (KB0022436).
A conda solve or a source build can exceed that. Build in an interactive
job (KB0023298, KB0025672):

```bash
srun -p interactive -A <slurm-account> --cpus-per-task=4 --mem=16G \
  --time=02:00:00 --pty bash
```

**Practice:** list every package when you create a conda environment. Conda
resolves them together, which avoids conflicts (KB0022379). `mamba` solves
faster and takes the same arguments. A small `pip install` on a login node is
fine.

**Open item:** the KB does not say whether compute nodes reach PyPI and
conda-forge. In an interactive job, check with
`curl -sI https://pypi.org | head -1`, then record the answer as Observed.

## Write the environment down

Rebuild from a file instead of copying an environment between systems. An
environment file also survives a purge or a lost home directory.

- conda: `conda env export > environment.yml`, then
  `conda env create -f environment.yml` (KB0022379). **Practice:**
  `conda env export --from-history` keeps only what you asked for. It
  rebuilds more reliably on the other cluster.
- pip: `pip freeze > requirements.txt`, then `pip install -r requirements.txt`.
- uv: commit `pyproject.toml` and `uv.lock`, then run `uv sync`
  (**External:** uv documentation).
- R: **Practice:** record `sessionInfo()` output with the project, or use
  `renv` for a lock file.

Keep the file in git with the code. Name the module versions it needs in a
comment or a README.

## Use an environment in a batch job

Activate the environment in the job script, not in `~/.bashrc`.

```bash
# venv
module load python/3.13.5
source /N/slate/<user>/venvs/quartz/<env>/bin/activate
python my_script.py

# conda
module load conda
conda activate /N/slate/<user>/conda/envs/quartz/<env>
python my_script.py
```

`conda activate` works when an IU conda module is loaded (KB0022379).
**Practice:** `conda run -p <env-dir> python my_script.py` runs one command
without activating. It suits a step in a pipeline.

Do not run `conda init`. It adds code to `~/.bashrc` that can break
`conda activate` and makes RED logins fail (KB0022379, KB0023231). If you
already ran it, remove the `conda initialize` block (KB0023231). For a
self-installed conda, use `source activate`, or move the block into a script
you source by hand (KB0022379).

**Practice:** any activation in `~/.bashrc` runs at every login and leaks into
every job. A conda base environment on Lustre also slows each shell start.
Keep `~/.bashrc` to variables and appended `PATH` entries (KB0023231).

`module save` keeps a set of modules as your login default (KB0023802).
**Practice:** still name versions in job scripts, so a job does not depend on
your login state.

## Anaconda licensing

**Open item:** the KB says nothing about Anaconda's terms of service. It
does not say whether IU research may use the `defaults` channel unlicensed.
The KB only recommends the conda module over installing Anaconda or
Miniconda (KB0023231). **Observed 2026-10-03** on Quartz with
`conda config --show-sources`: the module's configuration uses only
`conda-forge`. **Practice:** keep to `conda-forge`. If you install your own
conda, use Miniforge, which defaults to `conda-forge`. Ask RADL before
relying on the `defaults` channel; see `getting-help-from-research-technologies`.

## Common failures

| Symptom | Likely cause | Source |
| --- | --- | --- |
| `python3` is 3.6 or a package is missing | No python module loaded | KB0024539 |
| Disk or file quota error in home | `~/.conda`, `~/.cache`, or `~/.local` grew | KB0025028, KB0022379 |
| conda build vanished on a login node | 20-minute CPU limit | KB0022436 |
| `conda activate` fails, or RED will not log in | `conda init` block in `~/.bashrc` | KB0022379, KB0023231 |
| Import works on Quartz, fails on Big Red 200 | Environments are not interchangeable | KB0022379, KB0022631 |
| Wrong package version imported | `PYTHONPATH`, `.pth` files, or `~/.local` first | KB0022631 |
| venv breaks after a module default changed | venv bound to the old interpreter | Practice |
| Environment on scratch broke weeks later | Files purged after 30 days unread | KB0025317 |
| R package will not compile | Missing system library | KB0026504 |

Print Python's search path with
`python -c "import sys; print('\n'.join(sys.path))"` (KB0022631). Python's
`-s` flag skips the user site-packages directory (KB0022631).

## Getting help

Python, conda, R, and Jupyter questions go to RADL (KB0024539, KB0022379,
KB0024479). The `getting-help-from-research-technologies` skill has the
queues and what to send.

## Keep this file current

Re-run the module, conda, and pip commands quoted above on each system after
monthly maintenance. Record any version or default that changed, with the
date. Run them on Big Red 200 too; no Big Red 200 value is recorded yet.
Run `scripts/check-env-locations.sh` on a cluster and record what it showed.
Re-read KB0022379 and KB0025217 before changing the location advice. Close
the open items only with a KB number, a command and date, or a ticket.

## Sources

All IU KB articles, read 2026-10-03. URL form:
`https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=<number>`.

- [KB0022379](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022379) Install packages in a conda environment on IU's high performance computers
- [KB0022436](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022436) Run GPU-accelerated jobs on Quartz or Big Red 200 at IU
- [KB0022439](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022439) Available access to allocated and short-term storage capacity on IU's research systems
- [KB0022486](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022486) Policies regarding UITS research systems
- [KB0022631](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022631) Install Python packages on the research supercomputers at IU
- [KB0023231](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023231) Troubleshoot Research Desktop
- [KB0023298](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023298) Use Slurm to submit and manage jobs on IU's research computing systems
- [KB0023425](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023425) Lustre file systems at IU
- [KB0023802](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023802) Use modules to manage your software environment on IU research supercomputers
- [KB0024479](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024479) Install R packages in your home directory on the IU research supercomputers
- [KB0024539](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024539) Use Python on IU research supercomputers
- [KB0025028](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025028) About home directory space on IU research supercomputers
- [KB0025214](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025214) Use Apptainer on Quartz or Big Red 200 at IU
- [KB0025217](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025217) Use virtualenv to customize Python
- [KB0025317](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025317) Slate-Scratch high performance file system: Terms of service
- [KB0025672](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025672) Use Jupyter Notebook on Quartz
- [KB0026504](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0026504) Deal with external dependencies when receiving errors installing R packages on IU's research supercomputers

Non-KB sources, marked **External** above, were not re-fetched for this
file. Check them before relying on the detail:

- conda user guide, "Using custom locations for environment and package cache"
- uv documentation, "Caching" and "Projects"
- pip user guide, "Caching"; Apptainer user guide, "Build environment"
- conda-pack documentation
- R documentation, `?.libPaths`
- freedesktop.org XDG Base Directory specification
