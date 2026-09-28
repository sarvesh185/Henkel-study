# Data register

Every figure used, its value, its source, and how much weight it can carry. Cite by ID in the write-up (e.g. "229,042 t CO₂ [E-01]").

**Accessed:** 21–24 September 2026.

## Confidence key

| Tag | Meaning |
|---|---|
| **P** | **Primary registry** — auditable per installation/unit. Safe to build on. |
| **C** | **Computed** by me from primary data. Reproducible from `workings/`. |
| **O** | **Operator-published** — the company's own figure about itself. Generally reliable, occasionally mixes gross/net. |
| **S** | **Single source** — no corroboration found. Flag in text. |
| **U** | **Unverified / failed checking** — do not build on. State as unresolved. |
| **A** | **Assumption** — chosen by me, with a stated basis. Sensitivity required. |

---

## 1. Site (S)

| ID | Figure | Value | Conf | Source |
|---|---|---|---|---|
| S-01 | Site area | 1.4 km² / 143 ha | O | Henkel, Standort Düsseldorf; chemicalparks.com |
| S-02 | People on site | ~11,000 total, ~6,000 Henkel, ~90 nations | O | Henkel, Standort Düsseldorf |
| S-03 | Buildings / roads / rail | ~400 buildings, 15 km road, 21 km rail | O | Henkel, Standort Düsseldorf |
| S-04 | Tenants | Henkel, BASF, KLK Oleo | O | chemicalparks.com; BASF Düsseldorf |
| S-05 | Land acquired in Holthausen | 1899, 5 ha, rail + Rhine port access | O | Rheinische Industriekultur |
| S-06 | Production start on site | **1900** | O | Rheinische Industriekultur |
| S-07 | Persil factory / soap factory | 1906/07 | O | Rheinische Industriekultur |
| S-08 | Continuous spray-drying (Krause process) | **1920** | O | Rheinische Industriekultur |
| S-09 | Power plant on site | **1935** | O | Rheinische Industriekultur |
| S-10 | **Henkel Düsseldorf output** | **~400,000 t/yr** | **S** | Henkel, "Big factories, smaller footprint" (2021). **No second source. This is the €/t denominator — confirm on site.** |
| S-11 | BASF Düsseldorf output | ~1,400,000 t/yr | O | BASF DE site page, verbatim: *"rund 1,4 Mio. Tonnen Produkte"*. English page omits it. |
| S-12 | Site rank | 2nd-largest Laundry & Home Care site worldwide | O | Henkel |
| S-13 | High-bay warehouse | >200,000 pallets, 16 levels, €44m expansion 2024 | O | Henkel |
| S-14 | Adhesives output | ~100m Pritt sticks/yr, 30+ export countries | O | Henkel |
| S-15 | Energy metering | Online metering since **2013**; −26% energy since 2013; "digital backbone" | O | Henkel |
| S-16 | Recognition | WEF Lighthouse Factory 2020; Factory of the Year 2020 | O | Henkel |
| S-17 | Products made here | Persil, Perwoll, Weißer Riese, Spee, Pril, Bref; Pritt, Ponal, Metylan, Pattex, Loctite, Technomelt | O | Henkel |

## 2. Generation fleet (G) — Marktstammdatenregister, per unit

Queried by unit ID, 21 Sep 2026. **This is the authoritative live register** and supersedes the 2023 BNetzA list.

| ID | Unit | MaStR-Nr | Commissioned | Gross kW | Net kW | Status | Owner |
|---|---|---|---|---|---|---|---|
| G-01 | F03G1 | SEE956631893736 | **1963** | 10,000 | 9,000 | **Permanently decommissioned** | Henkel |
| G-02 | F03G2 | SEE949722134498 | **1965** | 13,200 | 11,880 | In operation | Henkel |
| G-03 | F03G3 | SEE952807166543 | **1965** | 13,200 | 11,880 | In operation | Henkel |
| G-04 | F13G5 | SEE945580171361 | **1980** | 20,000 | 18,000 | In operation | Henkel |
| G-05 | F13G6 | SEE907828499484 | **1983** | 20,000 | 18,000 | In operation | Henkel |
| G-06 | F18BHKW | SEE992491089179 | 2016 | 1,999 | 1,968 | In operation | Henkel |
| G-07 | BHKW BASF F17 | SEE957939399869 | 2016 | 1,999 | 1,968 | **Permanently decommissioned** | BASF |
| G-08 | Gasturbine (leased) | SEE964215288830 | 2012 | 8,900 | 8,600 | In operation | BASF |
| G-09 | V28PV (rooftop solar) | SEE919698093013 | — | 544 | — | In operation | Henkel |

