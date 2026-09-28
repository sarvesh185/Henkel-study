"""Figures for the RIZM submission. Palette from the validated reference instance."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter

from chp_model import (SCENARIOS, A, GAS_IN_MWH, TONNES_PRODUCT, COST_KEYS, EL_SHARE,
                       option_C_status_quo, option_A_replace,
                       option_A2_replace_el_sized, option_B_electrify,
                       option_D_operational, annuity, EF_GAS)

SURFACE = "#fcfcfb"
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e2e1dd"
CAT = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]   # fixed order
SEQ = ["#9ec5f4", "#3987e5", "#1c5cab"]                          # blue ramp, light->dark
POS, NEG, MID = "#2a78d6", "#e34948", "#f0efec"                  # diverging pair + neutral

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9,
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
    "text.color": INK, "axes.labelcolor": INK2, "axes.edgecolor": GRID,
    "xtick.color": INK2, "ytick.color": INK2,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.7,
    "savefig.facecolor": SURFACE, "savefig.bbox": "tight", "savefig.dpi": 200,
})

SCN = ["conservative", "mid", "optimistic"]
SCN_LBL = ["Conservative\n(well-maintained plant)", "Mid\n(typical condition)",
           "Optimistic\n(degraded plant)"]
SHORT = {"C. Status quo": "C.\nStatus quo",
         "A. Replace (heat-sized)": "A. Replace\n(heat-sized)",
         "A2. Replace (power-sized)": "A2. Replace\n(power-sized)",
         "B. Retire & electrify": "B. Retire &\nelectrify",
         "D. Operational only": "D. Operational\nonly"}
OPTS = [("C. Status quo", option_C_status_quo),
        ("A. Replace (heat-sized)", option_A_replace),
        ("A2. Replace (power-sized)", option_A2_replace_el_sized),
        ("B. Retire & electrify", option_B_electrify),
        ("D. Operational only", option_D_operational)]


def compute():
    out = {}
    for sn in SCN:
        s = SCENARIOS[sn]
        E = GAS_IN_MWH * s["eta_el"]
        H = GAS_IN_MWH * s["eta_th"]
        out[sn] = {}
        for name, fn in OPTS:
            r = fn(s, A, E, H)
            r["_total_per_t"] = sum(r[k] for k in COST_KEYS) / TONNES_PRODUCT
            r["_per_t"] = {k: r[k] / TONNES_PRODUCT for k in COST_KEYS}
            r["_sys"] = (r["emissions_tCO2"]
                         + r.get("grid_import_MWh", 0.0) * s["grid_ef_t_per_mwh"]
                         - r.get("grid_export_MWh", 0.0) * s["grid_ef_t_per_mwh"])
            out[sn][name] = r
    return out


D = compute()
eur = FuncFormatter(lambda v, p: f"{v:,.0f}")


# ---------------------------------------------------------------- Figure 1
def fig1():
    comps = [("fuel", "Fuel (natural gas)"), ("carbon", "Carbon (EUA on the short position)"),
             ("om", "O&M"), ("forgone_subsidy", "Forgone Industriestrompreis subsidy")]
    fig, ax = plt.subplots(figsize=(7.2, 4.1))
    x = np.arange(3)
    bottom = np.zeros(3)
    for i, (key, lbl) in enumerate(comps):
        vals = np.array([D[sn]["C. Status quo"]["_per_t"][key] for sn in SCN])
        ax.bar(x, vals, 0.52, bottom=bottom, label=lbl, color=CAT[i],
               edgecolor=SURFACE, linewidth=1.6, zorder=3)
        for xi, (v, b) in enumerate(zip(vals, bottom)):
            if v > 5:
                ax.text(xi, b + v / 2, f"{v:,.0f}", ha="center", va="center",
                        color="white", fontsize=8.5, fontweight="bold", zorder=4)
        bottom += vals
    for xi, tot in enumerate(bottom):
        ax.text(xi, tot + 2.5, f"{tot:,.0f}", ha="center", va="bottom",
                color=INK, fontsize=10, fontweight="bold", zorder=4)
    ax.set_xticks(x); ax.set_xticklabels(SCN_LBL, fontsize=8.5)
    ax.set_ylabel("€ per tonne of product")
    ax.set_title("Cost of running the existing fleet, by scenario",
                 loc="left", fontsize=11, fontweight="bold", pad=10)
    ax.yaxis.set_major_formatter(eur)
    ax.set_axisbelow(True); ax.xaxis.grid(False)
    ax.set_ylim(0, bottom.max() * 1.16)
    ax.legend(frameon=False, fontsize=8.2, loc="upper left",
              bbox_to_anchor=(0, -0.20), ncol=2)
    fig.savefig("fig1_current_case.png"); plt.close(fig)


# ---------------------------------------------------------------- Figure 2
def fig2():
    names = [n for n, _ in OPTS]
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    x = np.arange(len(names)); w = 0.26
    for j, sn in enumerate(SCN):
        vals = [D[sn][n]["_total_per_t"] for n in names]
        off = (j - 1) * w
        ax.bar(x + off, vals, w * 0.92, color=SEQ[j], edgecolor=SURFACE,
               linewidth=1.2, label=SCN[j].capitalize(), zorder=3)
        for xi, v in zip(x + off, vals):
            ax.text(xi, v + 3, f"{v:,.0f}", ha="center", va="bottom",
                    fontsize=7.4, color=INK2, rotation=90, zorder=4)
    ax.set_xticks(x)
    ax.set_xticklabels([SHORT[n] for n in names], fontsize=8.0)
    ax.set_ylabel("€ per tonne of product")
    ax.set_title("Total cost to deliver the same energy service",
                 loc="left", fontsize=11, fontweight="bold", pad=10)
    ax.yaxis.set_major_formatter(eur)
    ax.set_axisbelow(True); ax.xaxis.grid(False)
    ax.set_ylim(0, 282)
    ax.legend(frameon=False, fontsize=8.5, title="Scenario",
              title_fontsize=8.5, loc="upper left")
    fig.savefig("fig2_options.png"); plt.close(fig)


# ---------------------------------------------------------------- Figure 3
def fig3():
    names = [n for n, _ in OPTS if n != "C. Status quo"]
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    x = np.arange(len(names)); w = 0.26
    for j, sn in enumerate(SCN):
        sq = D[sn]["C. Status quo"]["_total_per_t"]
        vals = [sq - D[sn][n]["_total_per_t"] for n in names]
        off = (j - 1) * w
        cols = [POS if v >= 0 else NEG for v in vals]
        alpha = [0.45, 0.72, 1.0][j]
        ax.bar(x + off, vals, w * 0.92, color=cols, alpha=alpha,
               edgecolor=SURFACE, linewidth=1.2, zorder=3)
        for xi, v in zip(x + off, vals):
            ax.text(xi, v + (2.5 if v >= 0 else -2.5), f"{v:+,.1f}",
                    ha="center", va="bottom" if v >= 0 else "top",
                    fontsize=7.6, color=INK2, zorder=4)
    ax.axhline(0, color=INK, linewidth=1.3, zorder=4)
    ax.set_xticks(x)
    ax.set_xticklabels([SHORT[n] for n in names], fontsize=8.2)
    ax.set_ylabel("€ per tonne of product saved vs status quo")
    ax.set_title("Saving against the status quo — the replacement case crosses zero",
                 loc="left", fontsize=11, fontweight="bold", pad=10)
    ax.yaxis.set_major_formatter(eur)
    ax.set_axisbelow(True); ax.xaxis.grid(False)
    ax.set_ylim(-120, 42)
    h = [plt.Rectangle((0, 0), 1, 1, fc=POS, alpha=a) for a in (0.45, 0.72, 1.0)]
    l1 = ax.legend(h, ["Conservative", "Mid", "Optimistic"], frameon=False,
                   fontsize=8.2, title="Scenario (left to right, light to dark)",
                   title_fontsize=8.2, loc="upper left",
                   bbox_to_anchor=(0, -0.13), ncol=3)
    ax.add_artist(l1)
    ax.legend([plt.Rectangle((0, 0), 1, 1, fc=POS),
               plt.Rectangle((0, 0), 1, 1, fc=NEG)],
              ["Cheaper than status quo", "More expensive"], frameon=False,
              fontsize=8.2, loc="upper left", bbox_to_anchor=(0.55, -0.13))
    fig.savefig("fig3_saving.png"); plt.close(fig)


# ---------------------------------------------------------------- Figure 4
def fig4():
    base_s = SCENARIOS["mid"]
    E0 = GAS_IN_MWH * base_s["eta_el"]; H0 = GAS_IN_MWH * base_s["eta_th"]
    base = (sum(option_C_status_quo(base_s, A, E0, H0)[k] for k in COST_KEYS)
            - sum(option_A_replace(base_s, A, E0, H0)[k] for k in COST_KEYS)) / TONNES_PRODUCT
    params = [("Total efficiency (degradation)", "eta_tot", 0.70, 0.86, "0.70 / 0.86"),
              ("Discount rate", "discount", 0.05, 0.12, "5% / 12%"),
              ("Gas price", "p_gas", 25.0, 45.0, "€25 / €45 per MWh"),
              ("EUA price", "p_eua", 55.0, 126.0, "€55 / €126 per t CO₂"),
              ("Grid charge adder", "grid_adder", 10.0, 50.0, "€10 / €50 per MWh"),
              ("Electrical share of output", "el_share", 0.30, 0.40, "0.30 / 0.40")]
    rows = []
    for lbl, key, lo, hi, note in params:
        vv = []
        for val in (lo, hi):
            s2 = dict(base_s)
            if key == "eta_tot":
                s2["eta_tot"] = val
                s2["eta_el"] = EL_SHARE * val; s2["eta_th"] = (1 - EL_SHARE) * val
            elif key == "el_share":
                s2["eta_el"] = val * s2["eta_tot"]; s2["eta_th"] = (1 - val) * s2["eta_tot"]
            else:
                s2[key] = val
            E2 = GAS_IN_MWH * s2["eta_el"]; H2 = GAS_IN_MWH * s2["eta_th"]
            c = sum(option_C_status_quo(s2, A, E2, H2)[k] for k in COST_KEYS)
            a_ = sum(option_A_replace(s2, A, E2, H2)[k] for k in COST_KEYS)
            vv.append((c - a_) / TONNES_PRODUCT)
        rows.append((lbl, note, vv[0], vv[1], abs(vv[1] - vv[0])))
    rows.sort(key=lambda r: r[4])

    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    y = np.arange(len(rows))
    for i, (lbl, note, lo_v, hi_v, sw) in enumerate(rows):
        ax.barh(i, lo_v - base, left=base, height=0.5, color=POS, alpha=0.85,
                edgecolor=SURFACE, linewidth=1.2, zorder=3)
        ax.barh(i, hi_v - base, left=base, height=0.5, color=NEG, alpha=0.85,
                edgecolor=SURFACE, linewidth=1.2, zorder=3)
        ax.text(max(lo_v, hi_v, base) + 0.7, i, f"swing {sw:,.1f}", va="center",
                fontsize=7.8, color=INK2, zorder=4)
    ax.axvline(base, color=INK, linewidth=1.3, zorder=4)
    ax.text(base + 0.35, len(rows) - 0.38, f"base case {base:+,.1f}", fontsize=7.8,
            color=INK, fontweight="bold", ha="left", va="center", zorder=5)
    ax.axvline(0, color=INK2, linewidth=0.9, linestyle=(0, (4, 3)), zorder=2)
    ax.text(-0.35, len(rows) - 0.38, "break-even", fontsize=7.8, color=INK2,
            ha="right", va="center", zorder=5)
    ax.set_yticks(y); ax.set_yticklabels([f"{r[0]}\n{r[1]}" for r in rows], fontsize=8.2)
    ax.set_xlabel("Saving of option A vs status quo, € per tonne of product")
    ax.set_title("What actually moves the answer (mid scenario)",
                 loc="left", fontsize=11, fontweight="bold", pad=10)
    ax.set_axisbelow(True); ax.yaxis.grid(False)
    ax.set_xlim(-6.0, 27.0)
    ax.set_ylim(-0.7, len(rows) - 0.15)
    ax.legend([plt.Rectangle((0, 0), 1, 1, fc=POS, alpha=.85),
               plt.Rectangle((0, 0), 1, 1, fc=NEG, alpha=.85)],
              ["saving at the parameter's LOW value",
               "saving at the parameter's HIGH value"], frameon=False,
              fontsize=8.2, loc="upper left", bbox_to_anchor=(0, -0.28), ncol=2)
    fig.savefig("fig4_tornado.png"); plt.close(fig)


# ---------------------------------------------------------------- Figure 5
def fig5():
    names = [n for n, _ in OPTS]
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    x = np.arange(len(names)); w = 0.34
    site = [D["mid"][n]["emissions_tCO2"] / 1000.0 for n in names]
    syst = [D["mid"][n]["_sys"] / 1000.0 for n in names]
    ax.bar(x - w / 2, site, w * 0.94, color=CAT[1], edgecolor=SURFACE,
           linewidth=1.2, label="Site Scope 1", zorder=3)
    ax.bar(x + w / 2, syst, w * 0.94, color=CAT[0], edgecolor=SURFACE,
           linewidth=1.2, label="System-wide (incl. grid imports/exports)", zorder=3)
    for xi, v in zip(x - w / 2, site):
        ax.text(xi, v + 4, f"{v:,.0f}", ha="center", va="bottom", fontsize=7.6, color=INK2)
    for xi, v in zip(x + w / 2, syst):
        ax.text(xi, v + 4, f"{v:,.0f}", ha="center", va="bottom", fontsize=7.6, color=INK2)
    sq = D["mid"]["C. Status quo"]["emissions_tCO2"] / 1000.0
    ax.axhline(sq, color=INK2, linewidth=1.1, linestyle=(0, (5, 4)), zorder=2)
    ax.text(x[3], sq + 8, f"status quo, {sq:,.0f} kt", fontsize=7.8,
            color=INK2, ha="center", va="bottom")
    ax.set_xticks(x)
    ax.set_xticklabels([SHORT[n] for n in names], fontsize=8.0)
    ax.set_ylabel("kt CO₂ per year")
    ax.set_title("The cost-optimal replacement raises site Scope 1 while lowering system emissions",
                 loc="left", fontsize=10.5, fontweight="bold", pad=10)
    ax.set_axisbelow(True); ax.xaxis.grid(False)
    ax.set_ylim(0, 348)
    ax.legend(frameon=False, fontsize=8.4, loc="upper right")
    fig.savefig("fig5_emissions.png"); plt.close(fig)


for f in (fig1, fig2, fig3, fig4, fig5):
    f(); print("ok", f.__name__)

# numbers the document quotes, printed so they can be checked against the text
print("\n--- values used in the text ---")
for sn in SCN:
    sq = D[sn]["C. Status quo"]["_total_per_t"]
    print(f"{sn:13s} status quo {sq:7.2f}  " +
          "  ".join(f"{n.split('.')[0]}:{D[sn][n]['_total_per_t']:7.2f}"
                    f"({sq - D[sn][n]['_total_per_t']:+6.2f})"
                    for n, _ in OPTS if n != "C. Status quo"))
