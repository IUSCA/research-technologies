# R libraries and Jupyter kernels on IU clusters

Verified 2026-10-03 against the IU Knowledge Base (KB). This file is part of
the `managing-python-environments` skill. KB articles are listed in that
skill's Sources.

## R package libraries

`install.packages()` installs into home by default (KB0024479).
**Observed 2026-10-03** on Quartz in the R 4.5.1 `Renviron.site`: it sets
`R_LIBS_USER=~/R/Versions/%v/library`.

**Practice:** move a large library to Slate with one line in `~/.Renviron`:

```text
R_LIBS_USER=/N/slate/<user>/R/quartz/%v
```

Create that directory first. **External:** R adds `R_LIBS_USER` to
`.libPaths()` only if the directory exists (R documentation, `?.libPaths`).
Check the result with `.libPaths()` (KB0024479).

The default R version may change. You must keep your own version settings
(KB0024479). Load `r/<version>` explicitly in job scripts. For a failed
install, look for the missing library with `module av` or `module show`,
such as `module show gdal` (KB0026504). Install packages in RStudio on RED
with care, as behavior may differ (KB0024479).

## Jupyter kernels

Jupyter runs on RED or a compute node, not a login node (KB0025672). RADL
recommends plain `python` scripts on compute nodes over notebooks
(KB0025672). The `using-research-desktop` skill covers starting Jupyter on
RED.

**Observed 2026-10-03** on Quartz with `jupyter kernelspec list`: the
`jupyter/python3.14/2.20.0` module ships kernels for Python 3.12, 3.13, and
3.14, R 4.4.1 and 4.5.1, MATLAB, SAS, and bash. Its module description says
it will not work on login nodes. User kernels live under
`~/.local/share/jupyter`, from `jupyter --paths`.

**Practice:** to use your environment as a kernel, activate it. Then
register it once:

```bash
python -m ipykernel install --user --name <env> --display-name "<env> (Quartz)"
```

The kernel spec is a few small files in home, which is fine. The environment
needs `ipykernel`; a venv made with `--system-site-packages` on a python
module already has it. A kernel from a module-based venv may also need that
module's `PYTHONPATH` or libraries. Load the same python module before
starting Jupyter, or add an `env` block to the kernel's `kernel.json`.
