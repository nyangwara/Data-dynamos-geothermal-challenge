# LCoE calculation — methodology

## Definition

Levelized Cost of Energy (LCoE) is the constant per-MWh price that would make the present value of all revenue equal to the present value of all costs over the project lifetime:

```
LCoE = [annualized CapEx + average annual OpEx] × 1,000,000 / annual energy delivered (MWh)
```

Result units: €/MWh.

## Inputs

| Input | Base value | Notes |
|---|---|---|
| CapEx | €23.7M | Subsurface + surface + ATES + pipelines + 15% contingency |
| OpEx | €1.82M/yr | Electricity, maintenance (2.5% of CapEx), labour + insurance + monitoring |
| Heating delivered | 24,000 MWh/yr | 10 MWth × 2,400 hr FLEH |
| Cooling delivered | 7,500 MWh/yr | 5 MWth × 1,500 hr FLEH |
| Total delivered | 31,500 MWh/yr | |
| Discount rate | 7% | NL geothermal industry standard (commercial financing) |
| Lifetime | 25 yr | Typical NL geothermal doublet design life |

## Capital Recovery Factor (CRF)

```
CRF = r × (1+r)^n / ((1+r)^n - 1) = r / (1 - (1+r)^(-n))
```

For r = 7%, n = 25:

```
CRF = 0.07 / (1 - 1.07^(-25)) = 0.07 / 0.8156 = 0.0858
```

Annualized CapEx = 23.7 × 0.0858 = €2.03 M/yr.

## Result

```
LCoE = (2.03 + 1.82) × 1,000,000 / 31,500 = €122 / MWh
```

## Benchmark comparison

The NL Hybrid Geothermal benchmark range from EBN and TNO (2020-2024) is €80-€140/MWh. The recommended system at €122/MWh sits comfortably in the middle.

## Uncertainty (Monte Carlo)

Propagating uncertainty in flow rate, discount rate, CapEx, electricity price, and FLEH through the calculation gives:

- P10: €100/MWh
- P50: €123/MWh (matches deterministic)
- P90: €148/MWh

P90 just exceeds the upper bound of the NL benchmark range. See `03_analysis/notebooks/lead_ml_ds/lead_monte_carlo_v01.ipynb`.

## References

- EBN (2021). *Roadmap Geothermal Energy in the Netherlands*.
- IEA (2020). *Projected Costs of Generating Electricity, 2020 Edition*. Methodology Annex.
- TNO (2022). *Geothermal Energy in the Netherlands — Status Report*.

## Implementation

See `04_models/lcoe_workbook/lcoe_hybrid_system_v01.xlsx`, sheet 5 "LCoE", cell B17.
