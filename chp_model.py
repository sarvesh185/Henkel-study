"""
Henkel Duesseldorf-Holthausen: CHP reinvestment case.

Everything is expressed per tonne of HENKEL DUESSELDORF PRODUCT (EUR/t product),
never per tonne of CO2. Carbon prices are always labelled EUR/t CO2.

METHOD
------
The only hard consumption anchor in the public record is the site power plant's
verified ETS emissions. Gas input is back-calculated from it:

    gas_in = verified_CO2 / EF_gas          [E-01, D-01, D-02]

Gas input is therefore FIXED. What is uncertain is the plant's TOTAL efficiency
- how much of that fixed gas still emerges as useful electricity plus useful
heat after six decades of fouling, worn blading, seal leakage and stack losses.
Ageing reduces the total, not the split between power and heat, so the total is
the scenario axis and the electrical share is held at EL_SHARE throughout. The
axis is deliberately correlated with optimism about the prize:

    conservative : eta_tot 0.86  -> well-maintained plant  -> less to gain
    mid          : eta_tot 0.80  -> typical condition
    optimistic   : eta_tot 0.74  -> degraded plant         -> more to gain

paired with conservative / central / bullish carbon and power prices. This
brackets the answer instead of pretending to a point estimate.

The energy SERVICE (E GWh_el + H GWh_th per year) is held constant across all
options. Each option is costed on what it takes to deliver that same service.
This sidesteps the site's total electricity demand, which is not public.

Run:  python3 chp_model.py
Out:  console tables + chp_reinvestment_model.xlsx
"""

import numpy as np
import pandas as pd

pd.set_option("display.width", 220)

# ----------------------------------------------------------------------------
# 1. ANCHORS - public, primary-source, not assumptions
# ----------------------------------------------------------------------------
CO2_VERIFIED_2024 = 229_042      # t CO2, DEHSt installation 14310-0641      [E-01]
FREE_ALLOC_2024   = 63_398       # t CO2, same source                        [E-07]
EF_GAS            = 0.2016       # t CO2 / MWh gas, NCV, natural gas         [D-01]
TONNES_PRODUCT    = 400_000      # t/yr Henkel Duesseldorf - SINGLE SOURCE   [S-10]
MW_EL_LIVE        = 61.7         # MW net, 5 live units, MaStR               [G-10]

GAS_IN_MWH = CO2_VERIFIED_2024 / EF_GAS          # 1,136,121 MWh_gas         [D-02]

# ----------------------------------------------------------------------------
# 2. SCENARIOS - efficiency correlated with optimism, as described above
# ----------------------------------------------------------------------------
# The uncertain quantity is the plant's OVERALL efficiency, which is what ageing
# degrades: fouled heat exchangers, worn blade tips, seal and valve leakage and
# drifting combustion control all send energy up the stack rather than into
# either useful output. For a back-pressure steam CHP the electrical share of
# that total is comparatively stable, so it is held fixed and the total is varied.
EL_SHARE = 0.35          # electrical output as a share of total useful output

SCENARIOS = {
    "conservative": dict(
        label="Well-maintained plant / low optimism",
        eta_tot=0.86,                    # little degradation -> little to gain
        p_gas=30.0,                      # EUR/MWh gas
        p_eua=65.0,                      # EUR/t CO2
        p_power_wholesale=85.0,          # EUR/MWh
        grid_adder=45.0,                 # EUR/MWh on imported power
        cop_hp=2.5,
        discount=0.09,
        grid_ef_t_per_mwh=0.35,
        capex_factor=1.25,
    ),
    "mid": dict(
        label="Typical condition",
        eta_tot=0.80,
        p_gas=33.0,
        p_eua=82.5,
        p_power_wholesale=105.8,         # 2026 YTD computed mean            [P-01]
        grid_adder=30.0,
        cop_hp=3.0,
        discount=0.07,
        grid_ef_t_per_mwh=0.30,
        capex_factor=1.00,
    ),
    "optimistic": dict(
        label="Degraded plant / high optimism",
        eta_tot=0.74,                    # heavy degradation -> most to gain
        p_gas=36.0,
        p_eua=110.0,
        p_power_wholesale=120.0,
        grid_adder=20.0,
        cop_hp=3.5,
        discount=0.06,
        grid_ef_t_per_mwh=0.22,
        capex_factor=0.85,
    ),
}
# derive the split from the total for every scenario
for _s in SCENARIOS.values():
    _s["eta_el"] = EL_SHARE * _s["eta_tot"]
    _s["eta_th"] = (1.0 - EL_SHARE) * _s["eta_tot"]

