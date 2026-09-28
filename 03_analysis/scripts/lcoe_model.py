"""
Shared LCoE model for the hybrid geothermal heating+cooling system.

This is the SINGLE SOURCE OF TRUTH for the deterministic LCoE calculation. Both the
sensitivity tornado (`p3_lcoe_sensitivity_v01.ipynb`) and the Monte Carlo
(`lead_monte_carlo_v01.ipynb`) import `lcoe()` from here so the two analyses cannot
drift apart.

Design intent (why this replaces the earlier hand-entered sensitivities):
  * Heat-pump electricity is DERIVED from the coefficient of performance and the
    delivered heat (W = Q/COP), so HP-1 COP genuinely affects the result.
  * Heat-pump electricity scales with the heating full-load-equivalent hours (FLEH),
    so utilisation moves both the numerator (electricity) and the denominator
    (energy delivered) — not just the denominator.
  * Flow rate drives the direct geothermal heat; any shortfall to the heating peak is
    made up by the heat pumps (extra electricity), and doublet pumping electricity
    scales with flow. So the doublet-deliverability risk has a real, computed effect.

The base case reproduces the workbook deterministic LCoE (Sheet 5 `B17` = ~EUR 122/MWh).
"""

# ---- system-design constants (from surface_system_design_v01.md / LCoE workbook) ----
GEO_POWER_AT_P50 = 5.1      # MWth direct geothermal heat at 105 m3/h (BLT-01 P50)
FLOW_P50 = 105.0            # m3/h reference flow
HP1_HEAT = 3.42             # MWth delivered by HP-1 (return-brine) at base
HP2_HEAT = 2.17             # MWth delivered by HP-2 (ATES warm well) at base
PUMP_ELEC_BASE = 2250.0     # MWh/yr doublet + district circulation pumps at base flow
CAPEX_SUBTOTAL_EX_DRILL = 15.6   # EUR M, all CapEx line items except the USP-01 drilling line, pre-contingency
CONTINGENCY = 1.15          # 15% contingency multiplier
DRILLING_BASE = 5.0         # EUR M, USP-01 drilling (base)
MAINT_FRAC = 0.025          # maintenance = 2.5% of CapEx per year
FIXED_OPEX_M = 0.350        # EUR M/yr labour + monitoring + insurance (250k + 100k)

# Base electricity that is neither HP-heating nor doublet pumping (cooling chiller,
# auxiliaries, fixed loads). Calibrated so the base total electricity = 8750 MWh/yr,
# matching the LCoE workbook OpEx sheet.
_E_HEAT_BASE = None  # filled below
_E_FIXED = None      # filled below


def crf(discount, lifetime):
    """Capital recovery factor."""
    return discount / (1.0 - (1.0 + discount) ** (-lifetime))


def _heating_hp_electricity(flow, hp1_cop, hp2_cop, heating_fleh, heating_peak):
    """MWh/yr of heat-pump electricity for heating.

    Geothermal supplies q_geo (scales with flow); heat pumps fill the gap to the
    heating peak (HP-1 first up to its rating, then HP-2, then electric-resistance
    backup at COP 1 if the pumps cannot cover a large shortfall).
    """
    q_geo = GEO_POWER_AT_P50 * flow / FLOW_P50
    hp_gap = max(0.0, heating_peak - q_geo)
    q_hp1 = min(HP1_HEAT, hp_gap)
    q_hp2 = min(HP2_HEAT, hp_gap - q_hp1)
    q_backup = max(0.0, hp_gap - q_hp1 - q_hp2)          # electric resistance, COP 1
    load_mw = q_hp1 / hp1_cop + q_hp2 / hp2_cop + q_backup / 1.0
    return load_mw * heating_fleh


# Calibrate the fixed-electricity term so the base case totals 8750 MWh/yr.
_E_HEAT_BASE = _heating_hp_electricity(FLOW_P50, 3.5, 4.0, 2400.0, 10.0)
_E_FIXED = 8750.0 - _E_HEAT_BASE - PUMP_ELEC_BASE


