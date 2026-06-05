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
**Status:** **Proposed — YOU MUST FINALIZE IN PHASE 0**

**Context:** Need a learnable label that proxies "high risk" without predicting individual accidents.

**Options considered:**
1. Any order in next 12 months (broad, easier to predict, less meaningful)
2. **Serious order** (Stop Work + Time Unknown) in next 12 months
3. Critical injury / fatality (too rare)
4. Composite severity score across order types

**Decision:** *(Fill in after you inspect order type counts in EDA)*  
**Recommended starting point:** Binary — workplace receives ≥1 **Stop Work** OR **Time Unknown** order in 2023, with features from 2017–2022.

**Rationale:** Stop works and time-unknown orders are defined in the data dictionary as signaling immediate danger. More learnable than fatalities; more meaningful than any order.

**Trade-offs:** Proxy ≠ actual harm; reactive investigations inflate labels; selection bias (only inspected workplaces).

**Validation:** Check base rate in 2023; optionally correlate high scores with WSIB fatality sectors (narrative only).

---

### D005 — Train / test split
**Date:** 2026-06-05  
**Status:** **Proposed — confirm in Phase 0**

**Context:** Must validate the way the model will be used in production.

**Options considered:**
1. Random 80/20 split ❌ (leaks future into past)
2. **Out-of-time:** features ≤2022, target in 2023
3. Out-of-time: features ≤2021, target in 2022 (robustness check)

**Decision:** Out-of-time with features through end of 2022, target in 2023. Optional second check on 2022 target.

**Rationale:** Simulates "score workplaces today using history, inspect next year." Prevents temporal leakage.

**Trade-offs:** Single test year; COVID-era 2020–2021 may distort patterns.

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

## Pending decisions (fill as you go)

### D007 — Schema normalization across years
**Status:** Pending — Phase 1 EDA

### D008 — Snapshot / feature window design
**Status:** Pending — Phase 2

### D009 — Serious order type string mapping
**Status:** Pending — Phase 2 (order types changed casing 2023→2024)

### D010 — Model choice (logistic vs boosting primary)
**Status:** Pending — Phase 3

### D011 — Primary evaluation metric
**Status:** Pending — Phase 3 (recommended: lift@top decile)

### D012 — WSIB join vs slide mention only
**Status:** Pending — Phase 5
