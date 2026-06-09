# 5-Slide Executive Deck — Build Guide

> **Tool:** PowerPoint is safest for a government interview (universal, offline, easy to present). Canva is fine if you prefer nicer visuals — export to PDF as backup.
> **Audience:** Senior management (mostly non-technical). You narrate; slides stay sparse.
> **Time:** ~8–10 min present + Q&A. One key message per slide.
> **Numbers are real** (from `scripts/03_model.ipynb` + `04_boosting_shap.ipynb`).

**Design rules:**
- Max ~6 lines of text per slide. Big font (24pt+ body, 32pt+ titles).
- One visual per slide. Use your saved charts.
- Ministry-appropriate: clean, no clip-art, blue/grey palette.

**Charts to drop in:**
- Slide 4: `data/processed/lift_chart.png`
- Slide 3: `data/processed/feature_importance.png` + the LLM JSON snippet

---

## SLIDE 1 — From Reactive to Proactive

**Title:** Targeting Inspections Where Risk Is Highest

**Key message:** *We can prevent more harm with the same inspectors by predicting where serious risk concentrates.*

**Bullets:**
- Today, inspections are largely **reactive** (after a complaint, injury, or fatality) or broad sector campaigns.
- Inspector capacity is finite; most workplaces are never visited in a given year.
- **Opportunity:** rank workplaces by safety risk so proactive visits go to the highest-risk sites first.
- **The prize:** more serious problems caught — and injuries prevented — per inspector-day.

**Visual:** Simple arrow: "Reactive / broad campaigns → Risk-ranked targeting" OR a funnel (all workplaces → top-risk shortlist).

---

## SLIDE 2 — The Solution at a Glance

**Title:** A Risk-Scoring Engine for Inspection Planning

**Key message:** *Combine our enforcement history with inspection-report text to produce a ranked, explainable shortlist.*

**Bullets:**
- **Inputs:** enforcement & visit history (FIRE / Ontario open data) + inspection-report text (privacy-safe LLM extraction) + sector benchmarks (WSIB).
- **Engine:** ML model → **0–100 risk score + Low/Med/High tier + top-3 reason codes** per workplace.
- **Output:** a monthly prioritized inspection list, delivered in **Power BI** for planners.
- **Built on our stack:** Azure / Databricks / Power BI.

**Visual:** Left-to-right pipeline diagram:
`Data (structured + text) → Feature engineering → Risk model → Score + reason codes → Power BI for planners`

---

## SLIDE 3 — What Predicts Risk

**Title:** What the Data Says Drives Risk

**Key message:** *Risk is driven by enforcement history, recency, sector, and hazards surfaced from text — and we can explain every score.*

**Bullets:**
- **Target (be precise):** likelihood a workplace receives a **serious enforcement action** (stop-work / time-unknown order) on inspection — validated against actual serious injuries. *We do not claim to predict individual accidents.*
- **Top structured drivers:** prior orders & investigations, stop-work history, time since last visit, compliance rate, **industry sector** (construction & mining highest).
- **Text adds what structured fields miss:** an LLM converts narratives into features — e.g. *supervision failure*, *young/new worker*, *systemic cause*.

**Visual (two-panel):**
- Left: `feature_importance.png`
- Right: the LLM before/after — steel-tube report → JSON:
  ```
  hazard_type: caught-in / crush
  injury_severity: critical
  vulnerable_worker_flag: true
  supervision_failure_flag: true
  systemic_failure_flag: true
  ```

---

## SLIDE 4 — Does It Work? Validation & Impact

**Title:** Validated the Way It Would Be Used

**Key message:** *Targeting the top-scored workplaces finds ~4× more serious problems per inspection than the current baseline.*

**Bullets:**
- **Honest validation:** trained on history (2017–2022), tested on the next year (2023); cross-validated, not in-sample.
- **Result: ~4× lift in the top decile** — top-scored workplaces had a **32% serious-order rate vs 8% baseline**.
- **Robustness:** gradient boosting matched the simple model out-of-fold → the signal is real; we keep the **explainable** model with no accuracy penalty.
- **Business translation:** same harm prevented with far fewer visits — or far more harm prevented with the same budget.

**Visual:** `lift_chart.png` (decile bars, top decile ~4×).

**⚠️ Honesty guardrail (say out loud, don't overclaim):** prototype on public open data; metrics are directional, not a production guarantee.

---

## SLIDE 5 — Responsible, Fair & Ready to Deploy

**Title:** Built for a Government Environment

**Key message:** *Private, fair, explainable, human-in-the-loop, and deployable on our stack.*

**Bullets:**
- **Privacy (FIPPA/PHIPPA):** de-identify reports before processing; keep the LLM **in-tenant (Azure)** — no data to public APIs.
- **Fairness:** audit scores for disparate impact by region, sector, and firm size; exclude prohibited attributes.
- **Avoid feedback bias:** reserve some **random/exploratory** inspections so the model keeps learning the whole population.
- **Human-in-the-loop:** the model **ranks; inspectors decide.** Reason codes make every score reviewable.
- **Roadmap:** pilot one sector/region → validate → scale on Databricks → monitor drift & fairness.

**Visual:** 4 small icons (Privacy · Fairness · Human-in-the-loop · Roadmap) OR a simple pilot→scale timeline.

---

## Appendix slides (optional, keep hidden unless asked)
- A1: Target definition detail + selection bias (D004/D006)
- A2: Feature table + modeling table dictionary
- A3: Model metrics table (logistic vs LightGBM, CV)
- A4: LLM extraction prompt + schema (D013)

---

## Pre-flight checklist
- [ ] 5 slides max (appendix doesn't count, but keep it short)
- [ ] Both charts embedded and readable from across a room
- [ ] Target sentence on Slide 3 is exact (no overclaiming)
- [ ] Lift number (~4×) on Slide 4 matches notebook
- [ ] Export a **PDF backup** in case of software issues
- [ ] `AI_USAGE.md` ready to mention if asked
