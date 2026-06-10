# Technical Documentation — Predictive Risk Identification

This document describes the methodology, data, modeling decisions, and limitations behind the prototype I built for Option 1 of the assignment: identifying high-risk workplaces so the Ministry can target OHS inspections more effectively.

The short version: I built a workplace-level risk model on Ontario's public OHS field visit data (2017–2023). Scoring workplaces with a logistic regression and inspecting the top 10% would surface serious enforcement outcomes at roughly 4x the rate of the current baseline. I also prototyped an LLM extraction step that turns free-text inspection reports into structured risk features.

---

## 1. Problem framing

The Ministry wants to move from reactive to proactive inspection targeting. I framed this as a ranking problem rather than a prediction problem: we don't need to predict individual accidents (which is statistically fragile and ethically fraught), we need to rank workplaces so that limited inspection capacity is spent where serious findings are most likely.

Two framing decisions drove everything downstream:

- **Unit of analysis: the workplace.** FIRE treats the workplace as the inspected entity — NAICS codes, locations, and orders all attach to it. Field-visit grain would leak multiple correlated rows per workplace into the same period; organization grain blurs multi-site patterns. Workplace scores can still be rolled up to organizations for executive reporting.
- **Target: a proxy for serious risk, not harm itself.** Critical injuries and fatalities are too rare to train on. Instead I used serious enforcement actions — Stop Use/Stop Work Orders and Time Unknown Orders — which the data dictionary defines as signaling immediate danger. The fatalities data is reserved for narrative validation only.

## 2. Data

| Source | Use |
|---|---|
| Ontario OHS field visits, 2017–2024 (Ontario Data Catalogue) | Primary modeling data (~120k rows/year) |
| Sample inspection reports (3 provided) | LLM extraction demo |
| WSIB sector injury rates | Optional sector-level baseline feature |
| Allowed traumatic fatalities | Validation narrative only — too sparse and coarse to train on |

A few schema notes that mattered in practice:

- File schemas drift across years. 2021–2022 add extra ID columns; 2024 renames the ACT/contravener fields and splits stop-work orders into four subtypes (`STOP A057-6a/b/c/8`) with different casing on time-unknown orders. I stacked 2017–2023 on a shared core column set (`WORKPLACE ID`, `ORDER TYPE`, `CASE TYPE`, `FIELD VISIT DATE`, `PRIMARY NAICS`, `ORDER STATUS`) and held 2024 out rather than risk silently mislabeling the target.
- Order type strings are year-specific, so the serious-order label uses explicit per-year mappings rather than one hardcoded list.

## 3. Target and cohort definition

**Target:** binary, at workplace grain — did the workplace receive at least one Stop Use/Stop Work Order or Time Unknown Order in calendar year 2023?

**Snapshot design:** features are computed from all activity for the workplace from 2017 through 2022-12-31; the target is observed in 2023. This is an out-of-time split by construction — it simulates exactly how the model would be used ("score workplaces on their history, plan next year's inspections") and avoids the leakage that a random 80/20 split would introduce.

**Evaluation cohort:** workplaces with at least one visit in 2017–2022 *and* at least one visit in 2023 — 12,234 workplaces, with an 8.0% positive rate. This restriction matters. If I had included every historical workplace, the positive rate drops to ~0.6%, but most of those zeros mean "never re-inspected," not "safe." Labels only exist where the Ministry chose to inspect, so honest evaluation requires restricting to workplaces where the label was actually observable. Scores for never-revisited workplaces are extrapolations and I treat them as such (see Limitations).

I checked label stability before committing to a single test year: the serious-order rate was ~9.1% in 2022 and ~9.3% in 2023 (all visited workplaces), close enough that one out-of-time test year is defensible for a prototype.

## 4. Features

All features are computed strictly from the 2017–2022 window:

1. **Enforcement history** — order counts, stop-work counts, time-unknown counts, contraventions per visit
2. **Compliance behavior** — share of orders complied / not complied, repeat outstanding orders
3. **Inspection cadence** — days since last visit, visit count, investigation-to-inspection ratio
4. **Sector baseline** — historical serious-order rate at 2-digit NAICS (computed out-of-fold to avoid target leakage), with WSIB sector injury rates as an optional external prior
5. **Geography** — coarse region from postal code

Count features are `log1p`-transformed; NAICS is rolled up to 2-digit sector to keep coefficients stable and readable.

## 5. Modeling

**Primary model: logistic regression** with `class_weight='balanced'`. This was a deliberate choice, not a fallback. In an enforcement context the Ministry must be able to explain why a workplace was flagged — odds ratios and reason codes meet that bar; an opaque score does not.

