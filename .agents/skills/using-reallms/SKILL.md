---
name: using-reallms
description: Use REALLMS, IU's Research and Academic LLM Services - the on-premises REALLMS Chat and the OpenAI-compatible REALLMS API (IU LLM API). Covers who may use it, getting an API key through an RT Projects allocation, the base URL, Python and curl usage, keeping keys out of code, live model list discovery, which data classifications and PHI are allowed, rate limits and when to run LLMs on Quartz or Big Red 200 instead, support, and 401 troubleshooting. Use when calling an LLM from IU research code, choosing an IU LLM service for research data, or debugging a REALLMS request.
---

# Using REALLMS

Verified 2026-10-01 against the IU Knowledge Base (KB). Each claim names its
KB article; links are in Sources. Statements marked **Observed** come from
testing the live service on the date given.

REALLMS is IU's free, on-premises LLM service for research, teaching, and
administration (KB0026671, KB0027412). The live API is the judge of models and
behavior.

## Chat or API

REALLMS has two parts (KB0026671):

| Part | What it is | Who may use it | Source |
| --- | --- | --- | --- |
| REALLMS Chat | Open WebUI chat at `https://reallms.rescloud.iu.edu/` | Anyone with an IU account, no separate account | KB0027284 |
| REALLMS API | OpenAI-compatible API, LiteLLM routing, vLLM back end | Holders of a REALLMS API allocation in an RT Project | KB0027272, KB0027412 |

KB0026507 says the API is for IU researchers, faculty, and staff. Use Chat for
interactive work. Use the API from code, pipelines, and services.

The API is in beta, with possible unexpected downtime and changes (KB0027272).

## Get an API key

1. A PI creates an RT Project at `https://projects.rt.iu.edu` (KB0024132).
   The PI must be IU faculty or staff (KB0024132).
2. Request a "REALLMS API" allocation inside the project (KB0027272, KB0025604,
   KB0024132). Expect a reply within two business days (KB0024132).
3. Once approved, open the allocation's page and create a key (KB0027272).

Each key belongs to one person (KB0027272). Add teammates to the project and
allocation, and have each create their own key (KB0027272). Research projects
renew each June, and allocations expire with their project (KB0024132).

See the `managing-rt-projects` skill for RT Projects details.

## Keep the key secret

These rules are house practice, not KB policy:

- Store the key in an environment variable. This skill uses `REALLMS_API_KEY`
  as a convention.
- Load it from a git-ignored `.env` file or a secret manager.
- Never commit a key, paste one into a ticket, or print one in logs.
- Never echo the variable to check it. Test `[ -n "$REALLMS_API_KEY" ]`
  instead.
- If a key leaks, delete it on the allocation page and create a new one.

## Endpoint and usage

The base URL is `https://reallms.rescloud.iu.edu/direct/v1` (KB0027272).
**Observed 2026-09-21:** it answers from the public internet without the IU
VPN. **Observed 2026-10-01:** a keyless request to `/models` returns 401.

KB0027272 lists these endpoints: `/models`, `/chat/completions`,
`/completions`, `/embeddings`, `/rerank`, `/audio/transcriptions`, and
`/images/generations`. IU keeps more examples in the REALLMS API examples
repository at `https://github.iu.edu/ResearchApplicationsDeepLearning/REALLMS-API-examples`
(KB0027272).

From a shell (KB0027272 shows the same calls):

```bash
curl -sS https://reallms.rescloud.iu.edu/direct/v1/models \
  -H "Authorization: Bearer ${REALLMS_API_KEY}"

curl -sS https://reallms.rescloud.iu.edu/direct/v1/chat/completions \
  -H "Authorization: Bearer ${REALLMS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"model": "<model-id>", "messages": [{"role": "user", "content": "Why is the sky blue?"}]}'
```

From Python, any OpenAI-compatible client works with this base URL. With the
`openai` package:

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://reallms.rescloud.iu.edu/direct/v1",
    api_key=os.environ["REALLMS_API_KEY"],
)
reply = client.chat.completions.create(
    model="<model-id>",  # from /models, never from memory
    messages=[{"role": "user", "content": "Why is the sky blue?"}],
)
print(reply.choices[0].message.content)
```

## Discover models; do not trust a list

Model IDs change without notice. **Observed 2026-09-21:** previously
documented default models were withdrawn in September 2026. The KB promises
30 days' notice before a model is removed (KB0027412). It promises three
months for the one model labeled long-term supported (KB0027412).

KB0027272 listed these chat and completion models on 2026-10-01:
`gemma-4-31B-it`, `glm-5.2`, `gpt-oss-120b`, `granite-docling-258m`, and
`Qwen3-Coder-Next`. Treat that as a hint only.

**Observed 2026-10-01 with `scripts/reallms_models.py`:** `/models` listed
those five plus `Qwen3-ASR-1.7B`, `Qwen3-Embedding-8B`, `Qwen3-Reranker-8B`,
`embeddinggemma-300m`, `whisper`, and `z-image-turbo`. `gpt-oss-120b`
answered a real completion.

Before pinning a model in code or a config:

1. List live models: `scripts/reallms_models.py` (standard library only).
2. Send one real completion: `scripts/reallms_models.py --check <model-id>`.
3. Pin the ID in one configurable place, not scattered through code.

A model can appear in `/models` and still fail on a request. Step 2 catches
that. Request a new model with the REALLMS Model Suggestion Form
(KB0026671): `https://uitsradl-fireform.eas.iu.edu/online/form/index/reallms`.

## Data classification and acceptable use

