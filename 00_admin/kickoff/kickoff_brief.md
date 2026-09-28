# Project kickoff brief

**Project:** geothermal heating + cooling system for an urban district in the Netherlands
**Target reservoir:** Rotliegend Slochteren sandstone, Utrecht region
**Demand:** ≥10 MWth heating, ≥5 MWth cooling
**Wells available:** BLT-01, EVD-01, JUT-01, PKP-01
**Submission:** technical report (PDF) + 5-minute video pitch + source-code repo

## findings from the data

1. **BLT-01 is the only well that's economic at P50.** 5.1 MWth, 105 m³/h, k×h = 9.3 Dm. Reservoir at 1862 m TVD, 2 km from USP.
2. **JUT-01 is a credible secondary** (P50 = 2.3 MWth) but 7.7 km from USP.
3. **EVD-01 and PKP-01 are uneconomic at P50** (permeability <10 mD). De-risking wells only.
4. **Cleaned target_lithologies.csv** ready in `02_data_processed/cleaned_csv/`. TVD-corrected, gap-filled.
5. **PKP-01 LAS-derived effective porosity = 1.1%** vs ThermoGIS 9% — regional models can mislead.
6. **Geothermal gradient ≈ 31.7 °C/km** from BLT-01 BHT.
7. **USP location: X=141,171, Y=454,890** (RD New).

## The technical solution (proposed)

- **Doublet:** BLT-01 (producer) + new well USP-01 (injector) at (141278, 455412), 1.5 km from BLT-01, 0.5 km from USP.
- **Two heat pumps:** HP-1 on return brine (3.4 MWth), HP-2 on ATES warm well (2.2 MWth).
- **Absorption chiller** (3 MW) + electric chiller (2 MW) for cooling.
- **ATES storage** for seasonal balancing.
- **Total capacity:** 10.7 MWth heating, 6.0 MWth cooling.
- **LCoE:** €122/MWh (within NL hybrid benchmark €80–€140).


