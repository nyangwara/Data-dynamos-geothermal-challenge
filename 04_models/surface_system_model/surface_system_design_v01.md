# Surface system design — hybrid geothermal heating & cooling

**Configuration:** 1 geothermal doublet + 2 heat pumps + absorption chiller + electric chiller + ATES storage
**Target:** ≥10 MWth heating, ≥5 MWth cooling, urban district near USP, Utrecht
**Wells:** BLT-01 (existing, producer) + USP-01 (new, injector)

This document gives the team the technical scaffolding for Challenge 2. Every number here is defensible from first principles or NL geothermal benchmarks. Person 3 should treat this as a starting point — refine, challenge, and improve, but don't start from zero.

---

## 1. System topology

Five subsystems work together:

1. **Geothermal doublet** — extracts heat from the Rotliegend Slochteren reservoir
2. **Primary heat exchanger (HX-1)** — transfers heat from corrosive brine to clean district water
3. **Two heat pumps (HP-1, HP-2)** — boost output to meet peak heating demand
4. **Absorption chiller (ABS)** — converts geothermal heat to cooling in summer
5. **Electric chiller (EC) + ATES storage** — handles peak cooling and seasonal balancing

The plant building sits at the USP. Hot brine is piped 2 km from BLT-01 to the plant; cool brine returns 0.5 km to USP-01 for injection. The district network (supply at 70°C, return at 40°C) distributes heat to buildings.

## 2. The new well — USP-01

**Proposed location:** X = 141,278, Y = 455,412 (RD New)

This position is **1.5 km from BLT-01** (sufficient doublet spacing to prevent thermal breakthrough within 25 years at planned flow rates) and **0.53 km from the USP** (minimizes surface piping and heat loss).

**Predicted Slochteren properties** (inverse-distance weighted from BLT-01 and JUT-01, weights 0.84 / 0.16):

| Property | Predicted | Source analog (BLT-01) |
|---|---|---|
| Top depth (TVD) | 1,830 m | 1,862 m |
| Thickness | 123 m | 122 m |
| Porosity | 11.4% | 11.4% |
| Permeability | 75 mD | 82 mD |
| Reservoir temperature | 76 °C | 77 °C |
| Predicted flow rate (P50) | 97 m³/h | 105 m³/h |
| Predicted power | 4.7 MWth | 5.1 MWth |

**Why USP-01 is the injector, not the producer:** BLT-01 has proven 5.1 MWth deliverability — using it as producer locks in the baseline. USP-01 is a new well; if it underperforms, we still have BLT-01's known output. Risk mitigation: the side facing more uncertainty (the new well) takes the less-critical role.

**Risks for USP-01:**
- Reservoir top may be shallower or deeper than predicted (uncertainty ±50 m TVD based on regional dip)
- Injection acceptance — needs to take 105 m³/h at acceptable wellhead pressure. With 75 mD predicted permeability over 123 m, transmissivity is ~9.2 Dm, comparable to BLT-01. Injection should be feasible.
- Need to confirm position is away from regional faults — Person 2 to check this on the ThermoGIS structural map

## 3. Component sizing

### Geothermal doublet

Output at P50:
- Flow rate: 105 m³/h (29.2 kg/s assuming brine density ~1000 kg/m³)
- Production temperature: 77 °C
- Return (injection) temperature: 35 °C (ΔT = 42 °C)
- Direct heat: Q = ṁ × c_p × ΔT = 29.2 × 4180 × 42 = **5.1 MWth**

Brine handling:
- Salinity: typical Rotliegend brine 100,000–200,000 ppm TDS → corrosion-resistant materials throughout (duplex stainless steel HX tubes, GRE piping)
- Closed-loop secondary side (clean water) for district network — brine never enters the district piping

### Heat pump 1 — return brine heat recovery (HP-1)

Extracts additional heat from the 35 °C return brine, dropping it to ~15 °C before injection. Reinjection at 15 °C is on the edge of acceptable for Rotliegend (typical NL practice 25–35 °C); if reservoir engineering pushes back, this can be relaxed to 25 °C with lower HP output.

Sizing (case: brine from 35 → 15 °C):
- Heat extracted from brine: 29.2 × 4180 × 20 = 2.44 MW
- COP at this temperature lift (15 → 70 °C source, 70 → 90 °C sink): ~3.5
- Electric input: W = Q_cold / (COP − 1) = 2.44 / 2.5 = 0.98 MW
- Heat delivered: Q_hot = COP × W = **3.42 MWth**

### Heat pump 2 — ATES warm well booster (HP-2)

In winter, the ATES warm well (charged during summer with surplus heat) discharges to HP-2 as a low-temperature heat source.

Sizing:
- ATES warm well flow: 70 m³/h at 25 °C, cooled to 5 °C before reinjection to ATES cold well
- Heat extracted: 19.4 × 4180 × 20 = 1.62 MW
- COP at 5–25 °C source, 70–90 °C sink: ~4.0
- Electric input: 1.62 / 3.0 = 0.54 MW
- Heat delivered: **2.17 MWth**

### Total winter heating capacity

| Source | Power | Electricity in |
|---|---|---|
| Geothermal direct (BLT-01) | 5.10 MWth | 0 |
| Heat pump 1 (return brine) | 3.42 MWth | 0.98 MW |
| Heat pump 2 (ATES warm) | 2.17 MWth | 0.54 MW |
| **Total** | **10.69 MWth** | **1.52 MW** |

System overall COP (heat out / electricity in): 10.69 / 1.52 = **7.0**.

