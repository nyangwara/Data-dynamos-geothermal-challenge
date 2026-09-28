"""Render the raw-data -> deliverables workflow diagram (PNG + SVG)."""
import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUTDIR = os.path.join(ROOT, "05_visualizations", "system_diagrams")
os.makedirs(OUTDIR, exist_ok=True)

# --- palette (matches plotting_utils / deck) ---
INK = "#1F4E78"
ORANGE = "#D85A30"
BLUE = "#185FA5"
GOLD = "#E0A030"
TEAL = "#0F6E56"
GREEN = "#2E7D32"
GREY = "#5F5E5A"
LIGHT = "#F4F6F9"

plt.rcParams.update({"font.family": "sans-serif", "font.sans-serif": ["DejaVu Sans", "Arial"]})

fig, ax = plt.subplots(figsize=(16, 9))
ax.set_xlim(0, 16); ax.set_ylim(0, 9); ax.axis("off")

# ---- layer band definitions: (x, w, title, color) ----
COLW = 2.55
cols = [
    (0.20, "1 · RAW DATA\n01_data_raw", GREY),
    (2.95, "2 · PIPELINE\npipeline.py", BLUE),
    (5.70, "3 · PROCESSED\n02_data_processed", TEAL),
    (8.45, "4 · MODELS", ORANGE),
    (11.05, "5 · ANALYSIS \u2192 FIGURES", GOLD),
    (13.55, "6 · DELIVERABLES", INK),
]
BAND_Y, BAND_H = 0.70, 7.35
for x, title, color in cols:
    ax.add_patch(mpatches.FancyBboxPatch((x, BAND_Y), COLW, BAND_H,
                 boxstyle="round,pad=0.02,rounding_size=0.10",
                 fc=LIGHT, ec=color, lw=2.2, zorder=1))
    ax.add_patch(mpatches.FancyBboxPatch((x, BAND_Y + BAND_H - 0.72), COLW, 0.72,
                 boxstyle="square,pad=0", fc=color, ec=color, zorder=2))
    ax.text(x + COLW / 2, BAND_Y + BAND_H - 0.36, title, ha="center", va="center",
            color="white", fontsize=10.5, fontweight="bold", zorder=3)

boxes = {}   # id -> (cx, cy, w, h)

def node(col_i, y, text, fc="white", ec="#333333", key=None, h=0.82, fs=8.7, bold=False):
    x = cols[col_i][0]
    w = COLW - 0.36
    cx = x + 0.18 + w / 2
    ax.add_patch(mpatches.FancyBboxPatch((x + 0.18, y - h / 2), w, h,
                 boxstyle="round,pad=0.02,rounding_size=0.06",
                 fc=fc, ec=ec, lw=1.3, zorder=4))
    ax.text(cx, y, text, ha="center", va="center", fontsize=fs,
            fontweight="bold" if bold else "normal", zorder=5, color="#1a1a1a")
    if key:
        boxes[key] = (cx, y, w, h)
    return cx, y

# Column 1 · raw
node(0, 6.35, ".las well logs\n(4 wells)", key="las")
node(0, 5.15, "deviation surveys", key="surv")
node(0, 3.95, "lithostratigraphy\n(formation tops)", key="litho")
node(0, 2.60, "ThermoGIS snapshot", fc="#FBEEE6", ec=ORANGE, key="tgis")

# Column 2 · pipeline (vertical mini-chain)
node(1, 6.35, "ingest + IsolationForest QC", key="qc", fs=8.2)
node(1, 5.15, "MD \u2192 TVD  (survey interp)", key="tvd", fs=8.2)
node(1, 3.95, "petrophysics\ndensity-\u03d5 · Larionov · \u03d5e", key="petro", fs=8.2)
node(1, 2.60, "reservoir summary", key="psum2", fs=8.2)

# Column 3 · processed
node(2, 6.35, "target_lithologies.csv", key="target")
node(2, 5.15, "petrophysics_summary.csv\n\u03d5e · NTG", key="psum")
node(2, 3.95, "project_constants.csv", key="const")
node(2, 2.60, "monte_carlo/*.csv", key="mc")

# Column 4 · models
node(3, 6.15, "lcoe_model.py\nSINGLE SOURCE OF TRUTH\nbase \u20ac122/MWh",
     fc="#FBEEE6", ec=ORANGE, key="lcoe", h=1.15, fs=8.6, bold=True)
node(3, 4.35, "subsurface_assessment.xlsx\nranking + USP-01", key="subx", h=0.95, fs=8.2)
node(3, 2.85, "lcoe_hybrid_system.xlsx", key="lcx", fs=8.2)