All gas-fired; all flagged for heat extraction (CHP). Confidence **P**.

| ID | Derived | Value | Conf |
|---|---|---|---|
| G-10 | Henkel capacity in operation | **68.4 MW gross / 61.7 MW net** (5 units) | C |
| G-11 | Site capacity in operation | 77.3 MW gross / 70.3 MW net | C |
| G-12 | Total registered incl. retired | **89.3 MW gross** / 81.3 MW net | C |
| G-13 | Henkel capacity-weighted vintage | **1976** | C |
| G-14 | Share of live Henkel net capacity pre-1990 | **97%** | C |

### G-15 — The three-source capacity reconciliation

| Source | Figure | What it measures |
|---|---|---|
| BASF press release, 2016 | "~89 MW" | **Gross registered**, all 8 units = 89.3 MW |
| BNetzA Kraftwerksliste, Jan 2023 | 81.4 MW | **Net**, all units then operating = 81.3 MW |
| MaStR, Sep 2026 | 77.3 / 70.3 | Only units **currently operating** |

None is wrong. The gap is gross-vs-net plus two retirements. **Use net, currently-operating, and say why.** Confidence **C**.

## 3. EU ETS (E) — DEHSt installation list 2024

Parsed with integrity checks; see § 7. All confidence **P**.

### Verified emissions, t CO₂

| ID | Installation | ID no. | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 |
|---|---|---|---|---|---|---|---|---|
| E-01 | **Henkel Kraftwerk Holthausen** | 14310-0641 | 335,398 | 313,424 | 322,725 | 286,155 | 276,326 | **229,042** |
| E-02 | BASF Personal Care Anlage 40 | 14250-0036 | 94,819 | 82,334 | 99,426 | 93,346 | 75,123 | 86,166 |
| E-03 | BASF Personal Care Anlage 20 | 14616-0165 | 899 | 1,417 | 1,131 | 762 | 1,079 | 1,645 |
| E-04 | KLK Emmerich Anlage 10 (Ölfabrik) | 14616-0254 | — | — | — | — | — | 0 (new to scope 2024) |
| E-05 | SWD Heizkraftwerk Lausward | 14310-0531 | 1,144,305 | 1,377,984 | 1,089,909 | 915,963 | 896,571 | 982,738 |
| E-06 | Mercedes-Benz Düsseldorf HKW | 14310-0689 | — | — | — | — | — | 42,749 |

### Free allocation, t CO₂

| ID | Installation | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 |
|---|---|---|---|---|---|---|---|
| E-07 | Henkel Kraftwerk Holthausen | 74,860 | 70,139 | 83,081 | 80,947 | 78,812 | **63,398** |
| E-08 | BASF Anlage 40 | 82,043 | 80,351 | 82,872 | 82,830 | 82,830 | 81,806 |
| E-09 | BASF Anlage 20 | 95,902 | 93,924 | 67,963 | 67,963 | 67,963 | 67,963 |
| E-10 | SWD Lausward | 49,239 | 39,000 | 35,893 | 36,607 | 33,211 | 28,650 |

### 2024 positions

| ID | Installation | Emitted | Free | Net to buy | Covered | Carbon cost @ €82.50/t CO₂ |
|---|---|---|---|---|---|---|
| E-11 | **Henkel** | 229,042 | 63,398 | **165,644** | **27.7%** | **€13.7m** |
| E-12 | BASF Anlage 40 | 86,166 | 81,806 | 4,360 | 94.9% | €0.4m |
| E-13 | BASF Anlage 20 | 1,645 | 67,963 | **−66,318** | 4,132% | **−€5.5m (surplus)** |
| E-14 | SWD Lausward | 982,738 | 28,650 | 954,088 | 2.9% | €78.7m |

