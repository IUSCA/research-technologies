#!/usr/bin/env bash
# Read-only check of a research code repository before a run or a push.
#
# Usage: check-repo.sh [directory]
#
# Reports the current commit, uncommitted changes, tracked files that look
# like data, secrets, or large files, and where each remote points. Changes
# nothing. Exits 0 when nothing needs attention, 1 when something does, and
# 2 when the directory is not in a git repository.

set -u

dir=${1:-.}
large_bytes=$((10 * 1024 * 1024))
problems=0

warn() { printf 'WARN  %s\n' "$1"; problems=1; }
ok() { printf 'ok    %s\n' "$1"; }

if ! top=$(git -C "$dir" rev-parse --show-toplevel 2>/dev/null); then
  printf 'FAIL  %s is not in a git repository. Run git init there first.\n' "$dir"
  exit 2
fi
cd "$top" || exit 2
printf 'repo  %s\n' "$top"

if git rev-parse --verify -q HEAD >/dev/null; then
  ok "commit $(git describe --always --dirty) on branch $(git branch --show-current)"
else
  warn "no commits yet"
fi

if [ -z "$(git config user.name)" ] || [ -z "$(git config user.email)" ]; then
  warn "user.name or user.email is not set; commits will not say who made them"
fi

changes=$(git status --porcelain | wc -l)
if [ "$changes" -gt 0 ]; then
  warn "$changes uncommitted or untracked paths; results from this tree cannot be traced to a commit"
else
  ok "working tree is clean"
fi

[ -f .gitignore ] || warn "no .gitignore; data and outputs are easy to commit by mistake"

data_re='\.(csv|tsv|txt\.gz|parquet|feather|arrow|h5|hdf5|nc|zarr|npy|npz|mat|rds|rdata|sav|dta|sas7bdat|xlsx?|sqlite|db|pkl|pickle|pt|ckpt|safetensors|bam|cram|sam|vcf|bcf|fastq|fq|fa|fasta|bed|bigwig|bw|nii|dcm|svs|ndpi|tiff?|zip|tar|tgz|gz|bz2|xz|7z)$'
secret_re='(^|/)(\.env(\..*)?|.*\.pem|.*\.key|id_rsa|id_ed25519|.*api[-_]?key.*|.*secret.*|.*token.*|\.netrc|credentials.*)$'

data_files=$(git ls-files | grep -iE "$data_re" || true)
if [ -n "$data_files" ]; then
  warn "tracked files that look like data; confirm each is small, public example data:"
  printf '%s\n' "$data_files" | head -20 | sed 's/^/        /'
fi

secret_files=$(git ls-files | grep -iE "$secret_re" || true)
if [ -n "$secret_files" ]; then
  warn "tracked files that look like secrets; remove them and rotate the secret:"
  printf '%s\n' "$secret_files" | head -20 | sed 's/^/        /'
fi

big_files=$(git ls-files -z | xargs -0 -r stat -c '%s %n' 2>/dev/null |
  awk -v max="$large_bytes" '$1 > max { printf "%d MB  %s\n", $1 / 1048576, substr($0, index($0, " ") + 1) }')
if [ -n "$big_files" ]; then
  warn "tracked files over 10 MB:"
  printf '%s\n' "$big_files" | head -20 | sed 's/^/        /'
fi

remotes=$(git remote -v | awk '$3 == "(push)" { print $1, $2 }')
if [ -z "$remotes" ]; then
  printf 'note  no remote; the only copy of the history is in %s\n' "$top"
else
  while read -r name url; do
    case $url in
      *github.iu.edu*) printf 'note  remote %s is GitHub:IU (%s): Public and University-Internal only\n' "$name" "$url" ;;
      *github.com*) printf 'note  remote %s is GitHub.com (%s): check the repository visibility\n' "$name" "$url" ;;
      *) printf 'note  remote %s is %s\n' "$name" "$url" ;;
    esac
  done <<<"$remotes"
  if git rev-parse --verify -q '@{upstream}' >/dev/null; then
    ahead=$(git rev-list --count '@{upstream}..HEAD')
    [ "$ahead" -gt 0 ] && printf 'note  %s commits not pushed to %s\n' "$ahead" "$(git rev-parse --abbrev-ref '@{upstream}')"
  fi
fi

exit "$problems"