# ----------------------------------------------------------------------------
# 3. TECHNOLOGY AND POLICY ASSUMPTIONS - every one is an input, not a finding
# ----------------------------------------------------------------------------
A = dict(
    # modern gas CHP
    eta_el_new=0.45, eta_th_new=0.42,
    capex_chp_eur_per_mw_el=1_100_000.0,
    life_chp=20,
    om_fix_old_eur_per_mw_yr=38_000.0,     # 1965-83 fleet, high maintenance
    om_fix_new_eur_per_mw_yr=22_000.0,
    om_var_old_eur_per_mwh_el=4.5,
    om_var_new_eur_per_mwh_el=2.5,

    # electrification
    eta_eboiler=0.99,
    capex_hp_eur_per_mw_th=900_000.0,
    capex_eb_eur_per_mw_th=320_000.0,
    capex_storage_eur_per_mwh_th=45_000.0,
    storage_hours=8.0,
    capex_grid_eur_per_mw=180_000.0,       # connection reinforcement
    life_electrify=20,
    om_fix_hp_eur_per_mw_th=18_000.0,
    om_fix_eb_eur_per_mw_th=6_000.0,
    hp_share_of_heat=0.85,                 # heat pump covers base heat
    eboiler_share_of_heat=0.15,            # e-boiler is a true peaker

    # gas boiler fallback (used to value heat in option D)
    eta_boiler=0.92,

    # surplus electricity is EXPORTED, so it earns wholesale less fees - NOT the
    # delivered import price. Getting this wrong flatters any option that
    # over-produces electricity.
    export_fee_eur_per_mwh=8.0,

    # heat-side utilisation, set directly rather than borrowed from the
    # electrical full-load hours
    flh_heat_base=5_500.0,      # heat pump, base load
    flh_heat_peak=1_200.0,      # e-boiler, peaker

    # Industriestrompreis: 0.5 x eligible consumption x 37.44 EUR/MWh     [R-16]
    isp_diff_price=37.44,
    isp_share=0.50,
    isp_active=True,

    # free allocation treatment per option
    alloc_status_quo=FREE_ALLOC_2024,
    alloc_new_chp=FREE_ALLOC_2024,         # modern unit passes hi-eff test securely
    alloc_electrified=0.0,                 # heat from electricity: likely none [R-22]

    # operational-only case
    dispatch_capture=0.25,                 # realistic share of the theoretical envelope
    dispatch_hours_out_of_money=1432.0,    # 2026 YTD, computed                [D-11]
)


def annuity(capex, life, rate):
    """Level annual payment for a capex over `life` years at `rate`."""
    if rate == 0:
        return capex / life
    return capex * rate / (1.0 - (1.0 + rate) ** (-life))


def isp_credit(s, a):
    """EUR/MWh earned on electricity taken FROM THE GRID. Self-generation earns
    nothing, which is the structural bias in the subsidy."""
    return a["isp_share"] * a["isp_diff_price"] if a["isp_active"] else 0.0


# ----------------------------------------------------------------------------
# 4. THE FOUR OPTIONS
# ----------------------------------------------------------------------------
def option_C_status_quo(s, a, E, H):
    """Run the 1965-83 fleet as-is."""
    gas = GAS_IN_MWH
    emis = gas * EF_GAS
    short = max(0.0, emis - a["alloc_status_quo"])
    fuel = gas * s["p_gas"]
    carbon = short * s["p_eua"]
    om = a["om_fix_old_eur_per_mw_yr"] * MW_EL_LIVE + a["om_var_old_eur_per_mwh_el"] * E
    # opportunity cost: every self-generated MWh forgoes the subsidy it would
    # have earned as an import
    forgone = E * isp_credit(s, a)
    return dict(option="C. Status quo", fuel=fuel, carbon=carbon, om=om,
                power_purchase=0.0, forgone_subsidy=forgone, capex_annuity=0.0,
                gas_MWh=gas, emissions_tCO2=emis, grid_import_MWh=0.0)