**Robustness check: LightGBM** (`scripts/04_boosting_shap.ipynb`). This step turned out to be the most instructive part of the project. In-sample, LightGBM showed a 7.15x lift with ROC-AUC 0.97 — clearly memorization. Compared honestly with out-of-fold cross-validation, the two models are tied: logistic at 4.00x lift / 0.311 PR-AUC vs LightGBM at 3.73x / 0.284. Since boosting buys no accuracy here, I kept the fully interpretable model. I left both the inflated in-sample number and the honest cross-validated number in the notebook on purpose, because the gap between them is the whole argument for proper validation.

For feature attribution I used permutation importance (SHAP had a libllvmlite/numpy conflict in my environment; permutation importance is model-agnostic and answers the same question for this use case). Top drivers — industry sector, prior enforcement history, recency of visits, and compliance rate — are consistent between the boosted model and the logistic coefficients, which adds confidence the signal is real rather than a model artifact.

## 6. Evaluation

**Primary metric: lift in the top decile.** Accuracy is meaningless at an 8% base rate, and ROC-AUC doesn't map to the operational question. Lift@10% answers it directly: if inspectors visit the top 10% of scored workplaces, how much richer in serious findings is that list than the status quo?

| Metric | Result |
|---|---|
| Baseline serious-order rate | 8.0% |
| Top-decile rate | 32.5% in-sample, ~32% cross-validated |
| Lift @ top 10% (logistic) | ~4.0x (4.08x in-sample, 4.00x CV) |
| Lift @ top 10% (LightGBM, CV) | 3.73x |
| PR-AUC / ROC-AUC (logistic, CV) | 0.31 / 0.80 |

Lift is monotonic across all ten deciles (`data/processed/lift_chart.png`), which suggests the score is meaningful across the whole range, not just at the top cut.

## 7. LLM component

Inspection narratives contain risk signal that never makes it into structured FIRE fields — supervision failures, vulnerable workers, hazard specifics. I prototyped schema-constrained JSON extraction: de-identify the report text, then prompt an LLM to fill a fixed schema (hazard type, severity, supervision failure flag, vulnerable worker flag, etc.). The demo on one of the sample reports is in `data/processed/llm_extraction_example.json`.

I chose extraction over text embeddings deliberately. Named, auditable features can be explained to executives and challenged by inspectors; embedding dimensions cannot. In production this would run on an in-tenant Azure OpenAI deployment, and the LLM's role is strictly to structure text — it never assigns risk or triggers enforcement on its own.

## 8. Assumptions and limitations

These are the things I would raise unprompted in any deployment conversation:

- **Selection bias.** Labels exist only where the Ministry inspected. The model learns "risk conditional on being the kind of workplace that gets inspected." Mitigation: reserve a slice of inspection capacity for random/exploratory visits to generate unbiased labels over time.
- **Feedback loops.** If targeting becomes 100% model-driven, the model eventually only sees its own choices. The exploration capacity above also addresses this.
- **Proxy target.** Serious orders are not injuries. The model identifies elevated likelihood of serious enforcement findings; it does not predict accidents, and I would never present it as doing so.
- **Privacy.** Inspection text and supporting materials contain personal information. De-identification before any LLM processing is mandatory (FIPPA/PHIPA), and processing must stay in-tenant.
- **Fairness.** Risk scores should be audited by region, sector, and workplace size before deployment so that targeting doesn't simply amplify historical inspection patterns.
- **2024 data held out.** Schema changes meant I excluded 2024 from the prototype rather than rush a rename map. With more time, 2024 becomes a second out-of-time test year.

## 9. What production would look like

The prototype is a snapshot pipeline; production would be a scheduled scoring job: refresh workplace features from FIRE monthly, score the full register, surface ranked lists with reason codes in the inspectors' workflow, and retrain annually with the newest labeled year. The LLM extraction step would run in batch over inspection narratives to enrich the feature set. Model governance — drift monitoring, fairness audits, and the random-inspection holdout — would be part of the operating procedure from day one, not an afterthought.

## 10. Repository guide

| Path | Contents |
|---|---|
| `scripts/01_data_exploration.ipynb` | EDA: schema drift across years, target volume checks, base rates |
| `scripts/02_modeling_table.ipynb` | Builds the workplace-level modeling table (features + target) |
| `scripts/03_model.ipynb` | Logistic regression, lift chart, coefficients |
| `scripts/04_boosting_shap.ipynb` | LightGBM robustness check, permutation importance |
| `data/processed/` | Modeling table, lift chart, feature importance, LLM extraction example |
| `files/` | Executive slide deck and speaker script |

Setup and reproduction steps are in `README.md`.