| ID | Trend | Value | Conf |
|---|---|---|---|
| E-15 | Henkel emissions 2019→2024 | −32% (335,398 → 229,042) | C |
| E-16 | Henkel emissions 2023→2024 | **−17%** — part unit retirement [G-01], part possible dispatch switching | C |

## 4. Derived energy balance (D)

| ID | Figure | Value | Conf | Basis |
|---|---|---|---|---|
| D-01 | Natural gas emission factor | 0.2016 t CO₂/MWh (NCV) | A | IPCC/UBA standard |
| D-02 | **Gas input 2024** | **1,136,121 MWh ≈ 1.14 TWh** | C | E-01 ÷ D-01 |
| D-03 | Boundary caveat | D-02 is *all* gas inside the ETS installation. **Whether spray-dryer burners sit inside it or take steam from it is not publicly resolvable** and changes the split below. | U | — |
| D-04 | Electricity output band | 294–342 GWh/yr | C | D-02 × η_el 0.259–0.301 (= 0.35 × η_tot 0.74–0.86) |
| D-05 | Heat output band | 546–635 GWh/yr | C | D-02 × η_th 0.481–0.559 (= 0.65 × η_tot 0.74–0.86) |
| D-06 | Implied full-load hours | 4,769–5,543 h | C | D-04 ÷ G-10 net |
| D-07 | Carbon cost per tonne of product | **€34.2/t product** | C | E-11 ÷ S-10 |
| D-08 | Same, park-wide denominator | €7.6/t product | C | E-11 ÷ (S-10 + S-11) |
| D-09 | Efficiency uplift 0.285→0.45 | *Superseded.* Early single-point estimate, replaced by the three-scenario model; see write-up §4.2 and `model/chp_model.py`. | C | — |
| D-10 | Efficiency uplift 0.285→0.55 | *Superseded.* Same early single-point basis as D-09; replaced by the three-scenario model. | C | — |
| D-11 | Legacy CHP switching threshold, 2026 | **€71.9/MWh_el** | C | see `dispatch.py` |
| D-12 | Modern CHP switching threshold, 2026 | €59.9/MWh_el | C | same |
| D-13 | Henkel's "city of 100,000" claim | Consistent with D-04 only on the broad per-capita reading (~450 GWh), not the household one (~150 GWh). **Don't cite as a load figure.** | U | Henkel |

## 5. Prices (P) — computed from BNetzA/SMARD via Energy-Charts API

All confidence **C**; reproducible from `analyse_prices.py` and `capture.py`.

| ID | Metric | 2024 | 2025 | 2026 YTD (to 20 Sep) |
|---|---|---|---|---|
| P-01 | Mean day-ahead, DE-LU | €78.5/MWh | €91.0/MWh | **€105.8/MWh** |
| P-02 | Mean daily spread | €111.2/MWh | €130.4/MWh | **€178.8/MWh** |
| P-03 | Negative-price intervals | 5.2% | 4.7% | **7.3%** |
| P-04 | Minimum | −€135/MWh | −€250/MWh | **−€500/MWh** |
| P-05 | Maximum | €936/MWh | €583/MWh | €747/MWh |

| ID | Figure | Value | Conf |
|---|---|---|---|
| P-06 | Day-ahead moved to 15-min MTU | **1 October 2025** — visible in the raw series as a mid-2025 resolution change | C |
| P-07 | **Solar PV capture price / rate, 2026 YTD** | **€55.24/MWh = 52.2%** of baseload | C |
| P-08 | **Wind onshore capture price / rate, 2026 YTD** | **€93.98/MWh = 88.8%** | C |
| P-09 | Monthly solar capture rate 2026 | Jan 101% · Feb 82% · Mar 58% · **Apr 26%** · May 40% · Jun 59% · Jul 52% · Aug 53% · Sep 58% | C |
| P-10 | Independent cross-check of P-09 | Kpler reports German solar capture **25% in April 2026**; I computed 25.8%. Two methods, one answer. | C+O |

