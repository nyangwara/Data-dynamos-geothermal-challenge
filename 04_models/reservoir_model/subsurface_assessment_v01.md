# Subsurface assessment — Challenge 1 technical writeup

**Target reservoir:** Rotliegend Slochteren sandstone, Utrecht region (NL)
**Wells evaluated:** BLT-01, EVD-01, JUT-01, PKP-01
**Conclusion:** Recommended development is a single doublet with BLT-01 as producer and a new well USP-01 (proposed location: X=141,278, Y=455,412 RD New) as injector. The doublet at P50 delivers 5.1 MWth direct geothermal power; together with heat-pump augmentation and the proposed surface system, this meets the project's 10 MWth heating demand.

This document is the technical content for the Challenge 1 portion of the report. Every number here is reproducible from the cleaned datasets in `02_data_processed/` and the AI workflow notebook in `06_ai_workflow_bonus/notebooks/`.

---

## 1. Data inventory

| Data type | Source | Used for |
|---|---|---|
| LAS well logs (4 wells) | Challenge data pack | GR, RHOB, NPHI, DT — petrophysics |
| Deviation surveys (4 wells) | `well_path_data.xlsx` | MD→TVD conversion, lateral well position at depth |
| Lithostratigraphy (4 wells) | `lithostratigraphic_data.xlsx` | Reservoir interval identification |
| ThermoGIS reservoir model | `thermogis_data.xlsx` | P10/P50/P90 reservoir properties, regional context |
| BLT-01 bottom-hole temperature | LAS header (BHT = 167 °F at 2123 m MD) | Geothermal gradient calibration |
| Distance-to-USP values | Original `target_lithologies.csv` | USP location triangulation |

## 2. Data quality issues identified and resolved

| Issue | Where | Resolution |
|---|---|---|
| All 3,455 rows in `target_lithologies.csv` flagged `check` for MD depths in deviated wells | Source CSV | Built MD↔TVD interpolators from deviation surveys; converted every row to TVD |
| Corrupted RHOB values up to 7.5×10⁶ g/cc | JUT-01 LAS | Isolation Forest anomaly detection flagged and suppressed 158 samples |
| Corrupted DT values up to 2.8×10⁶ µs/ft | JUT-01 LAS | Isolation Forest anomaly detection flagged 193 samples |
| Missing porosity for JUT-01 and EVD-01 | Source CSV | Computed density-porosity from RHOB curves |
| Missing density for JUT-01 | Source CSV | Pulled from LAS RHOB curve directly |
| ThermoGIS reservoir tops differ from lithostratigraphy tops by up to 60 m TVD | Cross-check | Used well-specific lithostratigraphy tops (TVD-corrected) as authoritative |
| JUT-01 has a repeated Slochteren section at deeper TVD (3161 m) | Lithostratigraphy | Likely fault repeat; used the shallower (primary) occurrence |

The full audit trail is in the Isolation Forest QC reports under `06_ai_workflow_bonus/examples/qc_report_*.csv`.

## 3. Geothermal gradient calibration

BLT-01 records a bottom-hole temperature of 167 °F (75 °C) at MD 2123 m, corresponding to TVD ≈ 2050 m. With an assumed surface temperature of 10 °C (NL annual average), the geothermal gradient is:

$$G = (75 - 10) / 2.050 = 31.7 \text{ °C/km}$$

This is consistent with the Dutch onshore average (30–32 °C/km) and cross-validates against ThermoGIS reservoir temperatures to within ±7 °C across all four wells.

## 4. Petrophysical interpretation

Methodology (full implementation in `06_ai_workflow_bonus/pipeline/pipeline.py`):

- **Density-porosity:** ϕ_D = (ρ_ma − ρ_b) / (ρ_ma − ρ_fl), with ρ_ma = 2.65 g/cc (quartz matrix) and ρ_fl = 1.0 g/cc (water-saturated)
- **Vshale (Larionov, older rocks):** V_sh = 0.33 × (2^(2·IGR) − 1), IGR = (GR − 25) / (150 − 25)
- **Effective porosity:** ϕ_eff = ϕ_D − V_sh × 0.30 (shale porosity assumed 0.30, NL Permian convention)
- **Net-to-gross:** fraction of samples with V_sh < 0.5 AND ϕ_eff > 0.05

