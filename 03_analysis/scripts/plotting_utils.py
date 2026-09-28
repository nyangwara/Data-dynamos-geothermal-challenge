"""
Reusable plotting helpers for the team's notebooks.

Import from 03_analysis/notebooks/:
    sys.path.insert(0, '../../../03_analysis/scripts')
    from plotting_utils import COLORS, style_axes, composite_log_panel
"""
import matplotlib.pyplot as plt
import numpy as np

COLORS = {
    'producer': '#D85A30',
    'injector': '#185FA5',
    'usp': '#1F4E78',
    'sand': '#F4A460',
    'shale': '#5F5E5A',
    'hp': '#E0A030',
    'chiller': '#0F6E56',
    'good': '#2E7D32',
    'bad': '#C62828',
    'neutral': '#5C6BC0',
    'grid': '#E0E0E0',
}


def apply_style():
    """Apply consistent matplotlib styling across all team notebooks."""
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['DejaVu Sans', 'Arial'],
        'axes.spines.right': False,
        'axes.spines.top': False,
        'axes.linewidth': 0.8,
        'axes.labelsize': 11,
        'axes.titlesize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 9,
        'legend.frameon': False,
        'figure.dpi': 100,
    })


def style_axes(ax, grid=True):
    """Apply consistent style to a single axes object."""
    if grid:
        ax.grid(True, color=COLORS['grid'], linestyle=':', linewidth=0.4, alpha=0.6)


def composite_log_panel(df, top_tvd, base_tvd, title='', figsize=(9, 9)):
    """4-track log panel (GR, RHOB, porosity, Vshale) for a single well over a reservoir interval.

    df: DataFrame with columns MD, TVD, GR, RHOB, PHID, PHIE, VSH
    top_tvd, base_tvd: reservoir interval limits in TVD
    """
    apply_style()
    fig, axes = plt.subplots(1, 4, figsize=figsize, sharey=True)
    win = df[(df['TVD'] >= top_tvd - 30) & (df['TVD'] <= base_tvd + 30)]

    # Track 1: GR
    axes[0].plot(win['GR'], win['TVD'], color=COLORS['shale'], linewidth=0.7)
    axes[0].axhspan(top_tvd, base_tvd, color=COLORS['sand'], alpha=0.2)
    axes[0].axvline(60, color='gray', linestyle='--', alpha=0.5)
    axes[0].invert_yaxis()
    axes[0].set_xlim(0, 200)
    axes[0].set_xlabel('GR (gAPI)')
    axes[0].set_ylabel('TVD (m)')
    axes[0].set_title('Gamma ray', loc='left', fontweight='bold', fontsize=10)
    style_axes(axes[0])

    # Track 2: RHOB
    axes[1].plot(win['RHOB'], win['TVD'], color=COLORS['producer'], linewidth=0.7)
    axes[1].axhspan(top_tvd, base_tvd, color=COLORS['sand'], alpha=0.2)
    axes[1].invert_yaxis()
    axes[1].set_xlim(2.0, 2.9)
    axes[1].set_xlabel('RHOB (g/cc)')
    axes[1].set_title('Bulk density', loc='left', fontweight='bold', fontsize=10)
    style_axes(axes[1])

    # Track 3: Porosity (PHIE filled, PHID overlay)
    if 'PHIE' in win.columns:
        axes[2].fill_betweenx(win['TVD'], 0, win['PHIE'].clip(lower=0) * 100,
                              color=COLORS['sand'], alpha=0.6, label='ϕ_eff')
    if 'PHID' in win.columns:
        axes[2].plot(win['PHID'] * 100, win['TVD'], color=COLORS['shale'],
                     linewidth=0.6, label='ϕ_total')
    axes[2].axhspan(top_tvd, base_tvd, color=COLORS['sand'], alpha=0.2)
    axes[2].invert_yaxis()
    axes[2].set_xlim(0, 25)
    axes[2].set_xlabel('Porosity (%)')
    axes[2].set_title('Porosity', loc='left', fontweight='bold', fontsize=10)
    axes[2].legend(loc='lower right', fontsize=8)
    style_axes(axes[2])

    # Track 4: Vshale
    if 'VSH' in win.columns:
        axes[3].fill_betweenx(win['TVD'], 0, win['VSH'].clip(lower=0),
                              color=COLORS['shale'], alpha=0.6)
        axes[3].axvline(0.5, color='red', linestyle='--', alpha=0.5, label='Net cutoff')
    axes[3].axhspan(top_tvd, base_tvd, color=COLORS['sand'], alpha=0.2)
    axes[3].invert_yaxis()
    axes[3].set_xlim(0, 1)
    axes[3].set_xlabel('Vshale')
    axes[3].set_title('Shale volume', loc='left', fontweight='bold', fontsize=10)
    axes[3].legend(loc='lower right', fontsize=8)
    style_axes(axes[3])

    plt.suptitle(title, fontweight='bold', y=1.00)
    plt.tight_layout()
    return fig, axes


def tornado_chart(items, base_value, figsize=(11, 7), title='Sensitivity tornado'):
    """Render a tornado chart for sensitivity analysis.

    items: list of (label, low_delta, high_delta) tuples
    """
    apply_style()
    items_sorted = sorted(items, key=lambda x: max(abs(x[1]), abs(x[2])), reverse=False)
    fig, ax = plt.subplots(figsize=figsize)
    ys = np.arange(len(items_sorted))
    for i, (label, low, high) in enumerate(items_sorted):
        ax.barh(i, low, color=COLORS['good'], edgecolor='white', height=0.6)
        ax.barh(i, high, color=COLORS['bad'], edgecolor='white', height=0.6)
    ax.axvline(0, color='black', linewidth=1.2)
    ax.set_yticks(ys)
    ax.set_yticklabels([s[0] for s in items_sorted])
    ax.set_xlabel(f'Δ from base = {base_value}')
    ax.set_title(title, loc='left', fontweight='bold')
    style_axes(ax, grid=False)
    ax.grid(True, axis='x', color=COLORS['grid'], linestyle=':', linewidth=0.4)
    plt.tight_layout()
    return fig, ax