## 6. Costs and assumptions (C)

| ID | Input | Value | Conf | Source / basis |
|---|---|---|---|---|
| C-01 | Gas (THE/TTF) | €34.6 (2024), €37.2 (2025), €33.0 (2026 est) /MWh | A/O | FfE 2025 review; 2026 estimated |
| C-02 | EUA | €65 (2024), €75 (2025), **€82.50 (2026)** /t CO₂ | S | Trade reports; exceeded €90 in Jan 2026 |
| C-03 | EUA 2030 projection | ~€126/t CO₂ | S | Analyst consensus; used only as a scenario |
| C-04 | Electricity tax (Stromsteuer) | €20.50/MWh standard; **€0.50/MWh** with manufacturing relief | O | Statutory |
| C-05 | Spitzenausgleich | **Abolished from 2024** | O | EY / IHK |
| C-06 | BDEW industrial bands, 2025 | 20–70 GWh/yr: 15.9 ct/kWh · 70–150 GWh/yr: 14.4 ct/kWh | O | BDEW |
| C-07 | BDEW small/medium industry 2026 YTD | 17.2 ct/kWh (−0.4 vs 2025) | O | BDEW |
| C-08 | Modelled delivered industrial price | 16.26 ct/kWh no reductions; **10.73 ct/kWh** max reductions | O | SMARD modelled |
| C-09 | Gas boiler efficiency | 0.92 | A | Standard |
| C-10 | E-boiler efficiency | 0.99 | A | Standard |
| C-11 | Heat pump COP range | 2.5–4.0 | A | For a ~50 K lift to DH supply temperature |
| C-12 | Legacy CHP total efficiency | η_tot 0.74 / 0.80 / 0.86, electrical share 0.35 | **A** | **Inferred from vintage and unit type, not published. Ageing reduces the total, not the split; η_tot is the scenario axis and the widest swing in the study (write-up §4.3).** |
| C-13 | Modern CHP η_el / η_th | 0.45 / 0.42 | A | Modern gas CHP |
| C-14 | Gas-boiler heat cost, 2026 | €53.9/MWh_th | C | (C-01 + D-01×C-02) ÷ C-09 |
| C-15 | E-boiler capex | €250–400k per MW_th | A | Order of magnitude |
| C-16 | Network charge for this site | **Not public.** Almost certainly individually negotiated under §19(2) StromNEV in a closed distribution system. Swings power-to-heat 3×. | U | — |

## 7. Regulation (R)

