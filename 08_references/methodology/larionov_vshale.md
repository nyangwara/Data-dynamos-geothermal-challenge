# Larionov Vshale calculation — methodology

## Formula

For older (pre-Tertiary, here Permian) rocks:

```
V_sh = 0.33 × (2^(2·IGR) - 1)
```

where IGR is the gamma-ray index:

```
IGR = (GR - GR_clean) / (GR_shale - GR_clean)
```

We use GR_clean = 25 gAPI (clean sandstone baseline observed in JUT-01 and EVD-01 Slochteren) and GR_shale = 150 gAPI (typical NL Permian shale value). IGR is clipped to [0, 1] before the Larionov transformation.

## Why "older rocks" not "Tertiary"

Larionov published two formulas — one for Tertiary (younger, less compacted) rocks and one for older (pre-Tertiary) rocks. The two differ materially: for the same IGR, the older-rocks formula returns a lower V_sh because older shales are more compacted and exhibit higher gamma-ray response per unit of clay content. The Rotliegend Slochteren is Permian (~280 Ma) — firmly in "older rocks" territory.

Using the wrong formula would over-estimate V_sh and under-estimate NTG by roughly 5-10 percentage points across the four wells in this study.

## Reference

Larionov, V.V. (1969). *Borehole Radiometry*. Nedra Publishing House, Moscow. (Original Russian — most western citations are from secondary sources.)

A modern reference is:
- Asquith, G. & Krygowski, D. (2004). *Basic Well Log Analysis*. AAPG Methods in Exploration No. 16. Chapter on shale-volume calculations.

## Implementation

See `06_ai_workflow_bonus/pipeline/pipeline.py` function `compute_petrophysics`.
