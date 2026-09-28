# CHP reinvestment model — Henkel Düsseldorf-Holthausen

Supporting repository for a RIZM Field Value Engineer take-home. Sarvesh Patidar · September 2026

The question: **does replacing Henkel's 1965–1983 gas CHP fleet pay, measured in euros per tonne of product?**

This repository holds the model that answers it. The written study is submitted separately as `Use_case_CHP_reinvestment_Henkel.docx`; the section numbers referenced below point into it.

---

## Contents

```
README.md                          ← this file
DATA-REGISTER.md                   ← every input figure, its source and confidence rating
model/
├── chp_model.py                   ← the model. One file, ~450 lines, no solver
├── make_figures.py                ← the five figures in the write-up
└── chp_reinvestment_model.xlsx    ← results and assumptions, eight sheets
```

Run it:

```bash
pip install pandas numpy matplotlib openpyxl
cd model
python chp_model.py      # prints all result tables, writes the workbook
python make_figures.py   # writes fig1..fig5 PNG, prints the values quoted in the text
```

No network access, no API keys, no solver. A few seconds end to end.

---

## What the model is

A deterministic annuitised cost comparison. It costs four ways of delivering **the same energy service** and reports each in euros per tonne of product, across three scenarios. It is not an optimisation — see *Why not a solver* below.

### The anchoring move

No consumption data for this site is public. The only externally verified quantity is the power plant's ETS emissions, so gas input is obtained by inverting the emission factor:

```
gas input = 229,042 t CO₂ ÷ 0.2016 t CO₂/MWh = 1,136,121 MWh ≈ 1.14 TWh
```

Because emissions are verified by an accredited body, the gas figure inherits that verification. It is the firmest number in the study, and everything else is built on it.

**Gas input is therefore fixed.** What remains uncertain is the plant's *total* efficiency — how much of that fixed gas still emerges as useful electricity plus useful heat after six decades of fouling, worn blading, seal leakage and rising stack losses.

### Five steps

1. **Anchor** on verified emissions to fix gas input.
2. **Convert** that gas into an energy service using the scenario total efficiency and a fixed electrical share: `E` MWh of electricity and `H` MWh of heat per year.
3. **Hold that service constant** and cost four different ways of delivering it. This is the central choice — it makes the comparison fair and avoids needing the site's total electricity demand, which is not public.
4. **Annuitise** capital expenditure over an asset life at a scenario discount rate, so capex and opex add in the same units.
5. **Divide** by annual product tonnage.

Step 3 is what stops a modern high-efficiency unit looking cheap merely because it produces something different. Whatever an option over- or under-produces must be sold or bought at a real price, and that shows up as a cost line.

---

## The scenario axis

Ageing does not redistribute output between power and heat — it reduces the total. So **total efficiency is the scenario axis**, and the electrical share of useful output is held at `EL_SHARE = 0.35` throughout, which is characteristic of a back-pressure machine once steam conditions are set.

The axis is deliberately correlated with optimism about the prize: a well-maintained fleet leaves little to recover, a degraded one leaves a lot. Each efficiency case is paired with correspondingly soft or firm prices, so the answer comes out as a bracket rather than a false point estimate.

| Scenario | η_tot | η_el / η_th | E GWh | H GWh | Gas €/MWh | EUA €/t | Power delivered €/MWh | Discount |
|---|---|---|---|---|---|---|---|---|
| Conservative — well-maintained plant | 0.86 | 0.30 / 0.56 | 342 | 635 | 30.0 | 65.0 | 130.0 | 9 % |
| Mid — typical condition | 0.80 | 0.28 / 0.52 | 318 | 591 | 33.0 | 82.5 | 135.8 | 7 % |
| Optimistic — degraded plant | 0.74 | 0.26 / 0.48 | 294 | 546 | 36.0 | 110.0 | 140.0 | 6 % |

Note what "optimistic" means here: optimistic about the *case for replacing*, which is the degraded plant.

---

## The four options

Each must deliver the same `E` + `H`.

| | Function | How it delivers the service |
|---|---|---|
| **C. Status quo** | `option_C_status_quo` | The existing fleet, as-is. Fuel, carbon on the short position, O&M, and the forgone subsidy |
| **A. Replace, heat-sized** | `option_A_replace` | New CHP at η_el 0.45 / η_th 0.42, sized so its heat output equals `H`. Electricity falls out of that sizing and the surplus is exported |
| **A2. Replace, power-sized** | `option_A2_replace_el_sized` | New CHP sized so its electricity equals `E`; the heat shortfall is made up in a gas boiler. No export, so no export-price exposure |
| **B. Retire and electrify** | `option_B_electrify` | Heat pump on base heat, electric boiler on peak, thermal storage between them. All electricity bought from the grid — the electrified heat *and* the self-generation that is lost |
| **D. Operate better** | `option_D_operational` | Same fleet. In hours the plant is out of the money, import power and raise the heat in a boiler. No capital, fully reversible |