| ID | Instrument | Content | Conf | Source |
|---|---|---|---|---|
| R-01 | **FAR Art. 2a** | An electricity generator gets **no free allocation except for measurable heat from (a) high-efficiency cogeneration or (b) heat exported for district heating**. | P | Del. Reg. (EU) 2019/331 |
| R-02 | **Cross-boundary heat, GD6** | ETS→ETS heat: the **consumer** gets the allocation, producer gets nothing. ETS→non-ETS: the **producer** gets it. Heat used for electricity: no allocation. | P | EC Guidance Document 6 |
| R-03 | District heating sub-installation | Producer receives allocation; carbon-leakage exposure factor **fixed at 0.3 for all of Phase 4 (2021–2030)**, unlike others which decline after 2025. | P | GD6 |
| R-04 | Benchmarks 2026–2030 | IR (EU) **2026/1412**, adopted 29 Jun 2026. | P | EUR-Lex |
| R-05 | **Heat/fuel benchmark −34%** | Two trade sources assert it. **Commission press release IP/26/1044 does not state it; Annex I unreachable.** | **U** | **Directional only. No headline number depends on it.** |
| R-06 | EEG-Umlage | Zeroed 1 Jul 2022, **abolished 1 Jan 2023**. Renewables now budget-financed (KTF). | O | Enoplan; BNetzA |
| R-07 | BesAR | Moved from EEG to **EnFG**; now covers only **KWKG-Umlage + Offshore-Netzumlage**. Sector list cut **221→116**. Relief ~€650m (2023) vs ~€5bn historically. | O | Enoplan; Deloitte |
| R-08 | BesAR transition | Off-list companies keep access only until **last application in 2027 for calendar year 2028**. | O | Enoplan |
| R-09 | **KWKG term** | Extended by the 1 Apr 2025 amendment to **31 Dec 2030**. | O | Rödl |
| R-10 | **KWKG permitting deadline** | **31 Dec 2026** — BImSchG approval *or* binding equipment order; then up to 4 years to commission. | O | DS Werk; Rödl |
| R-11 | KWKG support duration | 30,000 full-load hours; annual eligible hours decline **3,500 (2025) → 2,500 (2030)**. | O | DS Werk |
| R-12 | KWKG >500 kW | **Auction track. Post-2025 annual volumes remain undefined.** A real planning risk. | O | DS Werk; BNetzA |
| R-13 | KWKG heat networks | Investment ceiling raised **€20m → €50m**; "unavoidable waste heat" **widened to include electricity generation facilities**. | O | Rödl |
| R-14 | KWKG new heat sources | Fossil fuels other than natural gas prohibited. | O | Rödl |
| R-15 | **Industriestrompreis** | Live **1 Jan 2026**, 3 years to 2028, ~€1.5bn/yr, ~2,000 companies. | O | BMWK; Pexapark; Grant Thornton |
| R-16 | Industriestrompreis formula | **Subsidy = 0.5 × eligible consumption × differential price**; 2026 differential price **€37.44/MWh** (≈ €18.72/MWh across the whole volume). | O | VODASUN |
| R-17 | Eligibility | Offtake point in Germany; sector on first **KUEBLL** partial list (~91 sectors, **WZ-2008** code); not in difficulty; no EU recovery order. **No minimum consumption.** | O | VODASUN |
| R-18 | **Reinvestitionspflicht** | **≥50% of subsidy** reinvested within **48 months**, in: renewables (own PV **and PPAs explicitly**) · efficiency incl. **waste-heat recovery**, ISO 50001 · demand flexibility incl. **battery storage, flexible thermal generation**, hydrogen · infrastructure/grid connections. | O | VODASUN |
| R-19 | **Flexibility bonus** | **+10%** on the subsidy if **≥80%** of required investment goes to demand-side flexibility. | O | VODASUN |
| R-20 | Deadlines | Registration from Dec 2026 · application **31 Mar 2027** for FY2026 · auditor memo **31 May 2027** for claims ≥10 GWh. | O | VODASUN |
| R-21 | **Henkel sector eligibility** | Detergents = WZ-2008 **20.41**; adhesives **20.52**. **Whether these are on the KUEBLL partial list is NOT confirmed. This gates the entire Industriestrompreis case.** | **U** | — |
| R-22 | Heat made *using* electricity | Whether it is eligible for heat-benchmark allocation is **unresolved**. Art. 2a covers the generator exclusion, not this. Matters for the e-boiler and heat-pump cases. | **U** | — |
| R-23 | iKWK route | Innovative-CHP auction track requires CHP + electric heat generator + innovative renewable heat feeding a heat network. Henkel has had a heat-network connection since Apr 2026. **BAFA Merkblatt not machine-readable — flag as a route, don't claim it.** | U | BAFA |
| R-24 | ETS2 | From 2027. Process gas is in ETS1 so no double coverage; site logistics and non-ETS1 fuel are exposed. | O | — |

## 8. District heating (H)

| ID | Figure | Value | Conf | Source |
|---|---|---|---|---|
| H-01 | **Operational since** | **13 April 2026** | O | Henkel press release |
| H-02 | Timeline | Agreement Sep 2022 · construction from Aug 2023 · live Apr 2026 | O | Henkel |
| H-03 | Infrastructure | 51 m steel chimney (56 t, 3.60 m dia.) with heat exchanger; 700 m² energy centre; **3.6 km** pipeline Benrath→Holthausen | O | Henkel; Stadtwerke Düsseldorf |
| H-04 | Coverage | Up to **35%** of district heat for Garath and Benrath | O | Stadtwerke Düsseldorf |
| H-05 | CO₂ saving | ~**6,500 t/yr** | O | Henkel |
| H-06 | Funding | NRW state economics ministry | O | Henkel |
| H-07 | Heat volume, back-calculated | **16–30 GWh_th/yr** (16 if displacing Lausward CHP heat, 30 if a gas boiler) | C | H-05 ÷ D-01 |
| H-08 | Implied thermal capacity | **~6–8 MW_th** at 4,000–5,000 full-load hours | C | H-07 |
| H-09 | Share of site heat output | 2.8–5.2% of central-case D-05 | C | — |
| H-10 | Counterparty | Stadtwerke Düsseldorf (Lausward, E-05/E-14) | O | — |