REALLMS is approved for Restricted and Critical data, including PHI
(KB0026817, KB0027272). KB0026507 also lists Public and University-internal.
It is one of two IU-managed AI developer toolkits (KB0026817).

Users must follow IT-01 (appropriate use) and IT-02 (misuse and abuse)
(KB0027412). Users must watch their primary IU email for usage notices
(KB0027412). Data sent to the API is not stored (KB0027412). Chats persist in
the Chat app, except temporary chats (KB0027412).

Research data is institutional data unless an agreement assigns ownership to a
sponsor or partner (KB0026817). The lead investigator decides whether a data
agreement constrains AI use (KB0026507). Ask the Data Steward for Research
Data at datard@iu.edu when unsure (KB0026817, KB0027272).

Do not send REALLMS-approved data to public or personal AI accounts. Those are
not approved for any institutional data (KB0026507).

**Open item:** KB0026507 excludes "research data with contractual,
regulatory, or legal constraints" from REALLMS. KB0026817, KB0027272, and
KB0027412 approve Critical data and PHI without that exception. Until resolved,
check any data use agreement or IRB terms before sending such data.

## High throughput: use the supercomputers instead

Heavy API use may be rate-limited (KB0027272, KB0027412). For high throughput,
UITS recommends the HPC LLM platform on Quartz and Big Red 200 (KB0027272).

Use the supercomputers for batch inference, fine-tuning, and RAG experiments
(KB0027473, KB0026530). They are not for hosting chatbots or web workflows;
use the REALLMS API for those (KB0027473).

On the supercomputers, load `hpc_llm` or `hpc_llm/gpu` (KB0026530). Run
`list-models` to see local models (KB0027470). `llama-server` gives a REST API
reachable only inside its own job (KB0027470). Submit work with a Slurm
Account Name from RT Projects (KB0027473). See the `submitting-hpc-jobs`
skill.

**Open item:** KB0027473 writes the module as `hpc_llm/gpu/` and as
`hpc-llm/gpu`. KB0026530 writes `hpc_llm/gpu`. Run `module spider hpc` on a
cluster; the system settles it.

## Support

Ask the UITS REALLMS team through `https://projects.rt.iu.edu/help/?queue=racs`
(KB0026671, KB0027272, KB0027412). They monitor it Monday to Friday, 8am to
5pm, except holidays (KB0027412). They respond to email within two business
days (KB0027412).

The IU HPC and AI User Community Slack has a `#reallms` channel (KB0026671,
KB0024086). For Chat knowledge collections, contact RADL at
`https://projects.rt.iu.edu/help/?queue=radl` (KB0027284).

Maintenance falls on the second Sunday of each month, 7am to 7pm Eastern
(KB0027412). REALLMS is typically down less than two hours then (KB0027412).
Check the date before reporting an outage.

**Open item:** KB0027473 and KB0026530 send LLM questions to the RADL queue.
The REALLMS articles use the `racs` queue. Use `racs` for REALLMS itself.

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| 401 `No api key passed in.` | No `Authorization` header was sent (Observed 2026-10-01). |
| 401 ``Malformed API Key passed in. Ensure Key has `Bearer ` prefix.`` | The key variable is empty or unset, so only `Bearer ` was sent (Observed 2026-09-21, 2026-10-01). |
| 401 `LiteLLM Virtual Key expected ... expected to start with 'sk-'` | The value is not shaped like a REALLMS key (Observed 2026-10-01). Check which variable you loaded. |
| Model not found, or a model that worked now fails | The model was withdrawn or renamed. List `/models` again. |
| Slow or refused responses under heavy use | Rate limiting (KB0027412). Back off, or move to the HPC LLM platform. Record the actual status code here once seen. |
| Errors on a second Sunday | Scheduled maintenance (KB0027412). |
| Key stopped working in July | The RT Project may have expired (KB0024132). Check its status in RT Projects. |

## Open items

- The KB does not say which model is the long-term supported one
  (KB0027412). Ask the REALLMS team before relying on any model past 30 days.
- The KB states no rate-limit numbers or key lifetime.
- The KB does not say whether students may request the allocation. KB0024132
  requires a faculty or staff PI for the project.
- Data classification, module name, and support queue: see items above.

## Keep this file current

Re-run `scripts/reallms_models.py` and update the observed lines when they
change. Re-read KB0027272 for the base URL and endpoint list each time. Date
every observation, and keep it marked **Observed**. Close an open item only
with a citation. When the KB and an observation disagree, record both.

## Sources

All IU KB articles, read 2026-10-01. URL form:
`https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=<number>`.

- [KB0024086](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024086) About the IU HPC and AI User Community Slack
- [KB0024132](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024132) Use RT Projects to request and manage access to specialized Research Technologies resources
- [KB0025604](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025604) About RT Projects at IU
- [KB0026507](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0026507) Generative AI tools at IU
- [KB0026530](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0026530) Access large language models with the HPC LLM platform on IU's research supercomputers
- [KB0026671](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0026671) About Research and Academic LLM Services (REALLMS) at IU
- [KB0026817](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0026817) Acceptable use of AI tools with IU research data
- [KB0027272](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0027272) About the Research and Academic LLM Services (REALLMS) API at IU
- [KB0027284](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0027284) About the Research and Academic LLM Services (REALLMS) Chat at IU
- [KB0027412](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0027412) Research and Academic LLM Services (REALLMS): Terms of service
- [KB0027470](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0027470) Use HPC LLM utilities to run large language models on IU's research supercomputers
- [KB0027473](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0027473) Common LLM workflows on IU's research supercomputers
