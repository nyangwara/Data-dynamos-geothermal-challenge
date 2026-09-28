# AI workflow — example outputs

Expected outputs produced by `notebooks/petrophysics_pipeline.ipynb` on the four challenge wells.

## Files
- `expected_output_summary.csv` — the per-well petrophysical summary the pipeline should produce. Re-run the notebook to verify reproducibility.
- `qc_report_<well>.csv` — anomaly detection reports. Documents every value the Isolation Forest flagged and suppressed.

## Use
After running the notebook, compare the `summary_df` output to `expected_output_summary.csv`. They should match exactly. If they don't, something in the pipeline changed.

The QC reports are also the audit trail for the QC step: they tell you which curves had anomalies, how many, and what value ranges were flagged.
