"""
Geothermal AI workflow — automated LAS-to-petrophysics pipeline.


Usage:
    from pipeline import run_pipeline
    
    df, summary, qc = run_pipeline(
        well_id='BLT-01',
        las_path='01_data_raw/well_logs_las/blt01.las',
        survey_path='02_data_processed/tvd_conversions/blt01_deviation_survey.csv',
        litho_path='01_data_raw/lithostratigraphy/lithostratigraphic_data.xlsx',
        litho_sheet='BLT-01'
    )
"""
import lasio
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from sklearn.ensemble import IsolationForest
import warnings
warnings.filterwarnings('ignore')


def ingest_las(las_path):
    """Read a LAS file, normalize column names, replace null sentinels with NaN."""
    las = lasio.read(las_path)
    df = las.df().reset_index()

    rename_map = {}
    for c in df.columns:
        if c.upper() in ['MD', 'DEPT', 'DEPTH']:
            rename_map[c] = 'MD'
        elif c.upper().startswith('DEPT'):
            if ':2' in c:
                rename_map[c] = 'MD'
            elif ':1' in c:
                rename_map[c] = '_DEPT_FT'
    df = df.rename(columns=rename_map)
    if '_DEPT_FT' in df.columns:
        df = df.drop(columns=['_DEPT_FT'])

    df = df.replace(-999.25, np.nan).replace(-999.2500, np.nan)
    return df, las


def detect_anomalies(df, curve, contamination=0.01):
    """Flag anomalous values in a curve using Isolation Forest."""
    values = df[curve].dropna().values.reshape(-1, 1)
    if len(values) < 100:
        return pd.Series(False, index=df.index)

    detector = IsolationForest(contamination=contamination, random_state=42, n_estimators=100)
    detector.fit(values)

    predictions = pd.Series(False, index=df.index)
    mask = df[curve].notna()
    predictions.loc[mask] = detector.predict(df.loc[mask, curve].values.reshape(-1, 1)) == -1
    return predictions


def qc_curves(df, curves=None):
    """Run anomaly detection on all numeric curves; suppress flagged values."""
    if curves is None:
        curves = [c for c in df.columns if c != 'MD' and df[c].dtype in [np.float64, np.float32]]

    report_rows = []
    cleaned_df = df.copy()
    for curve in curves:
        if df[curve].notna().sum() < 100:
            continue
        anomalies = detect_anomalies(df, curve)
        n_anom = int(anomalies.sum())
        if n_anom > 0:
            anom_vals = df.loc[anomalies, curve]
            report_rows.append({
                'curve': curve,
                'n_anomalies': n_anom,
                'pct_of_valid': round(100 * n_anom / df[curve].notna().sum(), 2),
                'anom_min': float(anom_vals.min()),
                'anom_max': float(anom_vals.max()),
                'curve_normal_min': float(df.loc[~anomalies, curve].min()),
                'curve_normal_max': float(df.loc[~anomalies, curve].max()),
            })
            cleaned_df.loc[anomalies, curve] = np.nan

    return cleaned_df, pd.DataFrame(report_rows)


def md_to_tvd_interpolator(survey_path):
    """Build MD→TVD and MD→XY-offset interpolators from a deviation survey CSV."""
    survey = pd.read_csv(survey_path)
    return {
        'tvd': interp1d(survey['Depth (m)'], survey['TVD (m)'],
                        kind='linear', fill_value='extrapolate', bounds_error=False),
        'x_offset': interp1d(survey['Depth (m)'], survey['X-offset (m)'],
                             kind='linear', fill_value='extrapolate', bounds_error=False),
        'y_offset': interp1d(survey['Depth (m)'], survey['Y-offset (m)'],
                             kind='linear', fill_value='extrapolate', bounds_error=False),
        'survey': survey,
    }


def add_tvd_columns(df, interp):
    """Add TVD, X_offset, Y_offset columns to a LAS DataFrame."""
    df = df.copy()
    df['TVD'] = interp['tvd'](df['MD'].values)
    df['X_offset'] = interp['x_offset'](df['MD'].values)
    df['Y_offset'] = interp['y_offset'](df['MD'].values)
    return df


