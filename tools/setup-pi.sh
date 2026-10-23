#!/usr/bin/env bash
# Set up the pi coding agent on an IU cluster login node, using IU's REALLMS
# models and this repository's skills. See START-HERE.md.
#
#   tools/setup-pi.sh
#
# Put the REALLMS API key in ~/.config/reallms/api-key first, or paste it when
# asked. In a terminal, the script offers to start pi when it finishes.
#
# Safe to re-run: it updates pi, refreshes the REALLMS model list, and keeps
# the key already saved. It asks for the REALLMS API key once, never for the
# IU passphrase, and never edits shell startup files.
#
# It writes:
#   ~/.local/share/pi-npm/         pi, installed with npm
#   ~/.local/bin/pi                a launcher that adds Node.js
#   ~/.config/reallms/api-key      the REALLMS API key, mode 600
#   ~/.pi/agent/models.json        the "reallms" provider, from the live service
#   ~/.pi/agent/settings.json      default model, and this repository's skills
set -euo pipefail

repo=$(cd "$(dirname "$0")/.." && pwd)
prefix=${SETUP_PI_PREFIX:-$HOME/.local/share/pi-npm}
bin_dir=${SETUP_PI_BIN_DIR:-$HOME/.local/bin}
key_file=${REALLMS_KEY_FILE:-$HOME/.config/reallms/api-key}
agent_dir=${PI_CODING_AGENT_DIR:-$HOME/.pi/agent}
models_script=$repo/.agents/skills/using-reallms/scripts/reallms_models.py
launcher=$bin_dir/pi
marker="# Written by research-technologies tools/setup-pi.sh."

say() { printf '==> %s\n' "$*"; }
die() { printf 'error: %s\n' "$*" >&2; exit 1; }

node_ok() {
  command -v node >/dev/null 2>&1 &&
    node -e 'const [a,b]=process.versions.node.split(".").map(Number); process.exit(a>22||(a==22&&b>=19)?0:1)'
}

# 1. Node.js 22.19 or newer. Quartz provides it as the nodejs module.
if ! node_ok; then
  if ! type module >/dev/null 2>&1 && [ -n "${LMOD_CMD:-}" ]; then
    module() { eval "$("$LMOD_CMD" bash "$@")"; }
  fi
  type module >/dev/null 2>&1 && module load nodejs >/dev/null 2>&1 || true
fi
node_ok || die "pi needs Node.js 22.19 or newer, and none was found here. On Quartz, 'module load nodejs' provides it."
node_bin=$(dirname "$(command -v node)")
# A module's Node.js may need the module's newer C++ runtime. Record where it
# came from, so pi still starts after a module purge.
node_libs=$(ldd "$node_bin/node" 2>/dev/null | awk '/libstdc\+\+/ {sub(/\/[^\/]*$/, "", $3); print $3}')
say "Node.js $(node --version) from $node_bin"

# 2. Install or update pi.
if [ -e "$launcher" ] && ! grep -qF "$marker" "$launcher"; then
  die "$launcher exists and was not written by this script. Move it aside and run again."
fi
say "Installing pi into $prefix"
npm install -g --prefix "$prefix" --ignore-scripts --no-fund --no-audit \
  --loglevel=error @earendil-works/pi-coding-agent
mkdir -p "$bin_dir"
lib_lines=
if [ -n "$node_libs" ]; then
  lib_lines="LD_LIBRARY_PATH=\"$node_libs\${LD_LIBRARY_PATH:+:\$LD_LIBRARY_PATH}\"
export LD_LIBRARY_PATH"
fi
cat > "$launcher" <<EOF
#!/bin/sh
$marker
# Re-run that script to update pi or move to a newer Node.js.
PATH="$node_bin:\$PATH"
export PATH
$lib_lines
exec "$prefix/bin/pi" "\$@"
EOF
chmod 755 "$launcher"
say "pi $("$launcher" --version)"

# 3. The REALLMS API key, asked for once and kept owner-only.
if [ ! -s "$key_file" ]; then
  [ -t 0 ] && printf 'Paste your REALLMS API key (input is hidden): '
  IFS= read -rs key || true
  [ -t 0 ] && printf '\n'
  [ -n "${key:-}" ] || die "no key entered. START-HERE.md says how to get one in RT Projects."
  mkdir -p "$(dirname "$key_file")"
  (umask 077; printf '%s\n' "$key" > "$key_file")
  unset key
fi
chmod 600 "$key_file"
REALLMS_API_KEY=$(cat "$key_file")
export REALLMS_API_KEY

# 4. The live model list. This also proves the key works.
say "Asking REALLMS which models answer"
mkdir -p "$agent_dir"
# pi reads the key file itself, per request, so the key never enters the
# environment of the commands pi runs. An agent that runs env cannot leak it.
python3 -I "$models_script" --pi "$agent_dir/models.json" --pi-api-key "!cat '$key_file'"

# 5. Default model and the skills, so pi finds them from any directory.
python3 -I - "$agent_dir" "$repo/.agents/skills" <<'PY'
import json, os, sys
agent_dir, skills = sys.argv[1], sys.argv[2]
models = json.load(open(os.path.join(agent_dir, "models.json")))["providers"]["reallms"]["models"]
path = os.path.join(agent_dir, "settings.json")
settings = json.load(open(path)) if os.path.exists(path) else {}
ids = [m["id"] for m in models]
if settings.get("defaultProvider") != "reallms" or settings.get("defaultModel") not in ids:
    settings["defaultProvider"] = "reallms"
    settings["defaultModel"] = ids[0]
paths = settings.setdefault("skills", [])
if skills not in paths:
    paths.append(skills)
with open(path, "w") as f:
    json.dump(settings, f, indent=2)
    f.write("\n")
print(f"==> Default model {settings['defaultModel']}; skills from {skills}")
PY

case ":$PATH:" in
  *":$bin_dir:"*) run=pi ;;
  *) run=$launcher; say "$bin_dir is not on your PATH, so start pi by its full path." ;;
esac
say "Done. Start pi any time with: $run"
say "First, ask it: Check whether I'm set up to use IU research computing."
if [ -t 0 ] && [ -t 1 ]; then
  printf 'Start pi now? [Y/n] '
  IFS= read -r answer || answer=n
  case "$answer" in
    n|N|no|NO) ;;
    *) exec "$launcher" ;;
  esac
fi
