# Decision Log

> Every major analytical choice gets an entry. Format: **Context → Options → Decision → Rationale → Trade-offs → Status**  
> Interviewers probe *why*, not *what*. This file is your defense brief.

---

## Template (copy for new decisions)

```
### D0XX — [Short title]
**Date:** YYYY-MM-DD  
**Status:** Proposed | Accepted | Revised

**Context:** What problem does this decision solve?

**Options considered:**
1. Option A — ...
2. Option B — ...

**Decision:** ...

**Rationale:** ...

**Trade-offs:** What we give up.

**Validation / how we'll know it's right:** ...
```

---

## Accepted decisions

### D001 — Assignment option
**Date:** 2026-06-04  
**Status:** Accepted

**Context:** Brief offers Option 1 (predictive risk) or Option 2 (end-to-end platform).

**Options considered:**
1. Option 1 — predictive model + risk scoring
2. Option 2 — data platform / pipeline design
3. Both — split effort

**Decision:** Option 1 only; mention production path on Slide 5.

**Rationale:** Role is Senior Data Scientist; job ad emphasizes predictive models, ML, LLM. Option 1 is demonstrable in available time and matches evaluation criteria.

**Trade-offs:** Less depth on Azure/Databricks architecture unless addressed on one slide.

---

### D002 — Unit of analysis
**Date:** 2026-06-04  
**Status:** Accepted

**Context:** Need consistent grain for features, target, and inspection targeting story.

**Options considered:**
1. Workplace (site)
2. Contravener / organization
3. Field visit

**Decision:** **Workplace** as primary unit; aggregate to organization for executive reporting if needed.

**Rationale:** FIRE defines workplace as the inspected entity; NAICS and location attach to workplace; inspectors visit sites. Field visit grain would leak multiple rows per workplace in same period.

**Trade-offs:** Multi-site organizations need roll-up logic; org-level patterns may blur.

---

### D003 — Data sources for prototype
**Date:** 2026-06-05  
**Status:** Accepted

**Context:** What data to use for the prototype model.

**Options considered:**
1. Ontario OHS field visit open data only
2. OHS + WSIB sector rates
3. OHS + WSIB + StatsCan employment

**Decision:** OHS 2017–2024 as primary; WSIB injury rates as optional sector baseline; StatsCan skip unless time permits.

**Rationale:** OHS data has workplace ID, orders, NAICS — sufficient for prototype. WSIB adds external prior at sector level. Firm-level WSIB join is messy and low ROI for weekend.

**Trade-offs:** No worker-count denominator without StatsCan; no complaint/injury events in open data.

---

### D004 — Target variable
**Date:** 2026-06-05  
**Status:** Accepted

**Context:** Need a learnable label that proxies "high risk" without predicting individual accidents.

**Options considered:**
1. Any order in next 12 months (broad, easier to predict, less meaningful)
2. **Serious order** (Stop Work + Time Unknown) in next 12 months
3. Critical injury / fatality (too rare)
4. Composite severity score across order types

**Decision:** Binary target at **workplace** grain — workplace receives ≥1 **Stop Use/Stop Work Order** OR **Time Unknown Order** in calendar year **2023**. Features come from 2017–2022. Evaluation cohort: workplaces with history (2017–2022) **and** a 2023 visit (~12,234 workplaces, **~8.0%** positive rate). Among all 2023 visits the rate is **~9.3%**.

**Rationale:** Data dictionary defines stop works and time-unknown orders as signaling immediate risk of injury. EDA confirmed enough volume (~14k row-level serious orders in 2023) and a learnable workplace-level base rate. More meaningful than "any order"; far more learnable than fatalities.

**Trade-offs:** Proxy ≠ actual harm; reactive investigations inflate labels; selection bias (only inspected workplaces have observed labels).

**Validation:** 2023 base rate ~9.3% (all visited) / ~8.0% (return-visit cohort). 2022 rate ~9.1% — stable enough to trust out-of-time design. Fatalities file used for narrative validation only, not training.

---

### D005 — Train / test split
**Date:** 2026-06-05  
**Status:** Accepted

**Context:** Must validate the way the model will be used in production.

**Options considered:**
1. Random 80/20 split ❌ (leaks future into past)
2. **Out-of-time:** features ≤2022, target in 2023
3. Out-of-time: features ≤2021, target in 2022 (robustness check)

**Decision:** Out-of-time — features through **2022-12-31**, target = serious order in **2023**. Prototype uses **2017–2023** files only (2024 held back until schema map exists). Optional robustness check: features ≤2021 → target 2022 (~9.1% serious rate).

**Rationale:** Simulates "score workplaces using history, inspect next year." 2022 and 2023 serious-order rates are within ~0.2 pp, so one test year is defensible.

**Trade-offs:** Single primary test year; COVID-era 2020–2021 may distort some patterns (mitigated by 5-year feature window).

---

### D006 — Selection bias mitigation (framing, not modeling)
**Date:** 2026-06-05  
**Status:** Accepted

**Context:** Labels exist only where Ministry chose to inspect.

**Options considered:**
1. Ignore (junior mistake)
2. Acknowledge + recommend exploration capacity + validate on proactive inspections subset
3. Complex inverse-probability weighting (too much for weekend)

