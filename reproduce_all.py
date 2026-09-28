"""
reproduce_all.py — single entry point that rebuilds every processed dataset
from the RAW data in 01_data_raw/.

Run from the project root:
    python reproduce_all.py            # regenerate all processed files in place
    python reproduce_all.py --verify   # write to a temp dir and diff vs committed (no overwrite)

Regenerates, in order:
  1. 02_data_processed/tvd_conversions/<well>_deviation_survey.csv   (from well_path_data.xlsx)
  2. 02_data_processed/cleaned_csv/<well>_lithostratigraphy_tvd.csv  (litho tops MD->TVD)
  3. 02_data_processed/cleaned_csv/target_lithologies_v01.csv        (per-sample Slochteren table)
  4. 02_data_processed/petrophysics/slochteren_petrophysics_summary_v01.csv
  5. 02_data_processed/reservoir_summary/project_constants_v01.csv   (gradient + USP triangulation)
  6. 02_data_processed/monte_carlo/lcoe_percentiles_v01.csv + lcoe_distribution_stats_v01.csv

Everything downstream (the two xlsx workbooks and the figures) consumes these files.
"""
import argparse
import sys
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "06_ai_workflow_bonus" / "pipeline"))
import pipeline as P  # noqa: E402
sys.path.insert(0, str(ROOT / "03_analysis" / "scripts"))
from lcoe_model import lcoe as lcoe_fn  # noqa: E402  (single source of truth for the LCoE)

WELLS = ["BLT-01", "EVD-01", "JUT-01", "PKP-01"]
RAW = ROOT / "01_data_raw"
LITHO_XLSX = RAW / "lithostratigraphy" / "lithostratigraphic_data.xlsx"
WELLPATH_XLSX = RAW / "well_paths" / "well_path_data.xlsx"

# Wellhead surface locations (RD New), from the LAS headers.
SURFACE_XY = {
    "BLT-01": (141577.55, 456881.76),
    "EVD-01": (136997.00, 441189.00),
    "JUT-01": (134098.00, 451726.00),
    "PKP-01": (118503.09, 453402.51),
}


def slug(well):
    return well.lower().replace("-", "")


def step1_deviation_surveys(out_processed):
    """Export each well's deviation survey sheet to CSV (lossless format conversion)."""
    out = out_processed / "tvd_conversions"
    out.mkdir(parents=True, exist_ok=True)
    for w in WELLS:
        df = pd.read_excel(WELLPATH_XLSX, sheet_name=w)
        df.to_csv(out / f"{slug(w)}_deviation_survey.csv", index=False)


def step2_litho_tvd(out_processed, surveys_dir):
    """Convert lithostratigraphy MD tops/bases to TVD using each well's survey."""
    out = out_processed / "cleaned_csv"
    out.mkdir(parents=True, exist_ok=True)
    for w in WELLS:
        interp = P.md_to_tvd_interpolator(surveys_dir / f"{slug(w)}_deviation_survey.csv")
        lt = pd.read_excel(LITHO_XLSX, sheet_name=w)
        rows = []
        for _, r in lt.iterrows():
            unit = r.get("Stratigrafical unit")
            top_md, bot_md = r.get("Top (m)"), r.get("Bottom (m)")
            if pd.isna(top_md) or pd.isna(bot_md):
                continue
            rows.append({
                "unit": unit,
                "top_md_m": top_md,
                "bottom_md_m": bot_md,
                "anomaly_code": r.get("Anomaly code"),
                "top_tvd_m": float(interp["tvd"](top_md)),
                "bottom_tvd_m": float(interp["tvd"](bot_md)),
            })
        pd.DataFrame(rows).to_csv(out / f"{slug(w)}_lithostratigraphy_tvd.csv", index=False)


# USP location (RD New). Triangulated by least squares from the four
# distance-to-USP values in the ORIGINAL target_lithologies.csv (residuals ~1e-7 km).
# The original CSV is not redistributed, so the solved constant is recorded here and
# used as the reference point for distance_to_usp below.
USP_XY = (141171.0, 454890.0)


