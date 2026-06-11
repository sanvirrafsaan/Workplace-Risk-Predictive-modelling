# Technical Documentation — Predictive Risk Identification

This document explains how I built the prototype for Option 1 of the assignment: a way to identify high-risk workplaces so the Ministry can target its Occupational Health and Safety (OHS) inspections more effectively. I have written it so that both a technical reader and a non-technical reader can follow it — where I use a technical term, I explain it in plain language the first time it appears.

**The short version:** I built a model that scores each workplace by how likely it is to receive a serious enforcement action. I trained it on Ontario's public OHS field-visit data (2017–2023). If inspectors used this model to visit the top 10% of scored workplaces, they would find serious problems about **4 times more often** than they do with untargeted visits. I also built a small demonstration of using a large language model (an "LLM" — the same kind of AI behind tools like ChatGPT) to turn free-text inspection reports into structured, usable data.

---

## 1. Problem framing

The Ministry wants to move from **reactive** inspections (going out after a complaint, injury, or fatality) to **proactive** ones (choosing where to go before harm happens). Inspectors are a scarce resource, and in any given year most workplaces are never visited, so the question is: *where do we send them to do the most good?*

I deliberately framed this as a **ranking problem**, not a prediction-of-accidents problem. In other words, the goal is not to predict whether a specific accident will happen at a specific site — that is statistically unreliable and ethically fraught. The goal is to **sort** workplaces from highest to lowest risk so that limited inspection capacity goes where serious findings are most likely.

Two early decisions shaped everything else:

- **What counts as one "thing" we score — the workplace.** The data records activity at a few different levels: individual field visits, workplaces, and organizations (a company that may own several workplaces). I chose the **workplace** as the unit. The Ministry's case system already treats the workplace as the inspected entity — industry code, location, and orders all attach to it. Scoring individual visits would put many related rows for the same site into the model and let them "echo" each other; scoring whole organizations would blur differences between a company's safe and unsafe sites. Workplace scores can still be added up to the organization level later for executive reporting.

- **What we actually predict — a stand-in for serious risk, not harm itself.** Critical injuries and fatalities are, thankfully, rare. There are too few of them to train a reliable model on. So instead of predicting injuries directly, I predict **serious enforcement actions** — specifically **Stop Use / Stop Work Orders** and **Time Unknown Orders**. The data dictionary defines these as orders an inspector issues when something is dangerous enough to halt work immediately. They are the best available signal that a site was genuinely unsafe. (The separate fatalities dataset is used only as a sanity-check narrative, never as a training target — it is too sparse and coarse to model.)

---

## 2. Data

| Source | How I used it |
|---|---|
| Ontario OHS field visits, 2017–2024 (Ontario Data Catalogue) | Main data for the model (~120k rows per year) |
| Sample inspection reports (3 provided) | Demonstration of the LLM text-extraction step |
| WSIB sector injury rates | Considered as an optional external "industry baseline" input (see §4) |
| Allowed traumatic fatalities | Validation narrative only — too sparse to train on |

A few practical notes about the data that affected the build:

- **The file format changed from year to year.** The 2021–2022 files add extra ID columns; the 2024 file renames key fields and splits stop-work orders into four sub-types with inconsistent capitalization. To avoid silently mislabeling my target, I combined 2017–2023 using a shared set of core columns (workplace ID, order type, case type, field-visit date, primary industry code, order status) and **deliberately held the 2024 file aside** rather than rush a fragile mapping of the renamed fields.
- **The exact wording of order types differs by year**, so the rule that decides "is this a serious order?" uses an explicit, per-year list of the right strings rather than one hardcoded list that would quietly miss some.

---

## 3. Target and how I chose which workplaces to evaluate

**The target (the thing the model learns to predict):** a yes/no label for each workplace — *did this workplace receive at least one Stop Use / Stop Work Order or Time Unknown Order during 2023?*

**The "snapshot" design — and why it avoids cheating.** I calculate every input feature from the workplace's history through **2022-12-31**, and I measure the target in **2023**. This is what's called an **out-of-time split**: the model only ever "sees the past" to predict "the future." This matters because it mirrors exactly how the model would be used in real life — *score each workplace on its history, then plan next year's inspections.* The common alternative, a random split of the rows, would let information from 2023 leak into training and make the results look better than they really are. I avoided that on purpose.

**Which workplaces I included (the evaluation cohort).** I restricted the analysis to workplaces that had **at least one visit in 2017–2022 and at least one visit in 2023** — **12,234 workplaces**, of which **8.0%** received a serious order in 2023.

That restriction is one of the most important judgment calls in the project, so let me explain it. If I had instead kept every workplace that ever appeared, the serious-order rate would drop to about 0.6% — but most of those zeros don't mean "safe," they mean "never re-inspected." We only know the outcome for a workplace if the Ministry actually chose to visit it. So an honest evaluation has to be limited to workplaces where the outcome was genuinely observable. For workplaces that were never revisited, any score the model gives is an educated extrapolation, and I treat it as such (see Limitations).