A and A2 are one option in two sizing conventions. Which is right turns on whether surplus power can actually be sold, which is a commercial question rather than an engineering one — and it is worth up to €13/t of product.

### Cost components

`COST_KEYS = ["fuel", "carbon", "om", "power_purchase", "forgone_subsidy", "capex_annuity"]`

| Component | Formula | Why this way |
|---|---|---|
| Fuel | gas × gas price | Fixed by emissions for C; derived from the heat or power requirement for the alternatives |
| Carbon | `max(0, emissions − free allocation)` × EUA price | Only the short position is a cash cost. Charging gross emissions would overstate every gas option by ~€5 m a year |
| O&M | fixed €/MW·a + variable €/MWh_el | Splitting the two lets plant age act on the fixed term, which is where a 1965 unit differs from a 2026 one |
| Power purchase | shortfall × (wholesale + grid adder − subsidy) | Imports are charged at the delivered price net of Industriestrompreis |
| Power export | surplus × (wholesale − export fee) | Exports earn wholesale less fees. They do **not** earn back grid charges that were never paid |
| Forgone subsidy | self-generated MWh × 0.5 × €37.44 | The Industriestrompreis pays only on grid offtake, so self-generation carries an opportunity cost |
| Capex annuity | `capex × r / (1 − (1+r)^−n)` | Level annual payment, so capital and operating costs add in the same units |

Every assumed input — efficiencies, capex rates, O&M rates, COP, asset lives, dispatch capture — sits in the `A` dictionary near the top of `chp_model.py` and is exported verbatim to sheet 8 of the workbook. None of it came from Henkel.

---

## What it outputs

`chp_model.py` prints six blocks to the console and writes the workbook:

| Sheet | Contents |
|---|---|
| 1 baseline service | Electricity and heat delivered by the fixed gas input, per scenario |
| 2 EUR per t product | Total cost of each option × scenario |
| 3 saving vs status quo | The headline table |
| 4 full results | Every cost component, un-aggregated |
| 5 emissions site / 5b system | CO₂ on both accounting boundaries |
| 6 sensitivity | One-at-a-time parameter swings, ordered |
| 7 sizing | Implied plant capacities and capex per option |
| 8 assumptions | Every input in the model, in one place |

### Headline result — saving against the status quo, €/t product

| Option | Conservative | Mid | Optimistic |
|---|---|---|---|
| A. Replace, heat-sized | −22.89 | **+10.28** | **+31.29** |
| A2. Replace, power-sized | −15.52 | +1.66 | +18.53 |
| B. Retire and electrify | −108.08 | −58.63 | −15.77 |
| D. Operate better | −1.11 | −0.55 | +0.27 |

The replacement case **crosses zero** between the conservative and mid scenarios. That range is the answer; collapsing it to a single number would be a worse one.

### What moves it — sensitivity on A vs C, mid scenario

| Parameter | Range | Swing €/t |
|---|---|---|
| Total efficiency (degradation) | 0.70 – 0.86 | **19.59** |
| Discount rate | 5 % – 12 % | 18.11 |
| Gas price | €25 – €45/MWh | 13.53 |
| EUA price | €55 – €126/t CO₂ | 9.68 |
| Electrical share of output | 0.30 – 0.40 | 0.22 |
| Grid charge adder | €10 – €50/MWh | 0.00 |

The grid adder shows zero **for this comparison only**: neither C nor a heat-sized A imports power, so the parameter never enters. It is the widest parameter in the study for option B, which swings about €57/t across the same range.

### The emissions result

Mid scenario, kt CO₂ a year:

| Option | Site Scope 1 | System-wide |
|---|---|---|
| C. Status quo | 229 | 229 |
| A. Replace, heat-sized | **284** | **189** |
| A2. Replace, power-sized | 207 | 207 |
| B. Retire and electrify | 0 | 173 |
| D. Operate better | 225 | 229 |

A modern CHP has higher electrical and *lower* thermal efficiency, so a heat-sized unit burns more gas than the 1965 fleet to raise the same steam — site Scope 1 rises 24 % — while its 315 GWh of exported surplus displaces grid power and system emissions fall 17 %. The cost-optimal option is the one that breaks Henkel's published 42 % Scope 1 and 2 reduction target. That contradiction is the most useful thing the model produces, and it came out of the arithmetic rather than being argued for.

---

## Why not a solver

PyPSA was the obvious instrument and was rejected for three reasons, in ascending order of importance:

1. **It needs inputs that do not exist here.** Network topology, nodal time series and per-asset constraints are not public for this site. Supplying them would mean inventing inputs and presenting them as data.
2. **There is nothing to optimise.** PyPSA solves capacity expansion and dispatch over a network. This decision is a comparison of four pre-specified discrete options — that is arithmetic.
3. **Arithmetic defensible line by line in a thirty-minute conversation beats an optimisation defensible only in outline.**