## 9. RIZM (Z)

| ID | Figure | Value | Conf | Source |
|---|---|---|---|---|
| Z-01 | Product layers | Digital Twin · Decision Hub · Operation Hub · Production Scheduling · Portfolio Manager · Autonomous Agent | O | rizm.de |
| Z-02 | Customers | BMW Group, B/S/H, **Currenta**, ZF, Mercedes-Benz, Volkswagen, Smurfit Kappa, Boehringer Ingelheim, Bosch, Infineum | O | rizm.de homepage logos |
| Z-03 | Currenta relevance | Operates Chempark multi-tenant utilities — structurally the same problem as Holthausen | C | — |
| Z-04 | BMW result | ">100 million EUR energy budget reduction"; homepage also says "high three-digit million range by 2030" — **their own material is internally inconsistent** | O | rizm.de |
| Z-05 | Scale claims | ">11 countries", ">147 plants implemented as twins", **">20 TWh optimized per day"** | O | rizm.de |
| Z-06 | Z-05 sanity check | **20 TWh/day fails a units check** — Germany's entire daily consumption is ~1.4 TWh. Almost certainly 20 TWh/yr or 20 GWh/day. **Save for the call, not the write-up.** | C | — |
| Z-07 | Founders | Elias Küpper CEO (Thermodynamics & Energy Systems) · Philipp Otten COO (Process Engineering & Simulation) · Joshua Küpper CBO (Statistics & Risk Management) | O | rizm.de/about |
| Z-08 | Mission language | *"Non-networked investment planning and incorrect operating methods lead to massive wrong decisions and **misallocations**"* | O | rizm.de/about |
| Z-09 | Method language | *"gut-feeling decisions are not audit-proof"*; advocates making **shape risk** transparent | O | CEO in e\|m\|w, Apr 2025 |
| Z-10 | Chicken-and-egg example | Thermal storage sizing × electrode boiler sizing × purchasing behaviour, co-optimised | O | rizm.de homepage |
| Z-11 | Operation Hub required params | *"ramping constraints, minimum loads and start-up costs"* | O | rizm.de |
| Z-12 | Deployment guidance | *"a validation phase in which the model is checked against historical data"* before live operation | O | rizm.de |
| Z-13 | Flexibility bands | Time windows, direction, kWh per 15-min block, limit price — sent to flexibility marketers (partner: Entelios). **RIZM does not trade.** | O | rizm.de; Entelios |
| Z-14 | Missing-data method | *"iterative approach for inverse calculations… back-calculated from known results"* — exactly what D-02 is | O | rizm.de Decision Hub FAQ |
| Z-15 | Comp | €60–90k base + €5–50k OTE (uncapped); seniority set in process | O | rizm.de careers |
| Z-16 | Language requirement | C1 German expected, but *"apply anyway… we keep a focus list"* | O | rizm.de careers |

---

## Verification log

### Integrity checks run

The DEHSt table publishes period **sums** and period **averages**. Sum ÷ period length must reproduce the published average. Six checks (emissions and allocation × three trading periods), all parsed rows: **all pass.** This is what validates column alignment.

It caught two real parsing errors:
1. A row split on a company name containing "Düsseldorf" (Stadtwerke Düsseldorf AG), shifting every column by one.
2. An off-by-one from a postcode token being read as data.

Both were found *because* the checks failed, not by eye. First-pass figures for E-05 were wrong and were corrected.

### Figures I refused to use