### Absorption chiller (ABS)

Single-effect LiBr / water absorption chiller, COP ≈ 0.7. Runs in summer when heating demand drops.

Driving heat: 80 °C input (from geothermal supply line via diversion valve)
- Cooling capacity: 3.0 MWth
- Heat input required: 3.0 / 0.7 = 4.3 MWth

### Electric chiller (EC) — peaking only

Conventional electric vapor-compression chiller, COP ≈ 5.0. Provides 2.0 MWth cooling capacity for summer peaks and as redundancy.

### ATES storage

Standard NL shallow aquifer storage system at ~100–200 m depth:
- Warm well: charged in summer (excess geothermal heat dumped at 25 °C), discharged in winter (feeds HP-2)
- Cold well: charged in winter (cool reject from operations at 7 °C), discharged in summer (passive cooling)
- Storage volume per well: ~50,000–100,000 m³ over a heating season
- Round-trip thermal efficiency: ~70%

### Summer cooling balance

| Source | Capacity |
|---|---|
| Absorption chiller (geothermal-driven) | 3.0 MWth |
| ATES cold well (passive cooling) | 1.0 MWth |
| Electric chiller (peaking) | 2.0 MWth |
| **Total available** | **6.0 MWth** |
| Demand | 5.0 MWth |

Headroom: 20% margin in summer.

## 4. Energy balance — annual

Assumptions:
- Heating full-load equivalent hours: 2,400 hr/yr (typical NL DHC)
- Cooling FLEH: 1,500 hr/yr
- District supply: 70 °C / Return: 40 °C (medium-temperature network)

| Item | Quantity |
|---|---|
| **Heat delivered annually** | 10 × 2,400 = 24,000 MWh/yr |
| **Cool delivered annually** | 5 × 1,500 = 7,500 MWh/yr |
| **Total useful energy** | **31,500 MWh/yr** |
| Heat pump electricity (winter) | ~5,500 MWh/yr |
| Chiller + auxiliary electricity (summer) | ~1,000 MWh/yr |
| Pump electricity (year-round, doublet + district) | ~2,250 MWh/yr |
| **Total electricity input** | **~8,750 MWh/yr** |
| **System-wide SPF** (Seasonal Performance Factor) | 31,500 / 8,750 = **3.6** |

Comparison: an air-source heat pump fleet covering the same demand would have SPF ~2.5–3.0. The geothermal contribution improves the system COP by ~20–30%, which is the economic case for drilling.

CO₂ avoided vs natural gas baseline (assuming 24,000 MWh/yr displaces gas at 0.20 kgCO₂/kWh):
- Gross gas displacement: 24,000 × 0.20 = 4,800 t CO₂/yr
- Less electricity emissions (assume NL grid ~0.25 kgCO₂/kWh in 2026): 8,750 × 0.25 = 2,190 t CO₂/yr
- **Net CO₂ saved: ~2,600 t CO₂/yr**

## 5. Operating modes

| Mode | When | What happens |
|---|---|---|
| Winter peak heating | Dec–Feb, T_amb < 5°C | Geothermal + HP-1 + HP-2 all running. ATES warm well discharging. |
| Shoulder | Mar–May, Oct–Nov | Geothermal + HP-1 only. ATES standby (charging if surplus). |
| Summer cooling | Jun–Aug | Absorption chiller on diverted geothermal heat. EC for peaks. ATES cold well discharging. |
| Off-peak | Late spring / early autumn nights | Charge ATES warm well from surplus geothermal. |

## 6. Critical assumptions & open questions

Things Person 3 should pressure-test:

- **Heat pump COP** values (3.5 and 4.0) are typical but vary with operating conditions. Real performance curves from a vendor (e.g., Carrier, Trane, Star Refrigeration) should be used in the final design.
- **District supply temperature** of 70 °C assumes a medium-temperature network. If the network can run at 55 °C (low-temp), heat pump output and COP both improve significantly. Worth investigating — depends on building radiator vs. underfloor heating mix in the district.
- **Injection temperature** of 15 °C is aggressive. NL standard practice is 25–35 °C. If we have to relax to 25 °C, HP-1 output drops to ~2.1 MW and we need additional capacity (a larger HP-2 or a third HP). This is a key decision worth modelling both ways.
- **ATES system permitting** — Dutch ATES requires permitting for the shallow aquifer; need to confirm the USP site doesn't conflict with existing drinking water protection zones.
- **Reservoir thermal breakthrough** — 1.5 km doublet spacing with 105 m³/h is at the lower end of safe. Tracer test or reservoir simulation recommended; for the report, the plug-flow pore-volume time is τ = π × φ × h × r²/q = π × 0.11 × 122 × 1500² / (105/3600) ≈ **103 years**, which after the ÷3 heterogeneity derate (see `doublet_design.md`) gives a practical estimate of ≈**34 years** — comfortably beyond the 25-year design life either way.

## 7. Process flow

See `05_visualizations/system_diagrams/process_flow_diagram_v01.svg`.

## 8. References for the report

- Van Wees et al. (2012) — ThermoGIS methodology for NL geothermal assessment
- Mijnlieff et al. (2014) — Rotliegend reservoir characterization, NL onshore
- Drijver et al. (2019) — HT-ATES design guidelines, KWR Water Research
- IF Technology (2018) — Dutch geothermal doublet design handbook
- NL ATES regulations: BUM-ATES (Beleidsregels Uitvoering Milieubeleid)

Person 4 should source these and add to `08_references/papers/`.
