# AI workflow — design and rationale

A short writeup for the bonus track: what we built, why these design choices, what it saves.

## What it does

Given a LAS file, a deviation survey, and a lithostratigraphy table, the workflow produces a clean reservoir-interval petrophysical summary — TVD-corrected, anomaly-filtered, with Vshale, effective porosity, and NTG. Output is a one-row summary per well plus a clean per-sample table.

## Pipeline steps

1. **Ingest LAS** with `lasio` — normalize column names, replace null sentinels.
2. **QC anomaly detection** with Isolation Forest — the ML element, per-curve, no hardcoded thresholds.
3. **MD → TVD conversion** via linear interpolation on the deviation survey.
4. **Find reservoir interval** by matching the formation name in the lithostratigraphy.
5. **Compute petrophysics**: density-porosity, Larionov Vshale, effective porosity.
6. **Summarize** — one row per well + cleaned per-sample DataFrame.

## Why Isolation Forest for QC

Three options were considered:

- **Hardcoded physical ranges** (RHOB ∈ [1.0, 3.5], etc.) — fast and transparent, but requires domain knowledge per curve, doesn't catch in-range-but-suspicious values, and fails when extending to exotic curves.
- **Z-score / percentile filter** — flag anything beyond N standard deviations. Assumes normal distribution; bimodal data (sand vs shale baseline) gets the sand population flagged.
- **Isolation Forest** (chosen) — unsupervised, learns each curve's density and flags points in sparse regions. No distributional assumption.

It caught the JUT-01 RHOB values up to 7.5 million g/cc without any prior knowledge of the corruption. That's the kind of QC step that scales to basin-wide screening.

## Why Larionov older-rocks for Vshale

The Rotliegend is Permian (~280 Ma) — firmly in "older rocks" by convention. Larionov's two formulas (younger Tertiary vs older pre-Tertiary) differ materially: older rocks are more compacted and return lower V_sh for the same IGR. Using the wrong formula would over-estimate shale and under-estimate NTG by 5-10 percentage points.

## Why density-porosity (not neutron-density crossplot)

Neutron-density is the textbook best practice. But only BLT-01 and PKP-01 have valid NPHI curves; EVD-01 and JUT-01 don't. For a consistent method across all four wells, we use density-porosity. The trade-off is ~1% porosity unit over-estimate in shaly zones, partially compensated by the Vshale correction.

## The cross-validation finding (PKP-01)

The workflow's most interesting output. ThermoGIS regional model says PKP-01 has 9% effective porosity; LAS-derived value is 1.1%. Both numbers are "right" — ThermoGIS is a regional average, the logs are well-specific reality. A human petrophysicist would notice this; this workflow surfaces it automatically by producing both numbers side-by-side.

If extended to ~50 NL wells, this regional-vs-local divergence map would itself be a finding worth publishing.

## Time savings

- Manually per well: ~2 hours (cleaning, MD→TVD, petrophysics, write-up)
- Pipeline per well: ~30 seconds (with reproducible audit trail)
- At basin scale (50 wells): ~100 analyst hours saved per assessment cycle

## Extensions for future iterations

1. **Permeability prediction** from porosity (Kozeny-Carman or rock-typed regression)
2. **LLM-based summary generation** — produce a one-paragraph human-readable description per well
3. **Facies classifier** on GR+RHOB+NPHI signature (clean sand, shaly sand, shale, tight)
4. **ThermoGIS API client** to automatically pull regional values and flag local-vs-regional divergence