| ID | Why |
|---|---|
| R-05 | Heat benchmark −34%: two trade sources assert it, the Commission's own press release does not, Annex I unreachable. Used directionally only; no headline number depends on it. |
| D-13 | "City of 100,000" — only reconciles on the broad per-capita reading. Not used as a load figure. |
| R-22 | Heat made using electricity: unresolved in Art. 2a. Flagged, not assumed. |
| R-21 | KUEBLL sector eligibility: unconfirmed, and it gates the Industriestrompreis case. Stated as a gate. |

### Deliberate deviations from source

1. **G-15** — used 81.3 MW net / 70.3 MW operating rather than the "89 MW" both companies publish. The registry is per-unit and auditable; the press figure is unattributed and gross.
2. **D-07** — used the Henkel-only 400 kt denominator (€34.2/t) rather than park-wide (€7.6/t), a 4.5× difference. Defended on the grounds that RIZM deploys for Henkel and Henkel's P&L funds the pilot. Sensitivity shown.
3. **Network charges** — promoted from "unknown, cut" to "decision-critical, named" after my own sensitivity showed they swing power-to-heat 3×.

### Single-source figures, ranked by how much damage they'd do if wrong

1. **S-10** (~400 kt/yr) — the entire denominator. Highest-value item to confirm on site.
2. **C-12** (legacy η_tot 0.74–0.86) — the widest single parameter in the study: €19.59/t of product across the tested range (write-up §4.3).
3. **C-02** (EUA €82.50) — immaterial; run as a scenario column, not a point estimate.

---

## Toolchain

| Tool | Used for |
|---|---|
| Claude (Opus 5) | Research direction, source triage, modelling, drafting |
| `pdftotext` + Python | DEHSt installation list and BNetzA Kraftwerksliste parsing |
| MaStR public JSON endpoint | Per-unit queries by MaStR-Nr (G-01…G-09) |
| Energy-Charts API (BNetzA/SMARD, CC BY 4.0) | Hourly + 15-min DE-LU prices and generation, 2024 – Sep 2026 |
| pandas / numpy | All arithmetic, integrity checks, capture rates, dispatch and storage models |
| Browser | Reading rizm.de and the full scorecard directly |

### Scripts in `workings/`

| File | Produces |
|---|---|
| `parse_ets.py` | Section 3 tables + integrity checks → `ets_site_installations.csv` |
| `analyse_prices.py` | P-01 … P-05 |
| `capture.py` | P-07 … P-09 (solar and wind capture rates) |
| `dispatch.py` | D-11, D-12, hours out of the money |
| `carbon.py` | D-07 … D-10 |
| `eboiler.py` | E-boiler hours-in-the-money and value |
| `storage.py` | E-boiler × storage sizing matrix |
| `balance.py` | G-10 … G-15, D-02 … D-06, H-07 … H-09 |
| `isp.py` | Industriestrompreis subsidy scenarios, forgone-subsidy hurdle |

---

## Primary sources