def total_electricity(flow=FLOW_P50, hp1_cop=3.5, hp2_cop=4.0,
                      heating_fleh=2400.0, heating_peak=10.0):
    """Annual electricity consumption (MWh/yr) for the whole system."""
    e_heat = _heating_hp_electricity(flow, hp1_cop, hp2_cop, heating_fleh, heating_peak)
    e_pump = PUMP_ELEC_BASE * flow / FLOW_P50
    return e_heat + e_pump + _E_FIXED


def capex_from_drilling(drilling=DRILLING_BASE):
    """Total CapEx (EUR M) as a function of the USP-01 drilling cost line."""
    return (CAPEX_SUBTOTAL_EX_DRILL + drilling) * CONTINGENCY


def lcoe(flow=FLOW_P50, discount=0.07, lifetime=25,
         heating_fleh=2400.0, cooling_fleh=1500.0,
         hp1_cop=3.5, hp2_cop=4.0, elec_price=100.0,
         capex_M=None, drilling=DRILLING_BASE,
         heating_peak=10.0, cooling_peak=5.0):
    """Deterministic LCoE in EUR/MWh.

    capex_M: if given, used directly (Monte Carlo samples this). Otherwise CapEx is
             derived from `drilling` (used by the drilling-cost sensitivity).
    """
    if capex_M is None:
        capex_M = capex_from_drilling(drilling)

    elec_mwh = total_electricity(flow, hp1_cop, hp2_cop, heating_fleh, heating_peak)
    elec_cost_M = elec_mwh * elec_price / 1e6
    opex_M = MAINT_FRAC * capex_M + FIXED_OPEX_M + elec_cost_M

    annualized_capex_M = capex_M * crf(discount, lifetime)
    energy_mwh = heating_peak * heating_fleh + cooling_peak * cooling_fleh
    return (annualized_capex_M + opex_M) * 1e6 / energy_mwh


BASE_INPUTS = dict(flow=FLOW_P50, discount=0.07, lifetime=25, heating_fleh=2400.0,
                   cooling_fleh=1500.0, hp1_cop=3.5, hp2_cop=4.0, elec_price=100.0,
                   drilling=DRILLING_BASE, heating_peak=10.0, cooling_peak=5.0)

# One-at-a-time tornado inputs: (label, kwarg, low_value, high_value)
SENSITIVITY_CASES = [
    ("Heating FLEH (\u00b120%)",        "heating_fleh", 1920.0, 2880.0),
    ("Discount rate (\u00b120%)",       "discount",     0.056,  0.084),
    ("Project lifetime (20\u219230 yr)", "lifetime",    20,     30),
    ("NL electricity price (\u00b120%)", "elec_price",  80.0,   120.0),
    ("Drilling cost (\u00b120%)",       "drilling",     4.0,    6.0),
    ("HP-1 COP (2.8 vs 4.2)",           "hp1_cop",      2.8,    4.2),
    ("USP-01 flow rate (\u00b120%)",    "flow",         84.0,   126.0),
]


def tornado_deltas():
    """Return [(label, delta_low, delta_high)] computed from the model."""
    base = lcoe(**BASE_INPUTS)
    out = []
    for label, kw, lo, hi in SENSITIVITY_CASES:
        d_lo = lcoe(**{**BASE_INPUTS, kw: lo}) - base
        d_hi = lcoe(**{**BASE_INPUTS, kw: hi}) - base
        out.append((label, d_lo, d_hi))
    return out


if __name__ == "__main__":
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    b = lcoe(**BASE_INPUTS)
    print(f"Base LCoE = {b:.2f} EUR/MWh (workbook B17 ~ 122.2)")
    print(f"Base electricity = {total_electricity():.0f} MWh/yr (workbook = 8750)")
    print(f"Base CapEx = {capex_from_drilling():.2f} EUR M (workbook = 23.7)")
    print("\nTornado (sorted by magnitude):")
    for label, lo, hi in sorted(tornado_deltas(), key=lambda x: max(abs(x[1]), abs(x[2])), reverse=True):
        print(f"  {label:28} low {lo:+6.1f}   high {hi:+6.1f}")