This is a boundary, not a dismissal. Once 15-minute metered data exists, co-optimising thermal storage against electric boiler capacity against procurement *is* a solver-class problem. Screening on public data calls for a transparent annuity model; sizing on real data calls for the optimiser.

---

## What the model cannot see

Stated here rather than discovered by a reader.

- **No time resolution.** It cannot see 15-minute spreads, negative-price hours or storage arbitrage. That is the honest limit of a public-data screening, and it is why the data request in §5 asks for what it asks for.
- **Every cost input is an assumption**, not a finding: capex €/MW, O&M rates, discount rate, COP, capex factors. All on sheet 8.
- **The O&M split between old and new plant is a judgement.** It favours replacement.
- **Option B loses its free allocation entirely**, because whether heat made *using* electricity earns heat-benchmark allocation is unresolved in the rules. If it does, B improves.
- **Option A assumes a modern unit passes the high-efficiency cogeneration test** and keeps its heat allocation. If the existing fleet already fails that test, C is worse than modelled and A improves.
- **The 400,000 t denominator is single-sourced.** Every €/t figure scales inversely with it, though no ranking or sign depends on it.
- **Dispatch capture in option D is set at 25 %** of the theoretical envelope — a stand-in for ramp limits, minimum loads and steam obligations that are not public.

---

## Two corrections made during development

Both are left visible because how they surfaced says something about the model's structure.

**Export pricing.** The first version valued surplus electricity from a replacement plant at the **delivered import** price, flattering that option by roughly €5 m a year, because it credited back grid charges an exporter never pays. Splitting import and export into separate lines in the cost stack is what made the error visible.

**The scenario axis.** An earlier version held total efficiency fixed at ~0.80 and varied only the electrical share between the three cases, which made "efficiency" look like the *least* important parameter tested — a paragraph had already been written explaining why. It was an artefact of testing the wrong variable. Testing the total instead gives the **widest** swing in the study, and the finding reversed. The write-up states the correction in §4.3 rather than quietly presenting the corrected version.

---

## Data and provenance

[`DATA-REGISTER.md`](./DATA-REGISTER.md) lists every figure used, with source and confidence rating: Primary (statutory register), Computed (derived here, reproducible from these scripts), Operator (the company's own published figure), Single source, or Assumption.

The DEHSt register was parsed from PDF, and the parsing is validated rather than eyeballed: the table publishes both period sums and period averages, so dividing each published sum by its period length must reproduce the published average. Six such checks run across all parsed rows and all six pass. This caught two real parsing errors — a row that split on a company name containing the word "Düsseldorf", and an off-by-one where a postcode was read as data.

Primary sources:

- **DEHSt** — *Emissionshandelspflichtige Anlagen in Deutschland 2024* (installations 14310-0641, 14250-0036, 14616-0165, 14616-0254)
- **Bundesnetzagentur** — Marktstammdatenregister, unit records queried 21 September 2026; Kraftwerksliste zum Szenariorahmen 2037
- **European Commission** — Del. Reg. (EU) 2019/331 Art. 2a; Guidance Document 6 on cross-boundary heat flows; Impl. Reg. (EU) 2026/1412
- **BMWK** — Pressepapier zum Industriestrompreis, 16 April 2026
- **KWKG** as amended 1 April 2025; **KWKAusV**
- **Fraunhofer ISE** — Energy-Charts API over Bundesnetzagentur SMARD data (CC BY 4.0)

---

## Tools, and scope of AI assistance

Python 3.11 with pandas and NumPy for the model, Matplotlib for the figures, openpyxl for the workbook. `pdftotext` (Poppler) plus Python parsing to extract the DEHSt and Bundesnetzagentur registers from PDF. The Marktstammdatenregister public JSON endpoint for per-unit queries. The Energy-Charts API over Bundesnetzagentur SMARD data for day-ahead prices and generation mix, used to compute the mean price, daily spreads, the negative-price share and the solar and wind capture rates.

**Claude (Opus 5) was used for:** finding and triaging public sources; extracting and parsing the register PDFs; writing the Python for the cost model, the sensitivity sweep and the figures; computing the price statistics; and drafting prose.

**I directed the work and own the reasoning:** which use case to pursue and which to cut; anchoring on verified emissions and making total efficiency the scenario axis; the €/tonne-of-product denominator; the rejection of PyPSA; which figures to trust and which to refuse; and the conclusions. The scenario-axis error above was caught by reading the model's own output and asking why the "high efficiency" and "low efficiency" cases were only 0.02 apart — the model and the write-up were both rebuilt as a result.

---

Sarvesh Patidar · Münster
