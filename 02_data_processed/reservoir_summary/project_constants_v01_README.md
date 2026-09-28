# project_constants_v01.csv

Constants used across the project, derived once and referenced everywhere.

## Contents
- `usp_x_rd_new`, `usp_y_rd_new`: USP location triangulated from the four `distance_to_usp_km` values in the original `target_lithologies.csv`. Least-squares fit; residuals ~10⁻⁷ km.
- `geothermal_gradient_C_per_km`: 31.7 °C/km, derived from BLT-01 BHT (167°F at 2123 m MD) with surface temp 10 °C. Consistent with NL onshore average.
- `surface_temperature_C`: 10 °C, NL annual average.
- `usp01_x_rd_new`, `usp01_y_rd_new`: proposed new well location (141278, 455412) — 1.5 km from BLT-01, 0.5 km from USP. See subsurface assessment doc for derivation.

## Produced by
`reproduce_all.py` (project root) — `step5_project_constants`. The geothermal gradient is
computed from BLT-01 BHT (167 °F = 75 °C) at **TVD 2,051 m** (= 2,123 m MD, converted via the
deviation survey) and surface 10 °C → 31.7 °C/km. The USP coordinates were triangulated by
least squares from the four distance-to-USP values in the *original* `target_lithologies.csv`
(not redistributed); the solved values (X=141171, Y=454890) are recorded as constants in
`step5_project_constants`.