**Decision:** Acknowledge explicitly in deck; recommend reserved random/exploratory inspection capacity; optionally evaluate model on **Inspection** case type only as sensitivity analysis.

**Rationale:** Senior DS wins on naming the trap and proposing operational mitigation, not on perfect statistical correction in a prototype.

**Trade-offs:** Model scores for never-inspected workplaces are extrapolations.

---

### D007 — Schema normalization across years
**Date:** 2026-06-05  
**Status:** Accepted

**Context:** OHS field visit files differ across years; need a stackable subset for the prototype.

**Options considered:**
1. Stack all years 2017–2024 as-is
2. Stack 2017–2023 with a shared column subset; handle 2024 separately
3. Use 2023 only

**Decision:** Stack **2017–2023** using core columns (`WORKPLACE ID`, `ORDER TYPE`, `CASE TYPE`, `FIELD VISIT DATE`, `PRIMARY NAICS`, `ORDER STATUS`). Drop extra 2021–2022 columns (`FIELD VISIT ID`, `ORDER ID`, `Unnamed: 0`) when concatenating. **Do not mix 2024 into the modeling table yet** — different column names and order-type strings.

**Rationale:** EDA showed 2020 matches 2023 schema; 2021–2022 add harmless extra ID columns; 2024 renames ACT/contravener fields and splits stop-work labels.

**Trade-offs:** Cannot use 2024 as test year without a rename map (D009).

---

### D008 — Snapshot / feature window design
**Date:** 2026-06-05  
**Status:** Accepted

**Context:** Need a clear point-in-time design to avoid leakage.

**Options considered:**
1. One row per workplace with all history ever
2. **Snapshot at 2022-12-31**, target in 2023
3. Rolling 12-month windows

**Decision:** Snapshot **2022-12-31**. Features = all visits/orders for that workplace in **2017–2022**. Target = serious order in **2023**. **Evaluation cohort** = workplaces with ≥1 visit in 2017–2022 **and** ≥1 visit in 2023 (~12,234 rows, ~8% positive). Operationally the model would score the full historical backlog; labels are only observed where inspection occurred.

**Rationale:** EDA showed that including all historical workplaces without a 2023 visit drops the positive rate to ~0.6% — most zeros mean "never inspected," not "low risk." Restricting evaluation to re-inspected workplaces gives honest labels.

**Trade-offs:** Smaller evaluation set; scores for never-revisited workplaces remain extrapolations (see D006).

---

### D009 — Serious order type string mapping
**Date:** 2026-06-05  
**Status:** Accepted

**Context:** Order type labels changed between 2023 and 2024.

**Decision:**
- **2023:** `Stop Use/Stop Work Order`, `Time Unknown Order`
- **2024:** `Time unknown order`, `STOP A057-6a/b/c/8` (four stop-work subtypes)

Use year-specific sets when labeling; do not assume one string works across years.

**Rationale:** Data dictionary defines the same serious concepts; open data just changed granularity/casing in 2024.

**Trade-offs:** Any cross-year target needs explicit mapping, not a single hardcoded list.

---

### D010 — Model choice (logistic vs boosting primary)
**Date:** 2026-06-07  
**Status:** Accepted

**Context:** Need a fast, interpretable baseline for the prototype and interview deck.

**Options considered:**
1. Logistic regression — linear, coefficient interpretability, fast
2. Gradient boosting (LightGBM/XGBoost) — higher AUC potential, less interpretable
3. Both — logistic primary, boosting as robustness check

**Decision:** **Logistic regression** as primary model. `log1p()` on count features; NAICS rolled to 2-digit sector; `class_weight='balanced'`.

**Rationale:** Assignment prioritizes interpretable drivers for Slide 3 and a single lift number for Slide 4. Logistic delivered **4.1× lift** in top decile with clear coefficients. Boosting optional if time permits.

**Trade-offs:** Misses nonlinear interactions; sector dummies dominate some coefficients.

**Validation:** Top-decile serious-order rate **32.5%** vs **8.0%** baseline; PR-AUC 0.32, ROC-AUC 0.81 on full 2023 cohort.

---

### D011 — Primary evaluation metric
**Date:** 2026-06-07  
**Status:** Accepted

**Context:** Ministry use case is **prioritizing inspections** — care about concentration of serious orders in highest-scored workplaces, not overall accuracy.

**Options considered:**
1. Accuracy — misleading at 8% base rate
2. ROC-AUC — threshold-free but not aligned to top-K targeting
3. **Lift@top decile** — rate in top 10% scored vs baseline
4. PR-AUC — good for imbalanced data, secondary

**Decision:** **Lift@top 10%** primary; **PR-AUC** secondary; ROC-AUC reported for completeness.

**Rationale:** Directly answers "if we inspect the top 10% scored, how much richer in serious orders vs random?" Prototype result: **4.1× lift** (32.5% vs 8.0%).

**Trade-offs:** Single decile cutoff; doesn't measure calibration across full score range (decile chart supplements).

**Validation:** Monotonic lift across deciles 1→10 in `data/processed/lift_chart.png`.

---

## Pending decisions (fill as you go)

### D012 — WSIB join vs slide mention only
**Status:** Pending — Phase 5
