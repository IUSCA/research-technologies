#!/usr/bin/env bash
# Read-only check of an Agent Skill directory before it is used or shared.
#
# Usage: check-skill.sh <skill-directory>
#
# Checks the SKILL.md frontmatter and length, then flags strings that may not
# belong in a skill: key-like tokens, private keys, email addresses, cluster
# paths, and long numeric identifiers. Changes nothing. Exits 0 when nothing
# was flagged, 1 when something was, and 2 when there is no SKILL.md.
# A clean result is not proof that the skill is safe to share.

set -u

dir=${1:?usage: check-skill.sh <skill-directory>}
skill=$dir/SKILL.md
problems=0

warn() { printf 'WARN  %s\n' "$1"; problems=1; }
ok() { printf 'ok    %s\n' "$1"; }

if [ ! -f "$skill" ]; then
  printf 'FAIL  no SKILL.md in %s\n' "$dir"
  exit 2
fi

front=$(awk 'NR == 1 && $0 != "---" { exit } NR > 1 && $0 == "---" { exit } NR > 1 { print }' "$skill")
name=$(printf '%s\n' "$front" | sed -n 's/^name:[[:space:]]*//p' | head -1)
desc=$(printf '%s\n' "$front" | sed -n 's/^description:[[:space:]]*//p' | head -1)
base=$(basename "$(cd "$dir" && pwd)")

if [ -z "$name" ]; then
  warn "no name in the frontmatter"
elif [ "$name" != "$base" ]; then
  warn "name '$name' does not match the directory name '$base'"
elif ! printf '%s' "$name" | grep -qE '^[a-z0-9]+(-[a-z0-9]+)*$'; then
  warn "name '$name' is not lowercase kebab-case"
else
  ok "name $name"
fi

if [ -z "$desc" ]; then
  warn "no description in the frontmatter; agents load a skill by its description"
elif [ "${#desc}" -gt 1024 ]; then
  warn "description is ${#desc} characters; the limit is 1024"
else
  ok "description, ${#desc} characters"
fi

lines=$(wc -l <"$skill")
if [ "$lines" -gt 500 ]; then
  warn "SKILL.md is $lines lines; move detail to references/ to stay under 500"
else
  ok "SKILL.md is $lines lines"
fi

# label|pattern pairs, matched case-insensitively against every text file.
checks=(
  'key-like token|(sk-[A-Za-z0-9_-]{16,}|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16})'
  'private key|BEGIN [A-Z ]*PRIVATE KEY'
  'secret assigned a value|(password|passwd|secret|token|api[_-]?key)[[:space:]]*[:=][[:space:]]*[^[:space:]<$]{6,}'
  'email address|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
  'cluster path|/N/(u|slate|project|scratch)/[A-Za-z0-9_-]+'
  'long numeric identifier|(^|[^0-9A-Za-z.:_/-])[0-9]{7,}([^0-9A-Za-z.]|$)'
)

files=$(find "$dir" -type f -size -2M -exec grep -Il . {} + 2>/dev/null)
for check in "${checks[@]}"; do
  label=${check%%|*}
  pattern=${check#*|}
  hits=$(printf '%s\n' "$files" | xargs -r grep -HniE "$pattern" 2>/dev/null | head -10)
  if [ -n "$hits" ]; then
    warn "possible $label; confirm each is a placeholder or safe to share:"
    printf '%s\n' "$hits" | cut -c1-160 | sed 's/^/        /'
  fi
done

[ "$problems" -eq 0 ] && ok "nothing flagged; read the skill before sharing it anyway"
exit "$problems"
