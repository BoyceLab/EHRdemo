# For Other Registries

If you run a patient registry that acquires EHR data through patient-directed SMART on FHIR (or is planning to), this pipeline pattern is adoptable. Here's how.

## Who this is for

Registries that:

- Collect EHR data from participants via OAuth 2.0 SMART on FHIR authorization (the "patient app" flow)
- Have a few hundred to a few thousand active participants
- Have at least one Python-fluent staff member, but no dedicated data engineering team
- Need a way for non-technical research staff to review individual participant records

## What carries over directly

| Universal challenge | Pipeline stage that addresses it |
|---|---|
| Heterogeneous payloads (CCDA / HTML / RTF / PDF mixed under uniform DocumentReference URLs) | Stage 2 — magic-byte format detection, per-format parsing |
| Subject references binding to source-EHR identifiers, not your canonical patient_id | Stage 4 — patient_identifier bridge derived from the audit table |
| Vendor-specific display-name omissions (e.g. Epic emitting LOINC codes without labels) | Stage 5 — built-in display-name lookup, extensible |
| Test or training patient records in the upstream EHR ingest | Stage 6 — config-file-driven exclusion list |
| Reviewer-friendly browsing of the merged record | The static HTML dashboard |

These apply regardless of disease area, registry size, or downstream storage technology.

## What you'll need to customize

### 1. Acquisition adapter

The pipeline assumes two pre-populated directories on disk: a flat directory of decoded clinical documents, and a parallel directory of FHIR Bundle JSON files. It does not perform the SMART on FHIR retrieval itself.

If you have an existing acquisition system (Databricks, Snowflake, S3 + Parquet, on-prem PostgreSQL, etc.), you write a thin adapter — typically 100-200 lines of Python or SQL — that produces the two directories from your retrieval logs.

### 2. Patient-identifier mapping queries

The pipeline expects two CSV files:

- `uuid_mapping.csv` — links each clinical document's UUID to a canonical `patient_id`
- `fhir_patient_mapping.csv` — links each external EHR identifier (typically an Epic patient identifier) to the same canonical `patient_id`

These come from SQL queries against your registry's own tables. The schema of the resulting CSVs is the contract; the source storage doesn't matter.

### 3. Display-name lookup

The built-in LOINC table covers the most common observations across patient populations: vital signs, basic and comprehensive metabolic panels, complete blood count, lipid and thyroid panels, coagulation studies, cardiac markers. For an ALS registry we added the ALSFRS-R code (LOINC 67131-4). Disease-specific registries should extend the lookup with the codes most central to their condition:

- Cardiology — cardiac-specific LOINC codes, ejection fraction measurements
- Oncology — NCI Thesaurus codes, tumor markers
- Endocrinology — additional thyroid, glucose, A1C variants
- Rare disease — disease-specific functional rating scales

Adding new codes is one-line entries in a Python dict.

### 4. Dashboard branding and copy

The HTML dashboard uses ALS TDI brand colors (Catalyst Purple `#93358C` and Foundation Navy `#1C355E`) and ARC Study-specific terminology. To rebrand:

- Edit the CSS variables at the top of `dashboard.html`
- Replace the welcome page copy
- Swap the institutional name in the header

The data-rendering logic (tabs, tables, source tags, filtering, exports) is generic and does not need changes.

## Estimated adoption effort

For a registry with one Python-fluent staff member:

| Task | Effort |
|---|---|
| Write acquisition adapter / downstream connector | 1-2 days |
| Write patient-identifier mapping SQL queries | 1 day |
| Extend display-name lookup with disease-specific codes | 1-2 days |
| Rebrand the dashboard | 1 day |
| End-to-end testing on real registry data | 2-4 days |
| **Total** | **~1-2 weeks** |

The pipeline is intentionally designed to avoid vendor-specific cloud services so that adoption does not require additional infrastructure spending or new business associate agreements.

## What to expect with your data

Based on our experience adapting the pipeline at ALS TDI:

- **Plan for >95% Epic-sourced data** at this point in the SMART on FHIR deployment timeline. Other vendors are coming online but represent a small minority of active patient-facing endpoints in 2026.
- **Expect a four-way split in document formats** — roughly 15% true C-CDA XML, 50% HTML fragments, 35% RTF notes, 5% PDF. Your specific mix will vary.
- **Patient-identifier reconciliation will surprise you.** The first patient table you find is rarely the right one. Verify linkage rate (it should be >95%) before assuming the mapping is complete.
- **Display-name coverage from raw exports is around 65-70%.** A small lookup table can recover most of the gap.
- **Plan to find test patients.** Add them to a `test_patients.txt` file as you spot them.

## How to start

You have two paths:

### Option A: Get the source code

The production pipeline is maintained internally at ALS TDI and is available to qualified collaborators on execution of a data use agreement. Email **[ARC data team contact]** with a short description of your registry and intended use.

### Option B: Build your own using the [JAMIA paper](pipeline.md) as a guide

Every stage of the pipeline is described in the methods of the JAMIA Brief Communication. With Python, pandas, openpyxl, pypdf, and the standard library, the full implementation is approximately 2,000 lines of code. Most of the value is in the design pattern, not the specific code.

## Stay in touch

If you adopt this pattern, we'd like to hear about your experience — both what worked and what didn't translate. Issues we documented (heterogeneous payloads, identifier provenance gaps, display-name omissions, test records) are likely to recur, but specific manifestations vary by registry. Aggregate experience across registries adopting patient-directed SMART on FHIR will inform improvements to the pattern over time.
