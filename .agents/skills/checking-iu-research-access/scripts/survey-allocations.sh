#!/usr/bin/env bash
# Survey the Slurm accounts you may charge, so you can record what each is for.
# Run it on a login node. It is read-only and light enough for a login node.
#
#   env -u LC_ALL ssh <user>@quartz.uits.iu.edu 'bash -s' < survey-allocations.sh
#
# Slurm does not know which RT Project an account belongs to; its description
# is just the account name. The "related groups" line is a guess from shared
# membership. Confirm each account in RT Projects (projects.rt.iu.edu), which
# shows the Slurm Account Name on the allocation.
#
# Prints Markdown for your private resources file. It names no other users.

set -u
unset LC_ALL
me=$(id -un)
cluster=$(sacctmgr -nP show assoc user="$me" format=Cluster 2>/dev/null | head -1)
since=$(date -d '-90 days' +%F)
year=$(date -d '-365 days' +%F)
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

groups=$(id -Gn | tr ' ' '\n' | grep -E '^condo_' || true)
for g in $groups; do
  getent group "$g" | cut -d: -f4 | tr , '\n' | grep . | sort -u > "$tmp/g.$g"
done

echo "## Slurm accounts on ${cluster:-$(hostname)}"
echo
echo "Observed $(date +%F) on $(hostname -f 2>/dev/null || hostname) with survey-allocations.sh."
echo "Default account: $(sacctmgr -nP show user "$me" format=DefaultAccount 2>/dev/null)."
echo

for a in $(sacctmgr -nP show assoc user="$me" format=Account 2>/dev/null | sort -u); do
  sacctmgr -nP show assoc account="$a" format=User | grep . | sort -u > "$tmp/acct"
  members=$(wc -l < "$tmp/acct")
  qos=$(sacctmgr -nP show assoc user="$me" account="$a" format=QOS | head -1)
  # sreport prints the account total on a line with an empty login.
  used=$(sreport -nP cluster AccountUtilizationByUser accounts="$a" \
    start="$since" -t hours format=Accounts,Login,Used 2>/dev/null)
  total=$(printf '%s\n' "$used" | awk -F'|' '$2=="" {print $3}' | head -1)
  mine=$(printf '%s\n' "$used" | awk -F'|' -v u="$me" '$2==u {print $3}' | head -1)
  fair=$(sshare -nP -A "$a" -u "$me" -o User,FairShare 2>/dev/null \
    | awk -F'|' -v u="$me" '$1 ~ u {print $2}' | head -1)
  jobs=$(sacct -u "$me" -A "$a" -S "$year" -X -n -P -o JobID 2>/dev/null | grep -c .)
  related=$(for g in $groups; do
      c=$(comm -12 "$tmp/acct" "$tmp/g.$g" | wc -l)
      [ "$c" -gt 0 ] && echo "$c $g ($c of $(wc -l < "$tmp/g.$g"))"
    done | sort -rn | head -3 | cut -d' ' -f2- | paste -sd, | sed 's/,/, /g')

  echo "### $a"
  echo
  echo "- RT Project: _confirm in RT Projects_"
  echo "- PI: _?_"
  echo "- Use for: _?_"
  echo "- Members: $members. QOS: ${qos:-none listed}."
  echo "- CPU hours since $since: ${total:-0} total, ${mine:-0} yours. Your fair share: ${fair:-?}."
  echo "- Your jobs since $year: $jobs."
  echo "- Related groups (guess from shared members): ${related:-none}."
  echo
done
