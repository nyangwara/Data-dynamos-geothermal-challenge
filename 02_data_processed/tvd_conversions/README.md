# TVD conversion tables — one per well

Each `<well>_deviation_survey.csv` is the original deviation survey for that well, used as the basis for all MD→TVD conversion in this project.

## Source
`01_data_raw/well_paths/well_path_data.xlsx` — one sheet per well.

## Columns
`Depth (m)` (MD), `Inclination (º)`, `Azimuth (º)`, `TVD (m)`, `X-offset (m)`, `Y-offset (m)`

## Usage
```python
import pandas as pd
from scipy.interpolate import interp1d

survey = pd.read_csv('blt01_deviation_survey.csv')
md_to_tvd = interp1d(survey['Depth (m)'], survey['TVD (m)'], kind='linear', fill_value='extrapolate')
# tvd_at_2000md = md_to_tvd(2000)
```

## Per-well summary
| Well | Stations | MD range (m) | TVD max (m) | Max inclination | Max lateral offset (m) |
|---|---|---|---|---|---|
| BLT-01 | 102 | 0–2123 | 2051 | 19.7° | 500 |
| EVD-01 | 21 | 300–2197 | 2181 | 16.2° | 161 |
| JUT-01 | 33 | 400–3409 | 3325 | 25.5° | 545 |
| PKP-01 | 110 | 25–2751 | 2404 | 37.3° | 1,238 |

PKP-01 is highly deviated — wellhead is 22.7 km from USP but bottom of well at different lateral position. Always use lateral position at depth of interest when computing distances at depth.
