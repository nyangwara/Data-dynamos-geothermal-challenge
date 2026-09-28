# Geothermal doublet design — methodology

## What is a doublet

A doublet is the standard geothermal heat-extraction architecture: one producer well brings hot brine from the reservoir to the surface; the surface plant extracts heat via a heat exchanger; one injector well returns the cooler brine to the same reservoir at a different location. The injection point must be far enough from the producer that the cool front from injection doesn't reach the producer within the project lifetime (thermal breakthrough).

## Producer / injector roles

Convention in this project: BLT-01 (the existing, proven well) is the producer; USP-01 (the new, unproven well) is the injector. This is a risk-management choice — the new well's uncertainty primarily affects how much water it can accept at acceptable wellhead pressures, not how much heat the system produces. The headline output number (5.1 MWth) is set by BLT-01 and is robust to USP-01 underperformance.

## Spacing — thermal breakthrough constraint

The simple plug-flow approximation for thermal breakthrough time:

```
τ = π × φ × h × r² / q
```

where:
- φ is the reservoir porosity (fraction)
- h is the reservoir thickness (m)
- r is the doublet spacing (m)
- q is the volumetric flow rate (m³/s)

For our recommended doublet: φ = 0.11, h = 122 m, r = 1500 m, q = 105/3600 = 0.029 m³/s.

```
τ = π × 0.11 × 122 × 1500² / 0.02917 ≈ 3.25 × 10⁹ s ≈ 103 years (geometrically)
```

The plug-flow result over-estimates by approximately 3x because real reservoirs have heterogeneous permeability — the cool front fingers through high-perm streaks. Industry rule of thumb is to divide by approximately 3 to get the practical breakthrough estimate: **~34 years**, comfortably longer than the 25-year design life. (Note: this plug-flow figure is the hydraulic pore-volume time; a true thermal-breakthrough calculation adds rock-matrix heat retardation, which lengthens it — so ~34 years is a conservative lower bound.)

Full reservoir simulation (e.g., DoubletCalc, MoReS, or Eclipse) should be used in the detailed engineering phase to refine this estimate.

## Spacing — surface piping constraint

Wider doublet spacing → longer surface pipelines → higher CapEx. At our 1.5 km spacing with USP-01 placed at the USP, hot brine line is 2.0 km (BLT-01 to plant) and cool brine return is 0.5 km (plant to USP-01). Total surface CapEx for these lines is approximately €2.3M.

A 2.5 km spacing would push thermal breakthrough beyond 80 years but add roughly €1.5M to pipelines. A 1.0 km spacing would save €0.8M on pipelines but bring breakthrough to ~13 years — unacceptable for a 25-year design life.

1.5 km is the sweet spot.

## Flow rate optimization

Higher flow rate → more thermal output → fewer wells needed for the same MW. But: higher flow rate also means faster thermal breakthrough (τ ∝ 1/q) and higher pump electricity (P_pump ∝ q²). The optimum balances heat output against pump electricity and breakthrough timing.

For NL Slochteren conditions, the typical economic flow rate is 80-150 m³/h per well. Our 105 m³/h sits in the middle of this range.

## Injection temperature

Lower injection temperature → more heat extracted per pass → higher thermal output. But: very cold injection accelerates thermal breakthrough and may exceed reservoir mechanical limits (cool brine has different density and viscosity, and cold injection can induce stress changes).

NL standard practice is 25-35 °C injection. Our 15 °C is aggressive — flagged in the report as needing engineering review. If we have to relax to 25 °C, HP-1 output drops by approximately one-third (cannot cool the return brine as far) and the system needs additional heat-pump or ATES capacity to make up the gap.

## References

- IF Technology (2018). *Dutch Geothermal Doublet Design Handbook*.
- Mijnlieff, H. F. et al. (2014). "Successful Drilling of Dutch Geothermal Targets". *Proceedings ECOS 2014*.
- Willems, C.J.L. et al. (2017). "Doublet deployment strategies for geothermal hot sedimentary aquifer exploitation". *Geothermics*, 65, p.222-233.

## Implementation in this project

See:
- `04_models/reservoir_model/subsurface_assessment_v01.md` for the design rationale
- `04_models/reservoir_model/subsurface_assessment_v01.xlsx` sheet 3 for the thermal breakthrough calculation
- `03_analysis/notebooks/lead_ml_ds/lead_reservoir_deliverability_v01.ipynb` for Darcy radial flow verification
