# 

<div class="als-hero" markdown>

# ARC <em>Clinical Browser</em>

**A reproducible, local-first ETL and visualization pipeline for patient-directed SMART on FHIR clinical records.**

Closing the analytics gap for patient registries that acquire EHR data via OAuth 2.0 but lack in-house data engineering capacity.

[Try the live demo](demo.md){ .als-button }
[How the pipeline works](pipeline.md){ .als-button .secondary }

<div class="tagline">An ALS Therapy Development Institute project · Dedicated to curing ALS</div>

</div>

## What this is

The **ARC Clinical Browser** is the analytics layer for the [ARC Study](https://www.als.net/arc/), a long-running natural-history study of amyotrophic lateral sclerosis (ALS) operated by the [ALS Therapy Development Institute](https://www.als.net/). Participants authorize ALS TDI through a patient-directed SMART on FHIR OAuth 2.0 flow, granting access to their longitudinal records across the multiple health systems where they receive care.

The pipeline takes the heterogeneous output of those retrievals — a mixture of CCDA documents, embedded HTML and RTF clinical notes, PDF reports, and FHIR Bundle resources — and converts it into a single, browser-loadable viewer that non-technical research staff can use to review every patient's full clinical record.

<div class="als-stats" markdown>

<div class="als-stat" markdown>
<div class="als-stat-num">22,686</div>
<div class="als-stat-label">Source Files Processed</div>
</div>

<div class="als-stat" markdown>
<div class="als-stat-num">109,599</div>
<div class="als-stat-label">FHIR Resources Extracted</div>
</div>

<div class="als-stat" markdown>
<div class="als-stat-num">98.6%</div>
<div class="als-stat-label">Patient-ID Linkage Rate</div>
</div>

<div class="als-stat" markdown>
<div class="als-stat-num">~13 min</div>
<div class="als-stat-label">End-to-End Runtime</div>
</div>

</div>

## Why it exists

Patient-directed SMART on FHIR has substantially expanded the data acquisition options available to patient registries — including non-network-affiliated registries that previously could not feasibly aggregate longitudinal records across multiple health systems. After the implementation deadlines of the 21st Century Cures Act, all certified EHRs in the United States now expose a standardized patient-facing API, allowing registries to retrieve clinical records on a participant's behalf with their explicit consent.

Acquiring data, however, is not the same as having usable data. The artifacts that come back are heterogeneous: CCDA documents, FHIR Bundles, and embedded narrative documents in formats determined by the source EHR vendor. Each must be decoded, parsed, deduplicated, joined to a canonical patient identifier, and rendered in a form clinicians and research staff can review. **Most patient registries don't have the in-house data engineering teams to do this work.** That is the analytics gap this pipeline closes.

## Quick start

!!! tip "If you just want to see what it looks like"
    The [Live Demo page](demo.md) embeds the dashboard with 50 fully-synthetic patients. No setup, no PHI, no signup.

!!! info "If you run a patient registry and want to adopt this pattern"
    Read [About the Pipeline](pipeline.md) for the architecture, then [For Other Registries](adopt.md) for the adaptation steps. Total adoption effort for a Python-fluent staff member is approximately one to two weeks.

## Where to learn more

- :material-information-outline: **[Live Demo](demo.md)** — try the dashboard with synthetic data
- :material-cog-outline: **[About the Pipeline](pipeline.md)** — six-stage architecture and design notes
- :material-share-variant-outline: **[For Other Registries](adopt.md)** — adaptation and adoption guide
- :material-shield-lock-outline: **[Privacy & Synthetic Data](privacy.md)** — what's safe to do with the demo

---

*This site documents a project of the [ALS Therapy Development Institute](https://www.als.net/), the world's largest nonprofit research institute focused solely on ALS treatments.*