- [DEHSt — Emissionshandelspflichtige Anlagen in Deutschland 2024](https://www.dehst.de/SharedDocs/downloads/DE/anlagenlisten/2021-2030/2024.pdf)
- [Marktstammdatenregister](https://www.marktstammdatenregister.de/)
- [BNetzA / NEP — Kraftwerksliste Szenariorahmen 2037](https://www.netzentwicklungsplan.de/sites/default/files/2023-01/Szenariorahmen_2037_Kraftwerksliste-genehmigt.pdf)
- [Energy-Charts API](https://api.energy-charts.info/)
- [FAR — Del. Reg. (EU) 2019/331, Art. 2a](https://www.legislation.gov.uk/eur/2019/331/article/2a/data.htm?view=plain)
- [EC Guidance Document 6 — Cross-Boundary Heat Flows](https://climate.ec.europa.eu/document/download/69b15cb9-8d5f-4937-8140-cbc8f2e75173_en)
- [EC press release IP/26/1044 — ETS benchmarks](https://ec.europa.eu/commission/presscorner/api/files/document/print/en/ip_26_1044/IP_26_1044_EN.pdf)
- [BMWK — Pressepapier zum Industriestrompreis](https://www.bundeswirtschaftsministerium.de/Redaktion/DE/Downloads/P-R/pressepapier-zum-industriestrompreis.pdf)

## Secondary sources

- [Henkel — Standort Düsseldorf](https://www.henkel.de/presse-und-medien/zahlen-und-fakten/standort-duesseldorf) · [~400 kt output](https://www.henkel.com/spotlight/2021-09-02-big-factories-smaller-footprint-1320318) · [waste heat live 13 Apr 2026](https://www.henkel.de/presse-und-medien/presseinformationen-und-pressemappen/2026-04-13-stadtwerke-duesseldorf-und-henkel-versorgen-ab-sofort-den-duesseldorfer-sueden-mit-industrieabwaerme-2142728)
- [Stadtwerke Düsseldorf — Energiezentrale Henkel](https://www.swd-ag.de/ueber-uns/presse/2025/20250715-energiezentrale-henkel-fernwaerme/)
- [BASF — Düsseldorf site, ~1.4 Mt/yr](https://www.basf.com/global/de/who-we-are/organization/locations/europe/german-sites/duesseldorf-und-monheim/duesseldorf) · [CHP units, "~89 MW"](https://www.basf.com/global/de/who-we-are/organization/locations/europe/german-sites/duesseldorf-und-monheim/news-releases/2016_07_08_neue-blockheizkraftwerke)
- [Rheinische Industriekultur — Henkel Werks- und Baugeschichte](https://www.rheinische-industriekultur.com/seiten/objekte/orte/duesseldorf/objekte/reisholz_henkel_intern.html)
- [chemicalparks.com — Henkel Düsseldorf](https://chemicalparks.com/chemical-parks/list-of-chemical-parks/show/henkel-ag-co-kgaa)
- [FfE — German electricity prices on EPEX Spot 2025](https://www.ffe.de/en/publications/german-electricity-prices-on-the-epex-spot-exchange-in-2025/)
- [BDEW Strompreisanalyse](https://www.bdew.de/service/daten-und-grafiken/bdew-strompreisanalyse/) · [etalytics — industrial price and Stromsteuer](https://etalytics.com/resources/blog/current-industrial-electricity-price-in-germany)
- [Enoplan — BesAR under EnFG; EEG-Umlage abolished](https://www.enoplan.de/besondere-ausgleichsregelung-nach-enfg-uebergangsregelung-nur-noch-bis-2028/)
- [Rödl — KWKG-Novelle 1 Apr 2025](https://www.roedl.com/insights/kwkg-novelle-was-ist-neu/) · [DS Werk — KWKG deadlines](https://dswerk.de/kraft-waerme-kopplung-industrie-kwkg-foerderung/)
- [VODASUN — Industriestrompreis: Voraussetzungen, Fristen, Reinvestitionspflicht](https://www.vodasun.de/industriestrompreis-2026-voraussetzungen-fristen-und-die-reinvestitionspflicht/) · [Pexapark](https://pexapark.com/blog/germany-seals-2026-industrial-power-price-subsidy-can-it-help-boost-the-ppa-market/) · [Grant Thornton](https://www.grantthornton.de/themen/2026/industriestrompreis-eu-kommission-genehmigt-deutsches-fordermodell/)
- [EU ETS benchmarks 2026–2030, heat benchmark −34% (unconfirmed)](https://refindustry.com/news/legislation/eu-updates-ets-free-allocation-benchmarks-for-2026-2030/)
- [Kpler — European solar capture rates, Jul 2026](https://www.kpler.com/blog/europes-solar-capture-rates-hit-record-lows-as-market-divergence-widens)
- [RIZM](https://rizm.de/en) · [Decision Hub](https://rizm.de/en/solution/decision-hub) · [Operation Hub](https://rizm.de/en/solution/operation-hub) · [About](https://rizm.de/en/about) · [Field Value Engineer posting](https://rizm.de/en/careers/forward-deployed-ai-energy-engineer) · [CEO on audit-proof decisions](https://rizm.de/en/press/gastbeitrag-von-elias-kuepper-im-e-m-w-magazin) · [Entelios partnership](https://www.entelios.de/rizm-entelios-ki-flexibilitaetsvermarktung-fuer-industrie/)
