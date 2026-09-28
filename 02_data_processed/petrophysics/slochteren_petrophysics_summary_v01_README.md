# slochteren_petrophysics_summary_v01.csv

Per-well petrophysical summary over the Slochteren interval (TVD-defined).

## Columns
- `well_id`, `slochteren_top_tvd_m`, `slochteren_base_tvd_m`, `thickness_tvd_m`
- `gr_mean_gapi`, `vshale_mean_frac`, `phi_total_frac`, `phi_eff_frac`
- `ntg_log_derived`, `n_log_samples`

## Headline results
| Well | Φ_eff | NTG | Reservoir quality |
|---|---|---|---|
| BLT-01 | 11.4% | 0.93 | Good — primary candidate |
| JUT-01 | 10.9% | 0.86 | Good — secondary candidate |
| EVD-01 | 8.0% | 0.82 | Tight |
| PKP-01 | 1.1% | 0.03 | Dead reservoir at this location |

## Method
- Density-porosity: ϕ = (2.65 − ρ_b) / (2.65 − 1.0)
- Vshale (Larionov older rocks): V_sh = 0.33 × (2^(2·IGR) − 1), IGR = (GR − 25)/125
- Effective porosity: ϕ_eff = ϕ_total − V_sh × 0.30
- NTG: fraction of samples where V_sh < 0.5 AND ϕ_eff > 0.05

## Compared to ThermoGIS
ThermoGIS reports regional model averages; LAS-derived values are well-specific. PKP-01 diverges most sharply (1.1% LAS vs 9% ThermoGIS) — flag clearly in the report.

## Produced by
`reproduce_all.py` (project root) — `step4_petrophysics_summary`, which calls
`06_ai_workflow_bonus/pipeline/pipeline.py`. Verified to reproduce this file exactly
(`python reproduce_all.py --verify`).
