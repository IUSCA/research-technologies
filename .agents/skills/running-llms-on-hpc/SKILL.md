---
name: running-llms-on-hpc
description: Run open-weight LLMs inside Slurm jobs on IU's Quartz and Big Red 200 with the HPC LLM platform - the hpc_llm modules, the shared model collection and list-models, llama.cpp's llama-server as an OpenAI-compatible API inside a GPU job, fitting a model on one H100, measured load times and token rates, pointing a client or coding agent at the in-job server, and when to use REALLMS instead. Use when running batch inference, benchmarks, or model evaluations, making high-volume LLM calls, or needing a model that REALLMS rate limits or does not serve.
---

# Running LLMs on HPC

Verified 2026-10-22 against the IU Knowledge Base (KB). Each claim names its
KB article; links are in Sources. Statements marked **Observed** come from
the live system on the date given. **External** marks llama.cpp behavior
from its own documentation.

The HPC LLM platform puts open-weight models and llama.cpp on Quartz, Big
Red 200, and Research Desktop (KB0026530). UITS recommends it over the
REALLMS API for high-throughput work (KB0027272). It suits batch inference,
fine-tuning, and RAG experiments (KB0027473). Benchmarks and model
evaluations are batch inference too.

## When to use it, and when not

| Need | Use | Source |
| --- | --- | --- |
| Many requests, batch inference, evaluations | This platform, in a batch job | KB0027272, KB0027473 |
| A model REALLMS does not serve | This platform, or your own `.gguf` | KB0027470 |
| A chatbot, a web app, or an always-on API | REALLMS, not the clusters | KB0026530, KB0027473 |
| A few calls from code or a laptop | REALLMS | `using-reallms` |

The supercomputers "are not appropriate for hosting LLMs for web workflows
and interactive chatbots" (KB0026530). The server's API "only works within
the system or compute job it is set up on" (KB0027470). So every request
must come from inside the same job.

Data rules follow the system, not the model. Quartz allows PHI, and Big Red
200 does not; see `iu-research-computing-map` before sending sensitive data.

## Modules and models

Load `hpc_llm` for CPU partitions, and `hpc_llm/gpu` for GPU partitions
(KB0026530). Run `list-models` to see the collection (KB0027470). Models
live under `/N/scratch/datahub/nvme/llms` (KB0026530). The module sets
`QUANTIZED_MODEL_PATH`, `UNQUANTIZED_MODEL_PATH`, and `SOURCE_MODEL_PATH`.

**Observed 2026-10-22** on Quartz:

- `module load hpc_llm` loads 1.3, and `module load hpc_llm/gpu` loads 1.4.
  Version 1.5 exists for both; name it to get it.
- `hpc_llm/gpu` also loads `cudatoolkit/12.8` and `llamacpp/gpu/08242026`.
  It swaps `gnu/14.2.0` for `gnu/12.2.0`.
- `list-models` named 28 models, including `gpt-oss-20b`, `gpt-oss-120b`,
  `gemma-4-31B-it`, and `qwen3.5-35b-a3b`.
- Each quantized model is a directory with one `*_Q4_K_M.gguf`. Some also
  hold an `mmproj` vision file or an `mtp-` draft file.
- Weight sizes: `gpt-oss-20b` 15.8 GB, `gemma-4-31B-it` 18.7 GB, and
  `gpt-oss-120b` 87.9 GB.

Very new models may need a newer llama.cpp than the module provides. Build
your own in Slate or Slate-Scratch then (KB0027470). For vLLM, UITS ships a
build script, `examples/BuildVLLM.sh` in the platform directory
(KB0027473).

## Fit the model on the GPU

A Quartz GPU job gets one H100. **Observed 2026-10-22:** the `h100-single`
and `h100-debug` QOS allow at most 1 GPU, 24 CPUs, and 380000M of memory
per node. Asking for 2 GPUs failed at submission with `QOSMaxGRESPerNode`.
The GPU showed `NVIDIA H100 80GB HBM3`.

- A model under about 70 GB fits whole. Offload every layer with `-ngl 999`.
- A larger mixture-of-experts model, such as `gpt-oss-120b`, still runs.
  Keep some expert layers in CPU memory with `--n-cpu-moe <n>` (External:
  llama.cpp). Raise `<n>` until the server loads.
- Request enough CPU memory for whatever stays off the GPU.

**Observed 2026-10-22** on `h100-debug`: `gpt-oss-120b` loaded in 46
seconds with `--n-cpu-moe 8` and 160G of job memory. It generated 56
tokens per second and read prompts at 113. That is about a sixth of
`gpt-oss-20b`'s rate on the same GPU.

## Serve a model inside a job

[scripts/llm-server.sbatch](scripts/llm-server.sbatch) starts
`llama-server` on a free port and waits until it answers. It then runs your
command with `LLM_BASE_URL` and `OPENAI_BASE_URL` pointing at it, and stops
the server when the command ends:

```bash
sbatch -A <slurm-account-name> llm-server.sbatch gpt-oss-20b python3 my_batch.py
```

**Observed 2026-10-22** on `h100-debug`, submitted with `-p h100-debug`:
the script served `gpt-oss-20b` after 7 seconds, and a chat completion
through `OPENAI_BASE_URL` answered. The job then ended cleanly.

