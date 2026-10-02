#!/usr/bin/env bash
# Print the facts about an IU Slurm cluster that the system itself reports:
# partitions, node and GPU counts, time limits, QOS limits, and array limits.
# Run it on a login node. It is read-only and light enough for a login node.
#
#   ssh <user>@quartz.uits.iu.edu 'bash -s' < describe-cluster.sh
#
# The live system is the judge for these facts. When this output disagrees
# with a skill or with the KB, record the output in the skill as Observed,
# with the date and host printed below.

set -u
echo "# $(hostname -f 2>/dev/null || hostname)  $(date -Iseconds)"

echo
echo "## Partitions (name, availability, time limit, nodes, CPUs/node, memory/node MB, GRES)"
sinfo -h -o '%R|%a|%l|%D|%c|%m|%G' | sort -u | column -t -s'|'

echo
echo "## Distinct nodes"
echo "all:      $(sinfo -h -N -o '%N' | sort -u | wc -l)"
echo "with GPU: $(sinfo -h -N -o '%N %G' | awk '$2 ~ /gpu/ {print $1}' | sort -u | wc -l)"

echo
echo "## GPUs by type (distinct nodes x GPUs per node)"
sinfo -h -N -o '%N %G' | sort -u | awk '
  $2 ~ /gpu/ {
    n = split($2, parts, ",")
    for (i = 1; i <= n; i++) {
      if (parts[i] !~ /^gpu/) continue
      g = parts[i]; sub(/\(.*/, "", g)
      k = split(g, f, ":")
      type = (k >= 3) ? f[2] : "gpu"; count = f[k] + 0
      nodes[type]++; gpus[type] += count
    }
  }
  END { for (t in nodes) printf "%-10s nodes=%d gpus=%d\n", t, nodes[t], gpus[t] }'

echo
echo "## Partition limits"
scontrol show partition -o | tr ' ' '\n' |
  grep -E '^(PartitionName|MaxTime|DefaultTime|MaxNodes|MaxCPUsPerNode|DefMemPerCPU|MaxMemPerNode|QoS|AllowAccounts)=' |
  paste -sd' ' | sed 's/ PartitionName=/\nPartitionName=/g'

echo
echo "## Scheduler limits"
scontrol show config | grep -E '^(MaxArraySize|MaxJobCount|MaxStepCount|MaxTasksPerNode|DefMemPerCPU|SlurmctldVersion|SLURM_VERSION) '

echo
echo "## QOS limits"
sacctmgr -nP show qos format=Name,MaxWall,MaxTRESPU,MaxJobsPU,MaxSubmitPU |
  awk -F'|' 'BEGIN {print "Name|MaxWall|MaxTRESPerUser|MaxJobsPerUser|MaxSubmitPerUser"} {print}' |
  column -t -s'|'
