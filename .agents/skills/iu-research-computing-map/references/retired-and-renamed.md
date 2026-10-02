# Retired and renamed IU research systems

Verified 2026-10-01. Do not plan work on any system marked retired.

The current KB names exactly two research supercomputers: Quartz and Big Red
200 (KB0025040, KB0023647). Any other cluster name in old documentation,
scripts, or hostnames refers to a retired system.

Retired KB articles drop out of KB search (KB0024722). The retirement dates
below therefore come from search-engine copies of archived KB pages. Those
archived URLs now return 404. Treat the dates as **External** and approximate.

## Retired systems

| System | Status | Evidence |
| --- | --- | --- |
| Big Red 3 | Retired. Search copy says retired from production on 2023-08-13. | Archived page "ARCHIVED: About Big Red 3 (Retired)"; absent from KB0025040 |
| Carbonate | Retired. Search copy says retired on 2023-12-17. | Archived page "ARCHIVED: About Carbonate at IU (Retired)"; absent from KB0025040 |
| Karst | Retired. No date recovered. | Archived page "ARCHIVED: About Karst at Indiana University (Retired)"; absent from KB0025040 |
| Mason | Retired. No date recovered. | Archived page "ARCHIVED: Mason at IU (Retired)"; absent from KB0025040 |
| Jetstream (the first system) | Succeeded by Jetstream2. | KB0024420 describes Jetstream2 as building on "the previous Jetstream project" |

Older notes and scripts may still use `carbonate` hostnames. Check that a host still resolves before using
it. A `carbonate` hostname may be a leftover name, or the host may be gone.

## Renamed services and partitions

| Old name | Current name | Source |
| --- | --- | --- |
| Research Database Complex (RDC) | Research Databases (ResDB) | KB0022656, KB0023697 |
| Quartz partition `gpu` | `v100`, renamed 2026-08-09 | KB0022436 |
| Quartz partition `hopper` | `h100-multi`, renamed 2026-08-09 | KB0022436 |
| `kb.iu.edu/d/<id>` article links | `servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=<KB number>` | Observed 2026-10-01: old links redirect to the KB home page |

Jobs that name the old Quartz partitions are rejected (KB0022436).

## Open items

- The KB itself no longer states retirement dates. Ask kb@iu.edu for the
  archived articles if a date matters (KB0024722).

## Keep this file current

Add a system here when it leaves KB0025040, with the date you noticed. Never
delete a row. A future agent may meet the old name in a script and needs to
learn it is gone.

## Sources

- [KB0022436](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022436) Run GPU-accelerated jobs on Quartz or Big Red 200 at IU
- [KB0022656](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0022656) Computing accounts at IU
- [KB0023647](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023647) Supercomputers for academic research at IU
- [KB0023697](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0023697) Research computing support at IU
- [KB0024420](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024420) About Jetstream2
- [KB0024722](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0024722) About archived content in the IU Knowledge Base
- [KB0025040](https://servicenow.iu.edu/kb?id=kb_article_view&sysparm_article=KB0025040) Hostnames of IU research supercomputers
- External: web search results for the archived pages above, 2026-10-01.
