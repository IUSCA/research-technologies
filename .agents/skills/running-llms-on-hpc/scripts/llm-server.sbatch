#!/bin/bash
# Serve one HPC LLM platform model inside a Quartz GPU job, then run a
# command against it. The server's OpenAI-compatible API answers only inside
# this job (KB0027470), at the address in LLM_BASE_URL.
#
# Replace SLURM_ACCOUNT with the Slurm Account Name from RT Projects, or pass
# -A on the command line. Submit from the directory that should get the logs:
#
#   sbatch llm-server.sbatch <model> <command> [args...]
#   sbatch llm-server.sbatch gpt-oss-20b python3 my_batch.py
#
# <model> is a name from list-models. The command sees these variables:
#   LLM_BASE_URL     http://127.0.0.1:<port>/v1
#   LLM_MODEL        the model name, as the API reports it
#   OPENAI_BASE_URL  the same URL, for OpenAI clients
#   OPENAI_API_KEY   a placeholder; the server checks no key
#
# Optional settings, passed with sbatch --export=ALL,NAME=value:
#   LLM_CTX          context length in tokens (default 65536)
#   LLM_SERVER_ARGS  more llama-server options, such as "--n-cpu-moe 16"
#                    for a model larger than one GPU

#SBATCH -J llm-server
#SBATCH -p h100-single
#SBATCH -A SLURM_ACCOUNT
#SBATCH -o llm-server_%j.txt
#SBATCH --nodes=1
#SBATCH --gpus-per-node=1
#SBATCH --cpus-per-task=24
#SBATCH --mem=160G
#SBATCH --time=02:00:00

set -u
model=${1:?usage: sbatch llm-server.sbatch <model> <command> [args...]}
shift
[ $# -gt 0 ] || { echo "usage: sbatch llm-server.sbatch <model> <command> [args...]"; exit 2; }

module load hpc_llm/gpu

# The main weights: the model's .gguf that is not a vision projector or a
# multi-token-prediction draft.
weights=$(ls "$QUANTIZED_MODEL_PATH/$model"/*.gguf 2>/dev/null | grep -v -e mmproj -e mtp- | head -1)
[ -n "$weights" ] || { echo "no .gguf for '$model' in $QUANTIZED_MODEL_PATH; run list-models"; exit 1; }

# A port from the job ID, so jobs sharing a node do not collide.
port=$((20000 + SLURM_JOB_ID % 20000))
log=llm-server_${SLURM_JOB_ID}.log
start=$(date +%s)
# shellcheck disable=SC2086  # LLM_SERVER_ARGS is a list of options
llama-server -m "$weights" --alias "$model" --host 127.0.0.1 --port "$port" \
  -ngl 999 -c "${LLM_CTX:-65536}" ${LLM_SERVER_ARGS:-} > "$log" 2>&1 &
server=$!
trap 'kill $server 2>/dev/null; wait $server 2>/dev/null' EXIT

until curl -sf "http://127.0.0.1:$port/health" > /dev/null; do
  if ! kill -0 "$server" 2>/dev/null; then
    echo "llama-server exited while loading; last lines of $log:"
    tail -20 "$log"
    exit 1
  fi
  sleep 2
done
echo "$model ready on port $port after $(( $(date +%s) - start ))s"

export LLM_BASE_URL=http://127.0.0.1:$port/v1 LLM_MODEL=$model
export OPENAI_BASE_URL=$LLM_BASE_URL OPENAI_API_KEY=none
"$@"
