# surface_system_design_v01.md

Technical writeup for Challenge 2  The integrated heating + cooling system design.

## What's in this document
1. System topology overview (doublet + 2 heat pumps + absorption chiller + ATES)
2. New well USP-01 location and predicted properties
3. Component sizing with first-principles calculations
4. Energy balance: winter, summer, annual
5. Operating modes and seasonal logic
6. Design considerations and engineering judgment (defensive analysis section)
7. Cross-reference to PFD and LCoE workbook
8. References for the report

## Headline numbers
- Heating delivered: 10.7 MWth (target ≥10 ✓)
- Cooling delivered: 6.0 MWth (target ≥5 ✓)
- System SPF: 3.6
- Annual CO₂ avoided: 2,612 t/yr

## 
- Pressure-test the COP assumptions with real vendor data
- Verify the injection temperature is acceptable to reservoir engineering
- Confirm ATES permitting feasibility at the USP site



## Companion files
- `lcoe_hybrid_system_v01.xlsx` — the economic model for this design
- `process_flow_diagram_v01.svg` — visual of the system