def option_A_replace(s, a, E, H):
    """Replace with a modern gas CHP, sized on HEAT (steam is the binding
    industrial requirement). Electricity then falls out of the heat sizing and
    any shortfall is imported."""
    gas = H / a["eta_th_new"]
    E_new = gas * a["eta_el_new"]
    emis = gas * EF_GAS
    short = max(0.0, emis - a["alloc_new_chp"])
    fuel = gas * s["p_gas"]
    carbon = short * s["p_eua"]

    flh = E / MW_EL_LIVE                      # keep the same utilisation
    mw_new = E_new / flh
    om = a["om_fix_new_eur_per_mw_yr"] * mw_new + a["om_var_new_eur_per_mwh_el"] * E_new

    # An electricity SHORTFALL is imported at the delivered price net of subsidy.
    # A SURPLUS is exported and earns wholesale less fees - not the import price.
    gap = E - E_new
    net_import_price = s["p_power_wholesale"] + s["grid_adder"] - isp_credit(s, a)
    export_price = s["p_power_wholesale"] - a["export_fee_eur_per_mwh"]
    if gap > 0:
        power_purchase = gap * net_import_price
    else:
        power_purchase = gap * export_price       # negative = revenue

    cap = annuity(mw_new * a["capex_chp_eur_per_mw_el"] * s["capex_factor"],
                  a["life_chp"], s["discount"])
    forgone = min(E_new, E) * isp_credit(s, a)
    return dict(option="A. Replace like-for-like", fuel=fuel, carbon=carbon, om=om,
                power_purchase=power_purchase, forgone_subsidy=forgone,
                capex_annuity=cap, gas_MWh=gas, emissions_tCO2=emis,
                new_MW_el=mw_new, E_new_GWh=E_new / 1000.0,
                grid_import_MWh=max(0.0, gap), grid_export_MWh=max(0.0, -gap))


def option_A2_replace_el_sized(s, a, E, H):
    """Replace with a modern gas CHP sized on ELECTRICITY (deliver the same E),
    and make up the heat shortfall in a gas boiler. No surplus power to export,
    which removes the export-price question entirely."""
    gas_chp = E / a["eta_el_new"]
    H_chp = gas_chp * a["eta_th_new"]
    H_short = max(0.0, H - H_chp)
    gas_boiler = H_short / a["eta_boiler"]
    gas = gas_chp + gas_boiler

    emis = gas * EF_GAS
    short = max(0.0, emis - a["alloc_new_chp"])
    fuel = gas * s["p_gas"]
    carbon = short * s["p_eua"]

    flh = E / MW_EL_LIVE
    mw_new = E / flh
    om = a["om_fix_new_eur_per_mw_yr"] * mw_new + a["om_var_new_eur_per_mwh_el"] * E
    cap = annuity(mw_new * a["capex_chp_eur_per_mw_el"] * s["capex_factor"],
                  a["life_chp"], s["discount"])
    forgone = E * isp_credit(s, a)
    return dict(option="A2. Replace, sized on power", fuel=fuel, carbon=carbon, om=om,
                power_purchase=0.0, forgone_subsidy=forgone, capex_annuity=cap,
                gas_MWh=gas, emissions_tCO2=emis, new_MW_el=mw_new,
                boiler_gas_GWh=gas_boiler / 1000.0, grid_import_MWh=0.0)


