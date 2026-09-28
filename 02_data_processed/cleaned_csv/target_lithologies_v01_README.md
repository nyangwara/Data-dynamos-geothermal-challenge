# target_lithologies_v01.csv

The repaired version of the originally-flagged `target_lithologies.csv` from the challenge data pack.

## What was wrong with the original
All 3,455 rows in the original carried `flag = check` with reason: *"AH depth — deviated well needs TVD conversion before use"*. The `depth_tvd_m` column was empty; `formation_top_tvd` actually held MD values; porosity/density were missing for JUT-01 and EVD-01.

## What was done
1. Parsed the 4 LAS files using `lasio`, removed null sentinels.
2. Built MD↔TVD interpolators from deviation surveys.
3. Identified true Slochteren intervals from lithostratigraphy (TVD-corrected).
4. Computed density-porosity: ϕ = (ρ_ma − ρ_b) / (ρ_ma − ρ_fl), ρ_ma=2.65, ρ_fl=1.0.
5. Recomputed lateral easting/northing at depth using deviation X/Y offsets.
6. Produced one row per LAS sample inside the Slochteren TVD interval.

## Output columns
- `well_id`, `easting`, `northing`, `md_m`, `depth_tvd_m`
- `porosity_pct`, `gamma_ray_api`, `bulk_density_gcc`
- `formation_top_md`, `formation_base_md`, `formation_top_tvd`, `formation_base_tvd`, `formation_thickness_tvd_m`
- `distance_to_usp_km` (from lateral position at depth to USP at X=141171, Y=454890)
- `flag` (all `ok`), `flag_reason` (provenance note)

## Rows per well
| Well | Rows |
|---|---|
| BLT-01 | 1,689 |
| JUT-01 | 836 |
| EVD-01 | 780 |
| PKP-01 | 730 |

## Produced by
`reproduce_all.py` (project root) — `step3_target_lithologies`, which calls
`06_ai_workflow_bonus/pipeline/pipeline.py`. Run `python reproduce_all.py` to regenerate,
or `python reproduce_all.py --verify` to diff against the committed file without overwriting.
(The `petrophysics_pipeline.ipynb` notebook only *displays* the summary; it does not write these CSVs.)