Before settling on a single test year, I checked that 2023 wasn't a fluke: the serious-order rate among all visited workplaces was about 9.1% in 2022 and 9.3% in 2023 — close enough that using one out-of-time test year is reasonable for a prototype.

---

## 4. Features (the inputs the model uses)

A **feature** is just a measurable input the model uses to make its prediction. All of mine are computed strictly from the 2017–2022 window so that nothing from the future leaks in. They fall into a few intuitive groups:

1. **Enforcement history** — how many orders, stop-work orders, and time-unknown orders the workplace has received in the past, and how many investigations it has had.
2. **Compliance behaviour** — the share of past orders the workplace actually complied with, plus a flag for whether it has any order history at all.
3. **Inspection cadence** — how recently we last visited, and how many times we've visited.
4. **Industry** — the workplace's industry, captured through its NAICS code (explained below).

**A note on NAICS.** NAICS is the standard North American industry classification — basically a code for "what kind of work happens here" (construction, mining, healthcare, etc.). The codes are hierarchical: the more digits, the more specific. I rolled each code up to its **2-digit sector level** (for example, `23` = Construction) rather than using the full, very specific 6-digit code. The fine-grained codes are too sparse — many would have only a handful of workplaces — and the broad sector is where the risk patterns actually show up and stay readable.

**Two small data-preparation steps worth explaining:**

- **`log1p` on the count features.** The count columns (number of orders, visits, etc.) are *heavy-tailed*: most workplaces have small numbers, but a few have very large ones (one had 771 orders). Feeding raw counts to this kind of model lets those few extreme workplaces dominate. The standard fix is to take the logarithm of the counts (`log1p` means "log of 1 + the value", which also handles zeros cleanly). This compresses the big numbers so the relationship the model is looking for behaves more sensibly. In plain terms: it stops a handful of outlier sites from drowning out everyone else.
- **One-hot encoding the industry sector.** A model needs numbers, not text labels like "Construction." **One-hot encoding** turns a single text column into several yes/no (1/0) columns — one per sector — so the model can learn a separate weight for each industry.

*On WSIB injury rates:* I considered adding province-wide injury rates by industry as an external "baseline risk" input. In the final prototype, industry risk is captured through the one-hot sector feature above; the WSIB rates are noted as a sensible enrichment for a production version rather than something I baked into this prototype.

---

## 5. The model

**Primary model: logistic regression.** Logistic regression is a well-understood, transparent model. For each workplace it outputs a **probability between 0 and 1** — its estimated likelihood of receiving a serious order. Importantly, it does this by giving each feature a **weight (coefficient)**, which means you can read off *why* a workplace scored the way it did. I chose it deliberately, not as a fallback: in an enforcement setting the Ministry must be able to explain why a workplace was flagged. A transparent score with clear reasons meets that bar; a black-box score does not.

I used the setting `class_weight='balanced'`. Because only 8% of workplaces are positive, a naive model could score everything "low risk" and still look accurate. This setting tells the model to pay proportionally more attention to the rare positive cases so it actually learns to find them.

**Robustness check: a gradient-boosting model (LightGBM).** This was the most instructive part of the project, so I'll explain it carefully. **Gradient boosting** is a more complex, more flexible family of models that can capture intricate patterns — but that flexibility makes it prone to *memorizing* the training data instead of learning generalizable signal.

When I fit LightGBM and scored it on the **same** rows it was trained on ("in-sample"), it looked spectacular — a 7.15x lift. That number is misleading: the model had simply memorized the answers. The honest way to compare two models is **cross-validation**, where you repeatedly train on part of the data and score the part that was held out, so a model never grades its own homework. Under that fair comparison, the two models are essentially tied: logistic regression at **4.00x lift** versus LightGBM at **3.73x**.

Because the complex model bought no real accuracy, I kept the simple, fully explainable one. I deliberately left *both* the inflated in-sample number and the honest cross-validated number in the notebook, because the gap between them is the whole point: it's the argument for validating properly.

**How I identified the most important drivers.** To see which features mattered most, I used **permutation importance**: you randomly shuffle one feature's values and measure how much the model's performance drops. A big drop means the feature was important; little drop means it wasn't. It's a model-agnostic method — it works on any model and is easy to explain to a non-technical audience. (I would normally use a method called SHAP for this, but it had a software-dependency conflict in my environment, and permutation importance answers the same question here.) The top drivers — industry sector, prior enforcement history, how recently the site was visited, and compliance rate — were consistent between the boosted model and the logistic model's coefficients, which gives me confidence the signal is real and not an artifact of one particular model.

---

## 6. Evaluation — how I measured success

**My primary metric: lift in the top 10% ("top decile").** Accuracy is meaningless here — with an 8% base rate, a model that says "no" to everyone is 92% accurate and completely useless. So I measure **lift**, which answers the operational question directly: *if inspectors visit the top 10% of workplaces ranked by the model, how much richer in serious findings is that group than a random selection would be?*

To get it, I score every workplace, sort them from highest to lowest, take the top 10%, and compare that group's serious-order rate to the overall 8% baseline.

