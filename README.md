# ARC Clinical Browser — Public Demo

This is a public demonstration of an internal clinical-records viewer used at the
[**ALS Therapy Development Institute (ALS TDI)**](https://www.als.net/) to review longitudinal
clinical data collected from ARC Study participants via patient-directed
SMART on FHIR with OAuth 2.0.

> ⚠️ **All data shown here are fully synthetic.** Names, MRNs, dates, and clinical
> patterns are randomly generated. No real patient information is present.

---

## What this demo shows

A single-file HTML dashboard backed by a single JSON data bundle. The viewer renders:

- **50 synthetic ALS patients** with clinically realistic progression patterns
- ~10,000 narrative documents (CCDA / HTML / RTF / PDF mix)
- ~5,800 lab and observation records with real public LOINC codes — including ALSFRS-R scores that decline at clinically realistic rates (~1 point/month average) and forced vital capacity (FVC) that follows
- ~260 problem/condition records with real public ICD-10 codes
- ~260 medication records with real public RxNorm codes (riluzole, edaravone, baclofen, glycopyrrolate, etc.)
- ~1,000 procedure records sequenced realistically: EMG/NCS at diagnosis, recurring spirometry, PEG tube and tracheostomy timed to disease progression
- ~670 encounters across multiple visit types (multidisciplinary ALS clinic, pulmonology, speech, physical therapy)
- Allergies, immunizations, care plans, diagnostic reports, and goals
- 13 FHIR resource categories
- **Per-tab CSV export** — every data tab has a download button so you can pull the displayed records as a properly-escaped CSV
- **Per-patient full-record export** — single button to download a tagged combined CSV of all data for one patient
- **Cohort-level patient list export** — download demographics for the whole cohort

Patients are generated with three onset profiles (limb-onset 70%, bulbar-onset 25%, respiratory-onset 5%) and three progression rates (slow / typical / fast) which influence everything from condition timing to PEG/trach probability. Every record is tagged `source: ccda` or `source: fhir` to reflect how the real pipeline attributes data provenance.

## What this demo does **not** show

- Any real patient information (this is a public demo)
- The actual SMART on FHIR retrieval layer (handled separately at ALS TDI)
- Production Databricks queries (those use real PHI and are kept private)

For a full description of the production pipeline, see the accompanying
**JAMIA Brief Communication** ([forthcoming]).

---

## Files in this folder

```
dashboard_demo.html          The viewer (single HTML file, ~36 KB)
demo_dashboard_data.json     Synthetic data bundle (~5 MB)
generate_synthetic_data.py   Regenerate the JSON with different seed/size
README.md                    This file
```

## How to run locally

1. Place `dashboard_demo.html` and `demo_dashboard_data.json` in the same folder
2. **Serve them with a local HTTP server** (browsers block `fetch()` from `file://` URLs):
   ```bash
   cd path/to/folder
   python -m http.server 8000
   ```
3. Open `http://localhost:8000/dashboard_demo.html` in a browser
4. The synthetic data loads automatically

## Hosting on GitHub Pages

Both files are static — no server needed. GitHub Pages handles the `fetch()` natively:

1. Add `dashboard_demo.html` and `demo_dashboard_data.json` to your `docs/` folder (or wherever GitHub Pages serves from)
2. Enable Pages in repo Settings → Pages → Source: `main` branch, `/docs` folder
3. The dashboard will be live at `https://<user>.github.io/<repo>/dashboard_demo.html`

## Embedding in MkDocs

Add an iframe in any MkDocs Markdown page:

```html
<iframe
  src="dashboard_demo.html"
  width="100%"
  height="800"
  style="border: 1px solid #d4cdbb; border-radius: 4px;">
</iframe>
```

For full-page integration, use a custom MkDocs page template or link directly:

```markdown
## Live demo
[Open the ARC Clinical Browser demo →](dashboard_demo.html){target=_blank}
```

You can also configure MkDocs to copy the JSON file to your site output by listing it in `mkdocs.yml`:

```yaml
extra_files:
  - dashboard_demo.html
  - demo_dashboard_data.json
```

## Regenerating the synthetic data

To produce a different cohort (different size, different seed, more or fewer patients):

```bash
python generate_synthetic_data.py
```

Edit the constants at the top of `generate_synthetic_data.py`:

```python
N_PATIENTS = 50         # change cohort size
SEED = 42               # change for different random patients
NAME_SUFFIX = " [DEMO]" # appended to every last name to mark synthetic
```

The generator uses real public clinical vocabularies (LOINC, ICD-10-CM, RxNorm, CPT, SNOMED CT)
because those code sets are public reference data, not protected information. Names are drawn
from a small fictional list with no real-person resemblance intended.

---

## About ALS TDI and the ARC Study

The ALS Therapy Development Institute is the world's largest nonprofit research institute focused
solely on ALS treatments. The ALS Research Collaborative (ARC) Study is a long-running natural-
history study of amyotrophic lateral sclerosis with over 1,000 participants nationwide.

Learn more: [www.als.net](https://www.als.net/) · ARC Study: [www.als.net/arc/](https://www.als.net/arc/)

## License & contact

This demo and the synthetic data generator are released for educational and reference purposes.
The production pipeline source code is maintained internally at ALS TDI and is available to
qualified collaborators on request.