Any OpenAI-compatible client works against that URL, including coding
agents that accept a custom OpenAI-compatible provider. The server checks
no key, so send any placeholder. Run the client inside the same job.

**Observed 2026-10-22** on `h100-debug`, `gpt-oss-20b`:

- The server was ready 7 to 11 seconds after starting.
- `/v1/models` listed the alias, and `/v1/chat/completions` answered.
- Generation ran at 310 tokens per second, and prompt reading at 540 to
  670.
- A request with a `tools` list returned a proper tool call, with or
  without `--jinja`. The chat template engine that tool calls need is on
  by default (External: llama.cpp).

**Observed 2026-10-23** on `h100-single`, `gemma-4-31B-it` (`Q4_K_M`),
submitted with `--export=ALL,LLM_CTX=131072,LLM_SERVER_ARGS='-np 1'`:

- The job waited about 2 minutes in the queue, with 247 jobs pending on
  the partition. The server was ready 15 to 17 seconds after starting.
- `-np 1` gave one slot holding the whole 131072-token context; the
  server log read `n_slots = 1, n_ctx_slot = 131072`.
- 59 recorded agent requests, replayed one at a time, had prompts of
  about 10,800 tokens at the median and none over 30,000. Generation ran at
  67 tokens per second, and prompt reading at about 1,650.
- Every tool call's arguments parsed as JSON.

## Faster than REALLMS only for throughput

The in-job server is not faster per request. **Observed 2026-10-23:** the
same 59 requests took a median of 6.4 seconds on REALLMS's
`gemma-4-31B-it` and 9.5 seconds in the job. In total they took 754 seconds
and 985 seconds. The REALLMS run was on a Friday afternoon.

- The gain is throughput: no shared rate limit, and several requests at
  once with more `-np` slots. Measure your own concurrency before counting
  on it.
- The models differ. The platform serves 4-bit `.gguf` files through
  llama.cpp, and REALLMS serves through vLLM. A result measured in a job
  does not predict what the same model ID does on REALLMS.
- Not every REALLMS model is in `list-models`. Check before planning a
  comparison.

## Run a coding agent against it

A coding agent can run inside the job, pointed at `LLM_BASE_URL` as a
custom OpenAI-compatible provider. Give it the model's context length,
such as 65536.

- Keep secrets out of the job's environment. **Observed 2026-10-22:** an
  agent asked to check access ran `env` and printed an API key from its
  environment into its answer. Have tools read keys from files instead.
- The agent writes files where it runs. Start it in a scratch directory.
- **Observed 2026-10-22**, one run each: `gpt-oss-20b` and `gpt-oss-120b`
  answered in 5 to 26 seconds. Neither loaded the access-check skill this
  repository expected; a larger REALLMS model did. Measure your own task
  before trusting a small local model with it.

## Run it interactively

For a short test, take a GPU shell first, then start the server in the
background inside it:

```bash
srun -p h100-debug -A <slurm-account-name> --gpus-per-node 1 --cpus-per-task 24 --mem 160G --time 1:00:00 --pty bash
module load hpc_llm/gpu
llama-server -m "$QUANTIZED_MODEL_PATH/gpt-oss-20b/gpt-oss-20b_Q4_K_M.gguf" --port 8080 -ngl 999 &
curl -s http://127.0.0.1:8080/v1/models
```

`h100-debug` allows one hour (`submitting-hpc-jobs`). Use `h100-single` for
longer runs.

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| `QOSMaxGRESPerNode` at submission | More than one GPU requested on `h100-single` or `h100-debug` (Observed 2026-10-22) |
| `llama-server: command not found` | `hpc_llm/gpu` not loaded in the job, or loaded on a login node where it was later purged |
| The server exits while loading | The model does not fit. Lower `-ngl`, add `--n-cpu-moe`, or pick a smaller model |
| `curl` cannot connect | The request came from outside the job, or used the wrong port (KB0027470) |
| A brand-new model fails to load | The module's llama.cpp is too old; build your own (KB0027470) |

## Support

Ask the Research Applications and Deep Learning team at
`https://projects.rt.iu.edu/help/?queue=radl` (KB0026530). See
`getting-help-from-research-technologies` for what to send.

## Keep this file current

Re-run `module spider hpc_llm` and `list-models` each quarter, and after
monthly maintenance. Update the observed versions, model names, and sizes.
Re-run `scripts/llm-server.sbatch` with a small model and update the
measured rates. Re-time the REALLMS comparison when either side changes.
Re-read KB0026530, KB0027470, and KB0027473 for module names and
recommended uses.

## Sources

All IU KB articles, read 2026-10-22. URL form:
`https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=<number>`.

- [KB0026530](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0026530) Access large language models with the HPC LLM platform on IU's research supercomputers
- [KB0027272](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0027272) About the Research and Academic LLM Services (REALLMS) API at IU
- [KB0027470](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0027470) Use HPC LLM utilities to run large language models on IU's research supercomputers
- [KB0027473](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0027473) Common LLM workflows on IU's research supercomputers

External: [llama.cpp server documentation](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md), read 2026-10-22.
