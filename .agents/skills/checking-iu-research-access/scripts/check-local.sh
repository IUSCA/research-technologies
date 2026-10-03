#!/usr/bin/env bash
# Check, from your own computer, whether you can reach IU research systems.
# Read-only. Never prompts for a passphrase and never answers Duo.
#
# Usage: check-local.sh [iu-username]
#   The username defaults to $IU_USER, then $USER.
#
# Each line starts with OK, MISSING, or SKIP, followed by what to do next.

set -u
user="${1:-${IU_USER:-$USER}}"
clusters="quartz.uits.iu.edu bigred200.uits.iu.edu"

say() { printf '%-8s %s\n' "$1" "$2"; }

for host in $clusters; do
  if ! getent hosts "$host" >/dev/null 2>&1; then
    say MISSING "$host does not resolve. Check DNS or your network."
    continue
  fi
  if ! timeout 8 bash -c "exec 3<>/dev/tcp/$host/22" 2>/dev/null; then
    say MISSING "$host port 22 unreachable. Check your network or firewall."
    continue
  fi
  # BatchMode fails instead of prompting. It succeeds only through an
  # existing shared connection or an approved SSH key. env -u LC_ALL stops
  # ssh forwarding a locale the cluster lacks, which adds warnings.
  if out=$(timeout 15 env -u LC_ALL ssh -o BatchMode=yes -o ConnectTimeout=8 \
      "$user@$host" 'echo "$(hostname) $(id -un)"' 2>&1); then
    say OK "$host login works without a prompt: $out"
  else
    case "$out" in
      *"Permission denied"*)
        say MISSING "$host needs an interactive login (passphrase and Duo). A person must log in once; see SKILL.md." ;;
      *)
        say MISSING "$host ssh failed: $(printf '%s' "$out" | tail -1)" ;;
    esac
  fi
done

# REALLMS answers anonymous requests with 401, which still proves reachability.
code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 15 \
  https://reallms.rescloud.iu.edu/direct/v1/models || echo 000)
if [ "$code" = 000 ]; then
  say MISSING "REALLMS API unreachable from this network."
elif [ -z "${REALLMS_API_KEY:-}" ]; then
  say SKIP "REALLMS API reachable (HTTP $code). REALLMS_API_KEY is not set, so access was not checked."
else
  code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 15 \
    -H "Authorization: Bearer ${REALLMS_API_KEY}" \
    https://reallms.rescloud.iu.edu/direct/v1/models || echo 000)
  if [ "$code" = 200 ]; then
    say OK "REALLMS API accepts REALLMS_API_KEY."
  else
    say MISSING "REALLMS API rejected REALLMS_API_KEY (HTTP $code). See the using-reallms skill."
  fi
fi

if command -v openstack >/dev/null 2>&1; then
  if timeout 30 openstack token issue -f value -c expires >/dev/null 2>&1; then
    say OK "Jetstream2: the openstack client has working credentials."
  else
    say SKIP "Jetstream2: openstack client found, but no working credentials. See the jetstream2 skill."
  fi
else
  say SKIP "Jetstream2: no openstack client installed. Only needed for Jetstream2 work."
fi
