---
name: jetstream2
description: Use Jetstream2, the IU-hosted OpenStack research cloud allocated through ACCESS - what it is for and not for, how allocations work, what happens when one expires, flavor and GPU rules, protected-data restrictions, and how it fits as a gateway that sends heavy work to HPC. Use when considering Jetstream2 for a science gateway, an always-on service, interactive analysis, or a prototype, or when checking whether data may go there.
---

# Jetstream2

Verified 2026-10-01. IU KB claims cite their KB number. Claims from the
Jetstream2 documentation are marked **External**. Links are in Sources.

Jetstream2 is a cloud, not a cluster. Use it for services and interactive
work. Send large or high-throughput computation to an HPC system
(KB0024420).

## What it is for

Jetstream2 is an OpenStack research cloud. Its primary system is at IU, with
regional systems at Arizona State, Cornell, Hawai'i, and TACC (KB0024420). It
offers GPUs, large-memory nodes, virtual clusters, Heat and Terraform, and the
Exosphere web interface (KB0024420).

The KB names these uses (KB0024420):

- Interactive, smaller-scale, on-demand processing.
- Infrastructure for gateways and other always-on services.
- A back end for science gateways that compute locally or route jobs to HPC
  or HTC systems.
- Prototyping workflows before porting them to larger systems.

It is not appropriate for large-scale parallel or high-throughput computing
(KB0024420).

## Data restrictions

The KB's PHI and data-classification lists do not include Jetstream2
(KB0023515, KB0025747).

**External:** Jetstream2 users agree not to store data protected by federal
security or privacy laws, such as HIPAA or FERPA. The exception is storage the
responsible University administrator specifically authorizes. The system does
not meet those laws' requirements by default. Export-controlled data needs
prior approval from the University Export Compliance Office.

Treat Jetstream2 as not approved for PHI or biobank participant data. Ask
SecureMyResearch (securemyresearch@iu.edu) before planning otherwise
(KB0025362).

## Allocations

The KB says access comes only through ACCESS allocations (KB0024420). You must
be on a valid allocation, or be its PI (KB0024420).

**External:** the Jetstream2 documentation says access is "primarily" through
ACCESS. It also lists NAIRR Pilot allocations for AI research. ACCESS accounts
are free. ACCESS has four project types:

| ACCESS project type | Credit threshold |
| --- | --- |
| Explore ACCESS | 400,000 |
| Discover ACCESS | 1,500,000 |
| Accelerate ACCESS | 3,000,000 |
| Maximize ACCESS | Not awarded in credits |

After an award, exchange credits for Jetstream2 resources. Then add users to
the ACCESS allocation and to the Jetstream2 allocation (External).

**Open item:** the KB and the Jetstream2 documentation differ on whether
ACCESS is the only route. Check with IU Jetstream2 support if NAIRR matters.

IU researchers can get help preparing an allocation request from IU
Jetstream2 support (KB0024420). Research Technologies also offers limited
consulting on moving workflows to Jetstream2 (KB0023965).

### When an allocation expires

**External:** expiry follows a fixed schedule:

- At expiry, users lose access.
- After 10 days without renewal or extension, all instances are shelved.
- After 30 days, all instances, volumes, shares, and images are destroyed and
  cannot be recovered.

PIs get notices at 90, 60, and 30 days before expiry (External). Back up
anything that matters before the deadline.

## Flavors and maintenance

**External:**

- Run only `g3.*` flavors on the GPU resource.
- Run only `r3.*` flavors on the large-memory resource.
- Standard `m3.*` flavors on those resources may be deleted without warning.
- GPU resources have maintenance on the first Tuesday of each month, 7am to
  7pm Eastern. GPU instances may be stopped and started then.
- System status is at `https://jetstream.status.io`.

## Gateways

**External:** gateways on Jetstream2 must follow its acceptable use policy.
The documentation recommends that each gateway publish its own acceptable use
policy. TrustedCI publishes a sample.

A gateway is the pattern the `iu-research-computing-map` skill describes. The
portal runs on Jetstream2, and heavy jobs go to an HPC system. The KB does not
say how a Jetstream2 service authenticates to Quartz or Big Red 200. That is
an open item for HPS.

## Acknowledgment

Acknowledge Jetstream2 in papers and talks that relied on it. KB0022739
points to the citation guidance at
`https://jetstream-cloud.org/research/index.html#cite-jetstream`.

## Keep this file current

Re-read KB0024420 and the Jetstream2 policies page before relying on any
External claim. The Jetstream2 documentation changes faster than the KB.
Update the ACCESS thresholds from the Jetstream2 allocation overview when they
change. Record a resolved open item with its source.

## Sources

IU KB articles, read 2026-10-01. URL form:
`https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=<number>`.

- [KB0022739](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022739) Acknowledge use of Jetstream or Jetstream2 in your published work
- [KB0023515](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023515) UITS Research Technologies systems and services for researchers working with data containing HIPAA-regulated PHI
- [KB0023965](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023965) Research Technologies services
- [KB0024420](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024420) About Jetstream2
- [KB0025362](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025362) About SecureMyResearch
- [KB0025747](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025747) Types of sensitive institutional data appropriate for UITS Research Technologies services

External, read 2026-10-01:

- [Jetstream2 acceptable use policies](https://docs.jetstream-cloud.org/general/policies/)
- [Jetstream2 allocations overview](https://docs.jetstream-cloud.org/alloc/overview/)
- [Jetstream2 gateway policies](https://docs.jetstream-cloud.org/general/gateways/)
