"""
Canonical data paths and load helpers.

Import from 03_analysis/notebooks/:
    sys.path.insert(0, '../../../03_analysis/scripts')
    from data_loading import paths, load_cleaned_target, load_petrophysics_summary
"""
import pandas as pd
from pathlib import Path

# Resolve the project root relative to this file
_HERE = Path(__file__).resolve().parent
ROOT = _HERE.parent.parent

paths = {
    'root': ROOT,
    'raw': ROOT / '01_data_raw',
    'processed': ROOT / '02_data_processed',
    'models': ROOT / '04_models',
    'viz': ROOT / '05_visualizations',
    'las': {
        'BLT-01': ROOT / '01_data_raw' / 'well_logs_las' / 'blt01.las',
        'EVD-01': ROOT / '01_data_raw' / 'well_logs_las' / 'evd01.las',
        'JUT-01': ROOT / '01_data_raw' / 'well_logs_las' / 'jut01.las',
        'PKP-01': ROOT / '01_data_raw' / 'well_logs_las' / 'pkp01.las',
    },
    'survey': {
        'BLT-01': ROOT / '02_data_processed' / 'tvd_conversions' / 'blt01_deviation_survey.csv',
        'EVD-01': ROOT / '02_data_processed' / 'tvd_conversions' / 'evd01_deviation_survey.csv',
        'JUT-01': ROOT / '02_data_processed' / 'tvd_conversions' / 'jut01_deviation_survey.csv',
        'PKP-01': ROOT / '02_data_processed' / 'tvd_conversions' / 'pkp01_deviation_survey.csv',
    },
    'lithostrat': ROOT / '01_data_raw' / 'lithostratigraphy' / 'lithostratigraphic_data.xlsx',
    'thermogis': ROOT / '01_data_raw' / 'thermogis' / 'thermogis_data.xlsx',
    'well_paths': ROOT / '01_data_raw' / 'well_paths' / 'well_path_data.xlsx',
    'cleaned_target': ROOT / '02_data_processed' / 'cleaned_csv' / 'target_lithologies_v01.csv',
    'petrophysics': ROOT / '02_data_processed' / 'petrophysics' / 'slochteren_petrophysics_summary_v01.csv',
    'constants': ROOT / '02_data_processed' / 'reservoir_summary' / 'project_constants_v01.csv',
    'lcoe': ROOT / '04_models' / 'lcoe_workbook' / 'lcoe_hybrid_system_v01.xlsx',
    'subsurface_assessment': ROOT / '04_models' / 'reservoir_model' / 'subsurface_assessment_v01.xlsx',
}


def load_cleaned_target():
    """Load the repaired target_lithologies.csv."""
    return pd.read_csv(paths['cleaned_target'])


def load_petrophysics_summary():
    """Load the per-well petrophysical summary."""
    return pd.read_csv(paths['petrophysics'])


def load_constants():
    """Load project constants (USP location, gradient, USP-01 coords)."""
    df = pd.read_csv(paths['constants'])
    return {row['parameter']: row['value'] for _, row in df.iterrows()}


def load_thermogis(well):
    """Load ThermoGIS data for one well (returns the full sheet)."""
    return pd.read_excel(paths['thermogis'], sheet_name=well)


def load_lithostrat(well, tvd=True):
    """Load lithostratigraphy for one well. If tvd=True, returns the pre-converted CSV.
    Otherwise returns the original MD-based xlsx sheet."""
    if tvd:
        slug = well.lower().replace('-', '')
        return pd.read_csv(ROOT / '02_data_processed' / 'cleaned_csv' / f'{slug}_lithostratigraphy_tvd.csv')
    return pd.read_excel(paths['lithostrat'], sheet_name=well)


def well_surface_locations():
    """Return wellhead XY locations in RD New coordinates."""
    return {
        'BLT-01': (141577.55, 456881.76),
        'EVD-01': (136997.00, 441189.00),
        'JUT-01': (134098.00, 451726.00),
        'PKP-01': (118503.09, 453402.51),
    }