# Column 5 · analysis -> figures
node(4, 6.35, "maps · cross-section\nlog panels", key="fig1", fs=8.2)
node(4, 4.95, "load profile · energy\nCapEx · process flow", key="fig2", fs=8.2)
node(4, 3.55, "tornado + Monte Carlo", key="fig3", fs=8.2)
node(4, 2.35, "PNG + SVG\n(05_visualizations)", fc="#FEF7E6", ec=GOLD, key="figout", fs=8.2)

# Column 6 · deliverables
node(5, 6.35, "technical report", fc="#E9EFF6", ec=INK, key="report")
node(5, 5.15, "pptx deck", fc="#E9EFF6", ec=INK, key="deck")
node(5, 3.95, "ThermoGIS\nverification report", fc="#E9EFF6", ec=INK, key="verif")
node(5, 2.60, "video", fc="#E9EFF6", ec=INK, key="video")

def arrow(a, b, color="#555555", ls="-", lw=1.6, rad=0.0):
    (ax0, ay0, aw, ah) = boxes[a]
    (bx0, by0, bw, bh) = boxes[b]
    start = (ax0 + aw / 2, ay0)
    end = (bx0 - bw / 2, by0)
    ax.add_patch(FancyArrowPatch(start, end, connectionstyle=f"arc3,rad={rad}",
                 arrowstyle="-|>", mutation_scale=12, lw=lw, color=color,
                 linestyle=ls, zorder=3))

# raw -> pipeline
arrow("las", "qc"); arrow("surv", "tvd"); arrow("litho", "petro")
# pipeline internal
for a, b in [("qc", "tvd"), ("tvd", "petro"), ("petro", "psum2")]:
    (ax0, ay0, aw, ah) = boxes[a]; (bx0, by0, bw, bh) = boxes[b]
    ax.add_patch(FancyArrowPatch((ax0, ay0 - ah / 2), (bx0, by0 + bh / 2),
                 arrowstyle="-|>", mutation_scale=9, lw=1.1, color=BLUE, zorder=3))
# pipeline -> processed
arrow("psum2", "target", rad=0.12); arrow("psum2", "psum"); arrow("psum2", "const", rad=-0.12)
# processed -> models / figures
arrow("psum", "subx", color=ORANGE)
arrow("const", "mc", rad=-0.05)
arrow("lcoe", "mc", color=ORANGE, rad=0.10)
arrow("lcoe", "lcx", color=ORANGE)
# processed -> analysis
arrow("target", "fig1", color=GOLD, rad=0.05)
arrow("mc", "fig3", color=GOLD, rad=-0.05)
arrow("lcoe", "fig3", color=ORANGE, rad=-0.18)
# analysis -> deliverables
arrow("fig1", "report", color=INK, rad=0.05)
arrow("fig2", "report", color=INK)
arrow("subx", "report", color=INK, rad=0.20)
arrow("lcx", "report", color=INK, rad=0.14)
arrow("fig3", "deck", color=INK, rad=-0.05)
# ThermoGIS dashed verify
(tx, ty, tw, th) = boxes["tgis"]; (px, py, pw, ph) = boxes["psum"]
ax.add_patch(FancyArrowPatch((tx + tw / 2, ty), (px - pw / 2, py - 0.15),
             connectionstyle="arc3,rad=0.28", arrowstyle="-|>", mutation_scale=11,
             lw=1.4, color=ORANGE, linestyle=(0, (4, 3)), zorder=3))
ax.text(6.0, 1.55, "verify  (PKP-01: ThermoGIS 9%  vs  LAS 1.1%)",
        fontsize=7.6, style="italic", color=ORANGE, ha="center")

# title + reproducibility footer
ax.text(0.20, 8.62, "Data flow \u2014 raw data to final deliverables",
        fontsize=17, fontweight="bold", color=INK)
ax.text(0.20, 8.20, "Data Dynamos · Geothermal Feasibility Study", fontsize=10.5, color=GREY)

ax.add_patch(mpatches.FancyBboxPatch((0.20, 0.06), 15.6, 0.5,
             boxstyle="round,pad=0.02,rounding_size=0.06", fc="#EEF2F6", ec="#C9D3DE", zorder=1))
ax.text(0.45, 0.31,
        "reproduce_all.py --verify  rebuilds layer 3 from layer 1 (committed diff = 0)   |   "
        "lcoe_model.py is imported by both the tornado and Monte Carlo (economics cannot drift)",
        fontsize=8.6, va="center", color="#333333", fontweight="bold")

plt.tight_layout()
png = os.path.join(OUTDIR, "data_flow_v01.png")
svg = os.path.join(OUTDIR, "data_flow_v01.svg")
fig.savefig(png, dpi=170, bbox_inches="tight")
fig.savefig(svg, bbox_inches="tight")
print("saved:", png)
print("saved:", svg)
