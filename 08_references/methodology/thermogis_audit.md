# ThermoGIS data audit

Required by the challenge brief: documenting which ThermoGIS layers were consulted, when, and how they influenced project decisions.

## Source

ThermoGIS portal (TNO): https://www.thermogis.nl/

The project did not access the live ThermoGIS API. All values were extracted from the `ThermoGIS_Data.xlsx` workbook supplied in the challenge data pack, which we treat as a snapshot of the TNO data for the four wells.

## Layers / sheets consulted

The workbook contains six sheets, one per well plus an overview. Per-well sheets include the following parameters at P10, P50, and P90:

- Reservoir top depth (m TVD)
- Net reservoir thickness (m)
- Porosity (fraction)
- Permeability (mD)
- Net-to-gross (fraction)
- Transmissivity k×h (Dm)
- Reservoir temperature (°C)
- Salinity (g/L)
- Pressure (bar)
- Flow rate (m³/h)
- Thermal power (MWth)
- Doublet lifetime (years)

## How each value was used

| Value | Used for | Confidence |
|---|---|---|
| Reservoir top (P50) | Cross-check against TVD-corrected lithostratigraphy. Used the lithostratigraphy values as authoritative where they diverged (typically by 20-60 m). | Medium — known to be a regional smoothing of local depth |
| Porosity (P50) | Cross-check against LAS-derived effective porosity. Found large divergence at PKP-01 (9% ThermoGIS vs 1.1% LAS). | Low — PKP-01 finding shows regional values can miss local variation by 10x |
| Permeability (P50) | Used directly — no alternative measurement available from the LAS logs in this dataset (no formation testing). | Medium — uncertain but no contradicting data |
| Reservoir temperature (P50) | Cross-validated against the calibrated geothermal gradient (31.7°C/km from BLT-01 BHT). Agreement within ±7°C across all four wells. | High |
| k×h (transmissivity, P50) | Used directly for ranking and flow rate prediction. | Medium |
| Flow rate (P50) | Used as the deliverability estimate for BLT-01 in the LCoE model (105 m³/h). | Medium - subject to actual well test if BLT-01 is workover-tested |
| Thermal power (P50) | Used as 5.1 MWth headline figure for BLT-01. | Medium - derived from flow rate + ΔT |

## Independent extractions

No additional ThermoGIS layers were extracted from the live portal during this project. Future iterations should consult:

- The 3D Rotliegend structural model (for fault avoidance at USP-01)
- Brine geochemistry layer (for material selection — TDS and pH affect corrosion design)
- ATES potential layer (for permitting feasibility check at the USP)

## Methodology limitation flagged

ThermoGIS is a regional probabilistic model. The PKP-01 finding (regional vs LAS-derived porosity differ by 8 percentage points, NTG by a factor of 30) shows that local heterogeneity can be larger than the model's P10-P90 spread. **Regional model values should never be used in isolation for site-specific go/no-go decisions.** This is the central methodological argument of the report.