def option_B_electrify(s, a, E, H):
    """Retire the fleet. Heat from a heat pump plus an e-boiler, with storage.
    All electricity - the lost self-generation AND the electrified heat - is
    bought from the grid, and therefore earns the subsidy."""
    H_hp = H * a["hp_share_of_heat"]
    H_eb = H * a["eboiler_share_of_heat"]
    el_hp = H_hp / s["cop_hp"]
    el_eb = H_eb / a["eta_eboiler"]
    el_total = E + el_hp + el_eb               # E is the self-generation we lose

    net_import_price = s["p_power_wholesale"] + s["grid_adder"] - isp_credit(s, a)
    power_purchase = el_total * net_import_price

    emis = 0.0
    carbon = 0.0 - a["alloc_electrified"] * s["p_eua"]   # no emissions, no allocation

    mw_hp = H_hp / a["flh_heat_base"]
    mw_eb = H_eb / a["flh_heat_peak"]
    mwh_store = mw_hp * a["storage_hours"]
    # grid connection must carry the electrified heat AND the power we no longer
    # self-generate, at the electrical peak
    mw_grid = (el_hp + el_eb) / a["flh_heat_base"] + MW_EL_LIVE

    capex = (mw_hp * a["capex_hp_eur_per_mw_th"]
             + mw_eb * a["capex_eb_eur_per_mw_th"]
             + mwh_store * a["capex_storage_eur_per_mwh_th"]
             + mw_grid * a["capex_grid_eur_per_mw"]) * s["capex_factor"]
    cap = annuity(capex, a["life_electrify"], s["discount"])
    om = a["om_fix_hp_eur_per_mw_th"] * mw_hp + a["om_fix_eb_eur_per_mw_th"] * mw_eb

    return dict(option="B. Retire & electrify", fuel=0.0, carbon=carbon, om=om,
                power_purchase=power_purchase, forgone_subsidy=0.0,
                capex_annuity=cap, gas_MWh=0.0, emissions_tCO2=emis,
                hp_MW_th=mw_hp, eb_MW_th=mw_eb, store_MWh_th=mwh_store,
                grid_MW=mw_grid, capex_total=capex, grid_import_MWh=el_total)


def option_D_operational(s, a, E, H):
    """Same fleet, better dispatch. In the hours the CHP is out of the money,
    import electricity and make the heat in a gas boiler instead. A capture
    factor haircuts the theoretical envelope to something a real plant with
    steam obligations and ramp limits could actually take."""
    base = option_C_status_quo(s, a, E, H)

    frac = (a["dispatch_hours_out_of_money"] / 8760.0) * a["dispatch_capture"]
    E_disp = E * frac                                  # MWh_el displaced
    gas_saved = E_disp / s["eta_el"]                   # gas no longer burned
    H_lost = gas_saved * s["eta_th"]                   # co-produced heat lost
    gas_boiler = H_lost / a["eta_boiler"]              # made up in a boiler

    gas_net_saved = gas_saved - gas_boiler
    fuel = base["fuel"] - gas_net_saved * s["p_gas"]
    emis = (GAS_IN_MWH - gas_net_saved) * EF_GAS
    short = max(0.0, emis - a["alloc_status_quo"])
    carbon = short * s["p_eua"]

    net_import_price = s["p_power_wholesale"] + s["grid_adder"] - isp_credit(s, a)
    power_purchase = E_disp * net_import_price
    om = a["om_fix_old_eur_per_mw_yr"] * MW_EL_LIVE + a["om_var_old_eur_per_mwh_el"] * (E - E_disp)
    forgone = (E - E_disp) * isp_credit(s, a)

    return dict(option="D. Operational only", fuel=fuel, carbon=carbon, om=om,
                power_purchase=power_purchase, forgone_subsidy=forgone,
                capex_annuity=0.0, gas_MWh=GAS_IN_MWH - gas_net_saved,
                emissions_tCO2=emis, displaced_GWh=E_disp / 1000.0,
                grid_import_MWh=E_disp)


COST_KEYS = ["fuel", "carbon", "om", "power_purchase", "forgone_subsidy", "capex_annuity"]


