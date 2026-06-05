# Step-by-Step Execution Plan (~9–10 hours)

> Work top to bottom. Each **Phase** = one subtask chat (or one focused work block).  
> **Rule:** Log every major choice in `learning documents/decision_log.md` before moving on.  
> **Cut order if behind:** WSIB join → gradient boosting → polish code. **Never cut:** target definition, bias/privacy slide, rehearsal.

---

## Before you start (15 min)

- [ ] Read `PROJECT_MASTER.md` (frozen decisions)
- [ ] Skim `01_SOLUTION_Option1_Predictive_Risk.md` Sections 3–5
- [ ] Create Python env: `pip install pandas openpyxl scikit-learn matplotlib shap` (shap optional)
- [ ] Open `learning documents/decision_log.md` — you'll write to it constantly

**Subtask chat name:** *(none — do this in master or solo)*

---

## Phase 0 — Lock decisions (45 min) ⭐ DO THIS FIRST

**Goal:** Be able to defend target, unit, split, and bias in one minute out loud.

| Step | Time | Do this |
|---|---|---|
| 0.1 | 15 min | Read data dictionary sections: Case, Events, Enforcement Actions, Stop Works, Orders |
| 0.2 | 20 min | Write **D001–D006** in `decision_log.md` (templates already seeded — fill in YOUR words) |
| 0.3 | 10 min | Say aloud: "My target is… My unit is… My biggest bias risk is…" |

**Subtask chat prompt:**  
> "Help me finalize decision_log entries D004 (target variable) and D005 (train/test split). Here is my draft. Challenge my choices like an interviewer would."

**Exit criteria:** 6 decisions logged; you can explain target without reading notes.

---

## Phase 1 — EDA: know your data (1 hr)

**Goal:** Confirm columns, row counts, order-type distribution, missingness, schema changes across years.

| Step | Time | Do this |
|---|---|---|
| 1.1 | 20 min | Load **2023** xlsx in notebook `src/notebooks/01_eda.ipynb` |
| 1.2 | 20 min | Count: rows, unique workplaces, case types, order types, blank orders |
| 1.3 | 20 min | Check **2017 vs 2024** column name differences (contravener ID renamed, etc.) |

**Questions to answer in notebook:**
- How many rows have blank/`NULL` order type? (visits with no order)
- What % are Investigation vs Inspection?
- How many Stop Work + Time Unknown orders per year?
- How many unique `WORKPLACE ID` per year?

**Subtask chat prompt:**  
> "I'm doing EDA on the Ontario OHS field visit xlsx. Help me write pandas code to load 2023, normalize column names across years, and produce the summary stats in Phase 1."

**Exit criteria:** Notebook runs; you have 5 bullet EDA findings written in notebook or decision log.

**Log:** D007 — how you handle schema drift across years (rename map vs lowest common denominator).

---

## Phase 2 — Build the modeling table (1.5 hr)

**Goal:** One row per **workplace × snapshot date** with features from the past and target in the future.

**Recommended design (simplest defensible):**

```
Snapshot date: 2022-12-31
Features:      all visits/orders for that workplace in 2017–2022
Target:        any serious order (Stop Work OR Time Unknown) in 2023
```

| Step | Time | Do this |
|---|---|---|
| 2.1 | 30 min | Stack 2017–2022 files → `visits_hist` |
| 2.2 | 30 min | Stack 2023 file → `visits_2023` |
| 2.3 | 30 min | Aggregate to workplace level: features + binary target |

**Feature columns to compute (minimum viable):**

| Feature | Definition |
|---|---|
| `n_visits_5y` | Count of field visits 2017–2022 |
| `n_orders_5y` | Count of orders issued |
| `n_stop_work_5y` | Count of stop work orders |
| `n_time_unknown_5y` | Count of time unknown orders |
| `n_investigations_5y` | Visits where case type = Investigation |
| `pct_complied_5y` | Complied orders / total orders with status |
| `days_since_last_visit` | Days from last visit to snapshot |
| `primary_naics` | Mode NAICS code |
| `investigation_ratio` | investigations / visits |

**Subtask chat prompt:**  
> "Build workplace-level modeling table: features from 2017–2022, target = serious order in 2023. Workplace grain. Give me step-by-step pandas logic and help me avoid leakage."

**Exit criteria:** CSV or DataFrame `modeling_table` with ~N workplaces, ~10 columns, target rate documented.

**Log:** D008 — snapshot design; D009 — serious order definition (exact order type strings).

---

## Phase 3 — Baseline model (1.5 hr)

**Goal:** Train logistic regression, report metrics that matter for the interview.

| Step | Time | Do this |
|---|---|---|
| 3.1 | 20 min | Handle missing NAICS, encode categoricals, train/test = already temporal (2023 is test) |
| 3.2 | 30 min | Fit **logistic regression** (class_weight='balanced' if imbalanced) |
| 3.3 | 30 min | Compute: ROC-AUC, PR-AUC, **precision@top 10%**, **lift vs random** |
| 3.4 | 10 min | Print top coefficients (interpretable drivers) |

