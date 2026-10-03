#!/bin/bash
# Report where Python, conda, uv, R, Jupyter, and Apptainer put
# environments, packages, and caches, and warn when they land in home.
#
# Read-only: it creates, changes, and installs nothing. It does not prompt.
# Run on a Quartz or Big Red 200 login node:
#   ssh <user>@quartz.uits.iu.edu 'bash -l -s' < check-env-locations.sh
# A login shell (-l) makes the module command available.
# Add --sizes to count files and space in the usual home locations.
# Counting walks those trees, so it can take a while on a full home.

sizes=0
[ "${1:-}" = "--sizes" ] && sizes=1

home_real=$(readlink -f "$HOME" 2>/dev/null || echo "$HOME")
warned=0

in_home() {
  local p
  p=$(readlink -m "$1" 2>/dev/null || echo "$1")
  case "$p" in
    "$HOME"/*|"$HOME"|"$home_real"/*|"$home_real"|/N/u/*|/geode*/home/*) return 0 ;;
  esac
  return 1
}

report() {
  # report <label> <path> <how it was set>
  local flag="ok  "
  if in_home "$2"; then flag="HOME"; warned=$((warned + 1)); fi
  printf '%s  %-22s %s  (%s)\n' "$flag" "$1" "$2" "$3"
}

# Expand a leading ~ only. Config text is never evaluated.
expand() { local v=$1; printf '%s' "${v/#\~/$HOME}"; }

echo "== Host $(hostname -s), home $home_real"
echo "HOME lines are under the home directory. Move them; see SKILL.md."
echo

echo "== Caches"
if [ -n "${XDG_CACHE_HOME:-}" ]; then
  cache_root=$XDG_CACHE_HOME; cache_how="XDG_CACHE_HOME"
else
  cache_root=$HOME/.cache; cache_how="default, XDG_CACHE_HOME unset"
fi
report "~/.cache root" "$cache_root" "$cache_how"

pip_conf=""
for f in "${PIP_CONFIG_FILE:-}" "$HOME/.config/pip/pip.conf" "$HOME/.pip/pip.conf"; do
  [ -n "$f" ] && [ -f "$f" ] && pip_conf=$f && break
done
if [ -n "${PIP_CACHE_DIR:-}" ]; then
  report "pip cache" "$PIP_CACHE_DIR" "PIP_CACHE_DIR"
elif [ -n "$pip_conf" ] && grep -q '^[[:space:]]*cache-dir' "$pip_conf"; then
  v=$(grep '^[[:space:]]*cache-dir' "$pip_conf" | head -1 | cut -d= -f2- | tr -d ' ')
  report "pip cache" "$(expand "$v")" "cache-dir in $pip_conf"
else
  report "pip cache" "$cache_root/pip" "default"
fi
[ -n "${PIP_NO_CACHE_DIR:-}" ] && echo "      PIP_NO_CACHE_DIR is set: pip keeps no cache"

if [ -n "${UV_CACHE_DIR:-}" ]; then
  report "uv cache" "$UV_CACHE_DIR" "UV_CACHE_DIR"
else
  report "uv cache" "$cache_root/uv" "default"
fi

if [ -n "${APPTAINER_CACHEDIR:-}" ]; then
  report "Apptainer cache" "$APPTAINER_CACHEDIR" "APPTAINER_CACHEDIR"
else
  report "Apptainer cache" "$HOME/.apptainer/cache" "default"
fi
echo

echo "== conda"
if ! command -v conda >/dev/null 2>&1 && type module >/dev/null 2>&1; then
  module load conda >/dev/null 2>&1
fi
if command -v conda >/dev/null 2>&1; then
  echo "conda: $(command -v conda) ($(conda --version 2>/dev/null))"
  [ -n "${CONDA_PKGS_DIRS:-}" ] && echo "      CONDA_PKGS_DIRS=$CONDA_PKGS_DIRS"
  [ -n "${CONDA_ENVS_PATH:-}" ] && echo "      CONDA_ENVS_PATH=$CONDA_ENVS_PATH"
  [ -n "${CONDA_ENVS_DIRS:-}" ] && echo "      CONDA_ENVS_DIRS=$CONDA_ENVS_DIRS"
  # The first writable entry is where new packages and named envs go.
  for key in pkgs_dirs envs_dirs; do
    first=1
    while read -r p; do
      [ -z "$p" ] && continue
      if [ -d "$p" ] && [ ! -w "$p" ]; then
        printf '      %-22s %s  (not writable, skipped by conda)\n' "$key" "$p"
        continue
      fi
      if [ $first -eq 1 ]; then
        report "$key (used)" "$p" "conda config"
        first=0
      else
        printf '      %-22s %s  (fallback)\n' "$key" "$p"
      fi
    done < <(conda config --show "$key" 2>/dev/null | sed -n 's/^  - //p')
  done
else
  echo "conda not found. On IU clusters it comes from 'module load conda'."
fi
if [ -f "$HOME/.condarc" ]; then
  echo "      ~/.condarc exists"
fi
echo

echo "== Shell start-up files"
for f in "$HOME/.bashrc" "$HOME/.bash_profile" "$HOME/.profile"; do
  [ -f "$f" ] || continue
  if grep -q '>>> conda initialize >>>' "$f"; then
    echo "WARN  $f has a 'conda initialize' block. The KB says remove it."
    warned=$((warned + 1))
  fi
  if grep -Eq '^[^#]*(conda|source) +activate|^[^#]*/bin/activate' "$f"; then
    echo "WARN  $f activates an environment at every login."
    warned=$((warned + 1))
  fi
done
echo

echo "== R"
if [ -n "${R_LIBS_USER:-}" ]; then
  report "R_LIBS_USER" "$R_LIBS_USER" "environment"
elif [ -f "$HOME/.Renviron" ] && grep -q '^R_LIBS_USER' "$HOME/.Renviron"; then
  v=$(grep '^R_LIBS_USER' "$HOME/.Renviron" | tail -1 | cut -d= -f2- | tr -d "\"'")
  report "R_LIBS_USER" "$v" "~/.Renviron"
else
  report "R_LIBS_USER" "$HOME/R/..." "site default, no ~/.Renviron setting"
fi
echo

echo "== Jupyter kernels (small files; home is fine)"
kdir=$HOME/.local/share/jupyter/kernels
if [ -d "$kdir" ]; then
  for k in "$kdir"/*/kernel.json; do
    [ -f "$k" ] || continue
    py=$(grep -m1 -o '"/[^"]*"' "$k" | tr -d '"')
    printf '      %-22s %s\n' "$(basename "$(dirname "$k")")" "${py:-(no absolute interpreter path)}"
    if [ -n "$py" ] && [ ! -e "$py" ]; then
      echo "WARN  kernel $(basename "$(dirname "$k")") points at a missing interpreter"
      warned=$((warned + 1))
    fi
  done
else
  echo "      none in $kdir"
fi
echo

if [ $sizes -eq 1 ]; then
  echo "== Size of the usual home locations"
  for d in .conda .cache .local .apptainer R miniconda3 miniforge3 anaconda3; do
    [ -d "$HOME/$d" ] || continue
    files=$(du -s --inodes "$HOME/$d" 2>/dev/null | cut -f1)
    space=$(du -sh "$HOME/$d" 2>/dev/null | cut -f1)
    printf '      ~/%-20s %8s  %8s files\n' "$d" "$space" "$files"
  done
  echo
fi

echo "== $warned item(s) to move or fix"
exit 0