| Metric | Result |
|---|---|
| Baseline serious-order rate (all workplaces) | 8.0% |
| Serious-order rate in the top 10% | 32.5% in-sample, ~32% cross-validated |
| **Lift in the top 10% (logistic)** | **~4.0x** (4.08x in-sample, 4.00x cross-validated) |
| Lift in the top 10% (LightGBM, cross-validated) | 3.73x |
| PR-AUC / ROC-AUC (logistic, cross-validated) | 0.31 / 0.80 |

The last row lists two secondary, more technical ranking scores. In plain terms, both measure how well the model sorts risky workplaces above safe ones. **ROC-AUC of 0.80** means that if you picked one risky and one safe workplace at random, the model would rank the risky one higher about 80% of the time — solid. **PR-AUC** is a stricter measure that focuses on the rare positive cases; 0.31 sounds low but is normal and respectable when only 8% of cases are positive. I report these for completeness, but the headline number is the lift.

The lift also rises smoothly across all ten ranked groups — the lowest-risk group is near zero and each group up is riskier, peaking at the top — which tells me the score is meaningful across the whole range, not just at the very top cut. The chart of this is saved at `data/processed/lift_chart.png`.

**How the "top 3 reasons" would work.** Because logistic regression assigns each feature a weight, for any individual workplace you can multiply each feature's value by its weight to see how much it contributed to that workplace's score, then surface the three largest contributors as plain-English reasons (e.g. "high prior order volume," "construction sector," "prior stop-work orders"). This is what would power the reason codes in a planner's dashboard. It is the model explaining its own decision — not a separate correlation analysis.

---

## 7. The LLM (text) component

Inspection reports contain risk signals in their written narratives that never make it into the tidy database fields — things like a supervision failure, the involvement of young or new workers, or the specific hazard. I built a small demonstration of capturing that signal.

The approach is **schema-constrained extraction**: I take the report text, remove any personal information, and then ask an LLM to fill in a fixed, predefined form — hazard type, severity, was there a supervision failure (yes/no), were vulnerable workers involved (yes/no), and so on. The LLM's only job is to read messy text and return structured, predictable fields. The demonstration on one of the sample reports is saved at `data/processed/llm_extraction_example.json`.

I chose this **extraction** approach over **text embeddings** (a technique that turns text into long lists of abstract numbers) on purpose. Named, structured fields can be explained to executives, audited, and challenged by inspectors; abstract embedding numbers cannot. In production this would run on an in-tenant Azure OpenAI deployment, and the LLM's role would stay strictly limited to *structuring text* — it would never assign risk or trigger enforcement on its own.

---

## 8. Assumptions and limitations

These are the issues I would raise unprompted in any real deployment conversation:

- **Selection bias.** We only know outcomes for workplaces the Ministry chose to inspect. So the model really learns "risk, *given that this is the kind of workplace we tend to inspect*." The mitigation is to reserve a slice of inspection capacity for random or exploratory visits, which generate unbiased labels over time.
- **Feedback loops.** If targeting became 100% model-driven, the model would eventually only ever see the workplaces it already chose, reinforcing its own blind spots. The exploratory-inspection capacity above addresses this too.
- **The target is a proxy.** Serious orders are a stand-in for danger, not injuries themselves. The model identifies an elevated likelihood of serious enforcement findings; I would never present it as predicting accidents.
- **Privacy.** Inspection text contains personal and health information. De-identifying it before any LLM processing is mandatory under Ontario's privacy laws (FIPPA/PHIPA), and processing must stay within the Ministry's own secure environment.
- **Fairness.** Before deployment, the scores should be audited across region, industry, and workplace size so that targeting doesn't simply amplify whoever has historically been inspected the most.
- **2024 data held out.** The 2024 file's renamed fields meant I excluded it rather than risk mislabeling the target. With more time, 2024 would become a valuable second out-of-time test year.

---

## 9. What a production version would look like

The prototype is a one-time snapshot. A production version would be a **scheduled scoring job**: refresh each workplace's features from the live case system monthly, score every workplace, and surface a ranked list — each with its top reason codes — inside the inspectors' existing planning tools. The model would be retrained each year as a new year of outcomes becomes available. The LLM extraction step would run in batch over inspection narratives to enrich the features. Crucially, governance — monitoring for the model drifting over time, fairness audits, and the random-inspection holdout — would be built in from day one, not added as an afterthought.

---

## 10. Repository guide

| Path | Contents |
|---|---|
| `scripts/01_data_exploration.ipynb` | Initial data exploration: format changes across years, target volume checks, base rates |
| `scripts/02_modeling_table.ipynb` | Builds the workplace-level table (one row per workplace: features + target) |
| `scripts/03_model.ipynb` | The logistic regression model, lift chart, and coefficients |
| `scripts/04_boosting_shap.ipynb` | The LightGBM robustness check and permutation importance |
| `data/processed/` | The modeling table, lift chart, feature-importance chart, and LLM extraction example |
| `files/` | The executive slide deck and speaker script |

Setup and reproduction steps are in `README.md`.
