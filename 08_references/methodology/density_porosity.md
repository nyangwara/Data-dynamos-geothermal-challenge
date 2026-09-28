# Density-porosity calculation — methodology

## Formula

```
ϕ_D = (ρ_ma - ρ_b) / (ρ_ma - ρ_fl)
```

where:
- ρ_b is the bulk density from the RHOB log (g/cc)
- ρ_ma is the matrix density — we use 2.65 g/cc (quartz, appropriate for the Slochteren Sandstone)
- ρ_fl is the fluid density — we use 1.0 g/cc (water-saturated brine, ignoring salinity correction)

The total porosity is then corrected for shale content to give effective porosity:

```
ϕ_eff = ϕ_D - V_sh × ϕ_sh
```

with ϕ_sh = 0.30 (shale porosity, NL Permian convention; range 0.25–0.35 in published literature).

## Why density-porosity (not neutron-density crossplot)

The textbook best practice for porosity is the neutron-density crossplot, which uses both NPHI (neutron porosity) and RHOB. The crossplot has two advantages: (a) it partially cancels shale-volume effects on porosity, and (b) it can flag gas-bearing intervals (gas pushes neutron down, density down — they diverge).

In this dataset, only BLT-01 and PKP-01 have valid NPHI curves. EVD-01 and JUT-01 do not. To use one consistent porosity method across all four wells, we use density-porosity throughout.

The trade-off is that density-porosity slightly over-estimates porosity in shaly intervals (the RHOB log doesn't perfectly distinguish clay from quartz). For the Rotliegend at this depth and temperature, the bias is small — about 1 porosity unit. The Vshale correction (subtracting V_sh × 0.30) substantially reduces this bias.

There is no gas in the Slochteren targets (geothermal aquifer), so the gas-bearing complication is moot here.

## Reference

- Schlumberger (1989). *Log Interpretation Principles/Applications*. Schlumberger Educational Services.
- Asquith, G. & Krygowski, D. (2004). *Basic Well Log Analysis*. AAPG Methods in Exploration No. 16.

## Implementation

See `06_ai_workflow_bonus/pipeline/pipeline.py` function `compute_petrophysics`.
