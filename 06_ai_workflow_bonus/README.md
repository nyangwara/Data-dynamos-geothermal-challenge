# AI workflow bonus — quick start

Run the demo notebook to see the full pipeline on all four wells.

## Files
- `notebooks/petrophysics_pipeline.ipynb` — demo notebook walking through every step on real data
- `pipeline/pipeline.py` — importable Python module — same logic, callable from anywhere
- `docs/workflow_design.md` — design rationale
- `examples/` — expected outputs for verification

## Running it

```bash
jupyter lab notebooks/petrophysics_pipeline.ipynb
```

Click Run > Run All Cells. Takes ~30 seconds. Produces a per-well petrophysics summary at the bottom.

## What it does (one paragraph for the report)

The workflow ingests a raw LAS file, runs an Isolation Forest anomaly detector on each curve to flag the most statistically isolated ~1% of points (fixed contamination, no per-curve thresholds), converts measured depth to TVD using a deviation survey, locates the target reservoir interval from a lithostratigraphy table, and computes density-porosity, Larionov Vshale, and effective porosity (with hard physical limits enforced in that step) — producing a one-row reservoir characterization per well plus a cleaned per-sample DataFrame. Time per well: ~30 seconds. Equivalent manual analysis: ~2 hours.