def _clean_reservoir_df(well, surveys_dir):
    df, _ = P.ingest_las(RAW / "well_logs_las" / f"{slug(well)}.las")
    df, qc = P.qc_curves(df)
    interp = P.md_to_tvd_interpolator(surveys_dir / f"{slug(well)}_deviation_survey.csv")
    df = P.add_tvd_columns(df, interp)
    df = P.compute_petrophysics(df)
    top_tvd, base_tvd = P.find_reservoir_interval(LITHO_XLSX, well, interp)
    return df, interp, top_tvd, base_tvd, qc


def step3_target_lithologies(out_processed, surveys_dir):
    out = out_processed / "cleaned_csv"
    frames = []
    for w in WELLS:
        df, interp, top_tvd, base_tvd, _ = _clean_reservoir_df(w, surveys_dir)
        lt = pd.read_excel(LITHO_XLSX, sheet_name=w)
        m = lt[lt["Stratigrafical unit"].str.contains("Slochteren", case=False, na=False)]
        row = m.iloc[m["Top (m)"].argmin()]
        top_md, base_md = float(row["Top (m)"]), float(row["Bottom (m)"])
        rdf = df[(df["TVD"] >= top_tvd) & (df["TVD"] <= base_tvd)].copy()
        sx, sy = SURFACE_XY[w]
        easting = (sx + rdf["X_offset"]).round(2)
        northing = (sy + rdf["Y_offset"]).round(2)
        frames.append(pd.DataFrame({
            "well_id": w,
            "easting": easting,
            "northing": northing,
            "md_m": rdf["MD"].round(2),
            "depth_tvd_m": rdf["TVD"].round(2),
            "porosity_pct": (rdf["PHID"] * 100).round(2) if "PHID" in rdf else np.nan,
            "gamma_ray_api": rdf["GR"].round(2) if "GR" in rdf else np.nan,
            "bulk_density_gcc": rdf["RHOB"].round(4) if "RHOB" in rdf else np.nan,
            "formation_top_md": top_md,
            "formation_base_md": base_md,
            "formation_top_tvd": round(top_tvd, 2),
            "formation_base_tvd": round(base_tvd, 2),
            "formation_thickness_tvd_m": round(base_tvd - top_tvd, 2),
            "distance_to_usp_km": (np.sqrt((easting - USP_XY[0]) ** 2 +
                                           (northing - USP_XY[1]) ** 2) / 1000).round(3),
            "flag": "ok",
            "flag_reason": ("TVD converted from deviation survey; porosity from "
                            "density-porosity equation (rho_ma=2.65, rho_fl=1.0)"),
        }))
    pd.concat(frames, ignore_index=True).to_csv(out / "target_lithologies_v01.csv", index=False)


def step4_petrophysics_summary(out_processed, surveys_dir):
    out = out_processed / "petrophysics"
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    for w in WELLS:
        df, _, top_tvd, base_tvd, _ = _clean_reservoir_df(w, surveys_dir)
        s = P.summarize_reservoir(df, top_tvd, base_tvd)
        rows.append({
            "well_id": w,
            "slochteren_top_tvd_m": s["top_tvd_m"],
            "slochteren_base_tvd_m": s["base_tvd_m"],
            "thickness_tvd_m": s["thickness_tvd_m"],
            "gr_mean_gapi": s["gr_mean_gapi"],
            "vshale_mean_frac": s["vsh_mean"],
            "phi_total_frac": s["phid_mean"],
            "phi_eff_frac": s["phie_mean"],
            "ntg_log_derived": s["ntg"],
            "n_log_samples": s["n_log_samples"],
        })
    pd.DataFrame(rows).to_csv(out / "slochteren_petrophysics_summary_v01.csv", index=False)


def step5_project_constants(out_processed):
    """Geothermal gradient from BLT-01 BHT (uses TVD) + USP/USP-01 coordinates."""
    out = out_processed / "reservoir_summary"
    out.mkdir(parents=True, exist_ok=True)
    # BLT-01: BHT 167 degF at bottom (TD 2123 m MD -> TVD 2051 m from the survey).
    bht_c = (167 - 32) / 1.8              # 75 C
    surface_c = 10.0
    tvd_bht_km = 2.0514                   # TVD at 2123 m MD (BLT-01 deviation survey)
    gradient = round((bht_c - surface_c) / tvd_bht_km, 1)  # 31.7 C/km
    df = pd.DataFrame([
        ["usp_x_rd_new", USP_XY[0], "m", "triangulated from 4 wells"],
        ["usp_y_rd_new", USP_XY[1], "m", "triangulated from 4 wells"],
        ["geothermal_gradient_C_per_km", gradient, "C/km",
         "derived from BLT-01 BHT 167F (75C) at TVD 2051 m (=2123 m MD), surface 10C"],
        ["surface_temperature_C", surface_c, "C", "NL annual avg"],
        ["usp01_x_rd_new", 141278.0, "m", "proposed new well (injector for BLT-01 doublet)"],
        ["usp01_y_rd_new", 455412.0, "m", "proposed new well"],
    ], columns=["parameter", "value", "unit", "source"])
    df.to_csv(out / "project_constants_v01.csv", index=False)