def run():
    rows, detail, service = [], [], []

    for name, s in SCENARIOS.items():
        E = GAS_IN_MWH * s["eta_el"]      # MWh_el delivered by the fixed gas input
        H = GAS_IN_MWH * s["eta_th"]      # MWh_th delivered
        service.append(dict(scenario=name, label=s["label"],
                            eta_tot=s["eta_tot"],
                            eta_el=s["eta_el"], eta_th=s["eta_th"],
                            E_GWh_el=E / 1000.0, H_GWh_th=H / 1000.0,
                            implied_flh=E / MW_EL_LIVE,
                            p_gas=s["p_gas"], p_eua=s["p_eua"],
                            p_power_delivered=s["p_power_wholesale"] + s["grid_adder"]))

        for fn in (option_C_status_quo, option_A_replace, option_A2_replace_el_sized,
                   option_B_electrify, option_D_operational):
            r = fn(s, A, E, H)
            total = sum(r[k] for k in COST_KEYS)
            rows.append(dict(scenario=name, option=r["option"],
                             **{k: r[k] / 1e6 for k in COST_KEYS},
                             total_mEUR=total / 1e6,
                             EUR_per_t_product=total / TONNES_PRODUCT,
                             emissions_tCO2=r["emissions_tCO2"],
                             system_tCO2=r["emissions_tCO2"]
                                 + r.get("grid_import_MWh", 0.0) * s["grid_ef_t_per_mwh"]
                                 - r.get("grid_export_MWh", 0.0) * s["grid_ef_t_per_mwh"]))
            detail.append(dict(scenario=name, **{k: v for k, v in r.items()
                                                 if k not in COST_KEYS}))

    svc = pd.DataFrame(service).set_index("scenario")
    res = pd.DataFrame(rows)

    print("=" * 96)
    print("STEP 1 - BASELINE: what the fixed gas input actually delivers")
    print("=" * 96)
    print(f"Gas input, fixed by verified ETS emissions: {GAS_IN_MWH:,.0f} MWh "
          f"({GAS_IN_MWH/1e6:.2f} TWh)\n")
    print(svc[["label", "eta_tot", "eta_el", "eta_th", "E_GWh_el", "H_GWh_th",
               "implied_flh", "p_gas", "p_eua", "p_power_delivered"]]
          .to_string(float_format=lambda x: f"{x:,.2f}"))

    print("\n" + "=" * 96)
    print("STEP 2 - COST TO DELIVER THAT SAME SERVICE, EUR per tonne of product")
    print("=" * 96)
    piv = res.pivot(index="option", columns="scenario", values="EUR_per_t_product")
    piv = piv[["conservative", "mid", "optimistic"]].sort_index()
    print(piv.to_string(float_format=lambda x: f"{x:,.2f}"))

    print("\n--- saving vs status quo, EUR/t product (positive = cheaper) ---")
    sq = piv.loc["C. Status quo"]
    print((sq - piv).drop(index="C. Status quo").to_string(float_format=lambda x: f"{x:+,.2f}"))

    print("\n" + "=" * 96)
    print("STEP 3 - COST BREAKDOWN, mid scenario, m EUR/yr")
    print("=" * 96)
    mid = res[res.scenario == "mid"].set_index("option")[COST_KEYS + ["total_mEUR"]]
    print(mid.loc[["C. Status quo", "A. Replace like-for-like",
                   "B. Retire & electrify", "D. Operational only"]]
          .to_string(float_format=lambda x: f"{x:,.2f}"))

    print("\n" + "=" * 96)
    print("STEP 4 - SCOPE 1 EMISSIONS, t CO2/yr")
    print("=" * 96)
    em = res.pivot(index="option", columns="scenario", values="emissions_tCO2")
    print("site Scope 1:")
    print(em[["conservative", "mid", "optimistic"]].sort_index()
          .to_string(float_format=lambda x: f"{x:,.0f}"))
    sysem = res.pivot(index="option", columns="scenario", values="system_tCO2")
    print("\nsystem-wide (site Scope 1 + grid imports - grid exports, at the scenario grid factor):")
    print(sysem[["conservative", "mid", "optimistic"]].sort_index()
          .to_string(float_format=lambda x: f"{x:,.0f}"))

    # ---- sensitivity: one-at-a-time on the mid scenario ------------------
    print("\n" + "=" * 96)
    print("STEP 5 - SENSITIVITY on the mid scenario: EUR/t product for A minus C")
    print("=" * 96)
    sens = []
    base_s = SCENARIOS["mid"]
    SENS = [("eta_tot", 0.70, 0.86), ("discount", 0.05, 0.12),
            ("p_gas", 25.0, 45.0), ("p_eua", 55.0, 126.0),
            ("grid_adder", 10.0, 50.0), ("el_share", 0.30, 0.40)]
    for param, lo, hi in SENS:
        out = {}
        for tag, val in (("low", lo), ("high", hi)):
            s2 = dict(base_s)
            if param == "eta_tot":
                s2["eta_tot"] = val
                s2["eta_el"] = EL_SHARE * val
                s2["eta_th"] = (1.0 - EL_SHARE) * val
            elif param == "el_share":
                s2["eta_el"] = val * s2["eta_tot"]
                s2["eta_th"] = (1.0 - val) * s2["eta_tot"]
            else:
                s2[param] = val
            E2 = GAS_IN_MWH * s2["eta_el"]; H2 = GAS_IN_MWH * s2["eta_th"]
            c = sum(option_C_status_quo(s2, A, E2, H2)[k] for k in COST_KEYS)
            a_ = sum(option_A_replace(s2, A, E2, H2)[k] for k in COST_KEYS)
            out[tag] = (c - a_) / TONNES_PRODUCT
        sens.append(dict(parameter=param, low_value=lo, high_value=hi,
                         saving_at_low=out["low"], saving_at_high=out["high"],
                         swing=abs(out["high"] - out["low"])))
    sdf = pd.DataFrame(sens).sort_values("swing", ascending=False)
    print(sdf.to_string(index=False, float_format=lambda x: f"{x:,.2f}"))
    print("\n-> the parameter with the widest swing is what the site visit must settle first.")

    # ---- sizing detail ---------------------------------------------------
    d = pd.DataFrame(detail)
    print("\n" + "=" * 96)
    print("STEP 6 - PLANT SIZING implied by each option (mid scenario)")
    print("=" * 96)
    dm = d[d.scenario == "mid"].set_index("option")
    cols = [c for c in ["new_MW_el", "E_new_GWh", "hp_MW_th", "eb_MW_th",
                        "store_MWh_th", "grid_MW", "capex_total", "displaced_GWh"]
            if c in dm.columns]
    print(dm[cols].to_string(float_format=lambda x: f"{x:,.1f}", na_rep="—"))

    # ---- workbook --------------------------------------------------------
    assum = []
    for k, v in A.items():
        assum.append(dict(block="technology / policy", parameter=k, value=v))
    for nm, s in SCENARIOS.items():
        for k, v in s.items():
            assum.append(dict(block=f"scenario: {nm}", parameter=k, value=v))
    for k, v in [("CO2_VERIFIED_2024", CO2_VERIFIED_2024), ("FREE_ALLOC_2024", FREE_ALLOC_2024),
                 ("EF_GAS", EF_GAS), ("TONNES_PRODUCT", TONNES_PRODUCT),
                 ("MW_EL_LIVE", MW_EL_LIVE), ("GAS_IN_MWH", round(GAS_IN_MWH))]:
        assum.append(dict(block="anchor (primary source)", parameter=k, value=v))

    with pd.ExcelWriter("chp_reinvestment_model.xlsx", engine="openpyxl") as xw:
        svc.to_excel(xw, sheet_name="1 baseline service")
        piv.to_excel(xw, sheet_name="2 EUR per t product")
        (sq - piv).drop(index="C. Status quo").to_excel(xw, sheet_name="3 saving vs status quo")
        res.to_excel(xw, sheet_name="4 full results", index=False)
        em.to_excel(xw, sheet_name="5 emissions site")
        sysem.to_excel(xw, sheet_name="5b emissions system")
        sdf.to_excel(xw, sheet_name="6 sensitivity", index=False)
        dm[cols].to_excel(xw, sheet_name="7 sizing")
        pd.DataFrame(assum).to_excel(xw, sheet_name="8 assumptions", index=False)
    print("\nwrote chp_reinvestment_model.xlsx")


if __name__ == "__main__":
    run()
