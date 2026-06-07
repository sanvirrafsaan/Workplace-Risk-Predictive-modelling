# Project Master — MLITSD Senior DS Assignment

> **This is the master context file.** When you return from a subtask chat, update the Status section here. When you open a new subtask chat, paste the relevant section + link back here.

---

## Assignment goal (never lose sight of this)

**Deliverable:** 5-slide executive presentation (presented live at interview)  
**Option chosen:** **Option 1 — Predictive Risk Identification**  
**Core ask:** Rank workplaces by safety risk using structured enforcement data + inspection text, with ML/LLM where appropriate, explainable for senior government leaders, respecting privacy/fairness/operational constraints.

**Optional but recommended:** One notebook + LLM extraction demo + `AI_USAGE.md`

---

## Frozen design decisions (update via `decision_log.md`)

| Decision | Choice | Why (one line) |
|---|---|---|
| Option | Option 1 | Role is Senior DS; demonstrates ML + LLM + stats |
| Unit of analysis | **Workplace** (aggregate to org for exec reporting) | Matches FIRE entity; inspection targets a site |
| Primary target | **Serious enforcement action** in forward window (Stop Work + Time Unknown orders) | Learnable, policy-meaningful proxy for immediate danger |
| Validation target | Critical injury/fatality correlation (not trained on) | North-star check; too rare to train |
| Train/test split | **Out-of-time** (e.g. features ≤2022 → predict 2023) | Matches deployment; avoids leakage |
| Baseline model | Logistic regression | Explainable odds ratios for executives |
| Performance model | Gradient boosting (optional) | Nonlinear interactions |
| Explainability | SHAP + reason codes | Required for enforcement context |
| Primary metric | **Lift in top decile** | Business metric: serious findings per inspection |
| LLM approach | Schema-constrained JSON extraction on de-identified text | Explainable > raw embeddings |
| WSIB use | Sector injury rates as **NAICS baseline feature** (optional) | External prior; not firm-level join |

---

## Data inventory

| File | Status | Role |
|---|---|---|
| `data/2017–2024_ohs_field_visit.xlsx` | ✅ Downloaded | **Primary modeling data** (~120k rows/yr) |
| `data/sample_inspection_reports.md` | ✅ Have | LLM/NLP demo (3 reports) |
| `data/Injury rates.xlsx` | ✅ Downloaded | WSIB sector no-lost-time injury rates → baseline feature |
| `data/Allowed_traumatic_fatalities.xlsx` | ✅ Downloaded | Validation narrative only (too sparse/coarse for training) |
| `data/2024-25_ohs_inspections.csv` | ✅ Have | Slide context (program-level counts) |
| Reference docs in `Reference documents/` | ✅ Have | Definitions, brief, job posting |

**Not available (frame as limitations):** bulk inspection text, complaint/injury event types from FIRE, worker counts.

---

## Repo structure

```
MLITSD-DS-Project/
├── PROJECT_MASTER.md          ← you are here (status + frozen decisions)
├── 00_STRATEGY_AND_PLAN.md    ← high-level strategy
├── 01_SOLUTION_Option1_Predictive_Risk.md  ← full solution + slide outline
├── 02_STEP_BY_STEP_PLAN.md    ← your hour-by-hour checklist
├── learning documents/
│   ├── decision_log.md        ← every major choice + trade-offs
│   └── concept_log.md         ← things you learned (optional, lightweight)
├── data/                      ← raw downloads (do not edit)
├── src/
│   └── notebooks/             ← your analysis notebooks
├── slides/                    ← final 5-slide deck
└── AI_USAGE.md                ← required by brief
```

---

## Multi-chat workflow

| Chat type | Purpose | When to use |
|---|---|---|
| **Master (this thread)** | Architecture, status, "what's next", cross-cutting decisions | Start/end of each work block; after completing a phase |
| **Subtask chat** | One focused deliverable (e.g. "build modeling table") | Each row in `02_STEP_BY_STEP_PLAN.md` |
| **Concept explainer** | Throwaway — "what is leakage?", "explain SHAP" | When stuck on a concept; paste summary into `concept_log.md` if worth keeping |

### Subtask chat prompt template

```
Context: MLITSD Senior DS assignment, Option 1 predictive risk.
Read: PROJECT_MASTER.md and decision_log.md in my repo.
Current phase: [e.g. Phase 3 — Feature engineering]
Task: [specific task]
Constraints: [e.g. out-of-time split, workplace grain, no leakage]
Output I need: [e.g. pandas code to aggregate visits to workplace-year]
Do NOT redo decisions already in decision_log.md.
```

When a subtask chat finishes, come back here and update **Progress tracker** below.

---

## Progress tracker

| Phase | Status | Artifact |
|---|---|---|
| 0. Setup & decisions | ✅ Done | D001–D009 accepted in `decision_log.md` |
| 1. Target & evaluation design | ✅ Done | D004, D005, D008 locked via EDA |
| 2. Data exploration (EDA) | 🟡 In progress | `scripts/01_data_exploration.ipynb` |
| 3. Modeling table | ⬜ Not started | `notebooks/02_modeling_table.ipynb` |
| 4. Features | ⬜ Not started | Feature list in decision log |
| 5. Baseline model + metrics | ⬜ Not started | `notebooks/03_model.ipynb` |
| 6. LLM text demo | ⬜ Not started | JSON extraction example |
| 7. Charts for slides | ⬜ Not started | lift chart, feature importance |
| 8. 5-slide deck | ⬜ Not started | `slides/` |
| 9. Rehearsal + AI_USAGE | ⬜ Not started | `AI_USAGE.md` |

---

## Feature groups (planned)

1. **Enforcement history** — order counts, stop works, time-unknown orders, contraventions/visit
2. **Compliance behavior** — % complied, % not complied, repeat outstanding
3. **Inspection cadence** — days since last visit, visit count, investigation ratio
4. **Sector baseline** — NAICS-level historical serious-order rate (out-of-fold); WSIB injury rate join
5. **Geography** — region from postal code (coarse)
6. **Text-derived** (demo only) — hazard type, severity, supervision failure, vulnerable worker flags

---

## Risks you must be able to explain (Slide 5)

- Selection / label bias (only inspected workplaces have labels)
- Feedback loop if 100% model-driven targeting
- FIPPA/PHIPPA — de-identify before LLM
- Fairness — audit by region/sector/size
- Overclaiming — risk likelihood, not accident prediction

---

## Last updated

- Date: 2026-06-05
- By: Phase 0 closed — D004/D005/D007/D008/D009 accepted after EDA
