# Live Demo

This page embeds the **ARC Clinical Browser** with 50 fully synthetic patients. No real patient data is present.

!!! warning "Synthetic Data Only"
    All names are drawn from a fictional list with a `[DEMO]` suffix; MRNs and patient IDs are random; clinical codes (LOINC, ICD-10, RxNorm, CPT) are real public reference data. Clinical patterns mimic ALS progression but reflect no real individual. See the [Privacy page](privacy.md) for details.

## Try it

<iframe class="dashboard-embed" src="dashboard_demo.html" title="ARC Clinical Browser Demo"></iframe>

[Open in a new tab :material-open-in-new:](dashboard_demo.html){ .als-button target="_blank" }

## What you can do

The dashboard auto-loads its synthetic data on page open. From there:

1. **Browse the patient list** in the left sidebar (scroll to see all 50)
2. **Click any patient** to open their detail view across 12 tabs
3. **Notice the source tags** — every row is tagged `source: ccda` or `source: fhir` reflecting where the data originated in the real pipeline
4. **Try the export buttons** — every tab has an "Export CSV" button; the patient header has "Export full record"; the sidebar has "Export Patient List"

## What's interesting to look at

The synthetic patients are generated with three onset profiles (limb 70%, bulbar 25%, respiratory 5%) and three progression rates (slow / typical / fast). These influence which clinical patterns each patient shows:

- **ALSFRS-R scores** decline at clinically realistic rates (~1 point/month for typical progressors)
- **FVC trajectories** mirror disease progression
- **EMG and nerve conduction studies** appear at or near diagnosis
- **Spirometry** repeats every 3-6 months
- **PEG tube placement** is more likely for bulbar-onset patients
- **Tracheostomy** appears only in late-stage / fast-progressing patients

Find a patient in the list whose name suggests bulbar onset and one with limb onset — their procedure timelines should look meaningfully different.

## What this demonstrates

The dashboard is a single static HTML file. The data is a single JSON file. Together they're loaded entirely client-side with no server, no API surface, no telemetry. In production at ALS TDI, the same dashboard runs against a ~210 MB JSON bundle of real ARC participant data on an analyst's local workstation; for sharing across the research team, the package is uploaded to organizational Box with named-user permissions. Nothing about the architecture changes between the demo and the production setting — only the data file.

This is the architectural pattern we recommend for any patient registry handling small-to-medium-sized cohorts (up to a few thousand patients). It is far simpler to operate and far easier to keep HIPAA-compliant than a server-backed analytics application.

## Want the full dataset behavior?

If you're a registry researcher evaluating this for your own use, the demo here is fully representative of the production behavior. The only differences are:

- The watermark across the top of the screen
- The `[DEMO]` suffix on every patient last name
- The number of patients (50 here vs. 71 in the production ARC dataset at the time of writing)
- All values are randomly generated

Everything else — the layout, the tabs, the source tags, the export buttons, the overall workflow — is identical.

For the underlying methods, see [About the Pipeline](pipeline.md). For an adaptation guide, see [For Other Registries](adopt.md).
