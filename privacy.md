# Privacy & Synthetic Data

This site is a public demonstration. **No real patient information is present anywhere in this repository or in the deployed site.** Here's exactly what we do and don't include.

## What's in the demo data

The 50-patient cohort embedded in the [Live Demo](demo.md) is generated from scratch by the `generate_synthetic_data.py` script in this repository. Specifically:

| Field | Source |
|---|---|
| First name | Drawn from a 50-name fictional list (`Alex`, `Bailey`, `Cameron`, ...) |
| Last name | Drawn from a 50-name fictional list, with `[DEMO]` suffix appended to every name |
| Patient ID | Random UUID generated at script run-time |
| MRN | Random 10-digit string |
| Date of birth | Random within plausible adult ALS demographics (1946–1981) |
| Gender | Random (male / female) |
| LOINC codes | Real public reference data (e.g., `8480-6` for systolic blood pressure) |
| ICD-10-CM codes | Real public reference data (e.g., `G12.21` for ALS) |
| RxNorm codes | Real public reference data (e.g., `83366` for riluzole) |
| CPT codes | Real public reference data (e.g., `95860` for EMG) |
| Lab values | Random within typical clinical ranges |
| ALSFRS-R trajectories | Algorithmically generated to mimic typical ALS progression (~1 point/month decline) |
| FVC trajectories | Algorithmically generated to mimic typical respiratory decline |
| Procedure timing | Algorithmically sequenced (EMG/NCS at diagnosis, PEG for bulbar onset, etc.) |
| Narrative documents | Single boilerplate text marked `[SYNTHETIC DEMO RECORD]` |

The clinical codes are public reference data — LOINC, ICD-10, RxNorm, and CPT are all maintained by national and international standards bodies and published openly. They are not patient-identifying.

## What's not in the demo data

We deliberately did **not** include any of the following from the real ARC dataset:

- Real patient names, dates of birth, or medical record numbers
- Real clinical narratives, discharge summaries, progress notes, or any text from any real patient's chart
- Real lab values, imaging results, pathology reports, or other clinical observations
- Real medication histories, prescription details, or treatment timelines
- Real provider names, encounter dates, or institutional identifiers
- Real demographics (race, ethnicity, address, contact information) — these fields are blank in the demo data

## How the demo is marked

Multiple layers of marking communicate that this is a demo:

1. **A purple striped watermark** runs across the top of every page of the dashboard, reading "DEMO WITH SYNTHETIC DATA · NO REAL PATIENT INFORMATION"
2. **Every patient last name** carries a `[DEMO]` suffix
3. **Every clinical narrative** begins with `[SYNTHETIC DEMO RECORD — not real clinical content]`
4. The dashboard **brand-sub label** in the sidebar reads "Demo · Synthetic Data Only"
5. The **welcome page** explicitly states the data is synthetic
6. The **README** and this site repeat the synthetic-data warning

## What the production pipeline looks like

In production at ALS TDI, the same dashboard runs against a real ARC participant dataset. That dataset contains protected health information and is **never** distributed publicly. Specifically:

- Real ARC participant data is stored on encrypted, organizationally-managed storage (Databricks workspace, ALS TDI organizational Box)
- Sharing across the research team uses ALS TDI's enterprise Box with named-user permissions, inheriting an existing Business Associate Agreement
- Source code for the pipeline is maintained internally and is not in this repository
- All processing runs locally on analyst workstations; no PHI is transmitted to external services
- The ARC Study operates under IRB oversight; analytic activities fall within the approved protocol

## Reusing the demo for other purposes

The synthetic data and the demo dashboard are released for educational and reference purposes. You're welcome to:

- Adapt the dashboard HTML and CSS for your own registry (see [For Other Registries](adopt.md))
- Use the synthetic data generator as a template for your own demo
- Cite this work in academic publications via the forthcoming JAMIA Brief Communication

The production pipeline source code is **not** included here. To request access for collaboration, contact the ARC Data Team at ALS TDI.

## Reporting concerns

If you believe any content in this repository or on this site contains real patient information that should not be public, please contact us immediately:

- Email: **[ARC data team contact]**
- ALS Therapy Development Institute, 480 Arsenal Street, Suite 201, Watertown, MA 02472

We take this very seriously. We will investigate any report within one business day.

---

*Dedicated to curing ALS.*