Results on the true Slochteren interval (TVD-defined) for each well:

| Well | Slochteren top (TVD) | Thickness | Mean GR | V_sh | ϕ_total | ϕ_eff | NTG | n samples |
|---|---|---|---|---|---|---|---|---|
| BLT-01 | 1,862 m | 122 m | 49 gAPI | 0.10 | 14.4% | **11.4%** | 0.93 | 1,689 |
| EVD-01 | 1,783 m | 77 m | 29 gAPI | 0.02 | 8.4% | **8.0%** | 0.82 | 780 |
| JUT-01 | 1,655 m | 126 m | 24 gAPI | 0.01 | 11.1% | **10.9%** | 0.86 | 836 |
| PKP-01 | 2,207 m | 64 m | 65 gAPI | 0.19 | 5.4% | **1.1%** | 0.03 | 730 |

## 5. ThermoGIS vs LAS comparison (the key finding)

ThermoGIS reports regional model averages; the LAS-derived numbers are well-specific. The two diverge most sharply for PKP-01:

| Well | ϕ ThermoGIS | ϕ LAS-derived | NTG ThermoGIS | NTG LAS-derived |
|---|---|---|---|---|
| BLT-01 | 17% | 11.4% | 0.98 | 0.93 |
| EVD-01 | 9% | 8.0% | 0.99 | 0.82 |
| JUT-01 | 11% | 10.9% | 0.99 | 0.86 |
| PKP-01 | 9% | **1.1%** | 0.95 | **0.03** |

**PKP-01 is effectively a dead reservoir at this location** — the actual Slochteren interval is dominated by shale (V_sh = 0.19, GR = 65 gAPI) with virtually no net pay (NTG = 0.03). The ThermoGIS regional model averages out this local depletion; a feasibility study relying only on ThermoGIS would have proposed this well as a viable candidate. This is a real-data finding worth highlighting in the report — it argues for always grounding regional models in well-specific log analysis.

## 6. Reservoir deliverability ranking

Combining ThermoGIS deliverability with LAS-derived quality:

| Rank | Well | Top (TVD) | k×h (Dm) | T (°C) | Flow rate P50 (m³/h) | Power P50 (MWth) | Dist. to USP (km) | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | **BLT-01** | 1,862 | 9.3 | 77 | 105 | **5.1** | 2.0 | Primary producer |
| 2 | JUT-01 | 1,655 | 4.8 | 72 | 55 | 2.3 | 7.7 | Viable but distant |
| 3 | EVD-01 | 1,783 | 0.4 | 72 | 0 | 0 | 14.3 | Uneconomic (k too low) |
| 4 | PKP-01 | 2,207 | 0.1 | 88 | 0 | 0 | 22.7 | Uneconomic + tight |

BLT-01 is the unambiguous primary candidate. It has:
- The highest k×h (9.3 Dm) — translates directly to flow rate
- The shortest distance to the USP (2.0 km — minimal pipeline)
- A proven petrophysical signature matching the ThermoGIS regional model
- An economic flow rate at P50 (105 m³/h, 5.1 MWth)

## 7. Recommended development — doublet design

### Producer: BLT-01

Use BLT-01 as-is with a recompletion workover. Production at 105 m³/h, 77 °C, ΔT = 42 °C against an injection temperature of 35 °C → **5.1 MWth direct geothermal output at P50**.

### Injector: USP-01 (new well, proposed)

**Proposed location:** X = 141,278, Y = 455,412 (RD New).

This position is 1.5 km from BLT-01 (sufficient spacing to defer thermal breakthrough beyond the project lifetime) and 0.53 km from the USP (minimizing surface infrastructure). Inverse-distance interpolation against BLT-01 (weight 0.84) and JUT-01 (weight 0.16) gives predicted properties:

