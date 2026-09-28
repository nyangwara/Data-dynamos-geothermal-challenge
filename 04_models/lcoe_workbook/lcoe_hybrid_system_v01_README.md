# lcoe_hybrid_system_v01.xlsx

LCoE model for the hybrid geothermal heating + cooling system.

## Sheets
1. **Assumptions** — all inputs in one place. Blue text on yellow = inputs; change for scenarios.
2. **CapEx** — capital cost breakdown (subsurface, surface plant, ATES, pipelines, contingency).
3. **OpEx** — annual operating costs (electricity, maintenance, labour, monitoring).
4. **Energy delivered** — annual MWh, SPF, CO₂ avoided.
5. **LCoE** — the headline number with full breakdown.
6. **Sensitivity** — pre-computed sensitivity ranges per input.

## Headline numbers (P50 base case)
| Metric | Value |
|---|---|
| Heating capacity | 10.70 MWth (target ≥10 ✓) |
| Cooling capacity | 6.00 MWth (target ≥5 ✓) |
| CapEx | €23.7M |
| OpEx | €1.82M/yr |
| Energy delivered | 31,500 MWh/yr |
| System SPF | 3.60 |
| Net CO₂ avoided | 2,612 t/yr |
| **LCoE** | **€122/MWh** (NL hybrid benchmark €80–€140) |

## Conventions
- Blue on yellow = input (changeable)
- Black = formula (don't edit; change inputs instead)
- Notes in column D explain sources

## How to run a scenario
1. Open `1. Assumptions` and change any input cell (blue/yellow).
2. Open `5. LCoE` to see the resulting LCoE.

The workbook auto-recalculates.
