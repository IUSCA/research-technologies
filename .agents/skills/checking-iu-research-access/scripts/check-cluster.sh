#!/usr/bin/env bash
# Report what your account can use on an IU research supercomputer.
# Run it on a login node. It is read-only and light enough for a login node.
#
#   env -u LC_ALL ssh <user>@quartz.uits.iu.edu 'bash -s' < check-cluster.sh
#
# env -u LC_ALL keeps ssh from forwarding a locale the cluster lacks.
#
# Each line starts with OK, MISSING, or INFO.

set -u
unset LC_ALL
say() { printf '%-8s %s\n' "$1" "$2"; }
# A non-interactive shell may not define the module command.
if ! type module >/dev/null 2>&1; then
  for f in /etc/profile.d/lmod.sh /etc/profile.d/z00_lmod.sh /etc/profile.d/modules.sh; do
    [ -r "$f" ] && . "$f" && break
  done
fi
me=$(id -un)
host=$(hostname -f 2>/dev/null || hostname)

say INFO "host $host, user $me, $(date -Iseconds)"
say INFO "groups: $(id -Gn)"

# Storage that comes with an account, or with a project allocation.
for d in "$HOME" "/N/slate/$me" "/N/scratch/$me"; do
  if [ -d "$d" ]; then say OK "$d exists"; else say MISSING "$d not found"; fi
done
projects=$(find /N/project -maxdepth 1 -mindepth 1 -type d -readable 2>/dev/null \
  -exec test -w {} \; -print 2>/dev/null | head -20 | tr '\n' ' ')
if [ -n "$projects" ]; then
  say OK "writable Slate-Project directories: $projects"
else
  say INFO "no writable /N/project directory found (normal without a Slate-Project allocation)"
fi

# Slurm accounts are the RT Projects allocations you may charge with -A.
if command -v sacctmgr >/dev/null 2>&1; then
  accts=$(sacctmgr -nP show assoc user="$me" format=Account 2>/dev/null | sort -u | tr '\n' ' ')
  if [ -n "$accts" ]; then
    say OK "Slurm accounts usable with -A: $accts"
  else
    say MISSING "no Slurm account. Join an RT Projects allocation for this system."
  fi
else
  say MISSING "sacctmgr not found; is this a cluster login node?"
fi

# A Scholarly Data Archive account shows up as working HSI access.
# HSI loads with "module load hpss" (KB0022463). It may want a password,
# so stdin is closed and a prompt counts as "not confirmed".
# The quota report lists an "sda" line when the account exists.
command -v quota >/dev/null 2>&1 || module load quota >/dev/null 2>&1
quota_out=$(command -v quota >/dev/null 2>&1 && quota 2>&1 | sed 's/\x1b\[[0-9;]*m//g')
command -v hsi >/dev/null 2>&1 || module load hpss >/dev/null 2>&1
if command -v hsi >/dev/null 2>&1 && timeout 60 hsi -q 'pwd' </dev/null >/dev/null 2>&1; then
  say OK "SDA reachable with hsi"
elif printf '%s\n' "$quota_out" | grep -q '^ *sda '; then
  say INFO "SDA account exists (quota lists sda), but hsi cannot log in non-interactively. Set up HSI authentication, such as a keytab (KB0022463)."
elif command -v hsi >/dev/null 2>&1; then
  say INFO "SDA not confirmed. Causes: no SDA account, hsi wants a password or keytab (KB0022463), or Sunday 7-10am maintenance."
else
  say INFO "hsi not available; SDA access not checked"
fi

if [ -n "$quota_out" ]; then
  say INFO "quota:"
  printf '%s\n' "$quota_out" | sed 's/^/         /'
fi