**Lift calculation (the number for your slide):**
```
baseline_rate = mean(y_test)
top_decile_rate = mean(y_test[scores >= 90th percentile])
lift = top_decile_rate / baseline_rate
```

**Subtask chat prompt:**  
> "I have a workplace modeling table with target = serious order in 2023. Help me train logistic regression and compute lift in the top decile. Explain what lift means for inspection planning."

**Exit criteria:** One lift number (e.g. "2.4×") + 3 interpretable coefficients you can say out loud.

**Log:** D010 — why logistic over black-box; D011 — primary metric = lift not AUC.

---

## Phase 4 — Optional: boosting + SHAP (1 hr) — skip if behind

| Step | Time | Do this |
|---|---|---|
| 4.1 | 30 min | Train LightGBM or sklearn HistGradientBoosting |
| 4.2 | 30 min | SHAP summary plot → save for Slide 3 |

**Subtask chat prompt:**  
> "Add gradient boosting and SHAP to my model notebook. Keep logistic as the explainability baseline."

---

## Phase 5 — WSIB enrichment (30 min) — optional

**Goal:** Join sector injury rate as a baseline-risk feature OR cite on slide only.

| Step | Time | Do this |
|---|---|---|
| 5.1 | 15 min | Parse `Injury rates.xlsx` (skip header rows; class/subclass tab) |
| 5.2 | 15 min | Map NAICS → WSIB class (coarse manual mapping for top sectors is fine) OR skip join and mention on slide |

**Note:** WSIB uses class/subclass, not NAICS directly. A coarse mapping is enough for a prototype.

**Log:** D012 — WSIB join approach or "mentioned only, not joined"

---

## Phase 6 — LLM text demo (45 min)

**Goal:** Show inspection narrative → structured JSON features (Slide 3).

| Step | Time | Do this |
|---|---|---|
| 6.1 | 15 min | Pick **Sample Report 2** (steel tubes / young workers) — richest signal |
| 6.2 | 20 min | Write extraction prompt → run in ChatGPT/Claude → save input + output |
| 6.3 | 10 min | Save to `data/llm_extraction_example.json` + note in `AI_USAGE.md` |

**Schema:**
```json
{
  "hazard_type": "",
  "injury_severity": "",
  "vulnerable_worker_flag": true,
  "supervision_failure_flag": true,
  "systemic_failure_flag": true,
  "order_sections": []
}
```

**Subtask chat prompt:**  
> "Write a FIPPA-safe LLM prompt to extract structured safety features from this inspection report. Schema: …"

**Exit criteria:** One before/after example for the deck.

---

## Phase 7 — Charts for slides (45 min)

| Chart | Slide | Source |
|---|---|---|
| Lift / decile bar chart | 4 | Phase 3 |
| Top 5 feature drivers (coef or SHAP) | 3 | Phase 3/4 |
| Solution diagram (boxes + arrows) | 2 | Draw in PowerPoint |
| LLM JSON example | 3 | Phase 6 |

---

## Phase 8 — Build 5 slides (2.5 hr)

Use outline in `01_SOLUTION_Option1_Predictive_Risk.md` Section 6.

| Slide | Time | Focus |
|---|---|---|
| 1 Problem | 20 min | Reactive → proactive; scarce inspectors |
| 2 Solution | 30 min | Data → model → score + reason codes → Power BI |
| 3 What predicts risk | 40 min | Target definition + drivers + LLM example |
| 4 Validation & impact | 40 min | Out-of-time + **your lift number** |
| 5 Responsible deploy | 20 min | Privacy, fairness, human-in-the-loop, roadmap |

**Subtask chat prompt:**  
> "Review my draft Slide 3 bullets against senior DS interview standards. Am I overclaiming?"

---

## Phase 9 — Rehearsal + compliance (1 hr)

| Step | Time | Do this |
|---|---|---|
| 9.1 | 30 min | Speaker notes from `01_SOLUTION` Section 7 |
| 9.2 | 20 min | Dry run × 2 out loud (target 8–10 min) |
| 9.3 | 10 min | Finish `AI_USAGE.md` — every AI tool cited |

---

## Time budget summary

| Phase | Hours | Required? |
|---|---|---|
| 0 Decisions | 0.75 | ✅ Required |
| 1 EDA | 1.0 | ✅ Required |
| 2 Modeling table | 1.5 | ✅ Required |
| 3 Baseline model | 1.5 | ✅ Strongly recommended |
| 4 Boosting/SHAP | 1.0 | Optional |
| 5 WSIB | 0.5 | Optional |
| 6 LLM demo | 0.75 | ✅ Required for brief |
| 7 Charts | 0.75 | ✅ Required |
| 8 Slides | 2.5 | ✅ Required |
| 9 Rehearsal | 1.0 | ✅ Required |
| **Total** | **~11 hr** | Cut optional → ~9 hr |

---

## When you return to master chat

Paste:
1. Which phase you finished
2. Any new decision log entries
3. Blockers
4. Updated lift number / key finding

Master chat will tell you what's next and whether you're on track.