def step6_monte_carlo(out_processed, seed=42, n=10_000):
    out = out_processed / "monte_carlo"
    out.mkdir(parents=True, exist_ok=True)
    np.random.seed(seed)  # matches lead_monte_carlo_v01.ipynb for reproducibility
    flow_rate = np.clip(np.random.normal(105, 105 * 0.15, n), 60, 150)
    elec_price = np.random.lognormal(np.log(100), 0.2, n)
    discount_rate = np.clip(np.random.normal(0.07, 0.015, n), 0.04, 0.10)
    capex = np.random.normal(23.7, 23.7 * 0.15, n)
    fleh = np.clip(np.random.normal(2400, 2400 * 0.10, n), 1500, 3200)
    # Deterministic LCoE per draw via the SHARED model (identical to lead_monte_carlo_v01.ipynb).
    lcoe = np.array([
        lcoe_fn(flow=flow_rate[i], discount=discount_rate[i], heating_fleh=fleh[i],
                elec_price=elec_price[i], capex_M=capex[i])
        for i in range(n)
    ])
    pd.DataFrame({
        "percentile": ["P10", "P25", "P50", "P75", "P90"],
        "lcoe_eur_per_mwh": [round(np.percentile(lcoe, p), 1) for p in [10, 25, 50, 75, 90]],
    }).to_csv(out / "lcoe_percentiles_v01.csv", index=False)
    pd.DataFrame({
        "metric": ["mean", "std", "P10", "P25", "P50", "P75", "P90", "min", "max", "n_simulations"],
        "lcoe_eur_per_mwh": [
            round(lcoe.mean(), 1), round(lcoe.std(), 1),
            *[round(np.percentile(lcoe, p), 1) for p in [10, 25, 50, 75, 90]],
            round(lcoe.min(), 1), round(lcoe.max(), 1), float(n),
        ],
    }).to_csv(out / "lcoe_distribution_stats_v01.csv", index=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true",
                    help="write to a temp dir and diff against committed files instead of overwriting")
    args = ap.parse_args()

    if args.verify:
        import tempfile
        out_processed = Path(tempfile.mkdtemp(prefix="repro_"))
    else:
        out_processed = ROOT / "02_data_processed"

    surveys_dir = out_processed / "tvd_conversions"
    step1_deviation_surveys(out_processed)
    step2_litho_tvd(out_processed, surveys_dir)
    step3_target_lithologies(out_processed, surveys_dir)
    step4_petrophysics_summary(out_processed, surveys_dir)
    step5_project_constants(out_processed)
    step6_monte_carlo(out_processed)
    print(f"[reproduce_all] wrote processed datasets to: {out_processed}")

    if args.verify:
        committed = ROOT / "02_data_processed"
        checks = [
            "petrophysics/slochteren_petrophysics_summary_v01.csv",
            "monte_carlo/lcoe_percentiles_v01.csv",
            "cleaned_csv/target_lithologies_v01.csv",
        ]
        for rel in checks:
            a = pd.read_csv(out_processed / rel)
            b = pd.read_csv(committed / rel)
            same_shape = a.shape == b.shape
            maxdiff, na_match = 0.0, True
            if same_shape:
                num = a.select_dtypes("number")
                bnum = b[num.columns]
                na_match = num.isna().equals(bnum.isna())        # NaN cells must line up
                if not num.empty:
                    maxdiff = float((num.fillna(0) - bnum.fillna(0)).abs().to_numpy().max())
            status = "OK" if (same_shape and na_match and maxdiff < 0.15) else "DIFF"
            print(f"  {rel}: shape {a.shape} vs {b.shape}, max_abs_diff={maxdiff:.3g} -> {status}")


if __name__ == "__main__":
    main()