| Property | Predicted USP-01 |
|---|---|
| Slochteren top (TVD) | 1,830 m |
| Thickness | 123 m |
| Porosity | 11.4% |
| Permeability | 75 mD |
| Reservoir temperature | 76 °C |
| Predicted flow rate (P50) | 97 m³/h |

USP-01 takes the injector role specifically because it is the new well with the more uncertain performance. Using BLT-01 (proven) as the producer locks in the 5.1 MWth baseline regardless of how USP-01 underperforms.

### Thermal breakthrough analysis

Doublet spacing of 1.5 km with 105 m³/h flow rate, 0.11 porosity, and 122 m thickness gives a breakthrough time estimate from the simple plug-flow approximation:

$$\tau_{\text{plug-flow}} = \pi \cdot \phi \cdot h \cdot r^2 / q = \pi \cdot 0.11 \cdot 122 \cdot 1500^2 / (105/3600) \approx 1.03 \times 10^{9}\ \text{s} \approx \textbf{103 years}$$

This plug-flow value is the hydraulic pore-volume sweep time. Applying the industry ÷3 heterogeneity (fingering) derate used in `08_references/methodology/doublet_design.md` gives a **practical estimate of ≈34 years**. Both figures comfortably exceed the 25-year project lifetime (a true thermal-breakthrough calculation, which includes rock-matrix heat retardation, is longer still). Tracer testing or full reservoir simulation should confirm the timing in the detailed engineering phase.

## 8. Resource adequacy for the demand

The brief requires ≥10 MWth heating and ≥5 MWth cooling. The recommended doublet delivers 5.1 MWth direct geothermal — half the heating target.

The shortfall is closed by the surface system (two heat pumps, absorption chiller, ATES). See `04_models/surface_system_model/surface_system_design_v01.md` for the integrated solution.

The conclusion is that **a single doublet is sufficient when augmented with the heat-pump-and-storage surface architecture**. A second geothermal doublet was considered but rejected on capital-cost grounds — the surface system delivers the gap at lower CapEx per MW than a second well pair.

## 9. Design considerations and engineering judgment

Items requiring detailed engineering before final investment decision:

- **USP-01 deliverability prediction (97 m³/h)** is based on inverse-distance interpolation against two analogs. A pre-drill seismic-based reservoir characterization should be run to validate the predicted Slochteren top depth (±50 m TVD uncertainty) and quality.
- **ThermoGIS regional model vs. LAS-specific data**: as PKP-01 demonstrated, regional averages can mask local heterogeneity. The recommendation to drill at USP-01 should be supported by a higher-resolution local 3D model (TNO can produce this).
- **Fault avoidance for USP-01**: the regional structural map needs to be checked to confirm the proposed location isn't on a major fault that could compartmentalize the reservoir.
- **Pressure depletion risk**: with 5.1 MW production over 25 years, cumulative volume extracted is ~22 million m³. Need to confirm reservoir pressure support is adequate; the injector returns equal volume but cooler.
- **Slochteren brine geochemistry**: composition data (TDS, scaling tendency) wasn't in the data pack. Brine sampling in BLT-01 during workover is needed to size the corrosion-resistant materials in the surface plant.

## 10. References

- ThermoGIS portal: https://www.thermogis.nl/
- Van Wees et al. (2012) — ThermoGIS methodology for NL geothermal assessment
- Mijnlieff et al. (2014) — Rotliegend reservoir characterization, NL onshore
- IF Technology (2018) — Dutch geothermal doublet design handbook
- Larionov (1969) — Vshale-from-gamma-ray formula, original publication

Person 4 should locate and add these to `08_references/papers/` and bibliography.

## 11. Reproducibility

Every number in this document is reproducible from:

1. The raw data in `01_data_raw/` (LAS, deviation surveys, lithostratigraphy, ThermoGIS)
2. The cleaned datasets in `02_data_processed/`
3. The AI workflow notebook `06_ai_workflow_bonus/notebooks/petrophysics_pipeline.ipynb`

Re-run the notebook (`Run All Cells`) to regenerate the petrophysical summary table — should match Section 4 exactly.