def find_reservoir_interval(litho_path, well_sheet, interp, formation_name='Slochteren Formation'):
    """Find the TVD interval for a named formation in the lithostratigraphy."""
    litho = pd.read_excel(litho_path, sheet_name=well_sheet)
    matches = litho[litho['Stratigrafical unit'].str.contains(formation_name, case=False, na=False)]
    if len(matches) == 0:
        return None, None
    row = matches.iloc[matches['Top (m)'].argmin()]
    top_tvd = float(interp['tvd'](row['Top (m)']))
    base_tvd = float(interp['tvd'](row['Bottom (m)']))
    return top_tvd, base_tvd


def compute_petrophysics(df, gr_clean=25, gr_shale=150, rho_ma=2.65, rho_fl=1.0,
                          shale_porosity=0.30, gr_curve='GR', rhob_curve='RHOB'):
    """Add density-porosity, Vshale (Larionov), and effective porosity columns."""
    df = df.copy()
    if rhob_curve in df.columns:
        df['PHID'] = (rho_ma - df[rhob_curve]) / (rho_ma - rho_fl)
        df.loc[df['PHID'] < 0, 'PHID'] = 0
        df.loc[df['PHID'] > 0.5, 'PHID'] = np.nan
    if gr_curve in df.columns:
        df['IGR'] = (df[gr_curve] - gr_clean) / (gr_shale - gr_clean)
        df.loc[df['IGR'] < 0, 'IGR'] = 0
        df.loc[df['IGR'] > 1, 'IGR'] = 1
        df['VSH'] = 0.33 * (2 ** (2 * df['IGR']) - 1)
        df.loc[df['VSH'] > 1, 'VSH'] = 1
    if 'PHID' in df.columns and 'VSH' in df.columns:
        df['PHIE'] = df['PHID'] - df['VSH'] * shale_porosity
        df.loc[df['PHIE'] < 0, 'PHIE'] = 0
    return df


def summarize_reservoir(df, top_tvd, base_tvd, gr_curve='GR'):
    """Compute the per-well reservoir summary table (one row)."""
    rdf = df[(df['TVD'] >= top_tvd) & (df['TVD'] <= base_tvd)]
    if len(rdf) == 0:
        return None
    net_mask = (rdf.get('VSH', pd.Series()) < 0.5) & (rdf.get('PHIE', pd.Series()) > 0.05)
    return {
        'top_tvd_m': round(top_tvd, 2),
        'base_tvd_m': round(base_tvd, 2),
        'thickness_tvd_m': round(base_tvd - top_tvd, 2),
        'n_log_samples': len(rdf),
        'gr_mean_gapi': round(rdf[gr_curve].mean(), 2) if gr_curve in rdf else None,
        'vsh_mean': round(rdf.get('VSH', pd.Series()).mean(), 4),
        'phid_mean': round(rdf.get('PHID', pd.Series()).mean(), 4),
        'phie_mean': round(rdf.get('PHIE', pd.Series()).mean(), 4),
        'ntg': round(net_mask.sum() / len(rdf), 4),
        'top_quartile_phie': round(rdf.get('PHIE', pd.Series()).quantile(0.75), 4),
    }


def run_pipeline(well_id, las_path, survey_path, litho_path=None, litho_sheet=None,
                 formation='Slochteren Formation', verbose=False):
    """End-to-end pipeline. Returns (clean_df, summary_dict, qc_report_df)."""
    df, _ = ingest_las(las_path)
    df, qc_report = qc_curves(df)
    interp = md_to_tvd_interpolator(survey_path)
    df = add_tvd_columns(df, interp)
    df = compute_petrophysics(df)

    if litho_path and litho_sheet:
        top_tvd, base_tvd = find_reservoir_interval(litho_path, litho_sheet, interp, formation)
        if top_tvd is None:
            return df, None, qc_report
        summary = summarize_reservoir(df, top_tvd, base_tvd)
        if summary:
            summary['well_id'] = well_id
        return df, summary, qc_report
    return df, None, qc_report
